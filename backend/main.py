import asyncio
import json
import os
import time
from pathlib import Path
from uuid import uuid4, UUID
import psycopg
from dotenv import load_dotenv

# Lokale Importe
from models import Applicant
from agents import agents_to_test

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/applicant_db")
INPUT_FILE = Path(__file__).parent.parent / "inputData" / "applicantData.json"
CONCURRENCY_LIMIT = 1 

async def init_db(conn):
    """Prüft und erstellt alle nötigen Tabellen beim Start."""
    async with conn.cursor() as cur:
        # 1. Haupttabelle: Applicant
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Applicant (
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                name VARCHAR(255),
                surname VARCHAR(255),
                mail VARCHAR(255),
                mobile_number VARCHAR(100),
                landline_number VARCHAR(100),
                dob VARCHAR(100), 
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (applicant_id, model_name)
            );
        """)
        # 2. Adresse
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Address (
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                address VARCHAR(255),
                house_number INT,
                postal_code VARCHAR(50),
                city VARCHAR(255),
                country VARCHAR(255),
                PRIMARY KEY (applicant_id, model_name),
                FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
            );
        """)
        # 3. Education
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Education (
                education_id SERIAL PRIMARY KEY,
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                education_category VARCHAR(255),
                school VARCHAR(255),
                graduation VARCHAR(255),
                graduation_grade VARCHAR(100),
                begin_date TIMESTAMP,
                end_date TIMESTAMP,
                FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
            );
        """)
        # 4. Career
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Career (
                career_id SERIAL PRIMARY KEY,
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                employer VARCHAR(255),
                job_description TEXT,
                begin_date TIMESTAMP,
                end_date TIMESTAMP,
                FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
            );
        """)
        # 5. Interests
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Interests (
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                hobbies TEXT,
                sports TEXT,
                volunteering TEXT,
                PRIMARY KEY (applicant_id, model_name),
                FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
            );
        """)
        # 6. Qualification
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS Qualification (
                qualification_id SERIAL PRIMARY KEY,
                applicant_id UUID NOT NULL,
                model_name VARCHAR(255) NOT NULL,
                qualification TEXT,
                FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
            );
        """)
        # 7. LLM Logs
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS LLM_Logs (
                log_id SERIAL PRIMARY KEY,
                applicant_id UUID,
                model_name VARCHAR(255),
                prompt_tokens INT,
                completion_tokens INT,
                total_tokens INT,
                duration_ms FLOAT,
                retries INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    print("✅ Datenbank-Tabellen initialisiert und bereit.")

async def process_single_entry(sem, conn, entry, model_name, agent):
    async with sem:
        # ID Logik
        if 'id' in entry:
            try:
                app_id = UUID(entry['id'])
            except ValueError:
                app_id = uuid4()
        else:
            app_id = uuid4()

        start_time = time.perf_counter()
        
        try:
            print(f"⏳ {model_name}: Starte für ID {str(app_id)}...")
            
            # KI-Aufruf
            result = await agent.run(
                f"Data: {json.dumps(entry, ensure_ascii=False)}"
            )
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # --- 🪄 DIE MAGIE ---
            # Wir fangen das Objekt direkt ab. Kein Text-Parsing mehr!
            if hasattr(result, 'data'):
                data = result.data
            else:
                data = result.output

            # DB Speichern
            async with conn.cursor() as cur:
                
                # 1. Haupttabelle Applicant
                dob_str = str(data.dob.date()) if data.dob else None
                await cur.execute(
                    """
                    INSERT INTO Applicant (applicant_id, model_name, name, surname, mail, mobile_number, landline_number, dob)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (applicant_id, model_name) DO UPDATE SET 
                        name = EXCLUDED.name,
                        surname = EXCLUDED.surname,
                        mail = EXCLUDED.mail,
                        mobile_number = EXCLUDED.mobile_number,
                        landline_number = EXCLUDED.landline_number,
                        dob = EXCLUDED.dob;
                    """,
                    (app_id, model_name, data.name, data.surname, data.mail, data.mobile_number, data.landline_number, dob_str)
                )

                # 2. Adresse (1:1 - Upsert)
                if data.address:
                    await cur.execute(
                        """
                        INSERT INTO Address (applicant_id, model_name, address, house_number, postal_code, city, country)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (applicant_id, model_name) DO UPDATE SET
                            address = EXCLUDED.address,
                            house_number = EXCLUDED.house_number,
                            postal_code = EXCLUDED.postal_code,
                            city = EXCLUDED.city,
                            country = EXCLUDED.country;
                        """,
                        (app_id, model_name, data.address.address, data.address.house_number, data.address.postal_code, data.address.city, data.address.country)
                    )

                # 3. Interessen (1:1 - Upsert)
                if data.interests:
                    await cur.execute(
                        """
                        INSERT INTO Interests (applicant_id, model_name, hobbies, sports, volunteering)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (applicant_id, model_name) DO UPDATE SET
                            hobbies = EXCLUDED.hobbies,
                            sports = EXCLUDED.sports,
                            volunteering = EXCLUDED.volunteering;
                        """,
                        (app_id, model_name, data.interests.hobbies, data.interests.sports, data.interests.volunteering)
                    )

                # 4. Education (1:N - Löschen und Neu anlegen)
                await cur.execute("DELETE FROM Education WHERE applicant_id = %s AND model_name = %s", (app_id, model_name))
                for edu in data.education:
                    await cur.execute(
                        """
                        INSERT INTO Education (applicant_id, model_name, education_category, school, graduation, graduation_grade, begin_date, end_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (app_id, model_name, edu.education_category, edu.school, edu.graduation, edu.graduation_grade, edu.begin_date, edu.end_date)
                    )

                # 5. Career (1:N - Löschen und Neu anlegen)
                await cur.execute("DELETE FROM Career WHERE applicant_id = %s AND model_name = %s", (app_id, model_name))
                for job in data.career:
                    await cur.execute(
                        """
                        INSERT INTO Career (applicant_id, model_name, employer, job_description, begin_date, end_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (app_id, model_name, job.employer, job.job_description, job.begin_date, job.end_date)
                    )

                # 6. Qualification (1:N - Löschen und Neu anlegen)
                await cur.execute("DELETE FROM Qualification WHERE applicant_id = %s AND model_name = %s", (app_id, model_name))
                for qual in data.qualifications:
                    await cur.execute(
                        """
                        INSERT INTO Qualification (applicant_id, model_name, qualification)
                        VALUES (%s, %s, %s)
                        """,
                        (app_id, model_name, qual.qualification)
                    )

                # 7. LLM Logs
                usage = result.usage()
                all_msgs = result.all_messages()
                model_responses = sum(1 for msg in all_msgs if msg.__class__.__name__ == 'ModelResponse')
                retries_count = max(0, model_responses - 1)

                await cur.execute(
                    """
                    INSERT INTO LLM_Logs (applicant_id, model_name, prompt_tokens, completion_tokens, total_tokens, duration_ms, retries)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (app_id, model_name, usage.input_tokens, usage.output_tokens, usage.total_tokens, duration_ms, retries_count)
                )

            print(f"✅ {model_name}: Komplettes Profil gespeichert in {duration_ms:.2f}ms")

        except Exception as e:
            print(f"❌ {model_name}: Fehler bei ID {str(app_id)[:8]} -> {e}")

async def main():
    if not INPUT_FILE.exists():
        print(f"FEHLER: Datei nicht gefunden unter {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"🚀 Starte Benchmark mit {len(raw_data)} Datensätzen.")

    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with await psycopg.AsyncConnection.connect(DB_URL, autocommit=True) as conn:
        
        # NEU: Initialisiere die Datenbank-Tabellen vor dem Benchmark!
        await init_db(conn)

        tasks = []
        for entry in raw_data:
            for model_name, agent in agents_to_test.items():
                tasks.append(
                    process_single_entry(sem, conn, entry, model_name, agent)
                )
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())