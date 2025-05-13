import psycopg2
import os
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME     = "data_challenge"
DB_USER     = "challenge"
DB_PASSWORD = "challenge"
DB_HOST     = "localhost"
DB_PORT     = "5432"
SUPERUSER   = os.getenv("SUPERUSER", "postgres")
SUPERPASS   = os.getenv("SUPERPASS", "postgres")


def user_exists(cursor, username):
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (username,))
    return cursor.fetchone() is not None


def main():

    su_conn = psycopg2.connect(
        dbname="postgres",
        user=SUPERUSER,
        password=SUPERPASS,
        host=DB_HOST,
        port=DB_PORT
    )
    su_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    su_cur = su_conn.cursor()

    if not user_exists(su_cur, DB_USER):
        su_cur.execute(
            sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s CREATEDB;")
               .format(sql.Identifier(DB_USER)),
            (DB_PASSWORD,)
        )
    else:
        su_cur.execute(
            sql.SQL("ALTER ROLE {} CREATEDB;")
               .format(sql.Identifier(DB_USER))
        )

    su_cur.close()
    su_conn.close()

    ch_conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    ch_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    ch_cur = ch_conn.cursor()

    ch_cur.execute(
        sql.SQL("DROP DATABASE IF EXISTS {};")
           .format(sql.Identifier(DB_NAME))
    )
    print(f"Creating database '{DB_NAME}' ...")
    ch_cur.execute(
        sql.SQL("CREATE DATABASE {} OWNER {};")
           .format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER))
    )

    ch_cur.close()
    ch_conn.close()

    db_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    db_cur = db_conn.cursor()

    db_cur.execute("DROP TABLE IF EXISTS public.electric_vehicles;")
    print("Creating table electric_vehicles ...")
    db_cur.execute(sql.SQL("""
        CREATE TABLE public.electric_vehicles (
            vin TEXT,
            county TEXT,
            "City" TEXT,
            "State" TEXT,
            "Postal Code" TEXT,
            "Model Year" TEXT,
            "Make" TEXT,
            "Model" TEXT,
            "Electric Vehicle Type" TEXT,
            "Clean Alternative Fuel Vehicle (CAFV) Eligibility" TEXT,
            "Electric Range" TEXT,
            "Base MSRP" TEXT,
            "Legislative District" TEXT,
            "DOL Vehicle ID" TEXT,
            "Vehicle Location" TEXT,
            "Electric Utility" TEXT,
            "2020 Census Tract" TEXT
        );
    """))

    db_cur.close()
    db_conn.close()

if __name__ == "__main__":
    main()
