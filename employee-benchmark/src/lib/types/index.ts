// 1. Basis-Informationen (Tabelle: Applicant)
export interface Applicant {
    applicant_id: string; // UUID
    model_name: string;
    name: string | null;
    surname: string | null;
    mail: string | null;
    mobile_number: string | null;
    landline_number: string | null;
    dob: string | null;
    extracted_at: string; // ISO Date String
    
    // Verknüpfte Daten (1:1 und 1:N Beziehungen)
    address?: Address;
    interests?: Interests;
    education?: Education[];
    career?: Career[];
    qualifications?: Qualification[];
}

// 2. Adresse (Tabelle: Address - 1:1)
export interface Address {
    address: string | null;
    house_number: number | null;
    postal_code: string | null;
    city: string | null;
    country: string | null;
}

// 3. Bildungsweg (Tabelle: Education - 1:N)
export interface Education {
    education_id?: number;
    education_category: string | null;
    school: string | null;
    graduation: string | null;
    graduation_grade: string | null;
    begin_date: string | null;
    end_date: string | null;
}

// 4. Berufserfahrung (Tabelle: Career - 1:N)
export interface Career {
    career_id?: number;
    employer: string | null;
    job_description: string | null;
    begin_date: string | null;
    end_date: string | null;
}

// 5. Interessen (Tabelle: Interests - 1:1)
export interface Interests {
    hobbies: string | null;
    sports: string | null;
    volunteering: string | null;
}

// 6. Qualifikationen (Tabelle: Qualification - 1:N)
export interface Qualification {
    qualification_id?: number;
    qualification: string;
}

// Interface für die KI-Auswahl (wird in +page.svelte und ApplicationsListCard genutzt)
export interface Provider {
    name: string;
    icon: string;
}

export interface ProviderBlock {
    provider: Provider; // Umbenannt von AIProvider zu provider
    metadata: {
        answerTime: number;
        tokens: number;
    };
    applications: Applicant[];
}