-- Tabelle für die extrahierten Fachdaten
CREATE TABLE IF NOT EXISTS Applicant (
    applicant_id UUID NOT NULL,
    model_name VARCHAR(255) NOT NULL, -- Erhöht auf 255 Zeichen für Sicherheit
    name VARCHAR(255),
    surname VARCHAR(255),
    mail VARCHAR(255),
    mobile_number VARCHAR(100),       -- Länger, falls LLM "+49 (0) 123..." schreibt
    landline_number VARCHAR(100),
    dob VARCHAR(100),                 -- WICHTIG: String statt Timestamp, um Formatfehler zu vermeiden!
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Zusammengesetzter Primärschlüssel verhindert Duplikate pro Modell
    PRIMARY KEY (applicant_id, model_name)
);

-- Tabelle für das Benchmarking (Performance & Kosten)
CREATE TABLE IF NOT EXISTS LLM_Logs (
    log_id SERIAL PRIMARY KEY,        -- Umbenannt zu log_id (klarer)
    applicant_id UUID,
    model_name VARCHAR(255),
    prompt_tokens INT,
    completion_tokens INT,
    total_tokens INT,
    duration_ms FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);