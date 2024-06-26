import json
import math
import os
from datetime import datetime


def get_device_id_from_null_dates(directory):
    """Obtiene el device_id del primer conjunto de archivos JSON."""
    device_id_map = {}

    for no_serie_folder in os.listdir(directory):
        no_serie_path = os.path.join(directory, no_serie_folder)
        if os.path.isdir(no_serie_path):
            for date_folder in os.listdir(no_serie_path):
                date_path = os.path.join(no_serie_path, date_folder)
                if os.path.isdir(date_path):
                    for filename in os.listdir(date_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(date_path, filename)
                            with open(file_path, "r") as f:
                                data = json.load(f)
                            if isinstance(data, list) and len(data) > 0:
                                device_id = data[0].get("device_id")
                                if device_id:
                                    device_id_map[no_serie_folder] = device_id
                                    break  # Solo necesitamos el primer archivo por carpeta
    return device_id_map


def get_apparent_power(active_power, power_factor):
    try:
        if active_power is not None and power_factor is not None and power_factor != 0:
            return active_power / power_factor
    except (ZeroDivisionError, TypeError):
        return None
    return None


def get_reactive_power(apparent_power, active_power):
    try:
        if apparent_power is not None and active_power is not None:
            tmp = pow(apparent_power, 2) - pow(active_power, 2)
            return math.sqrt(tmp)
    except TypeError:
        return None
    return None


def process_json_file(file_path, device_id_map):
    """Procesa un archivo JSON y lo transforma al formato para la base de datos."""

    with open(file_path, "r") as f:
        data = json.load(f)

    # Obtener no_serie y date del nombre del archivo
    file_name = os.path.basename(file_path)
    parts = file_name.split("-")
    no_serie = parts[0]
    date_str = "-".join(parts[1:4])  # Unir año, mes y día

    device_id = device_id_map.get(no_serie, None)  # Obtener device_id del mapa

    if not device_id:
        raise ValueError(f"No se encontró device_id para el número de serie {no_serie}")

    db_data = []

    for index, (time, values) in enumerate(data.items()):
        time_obj = datetime.strptime(f"{date_str} {time}", "%Y-%m-%d %H:%M:%S")
        time_obj = time_obj.replace(microsecond=0)  # Añadir milisegundos si es necesario

        db_record = {
            "device_id": device_id,
            "no_serie": no_serie,
            "pm_id": "",  # Reemplaza con el pm_id si lo tienes
            "date": {"$date": time_obj.isoformat() + ".000Z"},
            "index": index,
            "values": [None] * 40,  # Inicializar la lista con 40 elementos (None)
        }

        # Mapeo de valores del JSON al formato de la base de datos
        for fase in range(1, 4):
            db_record["values"][fase - 1] = values.get(f"Corriente Fase {fase}", None)  # IA, IB, IC
            db_record["values"][fase + 3] = values.get(f"Voltaje Fase {fase}", None)  # VA, VB, VC
            db_record["values"][fase + 11] = values.get(f"Potencia activa Fase {fase}", None)  # WA, WB, WC
            db_record["values"][fase + 15] = values.get(f"Potencia reactiva Fase {fase}", None)  # QA, QB, QC
            db_record["values"][fase + 19] = values.get(f"Potencia aparente Fase {fase}", None)  # UA, UB, UC
            db_record["values"][fase + 23] = values.get(f"Factor de potencia Fase {fase}", None)  # FPA, FPB, FPC
            db_record["values"][fase + 31] = values.get(f"Energia Activa Fase {fase}", None)  # WHA, WHB, WHC

        # Convertir valores a float antes de sumar
        for i in range(36):  # Convertir los primeros 36 valores
            if db_record["values"][i] is not None:
                db_record["values"][i] = float(db_record["values"][i])

        # Calcular valores para el índice 3 (sumas o promedios)
        db_record["values"][3] = sum([v for v in db_record["values"][0:3] if v is not None])  # I3 (suma)
        db_record["values"][7] = sum([v for v in db_record["values"][4:7] if v is not None]) / 3  # V3 (promedio)
        db_record["values"][15] = sum([v for v in db_record["values"][12:15] if v is not None])  # W3 (suma)
        db_record["values"][19] = sum([v for v in db_record["values"][16:19] if v is not None])  # Q3 (suma)
        db_record["values"][23] = sum([v for v in db_record["values"][20:23] if v is not None])  # U3 (suma)
        db_record["values"][27] = sum([v for v in db_record["values"][24:27] if v is not None]) / 3  # FPT3 (promedio)
        db_record["values"][35] = sum([v for v in db_record["values"][32:35] if v is not None])  # WH3 (suma)

        db_data.append(db_record)

    return db_data


def process_all_json_files(directory, device_id_map):
    """Procesa todos los archivos JSON en un directorio
    y guarda los datos formateados en un archivo insert.json.
    """

    all_db_data = []

    for no_serie_folder in os.listdir(directory):
        no_serie_path = os.path.join(directory, no_serie_folder)
        if os.path.isdir(no_serie_path):
            for date_folder in os.listdir(no_serie_path):
                date_path = os.path.join(no_serie_path, date_folder)
                if os.path.isdir(date_path):
                    for filename in os.listdir(date_path):
                        if filename.endswith("-FINAL.json"):
                            file_path = os.path.join(date_path, filename)
                            db_data = process_json_file(file_path, device_id_map)
                            all_db_data.extend(db_data)

    with open("insert.json", "w") as f:
        json.dump(all_db_data, f, indent=4)


if __name__ == "__main__":
    # Obtener el mapeo de device_id de NullDates
    device_id_map = get_device_id_from_null_dates("/Users/noriega/Documents/Projects/extractorMI3/NullDates")
    # Procesar los archivos en DataSISMEDIA usando el mapeo obtenido
    process_all_json_files("/Users/noriega/Documents/Projects/extractorMI3/DataSISMEDIA", device_id_map)