import os
from dotenv import load_dotenv
from pydantic_ai import Agent, models

load_dotenv()

# URL hart setzen
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434/v1'

print("Verbinde mit Ollama...")
try:
    local_model = models.infer_model('ollama:llama3.2')
except Exception as e:
    print(f"❌ Fehler: {e}")
    raise e

# --- ÄNDERUNG: One-Shot Prompting ---
# Statt Schema-Definition geben wir ein perfektes Beispiel.
# system_prompt = (
    "Du bist ein Daten-Extraktor. "
    "Extrahiere Informationen aus dem Text und gib sie als JSON zurück."
    "Identifiziere, was der Vorname (Name), Nachname (Surname) anhand von typischen Namen und Trennzeichen."
    "Falls das Geburtsdatum in einem ungewöhnlichen Format vorliegt, versuche es trotzdem zu extrahieren."
    "mobile_number kann auch unter anderen Namen wie 'handy' oder 'mobiltelefon' auftauchen. "
    "landline_number könnte auch 'telefon', 'festnetztelefon' oder 'zuhause' heißen. "
    "Nutze exakt dieses Format als Vorlage:\n"
    "{\n"
    '  "Name": "Max",\n'
    '  "Surname": "Mustermann",\n'
    '  "Mail": "max@example.com",\n'
    '  "Mobile_number": "+49123456",\n'
    '  "Landline_number": "030123456",\n'
    '  "Dob": "1990-01-01"\n'
    "}\n"
    "Antworte NUR mit dem JSON. Kein Markdown, keine Erklärungen."
# )

system_prompt=("You are an expert data extraction assistant. "
"Your task is to extract specific personal and contact information from the provided text and output it strictly as a JSON object. "
"Carefully distinguish between the first name (given name) and the surname (last name). "
"Assign the first name(s) to the 'Name' key and the last name to the 'Surname' key. "
"Look for common separators (like commas) and typical name structures. "
"Extract the date of birth and convert it into the standard 'YYYY-MM-DD' format, even if it is presented in an unusual format. "
"'Mobile_number' might also be referred to as 'Handy', 'Mobiltelefon', 'Cell', or 'Mobile'. "
"'Landline_number' might also be referred to as 'Telefon', 'Festnetztelefon', 'Zuhause', 'Home', or 'Landline'. "
"If any piece of information cannot be found in the text, use null for that key. "
"Use exactly this format as your template:\n"
"{\n"
'  "Name": "Max",\n'
'  "Surname": "Mustermann",\n'
'  "Mail": "max@example.com",\n'
'  "Mobile_number": "+49123456",\n'
'  "Landline_number": "030123456",\n'
'  "Dob": "1990-01-01"\n'
"}\n"
"Output ONLY the raw JSON object. Do not include markdown formatting, conversational text, or explanations.")

llama_agent = Agent(
    local_model,
    system_prompt=system_prompt
)

agents_to_test = {
    "llama3.2-local": llama_agent
}