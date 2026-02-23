import asyncio
import json
import os
import time
import ast
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

# Reinigt den String von Markdown und Code-Blöcken
def clean_string(text: str) -> str:
    text = str(text).strip()
    # Entferne ```json ... ``` oder ``` ... ```Wrapper
    if text.startswith("```"):
        lines = text.splitlines()
        # Wenn erste Zeile ```json ist, nimm alles danach
        if lines[0].strip().startswith("```"):
            text = "\n".join(lines[1:])
        # Wenn letzte Zeile ``` ist, schneide sie ab
        if text.strip().endswith("```"):
            text = text.strip()[:-3]
    return text.strip()

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
            print(f"⏳ {model_name}: Starte für ID {str(app_id)[:8]}...")
            
            # KI-Aufruf
            result = await agent.run(
                f"Data: {json.dumps(entry, ensure_ascii=False)}"
            )
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # --- FIX 1: Robustes Auslesen des Ergebnisses ---
            # Prüfen wo der Text steckt (API Unterschiede)
            if hasattr(result, 'data') and result.data:
                raw_text = str(result.data)
            elif hasattr(result, 'output') and result.output: # <--- Wichtig für Text-Responses
                raw_text = str(result.output)
            else:
                raw_text = str(result) # Fallback

            clean_text = clean_string(raw_text)
            
            # --- FIX 2: Die "Python-Syntax-Rettung" ---
            try:
                # Versuch 1: Standard JSON Parsing (Doppelte Anführungszeichen)
                json_data = json.loads(clean_text)
            except json.JSONDecodeError:
                try:
                    # Versuch 2: Python Dictionary Parsing (Einfache Anführungszeichen)
                    # Das rettet Antworten wie {'Name': 'Max'}
                    print(f"⚠️ {model_name}: Ungültiges JSON, versuche Python-Eval...")
                    json_data = ast.literal_eval(clean_text)
                except Exception:
                    # Wenn alles scheitert, Fehler werfen
                    print(f"💀 Parsing komplett gescheitert. Text war: {clean_text[:50]}...")
                    raise ValueError("Konnte Antwort nicht als JSON oder Dict lesen")

            # Validierung durch Pydantic
            # Wir nutzen **json_data (Dictionary Unpacking)
            data = Applicant(**json_data)

            # DB Speichern
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO Applicant (applicant_id, model_name, name, surname, mail, mobile_number, landline_number, dob)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (applicant_id, model_name) DO UPDATE SET 
                        name = EXCLUDED.name,
                        surname = EXCLUDED.surname,
                        mail = EXCLUDED.mail,
                        dob = EXCLUDED.dob;
                    """,
                    (app_id, model_name, data.name, data.surname, data.mail, data.mobile_number, data.landline_number, data.dob)
                )

                usage = result.usage()
                await cur.execute(
                    """
                    INSERT INTO LLM_Logs (applicant_id, model_name, prompt_tokens, completion_tokens, total_tokens, duration_ms)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (app_id, model_name, usage.request_tokens, usage.response_tokens, usage.total_tokens, duration_ms)
                )
            
            print(f"✅ {model_name}: Fertig in {duration_ms:.2f}ms")

        except Exception as e:
            print(f"❌ {model_name}: Fehler bei ID {str(app_id)[:8]} -> {e}")

async def main():
    if not INPUT_FILE.exists():
        print(f"FEHLER: Datei nicht gefunden unter {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        # Hier gehen wir davon aus, dass die JSON eine Liste ist
        raw_data = json.load(f)

    print(f"🚀 Starte Benchmark mit {len(raw_data)} Datensätzen.")

    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with await psycopg.AsyncConnection.connect(DB_URL, autocommit=True) as conn:
        tasks = []
        for entry in raw_data:
            for model_name, agent in agents_to_test.items():
                tasks.append(
                    process_single_entry(sem, conn, entry, model_name, agent)
                )
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())