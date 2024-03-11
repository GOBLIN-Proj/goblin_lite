"""
Data Fetcher Module
====================

This module provides a class for fetching various types of data from 31 output data tables managed by the DataManager.
It is designed to facilitate easy access and retrieval of data across different environmental impact scenarios.

Classes
-------
DataFetcher
    A class responsible for retrieving data from the output tables, offering methods to access specific types of data
    related to livestock, crops, land use, climate change, air quality, and eutrophication.

Dependencies
------------
- DataManager

Usage
-----
Initialize the DataFetcher class and use its methods to retrieve data from various output tables. The retrieved data
can be used for analysis, comparison, and visualization of environmental impacts across different scenarios.

Methods
-------
    - get_scenario_inputs(): Retrieves scenario input data.
    - get_stocking_rate_per_ha(): Fetches stocking rate per hectare data.
    - get_grassland_spared_area_by_soil_group(): Retrieves spared (destocked) grassland area data by soil group.
    - get_crop_farm_input_applied(): Fetches crop farm (fertiliser) input data.
    - get_crop_national_inputs(): Retrieves national crop input data.
    - get_transition_matrix(): Fetches the land use transition matrix.
    - get_baseline_livestock_data(): Retrieves baseline livestock data.
    - get_scenario_livestock_data(): Retrieves livestock data for specific scenarios.
    - get_livestock_output_summary(): Fetches a summary of livestock outputs.
    - get_grassland_scenario_farm_inputs(): Retrieves scenario-specific farm inputs for grassland.
    - get_grassland_baseline_farm_inputs(): Fetches baseline farm inputs for grassland.
    - get_total_grassland_area(): Retrieves total grassland area data.
    - get_total_spared_area(): Fetches total spared area data.
    - get_climate_change_animal_emissions_by_category(): Retrieves climate change emissions data for livestock by category.
    - get_climate_change_crop_emissions_by_category(): Retrieves climate change emissions data for crops by category.
    - get_climate_change_crop_emissions_aggregated(): Fetches aggregated climate change emissions data for crops.
    - get_climate_change_animal_emissions_aggregated(): Retrieves aggregated climate change emissions data for livestock.
    - get_animal_emissions_by_category_co2e(): Fetches livestock emissions data by category in CO2e.
    - get_crop_emissions_by_category_co2e(): Retrieves crop emissions data by category in CO2e.
    - get_climate_change_emission_totals(): Fetches total climate change emissions data.
    - get_eutrophication_emission_totals(): Retrieves total eutrophication emissions data.
    - get_air_quality_emission_totals(): Fetches total air quality emissions data.
    - get_eutrophication_animal_emissions_by_category(): Retrieves eutrophication emissions data for livestock by category.
    - get_eutrophication_crop_emissions_by_category(): Fetches eutrophication emissions data for crops by category.
    - get_air_quality_animal_emissions_by_category(): Retrieves air quality emissions data for livestock by category.
    - get_air_quality_crop_emissions_by_category(): Fetches air quality emissions data for crops by category.
    - get_landuse_emissions_totals(): Retrieves total land use change emissions data.
    - get_forest_flux(): Fetches annual forest carbon flux data.
    - get_forest_aggregate(): Retrieves aggregated forest carbon data.
    - get_total_afforested(): Retrieves data on total afforested area for each scenario.
    - get_landuse_areas(): Retrieves data on land use areas for each scenario and the baseline.

Each method in the DataFetcher class is designed to retrieve a specific type of data from the output tables managed by the DataManager. The methods return pandas DataFrames containing relevant data, which can be further analyzed or visualized as required.

The DataFetcher class streamlines the process of data retrieval from complex environmental impact models, making it easier for users to access and utilize the data for research, policy-making, or educational purposes. It ensures that data across different scenarios and impact categories is readily accessible for comprehensive environmental analysis.

Note:
    The class and its methods assume that the DataManager has been properly initialized and that the relevant data tables are available and correctly formatted. The users of this class should have a basic understanding of the data structure and the environmental impact scenarios to effectively utilize the retrieved data.
"""

from goblin_lite.resource_manager.database_manager import DataManager
import os

