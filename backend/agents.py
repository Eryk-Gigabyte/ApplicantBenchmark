import os
from dotenv import load_dotenv
from pydantic_ai import Agent, models

from models import Applicant

import pydantic_ai
print("🚀 PydanticAI Version:", pydantic_ai.__version__)

load_dotenv()

# URL hart setzen
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434/v1'

print("Verbinde mit Ollama...")
try:
    # local_model = models.infer_model('ollama:llama3.2')
    # local_model = models.infer_model('ollama:gemma3:12b')
    local_model = models.infer_model('ollama:qwen3:8b')
except Exception as e:
    print(f"❌ Fehler: {e}")
    raise e

system_prompt = (
    "You are an expert HR data extraction assistant. "
    "Your task is to extract personal information, contact details, addresses, education, career history, interests, and qualifications from the provided text. "
    "Rules: "
    "1. Carefully distinguish between the first name (Name) and the surname (Surname). "
    "2. Extract the date of birth and convert it into the standard 'YYYY-MM-DD' format, even if presented unusually. "
    "3. Note German synonyms: 'Mobile_number' might be 'Handy' or 'Mobiltelefon'. 'Landline_number' might be 'Festnetztelefon' or 'Telefon'. "
    "4. If a specific piece of information is missing, leave it empty or null according to the schema. "
    "5. For career and education, extract all listed entries into their respective lists."
)

llama_agent = Agent(
    local_model,
    system_prompt=system_prompt,
    output_type=Applicant, 
    retries=2 
)

agents_to_test = {
    "qwen3:8b": llama_agent
}