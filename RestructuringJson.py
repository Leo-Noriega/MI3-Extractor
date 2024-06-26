import json
import math
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

no_serie = os.getenv("NO_SERIE")
date = os.getenv("DATE")
data = {}
data_types = ['Energia Activa', 'Voltaje', 'Corriente', 'Factor de potencia', 'Potencia activa']


def get_apparent_power(active_power, power_factor):
    try:
        return active_power / power_factor
    except ZeroDivisionError:
        print("No se puede dividir entre 0")
        return None
    except TypeError:
        print("Tipo de variable no valida")
        return None


def get_reactive_power(apparent_power, active_power):
    try:
        tmp = pow(apparent_power, 2) - pow(active_power, 2)
        return math.sqrt(tmp)
    except TypeError:
        print("Fallo en la operacion")
        return None


def build_unified_json():
    for data_type in range(1, 6):
        with open(f'DataSISMEDIA/{no_serie}/{date}/{data_type}-{no_serie}-{date}.json') as f:
            json_data = json.load(f)

        for fase in json_data['valores']:
            for i, value in enumerate(fase['Valores']):
                time = (datetime(2024, 4, 1, 0, 5) + timedelta(minutes=5 * i)).time().isoformat()

                if time not in data:
                    data[time] = {}

                data[time][f'{data_types[data_type - 1]} Fase {fase["FaseCanal"]}'] = value

                # Si el tipo de dato es 'Potencia activa', calcular la potencia aparente y la potencia reactiva
                if data_types[data_type - 1] == 'Potencia activa':
                    active_power = value
                    power_factor = data[time].get(f'Factor de potencia Fase {fase["FaseCanal"]}', 0)

                    apparent_power = get_apparent_power(active_power, power_factor)
                    reactive_power = get_reactive_power(apparent_power, active_power)

                    data[time][f'Potencia aparente Fase {fase["FaseCanal"]}'] = apparent_power
                    data[time][f'Potencia reactiva Fase {fase["FaseCanal"]}'] = reactive_power

    with open(f'DataSISMEDIA/{no_serie}/{date}/{no_serie}-{date}-FINAL.json', 'w') as f:  # Modificación aquí
        json.dump(data, f, indent=4)
