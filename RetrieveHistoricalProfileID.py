import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv, set_key

from HistoricalProfiles import post_hist_perfiles
from RestructuringJson import build_unified_json

load_dotenv()
no_serie = os.getenv('NO_SERIE')
date = os.getenv('DATE')


def to_json(tipo_var):
    tipo_dispo = "2"
    tipo_perfil = "1"
    json_perfiles = ""

    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = datetime.strptime(date, "%Y-%m-%d")

    for i in range((end_date - start_date).days + 1):
        day = start_date + timedelta(days=i)
        fechaini = day.strftime("%Y-%m-%d")
        fechafin = day.strftime("%Y-%m-%d")
        set_key("../.env", "DATE", fechaini)

        # Asegúrate de que la carpeta 'DataSISMEDIA' exista
        os.makedirs(f'DataSISMEDIA/{no_serie}/{fechaini}', exist_ok=True)

        response = post_hist_perfiles(no_serie, tipo_var, tipo_dispo, tipo_perfil, fechaini, fechafin, json_perfiles)

        # Guarda el archivo JSON en la carpeta 'DataSISMEDIA'
        with open(f'DataSISMEDIA/{no_serie}/{fechaini}/{tipo_var}-{no_serie}-{fechaini}.json', 'w') as f:
            json.dump(response, f, indent=4)

for tipo_var in range(1, 6):
    to_json(str(tipo_var))

build_unified_json()
