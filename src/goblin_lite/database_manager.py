import sqlalchemy as sqa
from sqlalchemy_utils import create_database
import pandas as pd
from goblin_lite.database import get_local_dir
import os


class DataManager:
    def __init__(self):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()

    def data_engine_creater(self):
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "goblin_database.db")
        )
        engine_url = f"sqlite:///{database_path}"
        engine = sqa.create_engine(engine_url)

        # Create the database if it doesn't exist
        create_database(engine.url)

        return engine

    def create_or_clear_database(self):
        # Get the inspector for the engine
        inspector = sqa.inspect(self.engine)

        # Get the list of existing tables
        existing_tables = inspector.get_table_names()

        if existing_tables:
            # Drop each existing table
            with self.engine.begin() as connection:
                for table_name in existing_tables:
                    connection.execute(f"DROP TABLE {table_name}")
            print("Existing tables have been deleted.")
        else:
            # Create a temporary table and drop it to create the database
            print("No tables to clean.")

    def save_goblin_results_output_datatable(self, data, table, index=True):
        data.to_sql(
            table,
            self.engine,
            dtype={
                "farm_id": sqa.types.Integer(),
                "Year": sqa.types.Integer(),
                "Scenario": sqa.types.Integer(),
                "CO2": sqa.types.Float(),
                "CH4": sqa.types.Float(),
                "N2O": sqa.types.Float(),
                "CO2e": sqa.types.Float(),
            },
            if_exists="replace",
            index=index,
        )

    def get_goblin_results_output_datatable(self, table, index_col=None):
        dataframe = pd.read_sql("SELECT * FROM '%s'" % table, self.engine, index_col)

        return dataframe
