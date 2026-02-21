-- 1. Unabhängige Tabellen erstellen
CREATE TABLE Address (
    Address_ID SERIAL PRIMARY KEY,
    Address VARCHAR(255),
    House_number INT,
    Postal_code VARCHAR(20),
    City VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE Education (
    Education_ID SERIAL PRIMARY KEY,
    Education_category VARCHAR(50), -- z.B. ENUM-Ersatz
    School VARCHAR(255),
    Graduation VARCHAR(100),
    Graduation_grade CHAR(5),
    Begin_date TIMESTAMP,
    End_date TIMESTAMP
);

CREATE TABLE Career (
    Career_ID SERIAL PRIMARY KEY,
    Employer VARCHAR(255),
    Job_description TEXT,
    Begin_date TIMESTAMP,
    End_date TIMESTAMP
);

CREATE TABLE Interests (
    Interest_ID SERIAL PRIMARY KEY,
    Hobbies TEXT,
    Sports TEXT,
    Volunteering TEXT
);

CREATE TABLE Qualification (
    Qualification_ID SERIAL PRIMARY KEY,
    Qualification TEXT
);

-- 2. Haupttabelle Applicant mit Foreign Keys erstellen
CREATE TABLE Applicant (
    Applicant_ID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Surname VARCHAR(100),
    Mail VARCHAR(150),
    Mobile_number VARCHAR(50),
    Landline_number VARCHAR(50),
    Dob TIMESTAMP,
    Address_ID INT REFERENCES Address(Address_ID),
    Education_ID INT REFERENCES Education(Education_ID),
    Career_ID INT REFERENCES Career(Career_ID),
    Interest_ID INT REFERENCES Interests(Interest_ID),
    Qualification_ID INT REFERENCES Qualification(Qualification_ID)
);