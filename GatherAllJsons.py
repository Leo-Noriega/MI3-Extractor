import json
import math
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

data_types = ['Energia Activa', 'Voltaje', 'Corriente', 'Factor de potencia', 'Potencia activa']


def get_apparent_power(active_power, power_factor):
    active_power = float(active_power) if active_power is not None else None
    power_factor = float(power_factor) if power_factor is not None else None

    if (
            active_power is not None
            and power_factor is not None
            and power_factor != 0
            and not math.isnan(active_power)
            and not math.isnan(power_factor)
    ):
        try:
            return active_power / power_factor
        except ZeroDivisionError:
            print("No se puede dividir entre 0")
            return None
        except TypeError:
            print("Tipo de variable no valida")
            return None
    else:
        return None


def get_reactive_power(apparent_power, active_power):
    if apparent_power is not None and active_power is not None:
        try:
            tmp = pow(apparent_power, 2) - pow(active_power, 2)
            return math.sqrt(tmp)
        except TypeError:
            print("Fallo en la operacion")
            return None
    else:
        return None


def build_unified_json(no_serie, date):
    data = {}
    for data_type in range(1, 6):
        file_path = os.path.join("DataSISMEDIA", no_serie, date, f'{data_type}-{no_serie}-{date}.json')

        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            continue

        with open(file_path, 'r') as f:
            json_data = json.load(f)

        for fase in json_data['valores']:
            for i, value in enumerate(fase['Valores']):
                time = (datetime(2024, 4, 1, 0, 5) + timedelta(minutes=5 * i)).time().isoformat()

                if time not in data:
                    data[time] = {}

                data[time][f'{data_types[data_type - 1]} Fase {fase["FaseCanal"]}'] = value

    # Calcular potencia aparente y reactiva DESPUÉS del primer bucle
    for time, values in data.items():
        for fase in json_data['valores']:
            active_power = values.get(f'Potencia activa Fase {fase["FaseCanal"]}')
            power_factor = values.get(f'Factor de potencia Fase {fase["FaseCanal"]}')

            apparent_power = get_apparent_power(active_power, power_factor)
            reactive_power = get_reactive_power(apparent_power, active_power)

            values[f'Potencia aparente Fase {fase["FaseCanal"]}'] = apparent_power
            values[f'Potencia reactiva Fase {fase["FaseCanal"]}'] = reactive_power

    output_path = os.path.join("DataSISMEDIA", no_serie, date, f'{no_serie}-{date}-FINAL.json')
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


def process_data():
    for no_serie_folder in os.listdir("DataSISMEDIA"):
        for date_folder in os.listdir(os.path.join("DataSISMEDIA", no_serie_folder)):
            build_unified_json(no_serie_folder, date_folder)


if __name__ == "__main__":
    process_data()
