import subprocess

scripts = [
    "GatheringDates.py",
    "RetrieveHistoricalProfileID.py",
    "GatherAllJsons.py",
    "GatherAll.py",
    "RestructuringJson.py",
    "RefactorJsons.py",
    "UpdateDB.py"
]

for script in scripts:
    print(f"Ejecutando {script}...")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script}: {str(e)}")
        break
