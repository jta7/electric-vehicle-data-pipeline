
## ETL - Electric Vehicles Dataset

This project performs a complete ETL process on an electric vehicles dataset. It downloads the data, initializes a PostgreSQL database, loads the records, and exports the final table for use in Power BI or similar tools.

## Requirements

Make sure you have the following installed on your system:

- Python 3.7+
- PostgreSQL (client and server)
- `psql` available in the system PATH
- A bash-compatible shell (Linux/Mac or WSL)
- Power BI Desktop


## Environment Variables (optional)

The script `src/init_db.py` needs to connect as a PostgreSQL superuser to create the `challenge` role. By default, it connects using:

- Username: `postgres`
- Password: `postgres`

If your environment uses different superuser credentials, you can pass them by running the flow like this:

SUPERUSER=your_admin SUPERPASS=your_password ./run_etl.sh


## --> How to execute the ETL?

Steps :

1 -> git clone https://github.com/jta7/electric-vehicle-data-pipeline.git

2 -> cd electric-vehicle-data-pipeline

3 -> python3 -m venv venv

4 -> source venv/bin/activate

5 -> pip install -r requirements.txt

6 -> ./run_etl.sh

===================================================================================
|| Once completed, the file data/data_file.csv will be ready for use in Power BI.||
===================================================================================


## How to update the data file path in Power BI

If the data doesn't load correctly after downloading the repo, follow these steps:

Open dashboard.pbix in Power BI Desktop.

Right-click the data_file table > Edit query.

In the Power Query Editor, click Advanced Editor.

Replace the file path in the File.Contents("...") line with the path where you saved the repo.


EXAMPLE:

Source = Csv.Document(File.Contents("C:\\Users\YourUser\data_challenge\data\data_file.csv"), ...)
