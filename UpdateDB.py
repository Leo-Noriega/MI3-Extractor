import json
import threading
from datetime import datetime

from pymongo import UpdateOne, WriteConcern

from DBConnection import client

# Conectar a la base de datos 'sgen'
db = client['sgen']
collection = db['data'].with_options(write_concern=WriteConcern(w=1))


# Función para convertir las fechas en los documentos JSON a objetos datetime de Python
def convert_dates(data):
    for record in data:
        if 'date' in record and '$date' in record['date']:
            record['date'] = datetime.strptime(record['date']['$date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    return data


# Función para procesar un lote de datos y realizar las operaciones de actualización
def update_batch(data_slice, batch_id):
    operations = []
    for i, record in enumerate(data_slice):
        filter_query = {
            "device_id": record["device_id"],
            "no_serie": record["no_serie"],
            "date": record["date"]
        }
        update_query = {
            "$set": {
                "index": record["index"],
                "values": record["values"],
                "last_updated": datetime.utcnow()
            }
        }
        operations.append(UpdateOne(filter_query, update_query, upsert=True))

        # Procesar el lote de operaciones cuando alcanzamos el tamaño del lote
        if (i + 1) % batch_size == 0:
            print(f"Ejecutando lote de operaciones {batch_id}-{i // batch_size + 1}...")
            result = collection.bulk_write(operations)
            print(
                f"Lote {batch_id}-{i // batch_size + 1} completado. Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_count}")
            operations = []

    # Procesar cualquier operación restante que no llenó un lote completo
    if operations:
        print(f"Ejecutando último lote de operaciones {batch_id}...")
        result = collection.bulk_write(operations)
        print(
            f"Último lote {batch_id} completado. Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_count}")


# Verificación de índices
collection.create_index([("device_id", 1), ("no_serie", 1), ("date", 1)])

# Cargar los datos del JSON generado
print("Cargando datos del archivo insert.json...")
with open('insert.json', 'r') as f:
    data = json.load(f)

# Convertir las fechas en los datos cargados
print("Convirtiendo fechas en los datos cargados...")
data = convert_dates(data)

# Imprimir algunos registros para verificar
print("Primeros 5 registros después de la conversión:")
print(data[:5])

# Tamaño del lote y número de hilos
batch_size = 500
num_threads = 4

# Dividir el archivo JSON en partes más pequeñas para procesamiento paralelo
data_slices = [data[i::num_threads] for i in range(num_threads)]

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=update_batch, args=(data_slices[i], i + 1))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Todas las operaciones de actualización completadas.")
