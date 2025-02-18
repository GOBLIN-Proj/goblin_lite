"""
Crop Data Generator
===================
This module contains the CropDataGenerator class, which is responsible for generating crop data and farm outputs.
The class leverages the NationalCropData class to calculate crop data and farm outputs based on scenario-specific and baseline crop data.
"""
from crop_lca.national_crop_production import NationalCropData
from goblin_lite.resource_manager.scenario_data_fetcher import ScenarioDataFetcher
from goblin_lite.resource_manager.goblin_data_manager import GoblinDataManager

class CropDataGenerator:
    """
    A class to generate crop data and farm outputs for a specified scenario.

    This class is responsible for generating crop data and farm outputs. 
    It leverages the NationalCropData class to calculate crop data and farm outputs based on scenario-specific and baseline crop data.

    Attributes
    ----------
    calibration_year : int
        The year used for calibration.

    target_year : int
        The target year for the scenario.

    default_urea : float
        The default amount of urea used for crop production.

    default_urea_abated : float
        The default amount of urea abated.

    sc_fetcher : ScenarioDataFetcher
        An instance of ScenarioDataFetcher to fetch scenario-specific data.

    goblin_data_manager_class : GoblinDataManager
        An instance of GoblinDataManager to manage goblin data.

    Methods
    -------
    generate_crop_data()
        Generates and returns a DataFrame based on national level crop data.
    
    generate_crop_farm_data(urea=None, urea_abated=None)
        Generates and returns a DataFrame of farm outputs.
    """
    def __init__(self,goblin_data_manager, scenario_dataframe):
        self.sc_fetcher = ScenarioDataFetcher(scenario_dataframe)
        self.goblin_data_manager_class = goblin_data_manager
        self.calibration_year = self.goblin_data_manager_class.get_calibration_year()
        self.target_year = self.goblin_data_manager_class.get_target_year()
        self.default_urea = self.goblin_data_manager_class.get_default_urea()
        self.default_urea_abated = self.goblin_data_manager_class.get_default_urea_abated()

    def generate_crop_data(self):
        """
        Generates and returns a DataFrame based on national level crop data.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing national level crop data.
        """
        scenarios = self.sc_fetcher.get_scenario_list()

        for sc in scenarios:
            if sc > 0:
                crop_df = NationalCropData.gen_scenario_crop_production_dataframe(
                    self.calibration_year, self.target_year, sc, crop_df
                )
            else:
                crop_df = NationalCropData.gen_scenario_crop_production_dataframe(
                    self.calibration_year, self.target_year, sc
                )

        return crop_df


    def generate_crop_farm_data(
            self, urea = None, urea_abated=None
        ):
        """
        Generates and returns a DataFrame of farm outputs.

        Parameters
        ----------
        urea : float, optional
            The amount of urea used for crop production. If not provided, the default value is used.

        urea_abated : float, optional
            The amount of urea abated. If not provided, the default value is used.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing farm outputs.
        """
        urea = self.default_urea if urea is None else urea
        urea_abated = self.default_urea_abated if urea_abated is None else urea_abated

        crop_dataframe = self.generate_crop_data()

        subset_df = self.sc_fetcher.get_urea_proportions()

        # Set 'Scenarios' as the index of the DataFrame
        subset_df = subset_df.set_index('Scenarios')

        crop_farm_data = NationalCropData.gen_farm_data(
            crop_dataframe, subset_df, urea, urea_abated
        )


        return crop_farm_data