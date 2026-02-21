import asyncio
import json
from pathlib import Path
from agents import gpt_4o_agent 

async def process_bewerber_data(file_path: str):
    # 1. JSON Datei einlesen
    path = Path(file_path)
    if not path.exists():
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sicherstellen, dass es ein Array ist
    if not isinstance(data, list):
        print("Fehler: Das JSON sollte ein Array von Objekten sein.")
        return

    print(f"Starte Verarbeitung von {len(data)} Bewerbern...\n")

    # 2. Für jedes Element den Agenten aufrufen
    for index, entry in enumerate(data, start=1):
        # Wir wandeln das einzelne Element wieder in einen String für den Agenten um
        input_str = json.dumps(entry)
        
        try:
            # Agenten-Aufruf (async)
            # result.data ist automatisch eine Instanz deines BewerberProfil Models
            result = await bewerber_agent.run(f"Extrahiere Daten aus: {input_str}")
            
            bewerber = result.data
            print(f"[{index}] Erfolgreich verarbeitet: {bewerber.name} ({bewerber.email})")
            
            # Hier könntest du bewerber in eine DB speichern
            # save_to_db(bewerber)

        except Exception as e:
            print(f"[{index}] Fehler bei der Verarbeitung: {e}")

if __name__ == "__main__":
    # Pfad zu deiner JSON-Datei anpassen
    json_datei = "bewerber_input.json" 
    
    asyncio.run(process_bewerber_data(json_datei))