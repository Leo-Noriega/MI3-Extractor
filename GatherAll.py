import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv, set_key

from DBConnection import client
from HistoricalProfiles import post_hist_perfiles
from RestructuringJson import build_unified_json

# Conexión a la base de datos
db = client['sgen']
collection = db['data']


# Función para actualizar el archivo .env
def update_env_var(key, value):
    dotenv_path = '.env'
    set_key(dotenv_path, key, value)


# Función para generar JSON y guardar las respuestas
def to_json(no_serie, date, tipo_var):
    tipo_dispo = "2"
    tipo_perfil = "1"
    json_perfiles = ""
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = datetime.strptime(date, "%Y-%m-%d")

    for i in range((end_date - start_date).days + 1):
        day = start_date + timedelta(days=i)
        fechaini = day.strftime("%Y-%m-%d")
        fechafin = day.strftime("%Y-%m-%d")
        update_env_var("DATE", fechaini)

        os.makedirs(f'DataSISMEDIA/{no_serie}/{fechaini}', exist_ok=True)

        response = post_hist_perfiles(no_serie, tipo_var, tipo_dispo, tipo_perfil, fechaini, fechafin, json_perfiles)

        with open(f'DataSISMEDIA/{no_serie}/{fechaini}/{tipo_var}-{no_serie}-{fechaini}.json', 'w') as f:
            json.dump(response, f, indent=4)


# Función principal para procesar los datos
def process_data():
    no_series = collection.distinct('no_serie')

    for no_serie in no_series:
        results = collection.find({
            "no_serie": no_serie,
            "values.0": None,
            "values.1": None,
            "values.2": None,
            "values.3": None,
            "values.4": None,
            "values.5": None,
            "values.6": None
        }, {"date": 1})

        dates = {}

        for result in results:
            date_str = result['date'].strftime("%Y-%m-%d %H:%M:%S")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            day_str = date_obj.strftime("%Y-%m-%d")

            if day_str not in dates:
                dates[day_str] = []

            dates[day_str].append(date_str)

        for day in dates.keys():
            update_env_var("NO_SERIE", no_serie)
            update_env_var("DATE", day)

            for tipo_var in range(1, 6):
                to_json(no_serie, day, str(tipo_var))

            # Cargar las variables de entorno actualizadas
            load_dotenv()
            # Ejecutar build_unified_json después de actualizar .env
            build_unified_json()


# Ejecutar el procesamiento de datos
process_data()
