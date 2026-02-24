import subprocess
import time
import sys

# Konfiguration
NUM_RUNS = 50
SCRIPT_TO_RUN = "main.py"

def run_benchmark():
    print(f"🚀 Starte Benchmark-Schleife: {NUM_RUNS} Durchläufe...\n")
    
    start_time_total = time.perf_counter()

    for i in range(1, NUM_RUNS + 1):
        print(f"{'='*40}")
        print(f"🔄 Durchlauf {i} von {NUM_RUNS} wird gestartet...")
        print(f"{'='*40}")
        
        start_time_run = time.perf_counter()
        
        try:
            # sys.executable stellt sicher, dass GENAU das Python aus deinem Venv genutzt wird!
            result = subprocess.run([sys.executable, SCRIPT_TO_RUN], check=False)
            
            duration_run = time.perf_counter() - start_time_run
            
            if result.returncode == 0:
                print(f"✅ Durchlauf {i} erfolgreich beendet in {duration_run:.2f} Sekunden.\n")
            else:
                print(f"⚠️ Durchlauf {i} endete mit Fehlercode {result.returncode}.\n")
                
        except Exception as e:
            print(f"❌ Kritischer Fehler beim Starten von Durchlauf {i}: {e}\n")
            # Bei einem kritischen Systemfehler (z.B. Datei nicht gefunden) brechen wir ab
            break 

    duration_total = time.perf_counter() - start_time_total
    print(f"🎉 Alle {NUM_RUNS} Durchläufe abgeschlossen!")
    print(f"⏱️ Gesamtzeit: {duration_total:.2f} Sekunden.")

if __name__ == "__main__":
    run_benchmark()