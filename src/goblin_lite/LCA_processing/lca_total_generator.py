"""
LCA Total Generator
===================
This module contains the LCATotalGenerator class, which is responsible for generating total footprints for climate change, eutrophication, and air quality.
"""
from goblin_lite.resource_manager.data_fetcher import DataFetcher
from goblin_lite.resource_manager.database_manager import DataManager
from goblin_lite.impact_categories.climate_change import ClimateChangeTotal
from goblin_lite.impact_categories.eutrophication import EutrophicationTotal
from goblin_lite.impact_categories.air_quality import AirQualityTotal


class LCATotalGenerator:
    """
    Manages the calculation of total environmental footprints (climate change, eutrophication, air quality). 
    Utilizes ClimateChangeTotal, EutrophicationTotal, and AirQualityTotal classes.

    Attributes
    ----------
    db_reference_class : DataFetcher
        An instance of the DataFetcher class for retrieving data.
    data_manager_class : DataManager
        An instance of the DataManager class for database interactions.
    calibration_year : int
        Base year for model calibration.
    target_year : int 
        Year of analysis.
    scenario_dataframe : pandas.DataFrame
        Dataframe containing scenario-specific parameters.
    DATABASE_PATH : str, optional
        Path to the external database, if None, default internal database used.

    Methods
    -------
    generate_climate_change_totals()
        Calculates total climate change emissions for scenarios.
    generate_eutrophication_totals()
        Calculates total eutrophication emissions for scenarios.
    generate_air_quality_totals()
        Calculates total air quality emissions for scenarios.
    get_climate_emission_dataframes()
        Fetches climate change emission dataframes by category.
    get_air_quality_emission_dataframes()
        Fetches air quality emission dataframes by category.
    get_eutrophication_emission_dataframes()
        Fetches eutrophication emission dataframes by category.
    """
    def __init__(self, calibration_year, target_year, scenario_dataframe, DATABASE_PATH):
        self.db_reference_class = DataFetcher(DATABASE_PATH)
        self.data_manager_class = DataManager(DATABASE_PATH)
        self.calibration_year = calibration_year
        self.target_year = target_year
        self.scenario_dataframe = scenario_dataframe


    def generate_climate_change_totals(self):
        """
        Calculates total climate change emissions for scenarios.

        Details 
        -------
        * Leverages the ClimateChangeTotal class.
        * Fetches emission dataframes using `get_climate_change_emission_dataframes()`.
        * Saves results to a database via the DataManager class.

        Returns
        -------
        None
        """   
        climate_class = ClimateChangeTotal()

        dataframes = self.get_climate_emission_dataframes()

        climate_change_totals = climate_class.total_climate_change_emissions(
            self.calibration_year, self.target_year, self.scenario_dataframe, dataframes
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_totals", climate_change_totals))


    def generate_eutrophication_totals(self):
        """
        Calculates total eutrophication emissions for scenarios.

        Details 
        -------
        * Leverages the EutrophicationTotal class.
        * Fetches emission dataframes using `get_eutrophication_emission_dataframes()`.
        * Saves results to a database via the DataManager class.

        Returns
        -------
        None
        """   
        eutrophication_class = EutrophicationTotal()

        dataframes = self.get_eutrophication_emission_dataframes()

        eutrophication = eutrophication_class.total_eutrophication_emissions(dataframes)

        self.data_manager_class.save_goblin_results_output_datatable(
            eutrophication, "eutrophication_totals"
        )



    def generate_air_quality_totals(self):
        """
        Calculates total air quality emissions for scenarios.

        Details 
        -------
        * Leverages the AirQualityTotal class.
        * Fetches emission dataframes using `get_air_quality_emission_dataframes()`.
        * Saves results to a database via the DataManager class.

        Returns
        -------
        None
        """ 
        air_quality_class = AirQualityTotal()

        dataframes = self.get_air_quality_emission_dataframes()

        air_quality = air_quality_class.total_air_quality_emissions(dataframes)

        self.data_manager_class.save_goblin_results_output_datatable(
            air_quality, "air_quality_totals"
        )


    def get_climate_emission_dataframes(self):
        """
        Retrieves dataframes containing climate change emissions by category.

        This method fetches dataframes containing climate change emissions for different categories, such as "crop," "animal,"
        and "land," using the DataFetcher class.


        Returns
        -------
        dict
            A dictionary containing dataframes of climate change emissions for different categories.
        """

        crop = self.db_reference_class.get_climate_change_crop_emissions_aggregated()
        animal = self.db_reference_class.get_climate_change_animal_emissions_aggregated()
        land = self.db_reference_class.get_landuse_emissions_totals()

        total_emissions_dict = {
            "crop": crop,
            "animal": animal,
            "land": land,
        }

        return total_emissions_dict
    

    def get_air_quality_emission_dataframes(self):
        """
        Retrieves dataframes containing air quality emissions by category.

        This method fetches dataframes containing air quality emissions for different categories, such as "crop" and
        "animal," using the DataFetcher class.

        Returns
        -------
        dict
            A dictionary containing dataframes of air quality emissions for different categories.

        """

        crop = self.db_reference_class.get_air_quality_crop_emissions_by_category()
        animal = self.db_reference_class.get_air_quality_animal_emissions_by_category()

        total_emissions_dict = {
            "crop": crop,
            "animal": animal,
        }

        return total_emissions_dict
    
    def get_eutrophication_emission_dataframes(self):
        """
        Retrieves dataframes containing eutrophication emissions by category.

        This method fetches dataframes containing eutrophication emissions for different categories, such as "crop" and
        "animal," using the DataFetcher class.

        Returns
        -------
        dict
            A dictionary containing dataframes of eutrophication emissions for different categories.

        """

        crop = self.db_reference_class.get_eutrophication_crop_emissions_by_category()
        animal = self.db_reference_class.get_eutrophication_animal_emissions_by_category()

        total_emissions_dict = {
            "crop": crop,
            "animal": animal,
        }

        return total_emissions_dict