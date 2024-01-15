"""
===================
Goblin lite module
===================

The Goblin Lite module is designed for running environmental impact scenarios, particularly focused on land use, 
livestock, crop production, and their associated impacts on climate change, air quality, and eutrophication. It 
utilizes various data sources and models to simulate scenarios and calculate the environmental footprints of different 
agricultural practices and land use changes at the national level in the Irish context.

Classes
-------
ScenarioRunner
    A class responsible for orchestrating the entire scenario generation process, utilizing other classes and methods 
    to generate, analyze, and store scenario data.

Dependencies
------------
- ScenarioGeneration
- AnimalData
- Exports
- GrasslandOutput
- AirQualityTotal, EutrophicationTotal, ClimateChangeTotal
- DataManager
- DataFetcher
- TransitionMatrix
- LandCover
- Afforestation
- Runner
- NationalCropData

Usage
-----
The ScenarioRunner class is initialized with country-specific parameters, calibration year, target year, scenario 
configuration file path, and CBM CFS3 configuration file path. It generates a series of data tables representing 
various aspects of environmental impact under different agricultural and land use scenarios. These tables are stored 
and can be accessed for further analysis and visualization.

Key Methods
-----------
- run_scenarios(): Orchestrates the scenario generation process.
- generate_livestock_outputs(): Calculates livestock production outputs for scenarios.
- generate_air_quality_totals(), generate_eutrophication_totals(), generate_climate_change_totals(): Generate total 
  emissions and impacts for air quality, eutrophication, and climate change.
- generate_transition_matrix(): Creates a matrix representing land use transitions.
- generate_landuse_data(): Produces land use data based on scenario inputs.
- generate_crop_data(), generate_crop_farm_data(): Generate crop-related data and crop farm inputs.
- generate_baseline_farm_inputs(), generate_scenario_farm_inputs(): Estimate grassland farm inputs for baseline and scenario 
  cases.
- generate_grassland_areas(): Calculates spared and total grassland areas, spared area by soil group, and stocking rate for scenarios.
- generate_crop_footprint(), generate_aggregated_crop_footprint(): Calculate environmental footprints associated with crop production.
- generate_landuse_footprint(): Computes the environmental footprint of land use.
- generate_livestock_footprint(), generate_aggregated_livestock_footprint(): Estimate environmental impacts of livestock production.
- generate_afforestation_data(): Generates data related to afforestation activities.
- generate_forest_carbon(): Calculates forest carbon data based on afforestation and scenario data.

"""
from static_scenario_generator.scenarios import ScenarioGeneration
from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports
from grassland_production.grassland_output import GrasslandOutput
from goblin_lite.impact_categories import (
    AirQualityTotal,
    EutrophicationTotal,
    ClimateChangeTotal,
    ClimateChangeLivestock,
    EutrophicationLivestock,
    AirQualityLivestock,
    ClimateChangeLandUse,
    ClimateChangeCrop,
    EurtrophicationCrop,
    AirQualityCrop,
)
from goblin_lite.database_manager import DataManager
from goblin_lite.data_fetcher import DataFetcher
from landcover_assignment.transition_matrix import TransitionMatrix
from landcover_assignment.landcover import LandCover
from landcover_assignment.afforestation import Afforestation
from cbm_runner.runner import Runner
from crop_lca.national_crop_production import NationalCropData
import copy as copy
import numpy as np


