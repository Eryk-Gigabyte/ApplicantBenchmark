from pydantic_ai import Agent
from models import Applicant  
import logfire

# # Optional: Überwachung aktivieren (zeigt dir Tool-Calls und Validierung im Detail)
# logfire.configure(p_name='bewerber_extraktion')

system_prompt=(
        "Du bist ein Experte für Datenextraktion im Recruiting. "
        "Deine Aufgabe ist es, Informationen aus Bewerbungsunterlagen (Text oder JSON) "
        "zu extrahieren und sie präzise in das vorgegebene Datenbank-Schema zu überführen. "
        "Achte besonders auf korrekte Datumsformate (ISO) und die Trennung von Name und Vorname."
    ),

gpt_4o_agent = Agent(
    'openai:gpt-4o',
    result_type=Applicant,
    system_prompt = system_prompt
)