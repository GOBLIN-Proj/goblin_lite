"""
Impact Category Air Quality Module
==================================

The Impact Categories Air Quality  module is designed to calculate and analyze various environmental impacts in the context of land use change, livestock and crop production. 
The module integrates data from various sources like cattle and sheep lifecycle assessments, crop production data, 
and land use changes, providing a comprehensive view of environmental impacts.

Key Features
------------
Integration with Multiple Data Sources: Utilizes data from cattle, sheep, crop lifecycle assessments, and land use changes.
Environmental Impact Analysis: Calculates emissions contributing to climate change, eutrophication, and
air quality.

Flexible Data Handling: Works with different types of data inputs, including livestock and crop production data, land use transition data, and more.
"""

from cattle_lca.resource_manager.models import load_livestock_data, load_farm_data
from cattle_lca.lca import AirQualityTotals as CattleAirQualityTotals
from sheep_lca.lca import AirQualityTotals as SheepAirQualityTotals
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import AirQualityTotals as CropAirQualityTotals
from goblin_lite.impact_categories.common import CommonParams
import pandas as pd

class AirQualityLivestock:
    """
    A class for assessing the impact of livestock on air quality. It calculates emissions
    from cattle and sheep for both past and future scenarios, considering various emission categories.

    Attributes:
        ef_country (str): emission factor country.
        cattle_air_quality_class, sheep_air_quality_class: Classes for calculating emissions for each category.
        common_class (CommonParams): A class for managing various data and constants.

    Methods:
        air_quality_livestock_past(baseline_animals, baseline_farms):
            Calculates past emissions based on baseline data for animals and farm inputs.
        air_quality_livestock_future(scenario_animals, scenario_farms):
            Projects future emissions based on scenario data for animals and farm inputs.
        air_quality_livestock_dissagregated(baseline_animals, scenario_animals, baseline_farms, scenario_farms):
            Provides detailed emissions data combining past and future scenarios.

    """
    def __init__(self, ef_country):
        self.common_class = CommonParams()
        self.cattle_air_quality_class = CattleAirQualityTotals(ef_country)
        self.sheep_air_quality_class = SheepAirQualityTotals(ef_country)


    def air_quality_livestock_past(self, baseline_animals, baseline_farms):
        """
        Calculates past emissions based on baseline data for animals and farm inputs.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            baseline_farms (DataFrame): Data containing baseline farm information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        baseline_index = self.common_class.baseline_index
        kg_to_kt = self.common_class.kg_to_kt

        ammonia_dict = self.cattle_air_quality_class.create_emissions_dictionary(
            [baseline_index]
        )

        baseline_animals = load_livestock_data(baseline_animals)
        baseline_farms = load_farm_data(baseline_farms)

        past_farm_loc = list(baseline_farms.keys())[0]
        past_animals_loc = list(baseline_animals.keys())[0]

        ammonia_dict["manure_management"][baseline_index] += (
            self.cattle_air_quality_class.total_manure_NH3_AQ(
                baseline_animals[past_animals_loc]["animals"]
            )
            * kg_to_kt
        )
        ammonia_dict["soils"][baseline_index] += (
            self.cattle_air_quality_class.total_grazing_soils_NH3_AQ(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        ammonia_dict["soils"][baseline_index] += (
            self.cattle_air_quality_class.total_fertiliser_soils_NH3_AQ(
                baseline_farms[past_farm_loc].urea_n_fert,
                baseline_farms[past_farm_loc].urea_abated_n_fert,
                baseline_farms[past_farm_loc].an_n_fert,
            )
            * kg_to_kt
        )

        # Past Sheep
        ammonia_dict["manure_management"][baseline_index] += (
            self.sheep_air_quality_class.total_manure_NH3_AQ(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        ammonia_dict["soils"][baseline_index] += (
            self.sheep_air_quality_class.total_grazing_soils_NH3_AQ(
                baseline_animals[past_animals_loc]["animals"],
            )* kg_to_kt
        )

        return ammonia_dict

    def air_quality_livestock_future(self, scenario_animals, scenario_farms):
        """
        Projects future emissions based on scenario data for animals and farm inputs.

        Parameters:
            scenario_animals (DataFrame): Data containing scenario animal information.
            scenario_farms (DataFrame): Data containing scenario farm input information.    

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        scenario_animals_dataframe = scenario_animals

        index = [int(i) for i in scenario_animals_dataframe.Scenarios.unique()]

        scenario_animals = load_livestock_data(scenario_animals)
        scenario_farms = load_farm_data(scenario_farms)

        kg_to_kt = self.common_class.kg_to_kt

        # create emissions dictionary

        ammonia_dict = self.cattle_air_quality_class.create_emissions_dictionary(index)

        for sc in index:
            for farm_id in scenario_animals_dataframe.farm_id[
                scenario_animals_dataframe["Scenarios"] == sc
            ].unique():
                ammonia_dict["manure_management"][sc] += (
                    self.cattle_air_quality_class.total_manure_NH3_AQ(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                ammonia_dict["soils"][sc] += (
                    self.cattle_air_quality_class.total_grazing_soils_NH3_AQ(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )

                ammonia_dict["manure_management"][sc] += (
                    self.sheep_air_quality_class.total_manure_NH3_AQ(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                ammonia_dict["soils"][sc] += (
                    self.sheep_air_quality_class.total_grazing_soils_NH3_AQ(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )

            ammonia_dict["soils"][sc] += (
                self.cattle_air_quality_class.total_fertiliser_soils_NH3_AQ(
                    scenario_farms[sc].urea_n_fert,
                    scenario_farms[sc].urea_abated_n_fert,
                    scenario_farms[sc].an_n_fert,
                ) * kg_to_kt
            )
            

        return ammonia_dict

    def air_quality_livestock_dissagregated(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        """
        Combine past and future emissions data to provide a comprehensive view of livestock impact on air quality.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            scenario_animals (DataFrame): Data containing scenario animal information.
            baseline_farms (DataFrame): Data containing baseline farm input information.
            scenario_farms (DataFrame): Data containing scenario farm input information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        past_data = pd.DataFrame.from_dict(
            self.air_quality_livestock_past(baseline_animals, baseline_farms)
        )

        future_data = pd.DataFrame.from_dict(
            self.air_quality_livestock_future(scenario_animals, scenario_farms)
        )

        return pd.concat([past_data, future_data])
    


class AirQualityCrop:
    """
    A class for assessing the impact of crops on air quality. It calculates emissions
    from crops for both past and future scenarios, considering various emission categories.

    Attributes:
        ef_country (str): emission factor country.
        crop_air_quality_class: A class for calculating emissions for each category.
        common_class (CommonParams): A class for managing various data and constants.
        default_urea_proportion (float): The proportion of fertiliser inputs that is urea.
        default_urea_abated_porpotion (float): The proportion of urea that is abated urea.

    Methods:
        air_quality_crop_past(crop_dataframe):
            Calculates past emissions based on baseline data for animals and farm inputs.
        air_quality_crop_future(crop_dataframe, scenario_dataframe):
            Projects future emissions based on scenario data for animals and farm inputs.
        air_quality_crops_dissagregated(crop_dataframe, scenario_dataframe):
            Provides detailed emissions data combining past and future scenarios.

    """
    def __init__(self, ef_country, default_urea=None, default_urea_abated=None):
        self.common_class = CommonParams()
        self.ef_country = ef_country

        self.crop_air_quality_class = CropAirQualityTotals(ef_country)

        self.default_urea_proportion = default_urea
        self.default_urea_abated_porpotion = default_urea_abated

    def air_quality_crops_past(self, crop_dataframe):
        """
        Calculates past emissions based on baseline data for animals and farm inputs.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        baseline_index = self.common_class.baseline_index
        # base = self.baseline
        kg_to_kt = self.common_class.kg_to_kt

        crop_air_quality_dict = self.crop_air_quality_class.create_emissions_dictionary(
            [baseline_index]
        )

        data_frame = pd.DataFrame(crop_dataframe)

        # proportion of fertiliser inputs that is urea
        urea_proportion = self.default_urea_proportion
        urea_abated_proportion = self.default_urea_abated_porpotion
        # generate results and store them in the dictionary

        data = load_crop_farm_data(data_frame)

        base = list(data.keys())[0]

        crop_air_quality_dict["soils"][baseline_index] += (
            self.crop_air_quality_class.total_soils_NH3_AQ(
                data[base], urea_proportion, urea_abated_proportion
            )
        ) * kg_to_kt

        return crop_air_quality_dict

    def air_quality_crops_future(self, crop_dataframe, scenario_dataframe):
        """
        Projects future emissions based on scenario data for animals and farm inputs.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.
            scenario_dataframe (DataFrame): Data containing scenario information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        kg_to_kt = self.common_class.kg_to_kt

        data_frame = pd.DataFrame(crop_dataframe)

        urea_data = scenario_dataframe[
            ["Scenarios", "Urea proportion", "Urea abated proportion"]
        ].drop_duplicates()

        scenarios = list(urea_data["Scenarios"].values)

        crop_air_quality_dict = self.crop_air_quality_class.create_emissions_dictionary(
            scenarios
        )

        data = load_crop_farm_data(data_frame)

        for sc in scenarios:
            mask = urea_data["Scenarios"] == sc
            urea_proportion = urea_data.loc[mask, "Urea proportion"].item()
            urea_abated_proportion = urea_data.loc[
                mask, "Urea abated proportion"
            ].item()

            crop_air_quality_dict["soils"][sc] += (
                self.crop_air_quality_class.total_soils_NH3_AQ(
                    data[sc], urea_proportion, urea_abated_proportion
                )
            ) * kg_to_kt

        return crop_air_quality_dict

    def air_quality_crops_dissagregated(self, crop_dataframe, scenario_dataframe):
        """
        Combine past and future emissions data to provide a comprehensive view of crop impact on air quality.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.
            scenario_dataframe (DataFrame): Data containing scenario information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        past_data = pd.DataFrame.from_dict(self.air_quality_crops_past(crop_dataframe))

        future_data = pd.DataFrame.from_dict(
            self.air_quality_crops_future(crop_dataframe, scenario_dataframe)
        )

        return pd.concat([past_data, future_data])



class AirQualityTotal:
    """
    A class for assessing the total impact of livestock and crops on air quality. It calculates emissions
    from livestock and crops for both past and future scenarios, considering various emission categories.

    Attributes:
        common_class (CommonParams): A class for managing various data and constants.

    Methods:
        total_air_quality_emissions(dataframe_dict):
            Calculates total emissions for each scenario.

    """
    def __init__(self):
        self.common_class = CommonParams()


    def total_air_quality_emissions(self, dataframe_dict):
        """
        Calculates air quality total emissions for each scenario.

        Parameters:
            dataframe_dict (dict): A dictionary of dataframes containing baseline and scenario information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.
            
        """

        livestock_data = dataframe_dict["animal"]

        total_animal_and_crop_air_quality_emissions = livestock_data.copy(deep=True)

        total_animal_and_crop_air_quality_emissions[
            "Total"
        ] = total_animal_and_crop_air_quality_emissions.sum(axis=1)

        return total_animal_and_crop_air_quality_emissions
