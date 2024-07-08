"""
Database Manager
================

This module contains the DataManager class, which is responsible for managing the database
for the GOBLIN LCA framework. The DataManager class is responsible for creating, clearing, and
saving data to the database. It also retrieves data from the database.
"""
import sqlalchemy as sqa
from sqlalchemy_utils import create_database
import pandas as pd
from goblin_lite.database import get_local_dir
import os


class DataManager:
    """
    Manages the GOBLIN LCA database.

    This class is responsible for managing the database for the GOBLIN LCA framework. It is responsible for creating,
    clearing, and saving data to the database. It also retrieves data from the database.

    Attributes
    ----------
    database_dir : str
        The directory where the database is stored.

    engine : sqlalchemy.engine.base.Engine

    Methods
    -------
    data_engine_creater()
        Creates the database engine.

    create_or_clear_database()
        Creates or clears the database.

    save_goblin_results_output_datatable(data, table, index=True)
        Saves a DataFrame to the database.

    save_goblin_results_to_database(*args)
        Saves data to the database.

    get_goblin_results_output_datatable(table, index_col=None)
        Retrieves a DataFrame from the database.
 
    """

    def __init__(self, external_database_path=None):
        """
        Initializes the DataManager.

        Parameters
        ----------
        external_database_path : str, optional
            The path to an external database file. If None, the default local database is used.
        """

        if external_database_path:
            self.database_dir = os.path.dirname(external_database_path)
            self.database_name = os.path.basename(external_database_path)

        else:
            self.database_dir = get_local_dir()
            self.database_name = "goblin_database.db"
        self.engine = self.data_engine_creater()


    def data_engine_creater(self):
        """
        Creates the database engine based on either the default or provided external database path.

        Returns
        -------
        sqlalchemy.engine.base.Engine
            The database engine.
        """
        database_path = os.path.abspath(os.path.join(self.database_dir, self.database_name))
        engine_url = f"sqlite:///{database_path}"
        engine = sqa.create_engine(engine_url)
        create_database(engine_url)
        return engine

    # The rest of your class implementation remains unchanged.


    def create_or_clear_database(self):
        """
        Creates or clears the database.

        This method creates or clears the database. If the database already exists, it is cleared.

        Returns
        -------
        None
        """
        # SQLAlchemy 2.0 - Using the declarative approach for dropping tables
        metadata = sqa.MetaData()
        metadata.reflect(bind=self.engine)
        existing_tables = metadata.tables

        if existing_tables:
            with self.engine.begin() as connection:
                metadata.drop_all(bind=connection)  # Change: Drop all tables using metadata
            print("Existing tables have been deleted.")
        else:
            print("No tables to clean.")

    def save_goblin_results_output_datatable(self, data, table, index=True):
        """
        Saves a DataFrame to the database.

        This method saves a DataFrame to the database.

        Parameters
        ----------
        data : pandas.DataFrame
            The DataFrame to save.

        table : str
            The name of the table to save the DataFrame to.

        index : bool, optional
            Whether to save the index. Defaults to True.

        Returns
        -------
        None
        """
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
        """
        Saves data to the database.

        This method saves data to the database.

        Parameters
        ----------
        *args
            The data to save.

        Returns
        -------
        None
        """
        for table_name, table in args:
            self.save_goblin_results_output_datatable(table, table_name)

    def get_goblin_results_output_datatable(self, table, index_col=None):
        """
        Retrieves a DataFrame from the database.

        This method retrieves a DataFrame from the database.

        Parameters
        ----------
        table : str
            The name of the table to retrieve the DataFrame from.

        index_col : str, optional
            The column to use as the index. Defaults to None.

        Returns
        -------
        pandas.DataFrame
            The DataFrame retrieved from the database.
        """
        dataframe = pd.read_sql("SELECT * FROM '%s'" % table, self.engine, index_col)

        return dataframe
