import json
from uuid import UUID

from ApplicantBenchmark.backend.models_alt import Applicant

class DBService:
    def __init__(self, conn): # conn = deine DB Verbindung
        self.conn = conn

    async def save_applicant_result(self, applicant: Applicant):
        # Speichert das Ergebnis der KI
        query = """
            INSERT INTO extracted_applicants (applicant_id, model_name, data)
            VALUES (%s, %s, %s)
            ON CONFLICT (applicant_id, model_name) DO UPDATE SET data = EXCLUDED.data;
        """
        await self.conn.execute(query, (
            applicant.applicant_id, 
            applicant.model_name, 
            applicant.model_dump_json(by_alias=True)
        ))

    async def save_log(self, applicant_id: UUID, model_name: str, usage, duration_ms: float):
        # Speichert Token-Verbrauch und Zeit
        query = """
            INSERT INTO llm_logs (applicant_id, model_name, prompt_tokens, completion_tokens, duration_ms)
            VALUES (%s, %s, %s, %s, %s);
        """
        await self.conn.execute(query, (
            applicant_id, model_name, 
            usage.request_tokens, usage.response_tokens, duration_ms
        ))