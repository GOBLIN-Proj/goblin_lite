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
        create_database(engine_url)

        return engine

    def create_or_clear_database(self):
        # SQLAlchemy 2.0 - Using the declarative approach for dropping tables
        metadata = sqa.MetaData(bind=self.engine)
        metadata.reflect()
        existing_tables = metadata.tables

        if existing_tables:
            with self.engine.begin() as connection:
                metadata.drop_all(connection)  # Change: Drop all tables using metadata
            print("Existing tables have been deleted.")
        else:
            print("No tables to clean.")

    def save_goblin_results_output_datatable(self, data, table, index=True):
        data.to_sql(
            table,
            self.engine,
            dtype={
                "farm_id": sqa.types.Integer(),
                "Year": sqa.types.Integer(),
                "year": sqa.types.Integer(),
                "Scenarios": sqa.types.Integer(),
                "Scenario": sqa.types.Integer(),
                "CO2": sqa.types.Float(),
                "CH4": sqa.types.Float(),
                "N2O": sqa.types.Float(),
                "CO2e": sqa.types.Float(),
            },
            if_exists="replace",
            index=index,
        )

    def save_goblin_results_to_database(self, *args):
        for table_name, table in args:
            self.save_goblin_results_output_datatable(table, table_name)

    def get_goblin_results_output_datatable(self, table, index_col=None):
        dataframe = pd.read_sql("SELECT * FROM '%s'" % table, self.engine, index_col)

        return dataframe
