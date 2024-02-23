"""
Forest Carbon Generator
=======================
This module contains the ForestCarbonGenerator class, which is responsible for generating forest carbon data.
The class leverages the Runner class to calculate forest carbon data based on scenario-specific and baseline forest data.
"""
from cbm_runner.runner import Runner

class ForestCarbonGenerator:
    """
    Manages the process of generating forest carbon data, leveraging the CBM 
    Runner class (from the cbm_runner module) to perform the core carbon calculations.

    Attributes
    ----------
        calibration_year: int 
            The base year used for calibrating the carbon model.

        cbm_config_path: str
            The path to the configuration file for the CBM.

        scenario_dataframe: pandas.DataFrame
            Dataframe containing forest management scenario descriptions.

        afforestation_dataframe: pandas.DataFrame
            Dataframe containing information about afforestation activities.
    
    Methods
    -------
    generate_forest_carbon()
        Generates forest carbon data using the provided input data.
    """
    def __init__(self, calibration_year, cbm_config_path, scenario_dataframe, afforestation_dataframe):
        self.calibration_year = calibration_year
        self.cbm_configuration = cbm_config_path
        self.scenario_dataframe = scenario_dataframe
        self.afforestation_dataframe = afforestation_dataframe

    def generate_forest_carbon(self):
        """
        Generates forest carbon data using the provided input data.

        Returns:
            dict: A dictionary containing forest carbon data with keys 'forest_flux' and 'forest_aggregate'.
        """
        cbm_runner = Runner(
            self.cbm_configuration,
            self.calibration_year,
            self.afforestation_dataframe,
            self.scenario_dataframe,
        )

        cbm_runner.generate_input_data()

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


        forest_data = {"forest_flux": forest_flux, "forest_aggregate": forest_aggregate}

        return forest_data