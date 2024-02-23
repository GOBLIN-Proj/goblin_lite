"""
Animal Data Generation
======================
This module contains the AnimalDataGenerator class, which is responsible for generating animal data and livestock outputs
for a specified scenario. The class leverages the AnimalData and Exports classes to calculate animal data and livestock outputs
based on scenario-specific and baseline animal data.
"""
from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports

class AnimalDataGenerator:
    """
    A class to generate animal data and livestock outputs for a specified scenario.

    This class is responsible for generating animal data and livestock outputs for a specified scenario. It leverages the
    AnimalData and Exports classes to calculate animal data and livestock outputs based on scenario-specific and baseline animal data.

    Attributes
    ----------
    ef_country : str
        The country for which the livestock data is being generated.

    calibration_year : int
        The year used for calibration.

    target_year : int
        The target year for the scenario.

    scenario_input_dataframe : pandas.DataFrame
        A DataFrame containing scenario-specific input data required for livestock output calculations.

    Methods
    -------
    generate_animal_data()
        Generates animal data for a specified scenario.

    generate_livestock_ouputs()
        Generates and returns a DataFrame of livestock outputs for the given scenario.
    
    """
    def __init__(self, ef_country, calibration_year, target_year, scenario_input_dataframe):
        self.ef_country = ef_country
        self.calibration_year = calibration_year
        self.target_year = target_year
        self.scenario_input_dataframe = scenario_input_dataframe


    def generate_animal_data(self):
        """
        Generates animal data for baseline and scenarios.

        Returns
        -------
        tuple
            A tuple containing two pandas DataFrames: (baseline_animal_data, scenario_animal_data).
        """
        animal_class = AnimalData(
            self.ef_country, self.calibration_year, self.target_year, self.scenario_input_dataframe
        )
        # create dataframe for baseline animals
        baseline_animal_data = animal_class.create_baseline_animal_dataframe()

        # create dataframe for scenarios animals
        scenario_animal_data = animal_class.create_animal_dataframe()

        return baseline_animal_data, scenario_animal_data
    
    def generate_livestock_ouputs(self):
        """
        Generates and returns a DataFrame of livestock outputs for the given scenario.

        This method leverages the Exports class to calculate protein and milk production based on scenario-specific and baseline 
        animal data. It produces a summary DataFrame combining milk production data and beef (carcass) weight from protein production data.

        Returns
        -------
        pandas.DataFrame
            A DataFrame, named protein_and_milk_summary, combining milk production data and beef carcass weight, 
            indexed by 'Scenarios'.

        Notes
        -----
        The method performs the following steps:
        1. Initializes an instance of the Exports class with country-specific parameters, calibration year, target year, 
        and scenario inputs.
        2. Computes protein production data using `compute_system_protien_exports` of the Exports class, which includes 
        carcass weight information.
        3. Computes milk production data using `compute_system_milk_exports` of the Exports class.
        4. Creates the protein_and_milk_summary DataFrame by copying milk production data and appending the beef carcass 
        weight from the protein production data.
        5. Sets 'Scenarios' as the index of the protein_and_milk_summary DataFrame.

        The generated protein_and_milk_summary DataFrame provides a comprehensive overview of the livestock outputs, 
        including milk production and beef carcass weight, for both scenario-specific and baseline data comparisons.

        The attributes and methods referenced in this documentation are class attributes and methods and should be 
        available within the class instance when this method is called.
        """

        export_class = Exports(
            self.ef_country, self.calibration_year, self.target_year, self.scenario_input_dataframe
        )

        baseline_animal_data, scenario_animal_data = self.generate_animal_data()

        protein_production_df = export_class.compute_system_protien_exports(
            scenario_animal_data, baseline_animal_data
        )

        milk_production_df = export_class.compute_system_milk_exports(
            scenario_animal_data, baseline_animal_data
        )

        protein_and_milk_summary = milk_production_df.copy(deep=True)

        protein_and_milk_summary["total_beef_kg"] = protein_production_df[
            "carcass_weight_kg"
        ]
        # Set 'Scenarios' as the index
        protein_and_milk_summary = protein_and_milk_summary.set_index('Scenarios')

        return protein_and_milk_summary