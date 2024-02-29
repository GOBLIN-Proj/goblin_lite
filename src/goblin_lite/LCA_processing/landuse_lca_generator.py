"""
Landuse LCA Generator
=====================
This module contains the LandUseLCAGenerator class, which is responsible for generating land-use footprints for climate change.
"""

from goblin_lite.LCA_processing.impact_categories import ClimateChangeLandUse
from goblin_lite.resource_manager.database_manager import DataManager

class LandUseLCAGenerator:
    """
    Manages the calculation of climate change footprints associated with various land use types. 
    Employs the ClimateChangeLandUse class for specific calculations.

    Attributes
    ----------
    data_manager_class : DataManager
        An instance of the DataManager class for database interactions.
    ef_country : str
        Country code for emission factors.
    calibration_year : int
        Base year for model calibration.
    target_year : int 
        Year of analysis.
    landuse_data : pandas.DataFrame
        Dataframe containing land use information.
    transition_matrix : pandas.DataFrame
        Dataframe representing transitions between land use types.
    forest_data : pandas.DataFrame
        Dataframe containing forest-related data.
    AR_VALUE : str
        IPCC Assessment Report version (e.g., 'AR4', 'AR5') for impact calculations.

    Methods
    -------
    generate_landuse_footprint()
        Calculates climate change footprints for various land use types.

    Notes
    -----
    The wetlands category includes emissions from extraction and use of horticultural peat.
    """
    def __init__(self, ef_country, calibration_year, target_year, landuse_data, transition_matrix, forest_data, AR_VALUE):
        self.data_manager_class = DataManager()
        self.ef_country = ef_country
        self.calibration_year = calibration_year
        self.target_year = target_year
        self.landuse_data = landuse_data
        self.transition_matrix = transition_matrix
        self.forest_data = forest_data
        self.AR_VALUE = AR_VALUE


    def generate_landuse_footprint(self):
        """
        Calculates climate change footprints for various land use types (forest, grassland, wetland, cropland).

        Details
        -------
        * Leverages the ClimateChangeLandUse class.
        * Employs AR value (AR4, AR5) from the class instance for calculations.
        * Saves results to a database via the DataManager class.

        Returns
        -------
        None
        """   
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country
        calibration_year = self.calibration_year
        target_year = self.target_year

        climate_change_landuse_class = ClimateChangeLandUse(
            calibration_year,
            target_year,
            self.transition_matrix,
            self.landuse_data,
            self.forest_data,
            ef_country,
            AR_VALUE,
        )

        climate_change_landuse = climate_change_landuse_class.climate_change_landuse()

        self.data_manager_class.save_goblin_results_to_database(("climate_change_landuse", climate_change_landuse))