class DataFetcher:
    def __init__(self, DATABASE_PATH=None):
        """
        A class responsible for fetching various types of data from output data tables.

        This class allows easy access to the data saved in the output data tables managed by the DataManager.

        Parameters
        ----------
        DATABASE_PATH : str, optional
            The path to the external database. If None, the default internal database is used. (default is None)

        Methods
        -------
        get_scenario_inputs()
            Returns scenario input data from the "scenario_input_dataframe" output data table.

        get_stocking_rate_per_ha()
            Returns stocking rate per hectare data from the "per_hectare_stocking_rate" output data table.

        get_grassland_spared_area_by_soil_group()
            Returns spared (destocked) grassland area data by soil group from the "total_spared_area_by_soil_group" output data table.

        get_crop_farm_input_applied()
            Returns crop farm (fertiliser) input data from the "crop_farm_data" output data table.

        get_crop_national_inputs()
            Returns national crop input data from the "crop_input_data" output data table.

        get_transition_matrix()
            Returns the land use transition matrix from the "transition_matrix" output data table.

        get_baseline_livestock_data()
            Returns the summary of livestock data for the baseline scenario from the "baseline_animal_data" output data table.

        get_scenario_livestock_data()
            Returns the summary of livestock data for the scenarios from the "scenario_animal_data" output data table.

        get_livestock_output_summary()
            Returns the summary of livestock outputs from the "protein_and_milk_summary" output data table.

        get_grassland_scenario_farm_inputs()
            Returns scenario-specific farm inputs data from the "grassland_farm_inputs_scenario" output data table.

        get_grassland_baseline_farm_inputs()
            Returns baseline farm inputs data from the "grassland_farm_inputs_baseline" output data table.

        get_total_grassland_area()
            Returns the total grassland area data from the "total_grassland_area" output data table.

        get_total_spared_area()
            Returns the total spared (destocked) area data from the "total_spared_area" output data table.

        get_climate_change_animal_emissions_by_category()
            Returns climate change emissions data for livestock categories from the "climate_change_livestock_disaggregated" output data table.

        get_climate_change_crop_emissions_by_category()
            Returns climate change emissions data for crop categories from the "climate_change_crops_disaggregated" output data table.

        get_climate_change_crop_emissions_aggregated()
            Returns aggregated climate change emissions data for crops from the "climate_change_crops_aggregated" output data table.

        get_climate_change_animal_emissions_aggregated()
            Returns aggregated climate change emissions data for livestock from the "climate_change_livestock_aggregated" output data table.

        get_animal_emissions_by_category_co2e()
            Returns climate change emissions data for livestock categories converted to CO2e from the "climate_change_livestock_categories_as_co2e" output data table.

        get_crop_emissions_by_category_co2e()
            Returns climate change emissions data for crop categories converted to CO2e from the "climate_change_crops_categories_as_co2e" output data table.

        get_climate_change_emission_totals()
            Returns the total climate change emissions data from the "climate_change_totals" output data table.

        get_eutrophication_emission_totals()
            Returns the total eutrophication emissions data from the "eutrophication_totals" output data table.

        get_air_quality_emission_totals()
            Returns the total air quality emissions data from the "air_quality_totals" output data table.

        get_eutrophication_animal_emissions_by_category()
            Returns eutrophication emissions data for livestock categories from the "eutrophication_livestock_disaggregated" output data table.

        get_eutrophication_crop_emissions_by_category()
            Returns eutrophication emissions data for crop categories from the "eutrophication_crops_disaggregated" output data table.

        get_air_quality_animal_emissions_by_category()
            Returns air quality emissions data for livestock categories from the "air_quality_livestock_disaggregated" output data table.

        get_air_quality_crop_emissions_by_category()
            Returns air quality emissions data for crop categories from the "air_quality_crops_disaggregated" output data table.

        get_landuse_emissions_totals()
            Returns the total land use change emissions data from the "climate_change_landuse" output data table.

        get_forest_flux()
            Returns the annual forest carbon flux data from the "forest_carbon_flux" output data table.

        get_forest_aggregate()
            Returns the aggregated forest carbon data from the "forest_carbon_aggregate" output data table.

        get_total_afforested()
            Returns the total afforested data from the "cbm_afforestation_data" output data table.

        get_landuse_areas()
            Returns the land use areas data from the "land_use_areas" output data table.
        """
        self.data_manager_class = DataManager(DATABASE_PATH)

    def get_scenario_inputs(self):
        """
        Retrieve a DataFrame containing information about scenario inputs.

        Parameters
        ----------
        None
        
        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about scenario inputs. The index of the DataFrame is set to "index" for easier access to the data.
        
        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_scenario_inputs()
        """
        scenario_inputs = self.data_manager_class.get_goblin_results_output_datatable(
            "scenario_input_dataframe", index_col="index"
        )
        return scenario_inputs
    
    def get_stocking_rate_per_ha(self):
        """
        Retrieve a DataFrame containing information about stocking rate per hectare for each scenario.
        
        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about stocking rate per hectare for each scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_stocking_rate_per_ha()
        """
        stocking_rate = self.data_manager_class.get_goblin_results_output_datatable(
            "per_hectare_stocking_rate"
        )
        return stocking_rate

    def get_grassland_spared_area_by_soil_group(self):
        """
        Retrieve a DataFrame containing information about spared (destocked) grassland area by soil group for each scenario.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about spared (destocked) grassland area by soil group for each scenario. The index of the DataFrame is set to "index" for easier access to the data.
            
        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_grassland_spared_area_by_soil_group()
        """
        spared_area = self.data_manager_class.get_goblin_results_output_datatable(
            "total_spared_area_by_soil_group", index_col="index"
        )
        return spared_area
    
    def get_crop_farm_input_applied(self):
        """
        Retrieve a DataFrame containing information about fertilizer application to crops for each scenario.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about fertilizer application to crops for each scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_crop_farm_input_applied()
        """
        crop_inputs = self.data_manager_class.get_goblin_results_output_datatable(
            "crop_farm_data", index_col="index"
        )
        return crop_inputs
    
    def get_crop_national_inputs(self):
        """
        Retrieve a DataFrame containing information about national crop inputs for each scenario.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about national crop inputs for each scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_crop_national_inputs()
        """

        crop_inputs = self.data_manager_class.get_goblin_results_output_datatable(
            "crop_input_data", index_col="index"
        )
        return crop_inputs

    def get_transition_matrix(self):
        """
        Retrieve a DataFrame containing information about the land use transition matrix.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about the land use transition matrix. The index of the DataFrame is set to "index" for easier access to the data.

        Examples
        --------
            >>> data_manager = DataManager()
            >>> baseline_data = data_manager.get_transition_matrix()
        """
        transition_matrix = self.data_manager_class.get_goblin_results_output_datatable(
            "transition_matrix", index_col="index"
        )
        return transition_matrix
    
    def get_baseline_livestock_data(self):
        """Fetches and returns the baseline livestock data.

        This method is used to retrieve the baseline livestock data, which contains information about animal-related variables in the baseline scenario.
        The baseline scenario typically represents the reference state or the initial condition without any specific intervention or changes.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the baseline livestock data. The DataFrame includes various animal-related variables, such as the number
            of animals, animal species, their age, weight, and other relevant attributes. The data is indexed by 'index'.

        Examples
        --------
        >>> data_manager = DataManager()
        >>> baseline_data = data_manager.get_baseline_livestock_data()

        Note
        ----
        - The method relies on the `data_manager_class` to fetch the 'baseline_animal_data' from the 'goblin_results_output_datatable'.
        - The DataFrame returned by this method can be used for further analysis, comparison with other scenarios, or as a reference for
        understanding the livestock conditions in the baseline scenario.

        """

        livestock = self.data_manager_class.get_goblin_results_output_datatable(
            "baseline_animal_data", index_col="index"
        )
        return livestock

    def get_scenario_livestock_data(self):
        """
        Fetches and returns the livestock data for the specific scenario.

        This method is used to retrieve the livestock data for scenarios. The scenarios represents a specific configuration or set of conditions that differ from the baseline. It allows users to analyze and compare livestock-related variables under different scenarios.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the livestock data for the scenarios. The DataFrame includes various animal-related variables,
            such as the number of animals, animal species, their age, weight, and other relevant attributes. The data is indexed by 'index'.

        Examples
        --------
        >>> data_manager = DataManager()
        >>> scenario_data = data_manager.get_scenario_livestock_data()

        Note
        ----
        - The method relies on the `data_manager_class` to fetch the 'scenario_animal_data' from the 'goblin_results_output_datatable'.
        - The DataFrame returned by this method can be used for analysis, comparison with other scenarios, or to understand the livestock
        conditions in the selected scenario.

        """

        livestock = self.data_manager_class.get_goblin_results_output_datatable(
            "scenario_animal_data", index_col="index"
        )
        return livestock

    def get_livestock_output_summary(self):
        """
        Fetches the summary of livestock outputs from the "protein_and_milk_summary" output data table.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the summary of livestock outputs

        Notes
        -----
            The "protein_and_milk_summary" output data table stores the summary of livestock outputs, including information related
            to protein production, milk production in kg.

            Reported in kg.
        """

        protein_and_milk_summary = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "protein_and_milk_summary", index_col="Scenarios"
            )
        )
        return protein_and_milk_summary

    def get_grassland_scenario_farm_inputs(self):
        """
        Retrieve a DataFrame containing information about fertilizer application to grassland for each scenario.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about fertilizer application to grassland for each scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame provides valuable insights into the fertilizer application practices in various scenarios and their impact on grassland management and agricultural practices. Researchers and analysts working on environmental research and policy related to livestock farming and land use changes can utilize this data for their analyses.

            Reported in kg.

        """

        scenario_farm_inputs = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "grassland_farm_inputs_scenario", index_col="index"
            )
        )
        return scenario_farm_inputs

    def get_grassland_baseline_farm_inputs(self):
        """
        Retrieve a DataFrame containing information about fertilizer application to grassland in the baseline scenario.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about fertilizer application to grassland in the baseline scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame provides valuable insights into the fertilizer application practices for grassland in the baseline scenario. This data can be used to understand the initial conditions and establish a baseline for comparing fertilizer use in different scenarios or assessing the effectiveness of land management strategies.

            Reported in kg.

        """

        baseline_farm_inputs = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "grassland_farm_inputs_baseline", index_col="index"
            )
        )
        return baseline_farm_inputs

    def get_total_grassland_area(self):
        """
        Retrieve the total grassland area for baseline and scenarios.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about the total grassland area in a specific scenario. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame provides the total grassland area baseline and scenarios, which is valuable for understanding the land use distribution and assessing the impact of different scenarios on grassland conservation and management.

            Reported in ha.

        """
        total_grassland_area = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "total_grassland_area", index_col="index"
            )
        )
        return total_grassland_area

    def get_total_spared_area(self):
        """
        Retrieve the total spared area in all scenarios.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about the total spared area in all scenarios. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame provides the difference between the baseline grassland area and the scenario grassland area for each scenario. This information is crucial for understanding the changes in land use, particularly how much grassland has been spared or converted to other land uses across different scenarios.

            Reported in ha.

        """

        total_spared_area = self.data_manager_class.get_goblin_results_output_datatable(
            "total_spared_area", index_col="index"
        )
        return total_spared_area

    def get_climate_change_animal_emissions_by_category(self):
        """
        Retrieve the total climate change emissions from animal production by category and gas for each scenario and baseline.

        This method fetches data related to climate change emissions from animal production and provides a comprehensive breakdown of emissions by different categories and gases for each scenario and the baseline. The emissions are associated with the following categories:

        Emission Categories:
            - Enteric Fermentation (CH4)
            - Manure Management (N2O and CH4)
            - Pasture (Direct and Indirect N2O)
            - Soils (Fertilizer Application, CO2, Direct and Indirect N2O)

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about the total climate change emissions from animal production for each scenario and baseline, disaggregated by emission category and gas. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame includes emissions from different categories related to animal production, providing a detailed perspective on the contribution of each emission source to the overall climate change impact for different scenarios and the baseline. This information is valuable for environmental research and policy-making, as it helps identify key areas for emissions reduction and mitigation strategies under different scenarios. Researchers and policymakers can use this data to assess the effectiveness of various interventions in reducing greenhouse gas emissions and improving the sustainability of animal production systems.

            Reported in kilotons.

        """

        total_animal_gases = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "climate_change_livestock_disaggregated", index_col="index"
            )
        )
        return total_animal_gases

    def get_climate_change_crop_emissions_by_category(self):
        """
        Retrieve the total climate change emissions from crop production by category and gas for each scenario and baseline.

        This method fetches data related to climate change emissions from crop production and provides a comprehensive breakdown of emissions by different categories and gases for each scenario and the baseline. The emissions are associated with the following categories:

        Emission Categories:
            - Crop Residues (N2O)
            - Fertilizer (Direct and Indirect N2O)
            - Soils (CO2, N2O)

        Returns
        -------
        DataFrame
            A pandas DataFrame containing information about the total climate change emissions from crop production for each scenario and baseline, disaggregated by emission category and gas. The index of the DataFrame is set to "index" for easier access to the data.

        Notes
        -----
            The DataFrame includes emissions from different categories related to crop production, providing a detailed perspective on the contribution of each emission source to the overall climate change impact for different scenarios and the baseline. This information is valuable for environmental research and policy-making, as it helps identify key areas for emissions reduction and mitigation strategies under different scenarios. Researchers and policymakers can use this data to assess the effectiveness of various interventions in reducing greenhouse gas emissions and improving the sustainability of crop production systems.

            Reported in kilotons.

        """
        total_crops_gases = self.data_manager_class.get_goblin_results_output_datatable(
            "climate_change_crops_disaggregated", index_col="index"
        )
        return total_crops_gases

    def get_climate_change_crop_emissions_aggregated(self):
        """
        Get total aggregated greenhouse gas emissions for crop production.

        This method retrieves the total aggregated emissions for different greenhouse gases related to crop production.
        The emissions are calculated in terms of CH4 (methane), N2O (nitrous oxide), CO2 (carbon dioxide), and CO2E (carbon dioxide equivalent).

        Categories:
            - CH4 (Methane) emissions
            - N2O (Nitrous Oxide) emissions
            - CO2 (Carbon Dioxide) emissions
            - CO2E (Carbon Dioxide Equivalent) emissions

        Returns:
            pandas.DataFrame:
                A dataframe containing the total aggregated greenhouse gas emissions for crop production.
                The dataframe includes the emissions values for each of the mentioned categories.

        Note:
            The emission values are aggregated at a higher level, representing the cumulative emissions from various sources
            associated with crop production. They are not broken down into more specific subcategories as in the method
            `get_climate_change_crop_emissions_by_category`.

            Reported in kilotons.

        """

        total_crops_gases = self.data_manager_class.get_goblin_results_output_datatable(
            "climate_change_crops_aggregated", index_col="index"
        )
        return total_crops_gases

    def get_climate_change_animal_emissions_aggregated(self):
        """
        Get total aggregated greenhouse gas emissions for livestock production.

        This method retrieves the total aggregated emissions for different greenhouse gases related to livestock production.
        The emissions are calculated in terms of CH4 (methane), N2O (nitrous oxide), CO2 (carbon dioxide), and CO2E (carbon dioxide equivalent).

        Categories:
            - CH4 (Methane) emissions
            - N2O (Nitrous Oxide) emissions
            - CO2 (Carbon Dioxide) emissions
            - CO2E (Carbon Dioxide Equivalent) emissions

        Returns:
            pandas.DataFrame:
                A dataframe containing the total aggregated greenhouse gas emissions for livestock production.
                The dataframe includes the emissions values for each of the mentioned categories.

        Note:
            The emission values are aggregated at a higher level, representing the cumulative emissions from various sources
            associated with livestock production. They are not broken down into more specific subcategories as in the method
            `get_climate_change_animal_emissions_by_category`.

            Reported in kilotons.

        """

        total_animal_gases = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "climate_change_livestock_aggregated", index_col="index"
            )
        )
        return total_animal_gases

    def get_animal_emissions_by_category_co2e(self):
        """
        Get greenhouse gas emissions for livestock production by specific categories in CO2E (Carbon Dioxide Equivalent).

        This method retrieves the greenhouse gas emissions associated with livestock production, broken down into specific
        categories, and reported as CO2E values. The emissions categories considered include enteric fermentation, manure management,
        and direct/indirect N2O emissions from soils.

        Categories:
            - Enteric Fermentation (CH4): Methane emissions from digestive processes in livestock.
            - Manure Management (N2O and CH4): Nitrous Oxide and Methane emissions from the management of livestock manure.
            - Soils (Fertilizer Application, CO2, Direct and Indirect N2O):
                - Nitrous Oxide emissions from fertilizer application in soils.
                - Carbon Dioxide emissions from fertilzer application.
                - Nitrous Oxide emissions from direct and indirect sources related to soils, including emissions from manure application
                and animal deposits.

        Returns:
            pandas.DataFrame:
                A dataframe containing greenhouse gas emissions for livestock production by specific categories, expressed as CO2E values.

        Note:
            The emissions values in this dataframe are not aggregated, and they provide a detailed breakdown of emissions for
            different subcategories associated with livestock production.

            Reported in kilotons.

        """

        total_animal_co2e = self.data_manager_class.get_goblin_results_output_datatable(
            "climate_change_livestock_categories_as_co2e", index_col="index"
        )
        return total_animal_co2e

    def get_crop_emissions_by_category_co2e(self):
        """
        Get greenhouse gas emissions for crop production by specific categories in CO2E (Carbon Dioxide Equivalent).

        This method retrieves the greenhouse gas emissions associated with crop production, broken down into specific categories,
        and reported as CO2E values. The emissions categories considered include:
            - N2O (Nitrous Oxide): Emissions of nitrous oxide from crop-related activities.
            - CO2 (Carbon Dioxide): Carbon dioxide emissions from various crop processes.
            - Soils (CO2, N2O): Total Emissions from soil-related activities in crop production, including both carbon dioxide and nitrous oxide.

        Returns:
            pandas.DataFrame:
                A dataframe containing greenhouse gas emissions for crop production by specific categories, expressed as CO2E values.

        Note:
            The emissions values in this dataframe are not aggregated in the "soils" column.

            Reported in kilotons.

        """

        total_crop_co2e = self.data_manager_class.get_goblin_results_output_datatable(
            "climate_change_crops_categories_as_co2e", index_col="index"
        )
        return total_crop_co2e

    def get_climate_change_emission_totals(self):
        """Get the total greenhouse gas emissions for climate change from combined land use, crop, and livestock activities.

        This method retrieves the total greenhouse gas emissions for climate change resulting from combined land use, crop,
        and livestock activities. The emissions are reported for specific gases, including:
            - CH4 (Methane): Total methane emissions associated with climate change.
            - N2O (Nitrous Oxide): Total nitrous oxide emissions associated with climate change.
            - CO2 (Carbon Dioxide): Total carbon dioxide emissions associated with climate change.
            - CO2E (Carbon Dioxide Equivalent): Combined emissions of each gas converted to CO2E using the AR value specified
                                            in the configuration file.

        Returns:
            pandas.DataFrame:
                A dataframe containing the total greenhouse gas emissions for climate change, including CH4, N2O, CO2, and CO2E.

        Note:
            The emissions are aggregated and provide an overview of the overall climate change impact resulting from various
            land use, crop, and livestock activities.

            Reported in kilotons.

        """

        total_climate_change = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "climate_change_totals", index_col="index"
            )
        )
        return total_climate_change

    def get_eutrophication_emission_totals(self):
        """
        Get the total eutrophication emissions.

        This method retrieves the total eutrophication emissions associated with manure management, soils, and overall total.
        The emissions are reported in units of kilotons of PO4e (Phosphorus equivalent).

        Returns:
            pandas.DataFrame:
                A dataframe containing the total eutrophication emissions for manure management, soils, and the overall total.
                The emissions are reported in kilotons of PO4e and provide an overview of the eutrophication impact resulting
                from various agricultural activities.

        Note:
            Eutrophication is a process where excess nutrients, such as phosphorus, are introduced into water bodies, leading
            to an overgrowth of algae and aquatic plant life. This can have detrimental effects on water quality and ecosystems.

            Reported in kilotons.

        """

        total_eutrophication = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "eutrophication_totals", index_col="index"
            )
        )
        return total_eutrophication

    def get_air_quality_emission_totals(self):
        """
        Get the total air quality emissions.

        This method retrieves the total air quality emissions associated with NH3 (Ammonia) from various agricultural activities.

        Returns:
            pandas.DataFrame:
                A dataframe containing the total air quality emissions for NH3 (Ammonia).
                The emissions are reported in kilotons of NH3 and provide an overview of the air quality impact resulting
                from agricultural practices.

        Note:
            NH3 (Ammonia) is a significant air pollutant, and its emissions from agricultural activities can contribute to
            air quality degradation and have implications for human health and the environment.

            Reported in kilotons.

        """

        total_air_quality = self.data_manager_class.get_goblin_results_output_datatable(
            "air_quality_totals", index_col="index"
        )
        return total_air_quality

    def get_eutrophication_animal_emissions_by_category(self):
        """
        Get the eutrophication emissions from animal-related sources.

        This method retrieves the eutrophication emissions associated with manure management and soils from livestock-related activities.

        Returns:
            pandas.DataFrame:
                A dataframe containing the eutrophication emissions from animal-related sources, categorized into manure management
                and soils. The emissions are reported in kilotons of PO4e (Phosphate equivalent) and provide an overview of the
                eutrophication impact resulting from livestock-related practices.

        Note:
            Eutrophication is a process in which excessive nutrients, such as phosphorus (PO4e), are introduced into aquatic ecosystems,
            leading to the proliferation of algae and other aquatic plants. Livestock-related activities, such as manure management
            and fertilizer application to soils, can contribute to eutrophication in nearby water bodies.

            Reported in kilotons.

        """

        total_animal_gases = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "eutrophication_livestock_disaggregated", index_col="index"
            )
        )
        return total_animal_gases

    def get_eutrophication_crop_emissions_by_category(self):
        """
        Get the eutrophication emissions from crop-related sources.

        This method retrieves the eutrophication emissions associated with soils from crop-related activities.

        This is totaled in a single soils category.

        Returns:
            pandas.DataFrame:
                A dataframe containing the eutrophication emissions from crop-related sources, categorized as soils. The emissions
                are reported in kilotons of PO4e (Phosphate equivalent) and provide an overview of the eutrophication impact resulting
                from crop-related practices.

        Note:
            Eutrophication is a process in which excessive nutrients, such as phosphorus (PO4e), are introduced into aquatic ecosystems,
            leading to the proliferation of algae and other aquatic plants. Crop-related activities, particularly the application of
            fertilizers to soils, can contribute to eutrophication in nearby water bodies.

            Reported in kilotons.

        """

        total_crop_gases = self.data_manager_class.get_goblin_results_output_datatable(
            "eutrophication_crops_disaggregated", index_col="index"
        )
        return total_crop_gases

    def get_air_quality_animal_emissions_by_category(self):
        """Get the air quality emissions from animal-related sources.

        This method retrieves the air quality emissions associated with manure management and soils from animal-related activities.

        Returns:
            pandas.DataFrame:
                A dataframe containing the air quality emissions from animal-related sources, categorized as manure management and soils.
                The emissions are reported in kilotons of NH3 (Ammonia) and provide an overview of the atmospheric impact resulting
                from animal-related practices.

        Note:
            Air quality emissions, such as NH3 (Ammonia), can result from animal-related activities, particularly manure management
            practices and ammonia volatilization from soils. These emissions can have implications for air pollution and environmental
            quality.

            Reported in kilotons.

        """

        total_animal_gases = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "air_quality_livestock_disaggregated", index_col="index"
            )
        )
        return total_animal_gases

    def get_air_quality_crop_emissions_by_category(self):
        """Get the air quality emissions from crop-related sources.

        This method retrieves the air quality emissions associated with fertilizer application and soils from crop-related activities.

        This is totaled in a single soils category.

        Returns:
            pandas.DataFrame:
                A dataframe containing the air quality emissions from crop-related sources, categorized as fertilizer application and soils.
                The emissions are reported in kilotons of NH3 (Ammonia) and provide an overview of the atmospheric impact resulting from
                crop-related practices.

        Note:
            Air quality emissions, such as NH3 (Ammonia), can result from crop-related activities, particularly from fertilizer application
            and ammonia volatilization from soils. These emissions can have implications for air pollution and environmental quality.

            Reported in kilotons.

        """

        total_crops_gases = self.data_manager_class.get_goblin_results_output_datatable(
            "air_quality_crops_disaggregated", index_col="index"
        )
        return total_crops_gases

    def get_landuse_emissions_totals(self):
        """
        Get the land use emissions totals by gas.

        This method retrieves a dataframe that summarizes the total emissions for each land use category, categorized by different gas types
        such as CO2, CH4, and N2O, as well as a combined total in CO2E (CO2 equivalent).

        Returns:
            pandas.DataFrame:
                A dataframe containing the total emissions for each land use category, categorized by different gas types including CO2, CH4,
                and N2O, as well as a combined total in CO2E (CO2 equivalent). The emissions are reported in kilotons of CO2, CH4, and N2O
                for each land use category, providing an overview of the greenhouse gas contributions from land use activities.

        Note:
            Land use activities can contribute to greenhouse gas emissions through various processes, including soil management, crop residue
            decomposition, and land-use change. The emissions are reported in CO2, CH4, and N2O, and the combined CO2E allows for a unified
            measure of the overall greenhouse gas impact.

            Reported in kilotons.

        """
        total_animal_gases = (
            self.data_manager_class.get_goblin_results_output_datatable(
                "climate_change_landuse", index_col="scenario"
            )
        )
        return total_animal_gases

    def get_forest_flux(self):
        """
        Get the forest carbon annual flux.

        This method retrieves a dataframe that provides the forest carbon annual flux, reported in metric tons of carbon (tC). The flux is
        categorized into different components, including biomass, dead organic matter (DOM), and total ecosystem, which represents the combined
        biomass and DOM flux. Additionally, the carbon from harvested wood products are also reported.

        Returns:
            pandas.DataFrame:
                A dataframe containing the forest carbon annual flux, categorized into different components such as biomass, dead organic
                matter (DOM), and total ecosystem (combined biomass and DOM). The emissions from harvested wood products are also included in
                the report. The flux is reported in metric tons of carbon (tC), providing valuable insights into the carbon dynamics of forest
                ecosystems and their contributions to the carbon cycle.

        Note:
            Forest ecosystems play a crucial role in sequestering and releasing carbon through various processes. The annual carbon flux provides
            information on the net carbon exchange between the forest and the atmosphere, helping to understand the carbon balance and potential
            impacts on climate change.

            Reported in tons.

        """

        forest_flux = self.data_manager_class.get_goblin_results_output_datatable(
            "forest_carbon_flux", index_col="index"
        )
        return forest_flux

    def get_forest_aggregate(self):
        """
        Get the aggregated forest carbon emissions.

        This method retrieves a dataframe that provides the aggregated forest carbon emissions, including biomass, dead organic matter (DOM),
        and total ecosystem carbon. The reported values are in metric tons of carbon (tC). The dataframe contains information on the overall
        carbon storage and release within the forest ecosystem, including both living biomass and dead organic matter components.
        Additionally, the carbon from harvested wood products are also reported.

        Returns:
            pandas.DataFrame:
                A dataframe containing the aggregated forest carbon emissions, including biomass, dead organic matter (DOM), and total ecosystem
                carbon. The values are reported in metric tons of carbon (tC), providing valuable insights into the carbon storage and dynamics
                of the forest ecosystem.

        Note:
            Forest ecosystems play a crucial role in carbon sequestration, serving as a significant carbon sink. The aggregated forest carbon
            emissions data help quantify the overall carbon balance of the forest, considering both carbon uptake through photosynthesis and
            carbon release through decomposition and disturbances. Understanding the carbon dynamics in forests is essential for assessing their
            contribution to climate change mitigation efforts and evaluating the impacts of various management practices on carbon sequestration.

            Reproted in tons.

        """

        forest_aggregate = self.data_manager_class.get_goblin_results_output_datatable(
            "forest_carbon_aggregate", index_col="index"
        )
        return forest_aggregate

    def get_total_afforested(self):
        """
        Get the total afforested area for each scenario.

        This method retrieves a dataframe that provides the total area afforested in each scenario. The values are reported in hectares (ha),
        representing the extent of land that has been converted to forest through afforestation. The afforested areas are essential indicators
        of reforestation efforts and land-use changes to promote carbon sequestration and biodiversity conservation.

        Returns:
            pandas.DataFrame:
                A dataframe containing the total afforested area for each scenario. The values are reported in hectares (ha) and offer insights
                into the scale and impact of afforestation efforts within different land-use scenarios.

        Note:
            Afforestation involves converting non-forested land into forested areas. This land-use change plays a vital role in carbon sequestration,
            helping to offset carbon emissions and mitigate climate change. Additionally, afforested areas can contribute to enhancing biodiversity,
            ecosystem services, and sustainable land management practices.

            Reported in ha.

        """

        afforestation = self.data_manager_class.get_goblin_results_output_datatable(
            "cbm_afforestation_data", index_col="index"
        )
        return afforestation
    
    def get_landuse_areas(self):
        """
        Get the land use areas for each scenario and the baseline.

        This method retrieves a dataframe that provides the land use areas for each scenario and the baseline. The area values are reported in hectares (ha),
        representing the extent of land allocated to different land uses, including grassland, cropland, forest and farmable condition.

        Share variables for mineral soils, organic soils, organic mineral soils, rewetted, peat extraction, are fractions of the total area of the land use type.

        Returns:
            pandas.DataFrame:
                A dataframe containing the land use areas for each scenario and the baseline. The area values are reported in hectares (ha) and shares are
                fractions of the total area of the land use type.

        """

        landuse_areas = self.data_manager_class.get_goblin_results_output_datatable(
            "landuse_data", index_col="index"
        )
        return landuse_areas



    def dump_tables(self, data_path):
        """
        Dump all tables to a specified path.

        Parameters
        ----------
        path : str
            The path to the directory where the tables will be dumped.

        Returns
        -------
        None

        Notes
        -----
        This method is used to dump all the tables from the database to a specified directory. The tables are saved as CSV files.

        """
        tables = [(self.get_air_quality_animal_emissions_by_category, "air_quality_animal_emissions.csv"),
                    (self.get_air_quality_crop_emissions_by_category, "air_quality_crop_emissions.csv"),
                    (self.get_air_quality_emission_totals, "air_quality_emissions_totals.csv"),
                    (self.get_climate_change_animal_emissions_aggregated,"climate_change_animal_emissions_aggregated.csv"),
                    (self.get_climate_change_crop_emissions_aggregated, "climate_change_crop_emissions_aggregated.csv"),
                    (self.get_climate_change_emission_totals, "climate_change_emissions_totals.csv"),
                    (self.get_climate_change_animal_emissions_by_category, "climate_change_animal_emissions_by_category.csv"),
                    (self.get_climate_change_crop_emissions_by_category, "climate_change_crop_emissions_by_category.csv"),
                    (self.get_crop_national_inputs, "crop_catchment_inputs.csv"),
                    (self.get_crop_emissions_by_category_co2e, "crop_emissions_by_category_co2e.csv"),
                    (self.get_crop_farm_input_applied, "crop_farm_input_applied.csv"),
                    (self.get_eutrophication_emission_totals, "eutrophication_emission_totals.csv"),
                    (self.get_eutrophication_crop_emissions_by_category, "eutrophication_crop_emissions_by_category.csv"),
                    (self.get_eutrophication_animal_emissions_by_category, "eutrophication_animal_emissions_by_category.csv"),
                    (self.get_baseline_livestock_data, "baseline_livestock_data.csv"),
                    (self.get_scenario_livestock_data, "scenario_livestock_data.csv"),
                    (self.get_livestock_output_summary, "livestock_output_summary.csv"),
                    (self.get_landuse_areas, "landuse_areas.csv"),
                    (self.get_landuse_emissions_totals, "landuse_emissions_totals.csv"),
                    (self.get_total_afforested, "total_afforested.csv"),
                    (self.get_total_grassland_area, "total_grassland_area.csv"),
                    (self.get_transition_matrix, "transition_matrix.csv"),
                    (self.get_grassland_spared_area_by_soil_group, "grassland_spared_area_by_soil_group.csv"),
                    (self.get_grassland_scenario_farm_inputs, "grassland_scenario_farm_inputs.csv"),
                    (self.get_grassland_baseline_farm_inputs, "grassland_baseline_farm_inputs.csv"),
                    (self.get_scenario_inputs, "scenario_inputs.csv"),
                    (self.get_stocking_rate_per_ha, "stocking_rate_per_ha.csv"),
                    (self.get_forest_aggregate, "forest_aggregate.csv"),
                    (self.get_forest_flux, "forest_flux.csv"),
                    (self.get_total_spared_area, "total_spared_area.csv"),
                    (self.get_animal_emissions_by_category_co2e, "animal_emissions_by_category_co2e.csv")]
        

        for get_method, filename in tables:
            get_method().to_csv(os.path.join(data_path, filename))
