# Proyecto de Procesamiento de JSON

## Requisitos

- Python 3.x
- `venv` para entornos virtuales

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Crea un entorno virtual:
    ```sh
    python -m venv venv
    ```

3. Activa el entorno virtual:
    - En Windows:
      ```sh
      venv\Scripts\activate
      ```
    - En macOS y Linux:
      ```sh
      source venv/bin/activate
      ```

4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

5. Ejecuta los scripts según sea necesario, por ejemplo:
    ```sh
    python Main.py
    ```

## Estructura del Proyecto

- `DBConnection.py`: Contains the code that establishes a connection to a database
- `GatherAll.py` & `GatherAllJsons.py`: Contains the code that retrieves all the JSON files from the SISMEDIA API
- `GatheringDates.py`: Contains the code that retrieves the dates that are null form de database 
- `Main.py`: Contains the code that runs the entire project
- `RefactorJsons.py`: Contains the code that restructures the JSON file for an easy insert to the database
- `RestructuringJsons.py`: Contains the code that restructures the JSON files with the info gathered from both the databse and the SISMEDIA API
- `RetrieveHistoricalProfileID.py`: Contains the code that retrieves the historical profile from the SISMEDIA API
- `RetrieveToken.py`: Contains the code that retrieves the token from the SISMEDIA API
- `TestHistoricalProfiles.py`: *[Test only]*
- `TestToken.py`: *[Test only]*
- `UpdateDB.py`: Contains the code that updates the database with the new JSON file generated
- `requirements.txt`: Archivo de dependencias

## Notas

- The script generates the following:
    - `DataSISMEDIA`: Contains all the JSON files retrieved from the SISMEDIA API
    - `NullDates`: Contains all the JSON files with the dates that are null in the database
    - `insert.json`: Contains the JSON file restructured for an easy insert to the database