# JSON Processing Project

## Requirements

- Python 3.x
- `venv` for virtual environments

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```sh
      source venv/bin/activate
      ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Run the scripts as needed, for example:
    ```sh
    python Main.py
    ```

## Project Structure

- `DBConnection.py`: Contains the code that establishes a connection to a database
- `GatherAll.py` & `GatherAllJsons.py`: Contains the code that retrieves all the JSON files from the SISMEDIA API
- `GatheringDates.py`: Contains the code that retrieves the dates that are null from the database 
- `Main.py`: Contains the code that runs the entire project
- `RefactorJsons.py`: Contains the code that restructures the JSON file for an easy insert to the database
- `RestructuringJsons.py`: Contains the code that restructures the JSON files with the info gathered from both the database and the SISMEDIA API
- `RetrieveHistoricalProfileID.py`: Contains the code that retrieves the historical profile from the SISMEDIA API
- `RetrieveToken.py`: Contains the code that retrieves the token from the SISMEDIA API
- `TestHistoricalProfiles.py`: *[Test only]*
- `TestToken.py`: *[Test only]*
- `UpdateDB.py`: Contains the code that updates the database with the new JSON file generated
- `requirements.txt`: Dependencies file

## Notes

- The script generates the following:
    - `DataSISMEDIA`: Contains all the JSON files retrieved from the SISMEDIA API
    - `NullDates`: Contains all the JSON files with the dates that are null in the database
    - `insert.json`: Contains the JSON file restructured for an easy insert to the database