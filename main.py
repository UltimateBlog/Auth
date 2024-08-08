import subprocess

from db.startup import create_db_tables

if __name__ == "__main__":
    create_db_tables()
    subprocess.call(["nameko", "run", "services.blogger_services"])