class ScenarioRunner:
    """A class used to run scenarios based on the input configuration files. There are two configuration files required:
    (1) Scenario configuration files, containing the specified scenario parameters, (2) The CBM CFS3 configuration file, containing the nationally specific
    forest configuration settings.

    In total, the scenario runner generates data for each scenario and the selected baseline contained in 29 tables. These data tables can be referenced using the DataFetcher
    class, and visualized using the DataGrapher class.

    Tables are returned as pandas dataframes.

    Attributes
    ----------
    AR_VALUE : str
        The Assessment Report value. Default is "AR5".
    ef_country : str
        The country for which the scenario is being run.
    calibration_year : int
        The year for calibration data.
    target_year : int
        The target year for which the scenario is generated.
    config_path : str
        The path to the scenario configuration file.
    cbm_config_path : str
        The path to the CBM CFS3 configuration file.
    scenario_class : ScenarioGeneration
        An instance of the ScenarioGeneration class.
    data_manager_class : DataManager
        An instance of the DataManager class.

    Methods
    -------
    run_scenarios():
        Runs the scenario generation process based on the provided inputs.

    generate_livestock_outputs(scenario_animal_data, baseline_animal_data, scenario_inputs_df):
        Generates livestock outputs based on the scenario animal data, baseline animal data, and scenario inputs dataframe.

    generate_air_quality_totals(scenario_dataframe):
        Generates air quality totals based on the scenario dataframe.

    generate_eutrophication_totals(scenario_dataframe):
        Generates eutrophication totals based on the scenario dataframe.

    generate_climate_change_totals(calibration_year, target_year, scenario_dataframe):
        Generates climate change totals based on the calibration year, target year, and scenario dataframe.

    get_air_quality_emission_dataframes():
        Retrieves air quality emission dataframes.

    get_eutrophication_emission_dataframes():
        Retrieves eutrophication emission dataframes.

    get_climate_emission_dataframes():
        Retrieves climate emission dataframes.

    generate_transition_matrix(scenario_dataframe, grassland_area, spared_area):
        Generates the transition matrix based on the scenario dataframe, grassland area, and spared area.

    generate_landuse_data(scenario_dataframe, grassland_area, spared_area):
        Generates land use data based on the scenario dataframe, grassland area, and spared area.

    generate_crop_data(scenario_dataframe):
        Generates crop data based on the scenario dataframe.

    generate_crop_farm_data(scenario_dataframe, crop_dataframe, default_urea, default_urea_abated):
        Generates crop farm data based on the scenario dataframe, crop dataframe, default urea, and default urea abated.

    generate_baseline_farm_inputs(scenario_dataframe, scenario_animal_data, baseline_animal_data):
        Generates baseline farm inputs based on the scenario dataframe, scenario animal data, and baseline animal data.

    generate_scenario_farm_inputs(scenario_dataframe, scenario_animal_data, baseline_animal_data):
        Generates scenario farm inputs based on the scenario dataframe, scenario animal data, and baseline animal data.

    generate_grassland_areas(scenario_dataframe, scenario_animal_data, baseline_animal_data):
        Generates grassland areas and stocking rates based on the scenario dataframe, scenario animal data, and baseline animal data.

    generate_crop_footprint(crop_dataframe, scenario_dataframe, default_urea, default_urea_abated):
        Generates crop footprint based on the crop dataframe, scenario dataframe, default urea, and default urea abated.

    generate_aggregated_crop_footprint(crop_dataframe, scenario_dataframe, default_urea, default_urea_abated):
        Generates aggregated crop footprint based on the crop dataframe, scenario dataframe, default urea, and default urea abated.

    generate_landuse_footprint(landuse_data, transition_matrix, forest_data):
        Generates land use footprint based on the land use data, transition matrix, and forest data.

    generate_livestock_footprint(baseline_animal_data, scenario_animal_data, farm_inputs_baseline, farm_inputs_scenario):
        Generates livestock footprint based on the baseline animal data, scenario animal data, farm inputs for the baseline, and farm inputs for the scenario.

    generate_aggregated_livestock_footprint(baseline_animal_data, scenario_animal_data, farm_inputs_baseline, farm_inputs_scenario):
        Generates aggregated livestock footprint based on the baseline animal data, scenario animal data, farm inputs for the baseline, and farm inputs for the scenario.

    generate_afforestation_data(transition_matrix, scenario_dataframe):
        Generates afforestation data based on the transition matrix and scenario dataframe.

    generate_forest_carbon(afforestation_dataframe, scenario_dataframe):
        Generates forest carbon data based on the afforestation dataframe and scenario dataframe.
    """

    def __init__(
        self,
        ef_country,
        calibration_year,
        target_year,
        config_path,
        cbm_config_path,
        AR_VALUE="AR5",
    ):
        self.AR_VALUE = AR_VALUE
        self.ef_country = ef_country
        self.calibration_year = calibration_year
        self.target_year = target_year
        self.config_path = config_path
        self.cbm_config_path = cbm_config_path
        self.scenario_class = ScenarioGeneration()
        self.data_manager_class = DataManager()

    def run_scenarios(self):
        """
        Executes the scenario generation process using provided inputs and configurations.

        This method manages the complete scenario generation process. It prepares and generates data for various scenarios
        and the selected baseline across multiple domains (such as animal data, land use, crop data, carbon flux, etc.), 
        encapsulated in 26 distinct data tables. These tables are saved as pandas dataframes and are intended for subsequent
        analysis and visualization.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        The method executes the following steps:

        1. Initialize or clear the database using the DataManager instance (:attr:`data_manager_class`).

        2. Generate scenario input data by invoking the `generate_scenario_dataframe` method of the ScenarioGeneration class
        (:attr:`scenario_class`), using the configuration path provided in :attr:`config_path`.

        3. Create instances of the AnimalData class (:attr:`animal_class`) to generate data for animals, using parameters
        such as :attr:`ef_country`, :attr:`baseline_year`, :attr:`target_year`, and the generated scenario input data.

        4. Generate baseline and scenario-specific animal data using methods from the AnimalData class.

        5. Calculate farm inputs for both the baseline and scenario contexts using generated animal data.

        6. Compute Grassland area data and stocking rates based on the animal data and scenario inputs.

        7. Generate crop-related data and crop farm data for the scenario using the scenario input data.

        8. Create a transition matrix for land use changes and generate associated land use data.

        9. Produce afforestation data and corresponding forest carbon data, including flux and aggregate calculations,
        using the Carbon Budget Model (CBM) CFS3 runner.

        10. Execute Life Cycle Assessment (LCA) calculations for various environmental impact metrics, such as crop and
            livestock footprints, climate change, eutrophication, and air quality impacts.

        11. Generate summary outputs for livestock, including protein and milk production analysis, based on the animal data.

        12. Save all generated data to the database using the `save_goblin_results_to_database` method of the DataManager class,
            ensuring each dataset is labeled with its respective name for identification and retrieval.

        13. Print a completion message upon successfully running all scenarios.

        The method extensively utilizes class attributes and methods, assuming their availability and proper initialization
        within the class context when this method is invoked.
        """
        

        self.data_manager_class.create_or_clear_database()

        path = self.config_path
        ef_country = self.ef_country
        baseline_year = self.calibration_year
        target_year = self.target_year
        calibration_year = self.calibration_year

        default_urea = 0.2
        default_urea_abated = 0

        # generate scenario_data
        scenario_input_dataframe = self.scenario_class.generate_scenario_dataframe(path)

        try:
            afforest_year = scenario_input_dataframe["Afforest year"].unique().item()
        except ValueError as e:
            raise ValueError(
                "Error may be a results of multiple Afforest, scenarios should have identical Afforest years ... ",
                e,
            )

        animal_class = AnimalData(
            ef_country, baseline_year, target_year, scenario_input_dataframe
        )

        baseline_animal_data = animal_class.create_baseline_animal_dataframe()

        # create dataframe for scenarios animals
        scenario_animal_data = animal_class.create_animal_dataframe()

        # farm inputs
        grassland_farm_inputs_scenario = self.generate_scenario_farm_inputs(
            scenario_input_dataframe, scenario_animal_data, baseline_animal_data
        )

        grassland_farm_inputs_baseline = self.generate_baseline_farm_inputs(
            scenario_input_dataframe, scenario_animal_data, baseline_animal_data
        )

        # Grassland
        total_spared_area, total_grassland_area, total_spared_area_by_soil_group, per_hectare_stocking_rate= self.generate_grassland_areas(
            scenario_input_dataframe, scenario_animal_data, baseline_animal_data
        )

        crop_input_data = self.generate_crop_data(scenario_input_dataframe)
        crop_farm_data = self.generate_crop_farm_data(
            scenario_input_dataframe, crop_input_data, default_urea, default_urea_abated
        )

        transition_matrix = self.generate_transition_matrix(
            scenario_input_dataframe, total_grassland_area, total_spared_area
        )


        landuse_data = self.generate_landuse_data(
            scenario_input_dataframe, total_grassland_area, total_spared_area
        )

        cbm_afforestation_data = self.generate_afforestation_data(
            transition_matrix, scenario_input_dataframe
        )

        forest_data = self.generate_forest_carbon(
            afforest_year, cbm_afforestation_data, scenario_input_dataframe
        )

        forest_carbon_flux = forest_data["forest_flux"]
        forest_carbon_aggregate = forest_data["forest_aggregate"]

        # livestock ouputs
        protein_and_milk_summary = self.generate_livestock_ouputs(
            scenario_animal_data, baseline_animal_data, scenario_input_dataframe
        )

        #SAVE DATA
        self.data_manager_class.save_goblin_results_to_database(("scenario_input_dataframe",scenario_input_dataframe),
                                                                ("baseline_animal_data",baseline_animal_data),
                                                                ("scenario_animal_data",scenario_animal_data),
                                                                ("grassland_farm_inputs_scenario",grassland_farm_inputs_scenario),
                                                                ("grassland_farm_inputs_baseline",grassland_farm_inputs_baseline),
                                                                ("total_spared_area",total_spared_area),
                                                                ("total_grassland_area",total_grassland_area),
                                                                ("total_spared_area_by_soil_group",total_spared_area_by_soil_group),
                                                                ("per_hectare_stocking_rate",per_hectare_stocking_rate),
                                                                ("crop_input_data",crop_input_data),
                                                                ("crop_farm_data",crop_farm_data),
                                                                ("transition_matrix",transition_matrix),
                                                                ("landuse_data",landuse_data),
                                                                ("cbm_afforestation_data",cbm_afforestation_data),
                                                                ("forest_carbon_flux",forest_carbon_flux),
                                                                ("forest_carbon_aggregate",forest_carbon_aggregate),
                                                                ("protein_and_milk_summary",protein_and_milk_summary))

        # LCA
        self.generate_crop_footprint(
            crop_input_data, scenario_input_dataframe, default_urea, default_urea_abated
        )
        self.generate_aggregated_crop_footprint(
            crop_input_data, scenario_input_dataframe, default_urea, default_urea_abated
        )
        self.generate_landuse_footprint(
            landuse_data, transition_matrix, forest_data["forest_flux"]
        )
        self.generate_livestock_footprint(
            baseline_animal_data,
            scenario_animal_data,
            grassland_farm_inputs_baseline,
            grassland_farm_inputs_scenario,
            landuse_data, 
            transition_matrix,
            crop_input_data
        )
        self.generate_aggregated_livestock_footprint(
            baseline_animal_data,
            scenario_animal_data,
            grassland_farm_inputs_baseline,
            grassland_farm_inputs_scenario,
            landuse_data, 
            transition_matrix,
            crop_input_data
        )

        self.generate_climate_change_totals(
            calibration_year, target_year, scenario_input_dataframe
        )

        self.generate_eutrophication_totals()

        self.generate_air_quality_totals()

        print("Scenario Generation Complete ... \n")


    def generate_livestock_ouputs(
        self, scenario_animal_data, baseline_animal_data, scenario_inputs_df
    ):
        """
        Generates and returns a summary DataFrame of livestock outputs for the given scenario.

        This method leverages the Exports class to calculate protein and milk production based on scenario-specific and baseline 
        animal data. It produces a summary DataFrame combining milk production data and beef (carcass) weight from protein production data.

        Parameters
        ----------
        scenario_animal_data : pandas.DataFrame
            A DataFrame containing animal-related data specific to the scenario being analyzed.

        baseline_animal_data : pandas.DataFrame
            A DataFrame containing baseline animal-related data for comparison.

        scenario_inputs_df : pandas.DataFrame
            A DataFrame containing scenario-specific input data required for livestock output calculations.

        Returns
        -------
        pandas.DataFrame
            A summary DataFrame, named protein_and_milk_summary, combining milk production data and beef carcass weight, 
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

        ef_country = self.ef_country
        calibration_year = self.calibration_year
        target_year = self.target_year

        export_class = Exports(
            ef_country, calibration_year, target_year, scenario_inputs_df
        )

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
    

    def generate_air_quality_totals(self):
        """
        Generates total air quality emissions for the given scenario.

        This method calculates and generates the total air quality emissions for the specified scenarios based on the provided
        calculated air_quality emissions for crop and livestock. It uses the AirQualityTotal class to perform the calculations.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A DataFrame containing the scenario-specific data required for air quality emissions calculations.

        Returns
        -------
        None

        Notes
        -----
        The method utilizes the scenario_dataframe and the calculated air_quality emission for crop and livestock to determine the scenario-specific data for air quality emissions in total.
        calculations.

        It calls the get_air_quality_emission_dataframes method to obtain dataframes containing air quality emissions for
        different categories (e.g., crop, animal) using the DataFetcher class. These dataframes are used in the calculations
        performed by the AirQualityTotal class.

        The air_quality_class instance of AirQualityTotal is responsible for calculating the total air quality emissions
        for the given scenario. The result is stored in the air_quality DataFrame.

        The generated air_quality DataFrame is then saved as "air_quality_totals" using the DataManager instance
        (:attr:`data_manager_class`).

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        air_quality_class = AirQualityTotal()

        dataframes = self.get_air_quality_emission_dataframes()

        air_quality = air_quality_class.total_air_quality_emissions(dataframes)

        self.data_manager_class.save_goblin_results_output_datatable(
            air_quality, "air_quality_totals"
        )

    def generate_eutrophication_totals(self):
        """
        Generates total eutrophication emissions for the given scenario.

        This method calculates and generates the total eutrophication emissions for the specified scenarios based on the
        provided scenario_dataframe. It uses the EutrophicationTotal class to perform the calculations.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A DataFrame containing the scenario-specific data required for eutrophication emissions calculations.

        Returns
        -------
        None

        Notes
        -----
        The method utilizes the scenario_dataframe to determine the scenario-specific data for eutrophication emissions
        calculations.

        It calls the get_eutrophication_emission_dataframes method to obtain dataframes containing eutrophication emissions
        for different categories (e.g., crop, animal) using the DataFetcher class. These dataframes are used in the
        calculations performed by the EutrophicationTotal class.

        The eutrophication_class instance of EutrophicationTotal is responsible for calculating the total eutrophication
        emissions for the given scenario. The result is stored in the eutrophication DataFrame.

        The generated eutrophication DataFrame is then saved as "eutrophication_totals" using the DataManager instance
        (:attr:`data_manager_class`).

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        eutrophication_class = EutrophicationTotal()

        dataframes = self.get_eutrophication_emission_dataframes()

        eutrophication = eutrophication_class.total_eutrophication_emissions(dataframes)

        self.data_manager_class.save_goblin_results_output_datatable(
            eutrophication, "eutrophication_totals"
        )

    def generate_climate_change_totals(
        self, calibration_year, target_year, scenario_dataframe
    ):
        """
        Generates total climate change emissions for the given scenario.

        This method calculates and generates the total climate change emissions for the specified scenarios based on the
        provided calibration_year, target_year, and scenario_dataframe. It uses the ClimateChangeTotal class to perform the
        calculations.

        Parameters
        ----------
        calibration_year : int
            The year representing the calibration period for the emissions calculations.

        target_year : int
            The year representing the target period for the emissions calculations.

        scenario_dataframe : pandas.DataFrame
            A DataFrame containing the scenario-specific data required for climate change emissions calculations.

        Returns
        -------
        None

        Notes
        -----
        The method utilizes the calibration_year, target_year, and scenario_dataframe to determine the scenario-specific
        data for climate change emissions calculations.

        It calls the get_climate_emission_dataframes method to obtain dataframes containing climate change emissions for
        different categories (e.g., crop, animal, land) using the DataFetcher class. These dataframes are used in the
        calculations performed by the ClimateChangeTotal class.

        The climate_class instance of ClimateChangeTotal is responsible for calculating the total climate change emissions
        for the given scenario, taking into account the specified calibration_year, target_year, and scenario_dataframe.
        The result is stored in the climate_change DataFrame.

        The generated climate_change DataFrame is then saved as "climate_change_totals" using the DataManager instance
        (:attr:`data_manager_class`).

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        climate_class = ClimateChangeTotal()

        dataframes = self.get_climate_emission_dataframes()

        climate_change_totals = climate_class.total_climate_change_emissions(
            calibration_year, target_year, scenario_dataframe, dataframes
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_totals", climate_change_totals))

    def get_air_quality_emission_dataframes(self):
        """
        Retrieves dataframes containing air quality emissions by category.

        This method fetches dataframes containing air quality emissions for different categories, such as "crop" and
        "animal," using the DataFetcher class.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing dataframes of air quality emissions for different categories.

        Notes
        -----
        The method utilizes the DataFetcher class to obtain the dataframes containing air quality emissions data by
        category. It calls the `get_air_quality_crop_emissions_by_category` and
        `get_air_quality_animal_emissions_by_category` methods from the DataFetcher class to fetch emissions data for crops
        and animals, respectively.

        The method then constructs a dictionary, `total_emissions_dict`, with keys representing different categories ("crop"
        and "animal") and their corresponding dataframes as values.

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """
        db_reference_class = DataFetcher()

        crop = db_reference_class.get_air_quality_crop_emissions_by_category()
        animal = db_reference_class.get_air_quality_animal_emissions_by_category()

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

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing dataframes of eutrophication emissions for different categories.

        Notes
        -----
        The method utilizes the DataFetcher class to obtain the dataframes containing eutrophication emissions data by
        category. It calls the `get_eutrophication_crop_emissions_by_category` and
        `get_eutrophication_animal_emissions_by_category` methods from the DataFetcher class to fetch emissions data for
        crops and animals, respectively.

        The method then constructs a dictionary, `total_emissions_dict`, with keys representing different categories ("crop"
        and "animal") and their corresponding dataframes as values.

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        db_reference_class = DataFetcher()

        crop = db_reference_class.get_eutrophication_crop_emissions_by_category()
        animal = db_reference_class.get_eutrophication_animal_emissions_by_category()

        total_emissions_dict = {
            "crop": crop,
            "animal": animal,
        }

        return total_emissions_dict

    def get_climate_emission_dataframes(self):
        """
        Retrieves dataframes containing climate change emissions by category.

        This method fetches dataframes containing climate change emissions for different categories, such as "crop," "animal,"
        and "land," using the DataFetcher class.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing dataframes of climate change emissions for different categories.

        Notes
        -----
        The method utilizes the DataFetcher class to obtain the dataframes containing climate change emissions data by
        category. It calls the `get_climate_change_crop_emissions_aggregated`, `get_climate_change_animal_emissions_aggregated`,
        and `get_landuse_emissions_totals` methods from the DataFetcher class to fetch emissions data for crops, animals,
        and land, respectively.

        The method then constructs a dictionary, `total_emissions_dict`, with keys representing different categories
        ("crop", "animal", and "land") and their corresponding dataframes as values.

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """
        db_reference_class = DataFetcher()

        crop = db_reference_class.get_climate_change_crop_emissions_aggregated()
        animal = db_reference_class.get_climate_change_animal_emissions_aggregated()
        land = db_reference_class.get_landuse_emissions_totals()

        total_emissions_dict = {
            "crop": crop,
            "animal": animal,
            "land": land,
        }

        return total_emissions_dict

    def generate_transition_matrix(
        self, scenario_dataframe, grassland_area, spared_area
    ):
        """
        Generates and returns a land use transition matrix for the specified scenario.

        This method computes a transition matrix, representing land use changes between categories, based on the scenario 
        parameters and land use data provided. It leverages the TransitionMatrix class for calculations, considering the 
        baseline year, target year, total grassland area, and spared area from conversion.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.
        grassland_area : pandas.DataFrame
            A pandas DataFrame the total area of grassland.
        spared_area : pandas.DataFrame
            A pandas DataFrame the area of grassland spared (destocked).

        Returns
        -------
        numpy.ndarray
            The generated transition matrix as a NumPy array, illustrating the land use changes.

        Notes
        -----
        The method follows these steps:
        1. Initializes an instance of the TransitionMatrix class using the calibration year as the baseline year, target year, 
        scenario parameters, grassland area, and spared area.
        2. Calls the `create_transition_matrix` method of the TransitionMatrix instance to calculate the transition matrix.
        3. Returns the computed transition matrix, which is a NumPy array depicting the area transitions between different 
        land use categories.

        The transition matrix quantifies the changes in land use areas, providing insights into how different land use categories 
        are expected to shift under the scenario.

        The attributes and methods referenced in this documentation are class attributes and methods and should be 
        available within the class instance when this method is called.
        """
        baseline_year = self.calibration_year
        target_year = self.target_year

        transition = TransitionMatrix(
            baseline_year, target_year, scenario_dataframe, grassland_area, spared_area
        )

        transition_matrix = transition.create_transition_matrix()

        return transition_matrix

    def generate_landuse_data(self, scenario_dataframe, grassland_area, spared_area):
        """
        Generates land use data based on scenario parameters and land area information.

        This method calculates the current and projected future land use data using scenario parameters, baseline year, target year,
        total grassland area, and spared grassland area.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.
        grassland_area : pandas.DataFrame
            A DataFrame representing the total area of grassland.
        spared_area : pandas.DataFrame
            A DataFrame representing the area of grassland spared (destocked).

        Returns
        -------
        pandas.DataFrame
            A pandas DataFrame containing the generated land use data, which includes current and projected future land use areas for different
            land use categories.

        Notes
        -----
        The method utilizes the LandCover class to calculate the current and future land use data based on the given scenario parameters,
        baseline year, target year, grassland area, and spared grassland area. The future land use data represents the projected land use areas
        for different land use categories, taking into account the spared grassland areas.

        The resulting land use data is saved as a datatable using the `save_goblin_results_output_datatable` method from the DataManager class
        with the name "landuse_data".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available within the class
        instance when this method is called.
        """
        baseline_year = self.calibration_year
        target_year = self.target_year

        land = LandCover(
            baseline_year, target_year, scenario_dataframe, grassland_area, spared_area
        )

        landuse_data = land.combined_future_land_use_area()

        return landuse_data

    def generate_crop_data(self, scenario_dataframe):
        """
        Generates crop data based on scenario parameters and national CSO crop production data.

        This method calculates crop data at the national level and given scenario parameters for urea, baseline year, and target year.
        It uses scenario-specific crop production data provided by the NationalCropData class. The resulting crop data is saved
        as a datatable using the DataManager class.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.

        Returns
        -------
        pandas.DataFrame
            A pandas DataFrame containing the generated crop data.

        Notes
        -----
        The method utilizes the NationalCropData class to generate crop production for from national level data for Ireland for each scenario
        based on the given baseline year, target year, and scenario. It iterates through unique scenario values in the
        scenario_dataframe and generates crop data accordingly. The generated crop data is stored in the crop_df variable
        for each scenario, and the final crop data for the last scenario is returned as the output.

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        baseline_year = self.calibration_year
        target_year = self.target_year
        scenarios = scenario_dataframe["Scenarios"].unique()

        for sc in scenarios:
            if sc > 0:
                crop_df = NationalCropData.gen_scenario_crop_production_dataframe(
                    baseline_year, target_year, sc, crop_df
                )
            else:
                crop_df = NationalCropData.gen_scenario_crop_production_dataframe(
                    baseline_year, target_year, sc
                )

        return crop_df

    def generate_crop_farm_data(
        self, scenario_dataframe, crop_dataframe, default_urea, default_urea_abated
    ):
        """
        Generates crop farm data representing fertilizer inputs for each scenario.

        This method calculates crop farm data representing fertilizer inputs (in kg) for each scenario. It utilizes the provided
        crop production data and scenario parameters to determine the total amount of fertilizers (urea, urea abated, total N,
        P, and K fertilizers) required at the national level.

        Parameters
        ----------
        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.

        crop_dataframe : pandas.DataFrame
            A pandas DataFrame containing crop production data for different scenarios.

        default_urea : float
            The default proportion of urea applied in crop farming.

        default_urea_abated : float
            The default proportion of urea abated in crop farming.

        Returns
        -------
        pandas.DataFrame
            A pandas DataFrame containing the generated crop farm data representing fertilizer inputs (in kg) for each scenario.

        Notes
        -----
        The method first selects specific columns, namely 'Scenarios', 'Urea proportion', and 'Urea abated proportion', from
        the scenario_dataframe and drops any duplicate rows. This results in a subset_df that contains unique scenario
        parameters related to urea proportion and abatement.

        Using the provided crop_dataframe and the subset_df, the method then utilizes the NationalCropData class to calculate
        the fertilizer inputs (in kg) at the national level for each crop. The total amount of fertilizers, including urea,
        urea abated, total N, P, and K fertilizers, is calculated based on the given urea proportion and abatement parameters.

        The generated crop farm data, representing fertilizer inputs (in kg) for each scenario, is saved as a datatable using
        the `save_goblin_results_output_datatable` method from the DataManager class with the name "crop_farm_data".

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        subset_df = scenario_dataframe[
            ["Scenarios", "Urea proportion", "Urea abated proportion"]
        ].drop_duplicates()

        # Set 'Scenarios' as the index of the DataFrame
        subset_df = subset_df.set_index('Scenarios')

        crop_farm_data = NationalCropData.gen_farm_data(
            crop_dataframe, subset_df, default_urea, default_urea_abated
        )


        return crop_farm_data

    def generate_baseline_farm_inputs(
        self, scenario_dataframe, scenario_animal_data, baseline_animal_data
    ):
        """
        Generates baseline farm inputs for grassland.

        This method estimates the baseline farm inputs (fertilizer) application to grassland, at the national
        level for each scenario. The fertilizer application rates specified in the scenario_dataframe are used to determine
        the total amount of fertilizer (in kg) required for grassland.

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
        pandas.DataFrame
            A pandas DataFrame containing the generated baseline farm inputs for grassland, specifically the fertilizer
            application (in kg) at the national level for the baseline.

        Notes
        -----
        The method utilizes the provided scenario_dataframe, scenario_animal_data, and baseline_animal_data to estimate the
        baseline farm inputs for grassland. The scenario_dataframe contains the specified fertilizer application rates, which
        are used to calculate the total amount of fertilizer (in kg) required at the national level for each scenario.

        The baseline farm inputs, representing the fertilizer application (in kg) for grassland, are determined based on the
        national level data. The generated baseline farm
        inputs data is saved as a datatable using the `save_goblin_results_output_datatable` method from the DataManager
        class with the name "grassland_farm_inputs_baseline".

        The attributes and methods referenced in this documentation are class attributes and methods and should be
        available within the class instance when this method is called.
        """

        ef_country = self.ef_country
        baseline_year = self.calibration_year
        target_year = self.target_year

        grassland_class = GrasslandOutput(
            ef_country,
            baseline_year,
            target_year,
            scenario_dataframe,
            scenario_animal_data,
            baseline_animal_data,
        )

        farm_inputs_baseline = grassland_class.baseline_farm_inputs_data()

        return farm_inputs_baseline

    def generate_scenario_farm_inputs(
        self, scenario_dataframe, scenario_animal_data, baseline_animal_data
    ):
        """
        Generates scenario-specific farm inputs for grassland.

        This method estimates the scenario-specific farm inputs (fertilizer) application to grassland, at the
        national level for each scenario. The fertilizer application rates specified in the scenario_dataframe are used to
        determine the total amount of fertilizer (in kg) required for grassland in each scenario.

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
        pandas.DataFrame
            A pandas DataFrame containing the generated scenario-specific farm inputs for grassland, specifically the fertilizer
            application (in kg) at the national level for each scenario.

        Notes
        -----
        The method utilizes the provided scenario_dataframe, scenario_animal_data, and baseline_animal_data to estimate the
        scenario-specific farm inputs for grassland. The scenario_dataframe contains the specified fertilizer application rates,
        which are used to calculate the total amount of fertilizer (in kg) required at the national level for each scenario.

        The scenario-specific farm inputs, representing the fertilizer application (in kg) for grassland in each scenario, are
        determined based on the specified fertilizer application rates in the scenario_dataframe and other relevant data. The
        generated scenario-specific farm inputs data is saved as a datatable using the `save_goblin_results_output_datatable`
        method from the DataManager class with the name "livestock_farm_inputs_scenario".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available
        within the class instance when this method is called.
        """

        ef_country = self.ef_country
        baseline_year = self.calibration_year
        target_year = self.target_year

        grassland_class = GrasslandOutput(
            ef_country,
            baseline_year,
            target_year,
            scenario_dataframe,
            scenario_animal_data,
            baseline_animal_data,
        )

        farm_inputs_scenario = grassland_class.farm_inputs_data()

        return farm_inputs_scenario

    def generate_grassland_areas(
        self, scenario_dataframe, scenario_animal_data, baseline_animal_data
    ):
        """
        Calculate the total spared and total grassland areas for each scenario.

        This method calculates and returns the total spared, total grassland areas, spared area by soil group and stocking rate for each scenario based on the provided
        scenario_dataframe, scenario_animal_data, and baseline_animal_data. The GrasslandOutput class is utilized to perform
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

        Notes
        -----
        The method uses the provided scenario_dataframe, scenario_animal_data, and baseline_animal_data to calculate the total
        spared and total grassland areas for each scenario. The GrasslandOutput class is utilized to perform the necessary
        calculations based on the specified parameters.

        The calculated total spared and total grassland areas for each scenario are returned as a tuple containing two pandas
        DataFrame representing the total spared and total grassland areas, respectively.

        Additionally, the method saves the calculated total spared area and total grassland area as datatables using the
        `save_goblin_results_output_datatable` method from the DataManager class. The spared area datatable is saved with the name
        "total_spared_area", and the grassland area datatable with the name "total_grassland_area".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available
        within the class instance when this method is called.
        """
        ef_country = self.ef_country
        baseline_year = self.calibration_year
        target_year = self.target_year

        grassland_class = GrasslandOutput(
            ef_country,
            baseline_year,
            target_year,
            scenario_dataframe,
            scenario_animal_data,
            baseline_animal_data,
        )

        spared_area = grassland_class.total_spared_area()
        total_grassland = grassland_class.total_grassland_area()

        total_spared_area_by_soil_group = grassland_class.total_spared_area_breakdown()
        per_hectare_stocking_rate = grassland_class.grassland_stocking_rate()

        return spared_area, total_grassland, total_spared_area_by_soil_group, per_hectare_stocking_rate


    def generate_crop_footprint(
        self, crop_dataframe, scenario_dataframe, default_urea, default_urea_abated
    ):
        """
        Generate crop footprints for climate change, eutrophication, and air quality for each scenario.

        This method calculates and generates crop footprints for climate change, eutrophication, and air quality for each
        scenario based on the provided crop_dataframe and scenario_dataframe. The footprints are computed using default urea
        and urea abated values for the baseline, while urea values are derived from the scenario_dataframe for each scenario.
        The AR Value (AR4, AR5) is derived from the class attributes, which defaults to "AR5".

        Parameters
        ----------
        crop_dataframe : pandas.DataFrame
            A pandas DataFrame containing crop production data.

        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.

        default_urea : float
            The default proportion of urea used in crop production.

        default_urea_abated : float
            The default proportion of urea abated in crop production.

        Notes
        -----
        The method utilizes three different classes: ClimateChangeCrop, EutrophicationCrop, and AirQualityCrop to calculate
        and generate the crop footprints for climate change, eutrophication, and air quality, respectively. Each class is
        instantiated with the appropriate parameters (ef_country, default_urea, default_urea_abated, and AR_VALUE) to perform
        the necessary calculations.

        The calculated crop footprints for each scenario are saved as datatables using the `save_goblin_results_output_datatable`
        method from the DataManager class. The footprints for climate change are saved with the name "climate_change_crops_disaggregated",
        the footprints for eutrophication are saved with the name "eutrophication_crops_disaggregated", and the footprints for air quality
        are saved with the name "air_quality_crops_disaggregated".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available
        within the class instance when this method is called.
        """

        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country

        climate_change_crop_class = ClimateChangeCrop(
            ef_country, default_urea, default_urea_abated, AR_VALUE
        )

        climate_change_crops_disaggregated = climate_change_crop_class.climate_change_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        eutrophication_crop_class = EurtrophicationCrop(
            ef_country, default_urea, default_urea_abated
        )

        eutrophication_crops_disaggregated = eutrophication_crop_class.eutrophication_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        air_quality_crop_class = AirQualityCrop(
            ef_country, default_urea, default_urea_abated
        )

        air_quality_crops_disaggregated = air_quality_crop_class.air_quality_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_crops_disaggregated", climate_change_crops_disaggregated),
                                                                ("eutrophication_crops_disaggregated", eutrophication_crops_disaggregated),
                                                                ("air_quality_crops_disaggregated", air_quality_crops_disaggregated))


    def generate_aggregated_crop_footprint(
        self, crop_dataframe, scenario_dataframe, default_urea, default_urea_abated
    ):
        """
        Generate aggregated crop footprints for climate change.

        This method calculates and generates aggregated crop footprints for climate change based on the provided crop_dataframe
        and scenario_dataframe. The footprints for the baseline are computed using default urea and urea abated values, as well as the AR value (AR4, AR5)
        specified in the class instance.

        Parameters
        ----------
        crop_dataframe : pandas.DataFrame
            A pandas DataFrame containing crop production data.

        scenario_dataframe : pandas.DataFrame
            A pandas DataFrame containing scenario parameters.

        default_urea : float
            The default proportion of urea used in crop production.

        default_urea_abated : float
            The default proportion of urea abated in crop production.

        Notes
        -----
        The method utilizes the ClimateChangeCrop class to calculate and generate the crop footprints for climate change. The
        class is instantiated with the appropriate parameters (ef_country, default_urea, default_urea_abated, and AR_VALUE) to
        perform the necessary calculations.

        Two types of aggregated footprints are generated: climate_change_categories_as_co2e and climate_change_crops_aggregated.
        The climate_change_categories_as_co2e represents the footprints for each category of climate change gas (converted to CO2e),
        and climate_change_crops_aggregated represents the overall aggregated footprint for all climate change gases.

        The calculated aggregated crop footprints for climate change are saved as datatables using the `save_goblin_results_output_datatable`
        method from the DataManager class. The footprints for individual categories of climate change gases are saved with the name
        "climate_change_crops_categories_as_co2e", and the overall aggregated footprint is saved with the name "climate_change_crops_aggregated".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available within
        the class instance when this method is called.
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country

        climate_change_crop_class = ClimateChangeCrop(
            ef_country, default_urea, default_urea_abated, AR_VALUE
        )

        climate_change_categories_as_co2e = (
            climate_change_crop_class.climate_change_crops_categories_as_co2e(
                crop_dataframe, scenario_dataframe
            )
        )
        climate_change_crops_aggregated = (
            climate_change_crop_class.climate_change_crops_aggregated(
                crop_dataframe, scenario_dataframe
            )
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_crops_categories_as_co2e", climate_change_categories_as_co2e),
                                                                ("climate_change_crops_aggregated", climate_change_crops_aggregated))


    def generate_landuse_footprint(self, landuse_data, transition_matrix, forest_data):
        """
        Generate land-use footprints for climate change.

        This method calculates and generates land-use (forest, grassland, wetland, cropland) footprints for climate change based on the provided landuse_data,
        transition_matrix, and forest_data. The footprints are computed using the AR value (AR4, AR5) specified in the class instance.

        Parameters
        ----------
        landuse_data : pandas.DataFrame
            A pandas DataFrame containing land-use data.

        transition_matrix : pandas.DataFrame
            A pandas DataFrame containing the transition matrix for land-use changes.

        forest_data : pandas.Series
            A pandas Series containing forest carbon data.

        Notes
        -----
        The method utilizes the ClimateChangeLandUse class to calculate and generate the land-use footprints for climate change.
        The class is instantiated with the appropriate parameters (calibration_year, target_year, transition_matrix, landuse_data,
        forest_data, ef_country, and AR_VALUE) to perform the necessary calculations.

        The calculated land-use footprints for climate change are saved as a datatable using the `save_goblin_results_output_datatable`
        method from the DataManager class. The datatable is saved with the name "climate_change_landuse".

        The attributes and methods referenced in this documentation are class attributes and methods and should be available within
        the class instance when this method is called.
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country
        calibration_year = self.calibration_year
        target_year = self.target_year

        climate_change_landuse_class = ClimateChangeLandUse(
            calibration_year,
            target_year,
            transition_matrix,
            landuse_data,
            forest_data,
            ef_country,
            AR_VALUE,
        )

        climate_change_landuse = climate_change_landuse_class.climate_change_landuse()

        self.data_manager_class.save_goblin_results_to_database(("climate_change_landuse", climate_change_landuse))


    def generate_livestock_footprint(
        self,
        baseline_animal_data,
        scenario_animal_data,
        farm_inputs_baseline,
        farm_inputs_scenario,
        landuse_data, 
        transition_matrix,
        crop_data
    ):
        """
        Calculate the environmental footprints associated with livestock production for both the baseline and scenario datasets.

        This method estimates the climate change, eutrophication, and air quality impacts of livestock production. It utilizes data from both the baseline and scenario animal datasets, along with farm (fertilizer) inputs.

        Parameters
        ----------
        baseline_animal_data : DataFrame
            A DataFrame containing baseline animal data.
        scenario_animal_data : DataFrame
            A DataFrame containing scenario-specific animal data.
        farm_inputs_baseline : DataFrame
            A DataFrame containing farm inputs (fertilizers) for the baseline scenario.
        farm_inputs_scenario : DataFrame
            A DataFrame containing farm inputs (fertilizers) for the specific scenario.

        Returns
        -------
        None
            The method does not return any value. The results are saved to output data tables for further analysis.

        Notes
        -----
        - This method relies on the `AR_VALUE` (AR4, AR5) and `ef_country` attributes to calculate the environmental impacts, which should be set appropriately before calling this method.

        - The method utilizes the following classes for calculating impacts:
            - `ClimateChangeLivestock`: For climate change-related impacts.
            - `EutrophicationLivestock`: For eutrophication-related impacts.
            - `AirQualityLivestock`: For air quality-related impacts.

        - The calculated environmental footprints are not returned directly but are saved to the output data tables using the `save_goblin_results_output_datatable` method.

        See Also
        --------
        ClimateChangeLivestock : Class for calculating climate change impacts of livestock production.
        EutrophicationLivestock : Class for calculating eutrophication impacts of livestock production.
        AirQualityLivestock : Class for calculating air quality impacts of livestock production.
        save_goblin_results_output_datatable : Method to save data to output data tables.
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country
        calibration_year = self.calibration_year
        target_year = self.target_year


        climate_change_livestock_class = ClimateChangeLivestock(ef_country,calibration_year, target_year, transition_matrix, landuse_data, crop_data, AR_VALUE)


        climate_change_livestock_disaggregated = (
            climate_change_livestock_class.climate_change_livestock_dissagregated(
                baseline_animal_data,
                scenario_animal_data,
                farm_inputs_baseline,
                farm_inputs_scenario,
            )
        )

        eutrophication_livestock_class = EutrophicationLivestock(ef_country)

        eutrophication_livestock_disaggregated = (
            eutrophication_livestock_class.eutrophication_livestock_dissagregated(
                baseline_animal_data,
                scenario_animal_data,
                farm_inputs_baseline,
                farm_inputs_scenario,
            )
        )

        air_quality_livestock_class = AirQualityLivestock(ef_country)

        air_quality_livestock_disaggregated = air_quality_livestock_class.air_quality_livestock_dissagregated(
            baseline_animal_data,
            scenario_animal_data,
            farm_inputs_baseline,
            farm_inputs_scenario,
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_livestock_disaggregated", climate_change_livestock_disaggregated),
                                                                ("eutrophication_livestock_disaggregated", eutrophication_livestock_disaggregated),
                                                                ("air_quality_livestock_disaggregated", air_quality_livestock_disaggregated))

    def generate_aggregated_livestock_footprint(
        self,
        baseline_animal_data,
        scenario_animal_data,
        farm_inputs_baseline,
        farm_inputs_scenario,
        landuse_data, 
        transition_matrix,
        crop_data
    ):
        """
        Calculate the aggregated environmental footprints associated with livestock production for both the baseline and scenario datasets.

        This method estimates the aggregated climate change impacts of livestock production at the national level. It utilizes data from both the baseline and scenario animal datasets, along with farm (fertilizer) inputs.

        Parameters
        ----------
        baseline_animal_data : DataFrame
            A DataFrame containing baseline animal data.
        scenario_animal_data : DataFrame
            A DataFrame containing scenario-specific animal data.
        farm_inputs_baseline : DataFrame
            A DataFrame containing farm inputs (fertilizers) for the baseline scenario.
        farm_inputs_scenario : DataFrame
            A DataFrame containing farm inputs (fertilizers) for the specific scenario.

        Returns
        -------
        None
            The method does not return any value. The aggregated results are saved to output data tables for further analysis.

        Notes
        -----
        - This method relies on the `AR_VALUE` and `ef_country` attributes to calculate the environmental impacts, which should be set appropriately before calling this method.

        - The method utilizes the `ClimateChangeLivestock` class for calculating the climate change impacts of livestock production.

        - The aggregated climate change impacts are not returned directly but are saved to the output data tables using the `save_goblin_results_output_datatable` method.

        See Also
        --------
        ClimateChangeLivestock : Class for calculating climate change impacts of livestock production.
        save_goblin_results_output_datatable : Method to save data to output data tables.
        """
        AR_VALUE = self.AR_VALUE
        ef_country = self.ef_country
        calibration_year = self.calibration_year
        target_year = self.target_year


        climate_change_livestock_class = ClimateChangeLivestock(ef_country,calibration_year, target_year, transition_matrix, landuse_data, crop_data, AR_VALUE)

        climate_change_livestock_aggregated = (
            climate_change_livestock_class.climate_change_livestock_aggregated(
                baseline_animal_data,
                scenario_animal_data,
                farm_inputs_baseline,
                farm_inputs_scenario,
            )
        )
        climate_change_livestock_categories_as_co2e = (
            climate_change_livestock_class.climate_change_livestock_categories_as_co2e(
                baseline_animal_data,
                scenario_animal_data,
                farm_inputs_baseline,
                farm_inputs_scenario,
            )
        )

        self.data_manager_class.save_goblin_results_to_database(("climate_change_livestock_aggregated", climate_change_livestock_aggregated),
                                                                ("climate_change_livestock_categories_as_co2e", climate_change_livestock_categories_as_co2e))
        

    def generate_afforestation_data(self, transition_matrix, scenario_dataframe):
        """
        Generate afforestation data based on the given transition matrix and scenario data.

        This method calculates and generates afforestation data using the provided transition matrix and scenario data. Afforestation refers to the process of converting non-forest land into forested areas.

        Parameters
        ----------
        transition_matrix : DataFrame
            A DataFrame representing the transition matrix, which describes the changes in land use from one category to another.
        scenario_dataframe : DataFrame
            A DataFrame containing scenario-specific data.

        Returns
        -------
        DataFrame
            A DataFrame containing the generated afforestation data.

        Notes
        -----
        - The method utilizes the `Afforestation` class to generate afforestation data.

        - The generated afforestation data is saved to the output data table using the `save_goblin_results_output_datatable` method.

        - The `baseline_year` and `target_year` attributes are used in the process, and they should be set appropriately before calling this method.

        See Also
        --------
        Afforestation : Class for generating afforestation data.
        save_goblin_results_output_datatable : Method to save data to output data tables.
        """

        baseline_year = self.calibration_year
        target_year = self.target_year

        afforestation_class = Afforestation(
            baseline_year, target_year, scenario_dataframe
        )

        afforestation_data = afforestation_class.gen_cbm_afforestation_dataframe(
            transition_matrix
        )

        return afforestation_data


    def generate_forest_carbon(
        self, afforest_year, afforestation_dataframe, scenario_dataframe
    ):
        """
        Generate forest carbon data based on afforestation and scenario data.

        This method calculates and generates forest carbon data by running the Carbon Budget Model (CBM CFS3) using the provided afforestation data and scenario data.

        Parameters
        ----------
        afforest_year : int
            The target year for afforestation, representing the year when non-forest land is converted to forested areas.
        afforestation_dataframe : DataFrame
            A DataFrame containing the afforestation data, which represents the conversion of non-forest land to forested areas.
        scenario_dataframe : DataFrame
            A DataFrame containing scenario-specific data.

        Returns
        -------
        dict
            A dictionary containing the generated forest carbon data, as pandas.DataFrame, including aggregated and annual flux results.

        Notes
        -----
        - The method utilizes the `Runner` class to run the CBM model and generate forest carbon data.

        - The CBM model requires the `cbm_configuration` attribute, which should be set appropriately before calling this method.

        - The generated forest carbon data, both aggregated and annual flux results.

        - The `calibration_year` and `target_year` attributes are used in the process, and they should be set appropriately before calling this method.

        See Also
        --------
        Runner : Class for running the Carbon Budget Model (CBM CFS3).
        save_goblin_results_output_datatable : Method to save data to output data tables.
        """

        calibration_year = self.calibration_year
        target_year = afforest_year

        cbm_configuration = self.cbm_config_path

        cbm_runner = Runner(
            cbm_configuration,
            calibration_year,
            target_year,
            afforestation_dataframe,
            scenario_dataframe,
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
