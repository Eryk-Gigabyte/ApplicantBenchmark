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
    local_qwen3_4b = models.infer_model('ollama:qwen3:4b')
    local_qwen3_8b = models.infer_model('ollama:qwen3:8b')
    # local_qwen3_30b = models.infer_model('ollama:qwen3:30b')
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

retries = 3

qwen3_4b_agent = Agent(
    local_qwen3_4b,
    system_prompt=system_prompt,
    output_type=Applicant, 
    retries=retries 
)

qwen3_8b_agent = Agent(
    local_qwen3_8b,
    system_prompt=system_prompt,
    output_type=Applicant, 
    retries=retries 
)

# qwen3_30b_agent = Agent(
#     local_qwen3_30b,
#     system_prompt=system_prompt,
#     output_type=Applicant, 
#     retries=retries
# )

agents_to_test = {
    "qwen3:4b": qwen3_4b_agent,
    "qwen3:8b": qwen3_8b_agent,
    # "qwen3:30b": qwen3_30b_agent
}