from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Detailmodelle (entsprechend den SQL-Tabellen) ---

class Address(BaseModel):
    address: str = Field(alias="Address")
    house_number: int = Field(alias="House_number")
    postal_code: str = Field(alias="Postal_code")
    city: str = Field(alias="City")
    country: str = Field(alias="Country")

class Education(BaseModel):
    education_category: str = Field(alias="Education_category")
    school: str = Field(alias="School")
    graduation: str = Field(alias="Graduation")
    graduation_grade: str = Field(alias="Graduation_grade")
    begin_date: Optional[datetime] = Field(alias="Begin_date")
    end_date: Optional[datetime] = Field(alias="End_date")

class Career(BaseModel):
    employer: str = Field(alias="Employer")
    job_description: str = Field(alias="Job_description")
    begin_date: Optional[datetime] = Field(alias="Begin_date")
    end_date: Optional[datetime] = Field(alias="End_date")

class Interests(BaseModel):
    hobbies: Optional[str] = Field(alias="Hobbies")
    sports: Optional[str] = Field(alias="Sports")
    volunteering: Optional[str] = Field(alias="Volunteering")

class Qualification(BaseModel):
    qualification: str = Field(alias="Qualification")

# --- Hauptmodell (entsprechend der Applicant-Tabelle) ---

class Applicant(BaseModel):
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    mail: EmailStr = Field(alias="Mail")
    mobile_number: Optional[str] = Field(alias="Mobile_number")
    landline_number: Optional[str] = Field(alias="Landline_number")
    dob: datetime = Field(alias="Dob")
    
    # Hier bilden wir die Relationen ab
    address: Address
    education: Education
    career: Career
    interests: Interests
    qualification: Qualification

    class Config:
        # Erlaubt es, sowohl mit CamelCase (SQL) als auch snake_case (Python) zu arbeiten
        populate_by_name = True