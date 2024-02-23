"""
Grassland Data Generator
========================
This module contains the GrasslandDataGenerator class, which is responsible for generating grassland data and farm outputs.
The class leverages the GrasslandOutput class to calculate grassland data and farm outputs based on scenario-specific and baseline grassland data.
"""
from grassland_production.grassland_output import GrasslandOutput

class GrasslandDataGenerator:
    """
    Manages the process of generating grassland data and related farm outputs. Leverages 
    the GrasslandOutput class to perform core calculations.

    Attributes
    ----------
    ef_country : str
        Country code for emission factors.
    calibration_year : int
        Base year for model calibration.
    target_year : int 
        Year of analysis.
    scenario_dataframe : pandas.DataFrame
        Dataframe containing scenario-specific grassland parameters.
    scenario_animal_data : pandas.DataFrame
        Dataframe containing animal data for the scenarios.
    baseline_animal_data : pandas.DataFrame
        Dataframe containing baseline animal data.

    Methods
    -------
    generate_farm_inputs()
        Generates farm input data (from the GrasslandOutput class) for both baseline and scenario conditions.

    generate_grassland_areas()
        Calculates total spared grassland, total grassland area, spared area per soil type, and grassland stocking rate.
    """
    def __init__(self,ef_country, calibration_year, target_year, scenario_dataframe,scenario_animal_data,baseline_animal_data):
        self.ef_country = ef_country
        self.calibration_year = calibration_year
        self.target_year = target_year
        self.scenario_dataframe = scenario_dataframe
        self.scenario_animal_data = scenario_animal_data
        self.baseline_animal_data = baseline_animal_data


    def generate_farm_inputs(self):

        grassland_class = GrasslandOutput(
            self.ef_country,
            self.calibration_year,
            self.target_year,
            self.scenario_dataframe,
            self.scenario_animal_data,
            self.baseline_animal_data,
        )

        baseline_farm_inputs = grassland_class.baseline_farm_inputs_data()
        scenario_farm_inputs = grassland_class.farm_inputs_data()

        return baseline_farm_inputs, scenario_farm_inputs
    
    def generate_grassland_areas(self):
        """
        Calculate the total spared and total grassland areas for each scenario.

        This method calculates and returns the total spared, total grassland areas, spared area by soil group and stocking rate for each scenario based on the provided
        scenario_dataframe, scenario_animal_data, and baseline_animal_data attributes. The GrasslandOutput class is utilized to perform
        the necessary calculations for each scenario.

        The total spared area represents the area of grassland that will be converted (destocked) to other land uses (e.g., wetland,
        forests) in the target year compared to the baseline year. The total grassland area represents
        the remaining grassland area. Spared area by soil group represents the spared area by soil group (e.g., class 1, 2 and 3). 
        The stocking rate represents the stocking rate per hectare of grassland.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.

        scenario_animal_data : pandas.DataFrame
            A pandas DataFrame containing animal data for different scenarios.

        baseline_animal_data : pandas.DataFrame
            A pandas DataFrame containing baseline animal data.

        Returns
        -------
        tuple
            A tuple containing four pandas DataFrame: (total_spared_area, total_grassland_area, total_spared_area_by_soil_group, per_hectare_stocking_rate).

        """
        grassland_class = GrasslandOutput(
            self.ef_country,
            self.calibration_year,
            self.target_year,
            self.scenario_dataframe,
            self.scenario_animal_data,
            self.baseline_animal_data,
        )

        spared_area = grassland_class.total_spared_area()
        total_grassland = grassland_class.total_grassland_area()

        total_spared_area_by_soil_group = grassland_class.total_spared_area_breakdown()
        per_hectare_stocking_rate = grassland_class.grassland_stocking_rate()

        return spared_area, total_grassland, total_spared_area_by_soil_group, per_hectare_stocking_rate