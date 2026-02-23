-- 1. Haupttabelle: Applicant
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
    -- Zusammengesetzter Primärschlüssel
    PRIMARY KEY (applicant_id, model_name)
);

-- 2. Adresse (1:1 Beziehung zum Applicant)
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

-- 3. Ausbildung / Education (1:N Beziehung - ein Bewerber, mehrere Ausbildungen)
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

-- 4. Karriere / Career (1:N Beziehung)
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

-- 5. Interessen (1:1 Beziehung)
CREATE TABLE IF NOT EXISTS Interests (
    applicant_id UUID NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    hobbies TEXT,
    sports TEXT,
    volunteering TEXT,
    PRIMARY KEY (applicant_id, model_name),
    FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
);

-- 6. Qualifikationen (1:N Beziehung)
CREATE TABLE IF NOT EXISTS Qualification (
    qualification_id SERIAL PRIMARY KEY,
    applicant_id UUID NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    qualification TEXT,
    FOREIGN KEY (applicant_id, model_name) REFERENCES Applicant(applicant_id, model_name) ON DELETE CASCADE
);

-- 7. Logging Tabelle (unverändert)
CREATE TABLE IF NOT EXISTS LLM_Logs (
    log_id SERIAL PRIMARY KEY,
    applicant_id UUID,
    model_name VARCHAR(255),
    prompt_tokens INT,
    completion_tokens INT,
    total_tokens INT,
    duration_ms FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);