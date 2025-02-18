"""
Landuse LCA Generator
=====================
This module contains the LandUseLCAGenerator class, which is responsible for generating land-use footprints for climate change.
"""

from goblin_lite.impact_categories.climate_change import ClimateChangeLandUse
from goblin_lite.resource_manager.database_manager import DataManager

class LandUseLCAGenerator:
    """
    Manages the calculation of climate change footprints associated with various land use types. 
    Employs the ClimateChangeLandUse class for specific calculations.

    Attributes
    ----------
    goblin_data_manager : GoblinDataManager
        An instance of the GoblinDataManager class for managing goblin-specific data.
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
    DATABASE_PATH : str, optional
        Path to the external database, if None, default internal database used.
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
    def __init__(self, goblin_data_manager, landuse_data, transition_matrix, forest_data):
        """
        Parameters
        ----------
        goblin_data_manager : GoblinDataManager
            An instance of the GoblinDataManager class for managing goblin-specific data.
        landuse_data : pandas.DataFrame
            Dataframe containing land use information.
        transition_matrix : pandas.DataFrame
            Dataframe representing transitions between land use types.
        forest_data : pandas.DataFrame
            Dataframe containing forest-related data.
        """
        self.goblin_data_manager = goblin_data_manager
        self.DATABASE_PATH = self.goblin_data_manager.get_database_path()
        self.data_manager_class = DataManager(self.DATABASE_PATH)
        self.ef_country = self.goblin_data_manager.get_ef_country()
        self.calibration_year = self.goblin_data_manager.get_calibration_year()
        self.target_year = self.goblin_data_manager.get_target_year()
        self.landuse_data = landuse_data
        self.transition_matrix = transition_matrix
        self.forest_data = forest_data


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

        climate_change_landuse_class = ClimateChangeLandUse(
            self.goblin_data_manager,
            self.transition_matrix,
            self.landuse_data,
            self.forest_data
        )

        climate_change_landuse = climate_change_landuse_class.climate_change_landuse()

        self.data_manager_class.save_goblin_results_to_database(("climate_change_landuse", climate_change_landuse))