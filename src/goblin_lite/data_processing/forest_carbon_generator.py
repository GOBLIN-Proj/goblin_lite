"""
Forest Carbon Generator
=======================
This module contains the ForestCarbonGenerator class, which is responsible for generating forest carbon data.
The class leverages the Runner class to calculate forest carbon data based on scenario-specific and baseline forest data.
"""
from goblin_cbm_runner.default_runner.runner import Runner
from goblin_cbm_runner.resource_manager.cbm_runner_data_manager import DataManager
import os 

class ForestCarbonGenerator:
    """
    Manages the process of generating forest carbon data, leveraging the CBM 
    Runner class (from the cbm_runner module) to perform the core carbon calculations.

    Attributes
    ----------
    goblin_data_manager_class : object
        An instance of the data manager class used to retrieve configuration and database paths.

    calibration_year : int
        The base year used for calibrating the carbon model.

    cbm_config_path : str
        The path to the configuration file for the CBM.

    DATABASE_PATH : str
        The path to the database used by the CBM.

    sit_path : str, optional
        The path to the SIT directory.

    cbm_runner_data_manager : DataManager
        An instance of the DataManager class used to manage CBM runner data.

    Methods
    -------
    generate_forest_carbon()
        Generates forest carbon data using the provided input data.
    """
    def __init__(self, 
                 goblin_data_manager, 
                 scenario_dataframe, 
                 afforestation_dataframe):
        
        self.goblin_data_manager_class = goblin_data_manager
        self.calibration_year = self.goblin_data_manager_class.get_calibration_year()
        self.cbm_config_path = self.goblin_data_manager_class.get_cbm_configuration_path()
        self.DATABASE_PATH = self.goblin_data_manager_class.get_database_path()

        self.sit_path = os.path.dirname(self.DATABASE_PATH) if self.DATABASE_PATH else None
        self.cbm_runner_data_manager = DataManager(calibration_year = self.calibration_year,
                            config_file_path=self.cbm_config_path,
                            scenario_data=scenario_dataframe,
                            afforest_data=afforestation_dataframe,
                            sit_path=self.sit_path)

    def generate_forest_carbon(self):
        """
        Generates forest carbon data using the provided input data.

        Returns
        -------
        dict
            A dictionary containing forest carbon data with keys 'forest_flux', 'forest_aggregate', and 'afforestation_area'.
        """
        cbm_runner = Runner(self.cbm_runner_data_manager)

        # generation of aggregated results
        forest_aggregate = cbm_runner.run_aggregate_scenarios()

        # generation of annual flux results
        forest_flux = cbm_runner.run_flux_scenarios()

        # Define columns to exclude from inversion
        exclude_columns = ['Year', 'Scenario']

        # Invert values in forest_flux, excluding specific columns
        for col in forest_flux.columns:
            if col not in exclude_columns:
                forest_flux[col] = forest_flux[col] * -1

        # Invert values in forest_aggregate, excluding specific columns
        for col in forest_aggregate.columns:
            if col not in exclude_columns:
                forest_aggregate[col] = forest_aggregate[col] * -1


        afforestation_area_df = cbm_runner.get_afforestation_dataframe()

        forest_data = {"forest_flux": forest_flux, 
                       "forest_aggregate": forest_aggregate, 
                       "afforestation_area": afforestation_area_df}

        return forest_data