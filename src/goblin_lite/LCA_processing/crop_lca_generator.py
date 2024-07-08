"""
Crop LCA Generator
==================
This module contains the CropLCAGenerator class, which is responsible for generating crop footprints for climate change, eutrophication, and air quality.
"""
from goblin_lite.resource_manager.goblin_data_manager import GoblinDataManager
from goblin_lite.resource_manager.database_manager import DataManager
from goblin_lite.impact_categories.climate_change import ClimateChangeCrop
from goblin_lite.impact_categories.eutrophication import EurtrophicationCrop
from goblin_lite.impact_categories.air_quality import AirQualityCrop


class CropLCAGenerator:
    """
    Manages the calculation of crop-related footprints for various environmental impacts. 
    Leverages external classes for specific impact calculations.   

    Attributes
    ----------
    data_manager_class : DataManager
        An instance of the DataManager class for database interactions.
    goblin_data_manager : GoblinDataManager
        Handles data management for the GOBLIN LCA framework. 
    crop_dataframe : pandas.DataFrame
        Dataframe containing crop-related data.
    scenario_dataframe : pandas.DataFrame
        Dataframe containing scenario-specific parameters.
    DATABASE_PATH : str, optional
        Path to the external database, if None, default internal database used.
    AR_VALUE : str 
        IPCC Assessment Report version (e.g., 'AR4', 'AR5') for impact calculations.
    ef_country : str
        Country code for emission factors.
    default_urea : float
        Default urea application rate.
    default_urea_abated :  float
        Default urea abated application rate.

    Methods
    -------
    generate_crop_footprint()
        Calculates footprints for climate change, eutrophication, and air quality.

    generate_aggregated_crop_footprint()
        Calculates aggregated climate change footprints for crops.  
    """
    def __init__(self, ef_country, crop_dataframe, scenario_dataframe, DATABASE_PATH, AR_VALUE):
        self.data_manager_class = DataManager(DATABASE_PATH)
        self.goblin_data_manager = GoblinDataManager(AR_VALUE=AR_VALUE)
        self.crop_dataframe = crop_dataframe
        self.scenario_dataframe = scenario_dataframe
        self.AR_VALUE = AR_VALUE
        self.ef_country = ef_country
        self.default_urea = self.goblin_data_manager.get_default_urea()
        self.default_urea_abated = self.goblin_data_manager.get_default_urea_abated()

    def generate_crop_footprint(
        self, urea=None, urea_abated=None
    ):
        """
        Generate crop footprints for climate change, eutrophication, and air quality for each scenario.

        This method calculates and generates crop footprints for climate change, eutrophication, and air quality for each
        scenario based on the crop_dataframe and scenario_dataframe class attributes. The footprints are computed using default urea 
        and urea abated values (these can be overridden ) for the baseline, while urea values are derived from the scenario_dataframe for each scenario.
        The AR Value (AR4, AR5) is derived from the class attributes, which defaults to AR5.

        Data is saved to the database using the `save_goblin_results_to_database` method from the DataManager class.

        Details 
        -------
        * Footprints are generated for each scenario.
        * Employs default urea values for the baseline, scenario-specific urea from the `scenario_dataframe`.
        * Leverages the following classes:
            * ClimateChangeCrop
            * EutrophicationCrop
            * AirQualityCrop
        * Saves results to a database via the DataManager class.

        Parameters
        ----------
        urea : float, optional 
            Urea application rate. Defaults to class-level default.
        urea_abated : float, optional 
            Urea abated application rate. Defaults to class-level default.

        Returns
        -------
        None
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country

        urea = self.default_urea if urea is None else urea
        urea_abated = self.default_urea_abated if urea_abated is None else urea_abated

        climate_change_crop_class = ClimateChangeCrop(
            ef_country, urea, urea_abated, AR_VALUE
        )

        climate_change_crops_disaggregated = climate_change_crop_class.climate_change_crops_dissagregated(
            self.crop_dataframe, self.scenario_dataframe
        )

        eutrophication_crop_class = EurtrophicationCrop(
            ef_country, urea, urea_abated
        )

        eutrophication_crops_disaggregated = eutrophication_crop_class.eutrophication_crops_dissagregated(
            self.crop_dataframe, self.scenario_dataframe
        )

        air_quality_crop_class = AirQualityCrop(
            ef_country, urea, urea_abated
        )

        air_quality_crops_disaggregated = air_quality_crop_class.air_quality_crops_dissagregated(
            self.crop_dataframe, self.scenario_dataframe
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_crops_disaggregated", climate_change_crops_disaggregated),
                                                                ("eutrophication_crops_disaggregated", eutrophication_crops_disaggregated),
                                                                ("air_quality_crops_disaggregated", air_quality_crops_disaggregated))


    def generate_aggregated_crop_footprint(self, urea=None, urea_abated=None):
        """
        Generate aggregated crop footprints for climate change.

        This method calculates and generates aggregated crop footprints for climate change based on the provided crop_dataframe
        and scenario_dataframe. The footprints for the baseline are computed using default urea and urea abated values (these can be overridden), 
        as well as the AR value (AR4, AR5), defaults to AR5, specified in the class instance.

        Data is saved to the database using the `save_goblin_results_to_database` method from the DataManager class.

        Details 
        -------
        * Footprints are generated for each scenario.
        * Employs default urea values for the baseline, scenario-specific urea from the `scenario_dataframe`.
        * Leverages the ClimateChangeCrop class.
        * Saves results to a database via the DataManager class.

        Parameters
        ----------
        urea : float, optional 
            Urea application rate. Defaults to class-level default.
        urea_abated : float, optional 
            Urea abated application rate. Defaults to class-level default.


        Returns
        -------
        None
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country

        urea = self.default_urea if urea is None else urea
        urea_abated = self.default_urea_abated if urea_abated is None else urea_abated

        climate_change_crop_class = ClimateChangeCrop(
            ef_country, urea, urea_abated, AR_VALUE
        )

        climate_change_categories_as_co2e = (
            climate_change_crop_class.climate_change_crops_categories_as_co2e(
                self.crop_dataframe, self.scenario_dataframe
            )
        )
        climate_change_crops_aggregated = (
            climate_change_crop_class.climate_change_crops_aggregated(
                self.crop_dataframe, self.scenario_dataframe
            )
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_crops_categories_as_co2e", climate_change_categories_as_co2e),
                                                                ("climate_change_crops_aggregated", climate_change_crops_aggregated))
