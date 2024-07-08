"""
Impact Category Climate Change
==============================

The Impact Categories Climate Change module is designed to calculate and analyze various environmental impacts in the context of land use change, livestock and crop production. 
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
from cattle_lca.lca import ClimateChangeTotals as CattleClimateChangeTotals
from sheep_lca.lca import ClimateChangeTotals as SheepClimateChangeTotals
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import ClimateChangeTotals as CropClimateChangeTotals
import landcover_lca.lca_emission as landuse_lca
import landcover_lca.models as landuse_models
from goblin_lite.resource_manager.goblin_data_manager import GoblinDataManager
import pandas as pd
from goblin_lite.impact_categories.common import CommonParams


class ClimateChangeLandUse:
    """
    A class for calculating the impact of land use changes on climate change across various land types.

    Attributes:
        calibration_year (int): The baseline year for calculations.
        target_year (int): The target year for future projections.
        transition_data (DataFrame): Data detailing land use transitions.
        landuse_data (DataFrame): Specific data related to land use.
        forest_data (DataFrame): Data related to forest areas.
        ef_country (str): emission factor country.
        AR_VALUE (str): The assessment report value (default 'AR5').

    Methods:
        climate_change_landuse_past(): Calculates past emissions for different land uses.
        climate_change_landuse_future(): Projects future emissions based on land use scenarios.
        climate_change_landuse(): Combines past and future data for a comprehensive view.

    """
    def __init__(
        self,
        calibration_year,
        target_year,
        transition_data,
        landuse_data,
        forest_data,
        ef_country,
        AR_VALUE="AR5",
    ):
        self.common_class = CommonParams()
        self.baseline = calibration_year
        self.target_year = target_year
        self.ef_country = ef_country
        self.goblin_data_manager_class = GoblinDataManager(AR_VALUE=AR_VALUE)

        self.forest_data = forest_data

        self.transition_matrix = landuse_models.load_transition_matrix(
            transition_data, ef_country, calibration_year, target_year
        )

        self.land_use_data = landuse_models.load_land_use_data(
            landuse_data, calibration_year
        )

    def climate_change_landuse_past(self):
        """
        Calculate past emissions for different land use types, considering various greenhouse gases.

        Returns:
            DataFrame: A dataframe with emissions data for different land use types and gases.

        """
        baseline_index = self.common_class.baseline_index
        base = -self.baseline
        baseline = self.baseline
        ef_country = self.ef_country
        land_use_data = self.land_use_data
        transition_matrix = self.transition_matrix
        forest_data = self.forest_data
        kg_to_kt = self.common_class.kg_to_kt
        t_to_kt = self.common_class.t_to_kt

        emission_df = pd.DataFrame(
            columns=["CO2", "CH4", "N2O", "CO2e"],
            index=pd.MultiIndex.from_product(
                [
                    # list(scenario_list),
                    [baseline_index],
                    ["cropland", "grassland", "forest", "wetland", "total"],
                    [baseline],
                ],
                names=["scenario", "land_use", "year"],
            ),
        )

        emission_df.index.levels[0].astype(int)
        #need to add one year to the forest baseline year to get the correct data
        past_forest_mask = (forest_data["Year"] == baseline +1) & (
            forest_data["Scenario"] == baseline_index
        )

        emission_df.loc[
            (
                baseline_index,
                "total",
                baseline,
            ),
            "CH4",
        ] = (
            landuse_lca.total_ch4_emission(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )
        emission_df.loc[
            (
                baseline_index,
                "total",
                baseline,
            ),
            "CO2",
        ] = (
            (
                landuse_lca.total_co2_emission(
                    land_use_data[base],
                    land_use_data[base],
                    transition_matrix[base],
                    ef_country,
                )
            )
            * kg_to_kt
        ) + (
            forest_data.loc[past_forest_mask, "Total Ecosystem"].item()
            * t_to_kt
            * self.goblin_data_manager_class.get_AR_values()["CO2e"]
        )

        emission_df.loc[
            (
                baseline_index,
                "total",
                baseline,
            ),
            "N2O",
        ] = (
            landuse_lca.total_n2o_emission(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df.loc[
            (baseline_index, "cropland", baseline),
            "CO2",
        ] = (
            landuse_lca.total_co2_emission_cropland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df.loc[
            (
                baseline_index,
                "cropland",
                baseline,
            ),
            "CH4",
        ] = (
            landuse_lca.total_ch4_emission_cropland(
                ef_country,
                transition_matrix[base],
                land_use_data[base],
                land_use_data[base],
            )
            * kg_to_kt
        )

        emission_df.loc[
            (
                baseline_index,
                "cropland",
                baseline,
            ),
            "N2O",
        ] = (
            landuse_lca.total_n2o_emission_cropland(
                ef_country,
                transition_matrix[base],
                land_use_data[base],
                land_use_data[base],
            )
            * kg_to_kt
        )

        emission_df.loc[
            (
                baseline_index,
                "grassland",
                baseline,
            ),
            "CO2",
        ] = (
            landuse_lca.total_co2_emission_grassland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df.loc[
            (
                baseline_index,
                "grassland",
                baseline,
            ),
            "CH4",
        ] = (
            landuse_lca.total_ch4_emission_grassland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df.loc[
            (baseline_index, "grassland", baseline),
            "N2O",
        ] = (
            landuse_lca.total_n2o_emission_grassland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )
        emission_df.loc[
            (
                baseline_index,
                "wetland",
                baseline,
            ),
            "CO2",
        ] = (
            landuse_lca.total_co2_emission_wetland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
        ) * kg_to_kt

        emission_df.loc[
            (
                baseline_index,
                "wetland",
                baseline,
            ),
            "CH4",
        ] = (
            landuse_lca.total_ch4_emission_wetland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )
        emission_df.loc[
            (
                baseline_index,
                "wetland",
                baseline,
            ),
            "N2O",
        ] = (
            landuse_lca.total_n2o_emission_wetland(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )
        emission_df.loc[
            (
                baseline_index,
                "forest",
                baseline,
            ),
            "CO2",
        ] = (landuse_lca.total_co2_emission_forest(
              land_use_data[base],
               land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt)+ (forest_data.loc[past_forest_mask, "Total Ecosystem"].item()
            * t_to_kt
            * self.goblin_data_manager_class.get_AR_values()["CO2e"]
            )

        emission_df.loc[
            (baseline_index, "forest", baseline),
            "CH4",
        ] = (
            landuse_lca.total_ch4_emission_forest(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df.loc[
            (baseline_index, "forest", baseline),
            "N2O",
        ] = (
            landuse_lca.total_n2o_emission_forest(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        )

        emission_df["CO2e"] = (
            emission_df["CO2"]
            + (emission_df["CH4"] * self.goblin_data_manager_class.get_AR_values()["CH4"])
            + (emission_df["N2O"] * self.goblin_data_manager_class.get_AR_values()["N2O"])
        )

        return emission_df

    def climate_change_landuse_future(self):
        """
        Project future emissions based on various land use scenarios.

        Returns:
            DataFrame: A dataframe with projected emissions data for different land use types and gases.

        """
        base = -self.baseline
        baseline = self.baseline
        target_year = self.target_year
        ef_country = self.ef_country
        land_use_data = self.land_use_data
        transition_matrix = self.transition_matrix
        forest_data = self.forest_data
        kg_to_kt = self.common_class.kg_to_kt
        t_to_kt = self.common_class.t_to_kt

        index = [int(i) for i in self.land_use_data.keys() if int(i) >= 0]

        emission_df = pd.DataFrame(
            columns=["CO2", "CH4", "N2O", "CO2e"],
            index=pd.MultiIndex.from_product(
                [
                    list(index),
                    ["cropland", "grassland", "forest", "wetland", "total"],
                    [target_year],
                ],
                names=["scenario", "land_use", "year"],
            ),
        )

        emission_df.index.levels[0].astype(int)

        for sc in index:
            future_forest_mask = (forest_data["Year"] == target_year) & (
                forest_data["Scenario"] == sc
            )

            emission_df.loc[
                (
                    sc,
                    "total",
                    target_year,
                ),
                "CH4",
            ] = (
                landuse_lca.total_ch4_emission(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )
            emission_df.loc[
                (
                    sc,
                    "total",
                    target_year,
                ),
                "CO2",
            ] = (
                (
                    landuse_lca.total_co2_emission(
                        land_use_data[sc],
                        land_use_data[base],
                        transition_matrix[sc],
                        ef_country,
                    )
                )
                * kg_to_kt
            ) + (
                forest_data.loc[future_forest_mask, "Total Ecosystem"].item()
                * t_to_kt
                * self.goblin_data_manager_class.get_AR_values()["CO2e"]
            )

            emission_df.loc[
                (
                    sc,
                    "total",
                    target_year,
                ),
                "N2O",
            ] = (
                landuse_lca.total_n2o_emission(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

            emission_df.loc[
                (sc, "cropland", target_year),
                "CO2",
            ] = (
                landuse_lca.total_co2_emission_cropland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

            emission_df.loc[
                (
                    sc,
                    "cropland",
                    target_year,
                ),
                "CH4",
            ] = (
                landuse_lca.total_ch4_emission_cropland(
                    ef_country,
                    transition_matrix[sc],
                    land_use_data[base],
                    land_use_data[sc],
                )
                * kg_to_kt
            )

            emission_df.loc[
                (
                    sc,
                    "cropland",
                    target_year,
                ),
                "N2O",
            ] = (
                landuse_lca.total_n2o_emission_cropland(
                    ef_country,
                    transition_matrix[sc],
                    land_use_data[base],
                    land_use_data[sc],
                )
                * kg_to_kt
            )

            emission_df.loc[
                (
                    sc,
                    "grassland",
                    target_year,
                ),
                "CO2",
            ] = (
                landuse_lca.total_co2_emission_grassland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

            emission_df.loc[
                (
                    sc,
                    "grassland",
                    target_year,
                ),
                "CH4",
            ] = (
                landuse_lca.total_ch4_emission_grassland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

            emission_df.loc[
                (sc, "grassland", target_year),
                "N2O",
            ] = (
                landuse_lca.total_n2o_emission_grassland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )
            emission_df.loc[
                (
                    sc,
                    "wetland",
                    target_year,
                ),
                "CO2",
            ] = (
                landuse_lca.total_co2_emission_wetland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
            ) * kg_to_kt

            emission_df.loc[
                (
                    sc,
                    "wetland",
                    target_year,
                ),
                "CH4",
            ] = (
                landuse_lca.total_ch4_emission_wetland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )
            emission_df.loc[
                (
                    sc,
                    "wetland",
                    target_year,
                ),
                "N2O",
            ] = (
                landuse_lca.total_n2o_emission_wetland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )
            emission_df.loc[
                (
                    sc,
                    "forest",
                    target_year,
                ),
                "CO2",
            ] = (
                landuse_lca.total_co2_emission_forest(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            ) + (
                forest_data.loc[future_forest_mask, "Total Ecosystem"].item()
                * t_to_kt
                * self.goblin_data_manager_class.get_AR_values()["CO2e"]
            )

            emission_df.loc[
                (sc, "forest", target_year),
                "CH4",
            ] = (
                landuse_lca.total_ch4_emission_forest(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )
            emission_df.loc[
                (sc, "forest", target_year),
                "N2O",
            ] = (
                landuse_lca.total_n2o_emission_forest(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

        emission_df["CO2e"] = (
            emission_df["CO2"]
            + (emission_df["CH4"] * self.goblin_data_manager_class.get_AR_values()["CH4"])
            + (emission_df["N2O"] * self.goblin_data_manager_class.get_AR_values()["N2O"])
        )

        return emission_df

    def climate_change_landuse(self):
        """
        Combine past and future emissions data to provide a comprehensive view of land use impact on climate change.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        past_data = self.climate_change_landuse_past()

        future_data = self.climate_change_landuse_future()

        return pd.concat([past_data, future_data])


class ClimateChangeLivestock:
    """
    A class for assessing the impact of livestock on climate change. It calculates emissions 
    from cattle and sheep for both past and future scenarios, considering various greenhouse gases.

    Attributes:
        ef_country (str): emission factor country..
        calibration_year (int): The year used as a baseline for calculations.
        target_year (int): The target year for future scenario projections.
        transition_data, landuse_data, crop_data (DataFrame): DataFrames containing relevant data for calculations.
        AR_VALUE (str): The assessment report value, defaulting to 'AR5'.
        cattle_climate_change_class, sheep_climate_change_class, crop_climate_change_class: Classes for calculating emissions for each category.
        goblin_data_manager_class (GoblinDataManager): A class for managing various data and constants.

    Methods:
        climate_change_livestock_past(baseline_animals, baseline_farms):
            Calculates past emissions based on baseline data for animals and farm inputs.
        climate_change_livestock_future(scenario_animals, scenario_farms):
            Projects future emissions based on scenario data for animals and farm inputs.
        climate_change_livestock_dissagregated(baseline_animals, scenario_animals, baseline_farms, scenario_farms):
            Provides detailed emissions data combining past and future scenarios.
        climate_change_livestock_aggregated(baseline_animals, scenario_animals, baseline_farms, scenario_farms):
            Provides aggregated emissions data for easy interpretation and analysis.
        climate_change_livestock_categories_as_co2e(baseline_animals, scenario_animals, baseline_farms, scenario_farms):
            Converts emissions data into CO2 equivalents for various categories.

    """
    def __init__(self, ef_country,calibration_year, target_year, transition_data, landuse_data, crop_data, AR_VALUE="AR5"):
        self.common_class = CommonParams()
        self.cattle_climate_change_class = CattleClimateChangeTotals(ef_country)
        self.sheep_climate_change_class = SheepClimateChangeTotals(ef_country)
        self.crop_climate_change_class = CropClimateChangeTotals(ef_country)
        self.goblin_data_manager_class = GoblinDataManager(AR_VALUE=AR_VALUE)
        self.ef_country = ef_country
        self.baseline = calibration_year

        self.transition_matrix = landuse_models.load_transition_matrix(
            transition_data, ef_country, calibration_year, target_year
        )

        self.land_use_data = landuse_models.load_land_use_data(
            landuse_data, calibration_year
        )

        self.crop_data =  load_crop_farm_data(crop_data)

    def climate_change_livestock_past(self, baseline_animals, baseline_farms):
        """
        Calculate past livestock-related emissions for cattle and sheep, including various emission categories.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            baseline_farms (DataFrame): Data containing baseline farm information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        base = -self.baseline
        baseline_index = self.common_class.baseline_index
        kg_to_kt = self.common_class.kg_to_kt
        ef_country = self.ef_country
        land_use_data = self.land_use_data
        transition_matrix = self.transition_matrix
        crop_data = self.crop_data
        crop_base = list(crop_data.keys())[0]


        emissions_dict = self.cattle_climate_change_class.create_emissions_dictionary(
            [baseline_index]
        )

        baseline_animals = load_livestock_data(baseline_animals)
        baseline_farms = load_farm_data(baseline_farms)

        past_farm_loc = list(baseline_farms.keys())[0]

        past_animals_loc = list(baseline_animals.keys())[0]

        emissions_dict["enteric_ch4"][baseline_index] += (
            self.cattle_climate_change_class.CH4_enteric_ch4(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["manure_management_N2O"][baseline_index] += (
            self.cattle_climate_change_class.Total_storage_N2O(
                baseline_animals[past_animals_loc]["animals"]
            )
            * kg_to_kt
        )
        emissions_dict["manure_management_CH4"][baseline_index] += (
            self.cattle_climate_change_class.CH4_manure_management(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["manure_applied_N"][baseline_index] += (
            self.cattle_climate_change_class.Total_N2O_Spreading(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["N_direct_PRP"][baseline_index] += (
            self.cattle_climate_change_class.N2O_total_PRP_N2O_direct(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        emissions_dict["N_indirect_PRP"][baseline_index] += (
            self.cattle_climate_change_class.N2O_total_PRP_N2O_indirect(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        emissions_dict["N_direct_fertiliser"][baseline_index] = (
            self.cattle_climate_change_class.N2O_direct_fertiliser(
                baseline_farms[past_farm_loc].urea_n_fert,
                baseline_farms[past_farm_loc].urea_abated_n_fert,
                baseline_farms[past_farm_loc].an_n_fert,
            )
            * kg_to_kt
        )

        emissions_dict["N_indirect_fertiliser"][baseline_index] += (
            self.cattle_climate_change_class.N2O_fertiliser_indirect(
                baseline_farms[past_farm_loc].urea_n_fert,
                baseline_farms[past_farm_loc].urea_abated_n_fert,
                baseline_farms[past_farm_loc].an_n_fert,
            )
            * kg_to_kt
        )

        emissions_dict["soils_CO2"][baseline_index] += (
            self.cattle_climate_change_class.CO2_soils_GWP(
                baseline_farms[past_farm_loc].total_urea_kg,
                baseline_farms[past_farm_loc].total_lime_kg,
            )
            * kg_to_kt
        )

        # Past Sheep
        emissions_dict["enteric_ch4"][baseline_index] += (
            self.sheep_climate_change_class.CH4_enteric_ch4(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["manure_management_N2O"][baseline_index] += (
            self.sheep_climate_change_class.Total_storage_N2O(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["manure_management_CH4"][baseline_index] += (
            self.sheep_climate_change_class.CH4_manure_management(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["N_direct_PRP"][baseline_index] += (
            self.sheep_climate_change_class.N2O_total_PRP_N2O_direct(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        emissions_dict["N_indirect_PRP"][baseline_index] += (
            self.sheep_climate_change_class.N2O_total_PRP_N2O_indirect(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        # Totals
        emissions_dict["soil_histosol_N_direct"][baseline_index] = (
                landuse_lca.drainage_n2O_organic_soils_in_grassland(
                    land_use_data[base],
                    land_use_data[base],
                    transition_matrix[base],
                    ef_country,
                )
                * kg_to_kt
            )
        
        emissions_dict["crop_residue_direct"][baseline_index] += (
            self.crop_climate_change_class.total_residue_per_crop_direct(
                crop_data[crop_base],
            )
        ) * kg_to_kt

        emissions_dict["soil_organic_N_direct"][baseline_index] = (
            emissions_dict["manure_applied_N"][baseline_index]
            + emissions_dict["N_direct_PRP"][baseline_index]
        )
        emissions_dict["soil_organic_N_indirect"][baseline_index] = emissions_dict[
            "N_indirect_PRP"
        ][baseline_index]

        emissions_dict["soil_inorganic_N_direct"][baseline_index] = emissions_dict[
            "N_direct_fertiliser"
        ][baseline_index]
        emissions_dict["soil_inorganic_N_indirect"][baseline_index] = emissions_dict[
            "N_indirect_fertiliser"
        ][baseline_index]

        emissions_dict["soil_N_direct"][baseline_index] = (
            emissions_dict["soil_organic_N_direct"][baseline_index]
            + emissions_dict["soil_inorganic_N_direct"][baseline_index]
            + emissions_dict["soil_histosol_N_direct"][baseline_index]
            +emissions_dict["crop_residue_direct"][baseline_index]
        )

        emissions_dict["soil_N_indirect"][baseline_index] = (
            emissions_dict["soil_inorganic_N_indirect"][baseline_index]
            + emissions_dict["soil_organic_N_indirect"][baseline_index]
        )

        emissions_dict["soils_N2O"][baseline_index] = (
            emissions_dict["soil_N_direct"][baseline_index]
            + emissions_dict["soil_N_indirect"][baseline_index]
        )

        return emissions_dict

    def climate_change_livestock_future(self, scenario_animals, scenario_farms):
        """
        Calculate scenario livestock-related emissions for cattle and sheep, including various emission categories.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            baseline_farms (DataFrame): Data containing baseline farm information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        base = -self.baseline
        scenario_animals_dataframe = scenario_animals
        ef_country = self.ef_country
        land_use_data = self.land_use_data
        transition_matrix = self.transition_matrix
        crop_data = self.crop_data


        index = [int(i) for i in scenario_animals_dataframe.Scenarios.unique()]

        scenario_animals = load_livestock_data(scenario_animals)
        scenario_farms = load_farm_data(scenario_farms)

        kg_to_kt = self.common_class.kg_to_kt

        # create emissions dictionary

        emissions_dict = self.cattle_climate_change_class.create_emissions_dictionary(
            index
        )

        # generate results and store them in the dictionary

        for sc in index:
            for farm_id in scenario_animals_dataframe.farm_id[
                scenario_animals_dataframe["Scenarios"] == sc
            ].unique():
                emissions_dict["enteric_ch4"][sc] += (
                    self.cattle_climate_change_class.CH4_enteric_ch4(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                emissions_dict["manure_management_N2O"][sc] += (
                    self.cattle_climate_change_class.Total_storage_N2O(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                emissions_dict["manure_management_CH4"][sc] += (
                    self.cattle_climate_change_class.CH4_manure_management(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                emissions_dict["manure_applied_N"][sc] += (
                    self.cattle_climate_change_class.Total_N2O_Spreading(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                emissions_dict["N_direct_PRP"][sc] += (
                    self.cattle_climate_change_class.N2O_total_PRP_N2O_direct(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )

                emissions_dict["N_indirect_PRP"][sc] += (
                    self.cattle_climate_change_class.N2O_total_PRP_N2O_indirect(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                emissions_dict["enteric_ch4"][sc] += (
                    self.sheep_climate_change_class.CH4_enteric_ch4(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                emissions_dict["manure_management_N2O"][sc] += (
                    self.sheep_climate_change_class.Total_storage_N2O(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                emissions_dict["manure_management_CH4"][sc] += (
                    self.sheep_climate_change_class.CH4_manure_management(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                emissions_dict["N_direct_PRP"][sc] += (
                    self.sheep_climate_change_class.N2O_total_PRP_N2O_direct(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )
                emissions_dict["N_indirect_PRP"][sc] += (
                    self.sheep_climate_change_class.N2O_total_PRP_N2O_indirect(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )

            emissions_dict["N_direct_fertiliser"][sc] = (
                self.cattle_climate_change_class.N2O_direct_fertiliser(
                    scenario_farms[sc].urea_n_fert,
                    scenario_farms[sc].urea_abated_n_fert,
                    scenario_farms[sc].an_n_fert,
                )
                * kg_to_kt
            )

            emissions_dict["N_indirect_fertiliser"][sc] += (
                self.cattle_climate_change_class.N2O_fertiliser_indirect(
                    scenario_farms[sc].urea_n_fert,
                    scenario_farms[sc].urea_abated_n_fert,
                    scenario_farms[sc].an_n_fert,
                )
                * kg_to_kt
            )
            emissions_dict["soils_CO2"][sc] += (
                self.cattle_climate_change_class.CO2_soils_GWP(
                    scenario_farms[sc].total_urea_kg,
                    scenario_farms[sc].total_lime_kg,
                )
                * kg_to_kt
            )

            # Add the totals
            emissions_dict["soil_histosol_N_direct"][sc] += (
                landuse_lca.drainage_n2O_organic_soils_in_grassland(
                    land_use_data[sc],
                    land_use_data[base],
                    transition_matrix[sc],
                    ef_country,
                )
                * kg_to_kt
            )

            emissions_dict["crop_residue_direct"][sc] += (
            self.crop_climate_change_class.total_residue_per_crop_direct(
                crop_data[sc],
            )
            ) * kg_to_kt
            
            emissions_dict["soil_organic_N_direct"][sc] = (
                emissions_dict["manure_applied_N"][sc]
                + emissions_dict["N_direct_PRP"][sc]
            )
            emissions_dict["soil_organic_N_indirect"][sc] = emissions_dict[
                "N_indirect_PRP"
            ][sc]

            emissions_dict["soil_inorganic_N_direct"][sc] = emissions_dict[
                "N_direct_fertiliser"
            ][sc]
            emissions_dict["soil_inorganic_N_indirect"][sc] = emissions_dict[
                "N_indirect_fertiliser"
            ][sc]

            emissions_dict["soil_N_direct"][sc] = (
                emissions_dict["soil_organic_N_direct"][sc]
                + emissions_dict["soil_inorganic_N_direct"][sc]
                + emissions_dict["soil_histosol_N_direct"][sc]
                + emissions_dict["crop_residue_direct"][sc] 
            )

            emissions_dict["soil_N_indirect"][sc] = (
                emissions_dict["soil_inorganic_N_indirect"][sc]
                + emissions_dict["soil_organic_N_indirect"][sc]
            )

            emissions_dict["soils_N2O"][sc] = (
                emissions_dict["soil_N_direct"][sc]
                + emissions_dict["soil_N_indirect"][sc]
            )

        return emissions_dict

    def climate_change_livestock_dissagregated(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        """
        Combine past and future emissions data to provide a comprehensive view of livestock impact on climate change.
        
        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            scenario_animals (DataFrame): Data containing scenario animal information.
            baseline_farms (DataFrame): Data containing baseline farm input information.
            scenario_farms (DataFrame): Data containing scenario farm input information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        past_data = pd.DataFrame.from_dict(
            self.climate_change_livestock_past(baseline_animals, baseline_farms)
        )

        future_data = pd.DataFrame.from_dict(
            self.climate_change_livestock_future(scenario_animals, scenario_farms)
        )

        return pd.concat([past_data, future_data])

    def climate_change_livestock_aggregated(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        """
        Combine past and future emissions data to provide a comprehensive view of livestock impact on climate change
        for various GHG categories.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            scenario_animals (DataFrame): Data containing scenario animal information.
            baseline_farms (DataFrame): Data containing baseline farm input information.
            scenario_farms (DataFrame): Data containing scenario farm input information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        dissagregated_animal_emissions = self.climate_change_livestock_dissagregated(
            baseline_animals, scenario_animals, baseline_farms, scenario_farms
        )

        emissions_groups = (
            self.goblin_data_manager_class.get_climate_change_livestock_emissions_groups()
        )
        AR_values = self.goblin_data_manager_class.get_AR_values()

        total_animal_emissions = pd.DataFrame(
            columns=emissions_groups.keys(), index=dissagregated_animal_emissions.index
        )

        for col in total_animal_emissions.columns:
            try:
                total_animal_emissions[col] = (
                    dissagregated_animal_emissions[emissions_groups[col][0]].values
                    + dissagregated_animal_emissions[emissions_groups[col][1]].values
                )
            except IndexError:
                total_animal_emissions[col] = dissagregated_animal_emissions[
                    emissions_groups[col][0]
                ].values

        total_animal_emissions["CO2e"] = (
            (total_animal_emissions["CH4"] * AR_values["CH4"])
            + (total_animal_emissions["N2O"] * AR_values["N2O"])
            + total_animal_emissions["CO2"]
        )

        return total_animal_emissions

    def climate_change_livestock_categories_as_co2e(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        """
        Combine past and future emissions data to provide a comprehensive view of livestock impact on climate change
        for various GHG categories, converted to CO2 equivalents.

        Parameters:
            baseline_animals (DataFrame): Data containing baseline animal information.
            scenario_animals (DataFrame): Data containing scenario animal information.
            baseline_farms (DataFrame): Data containing baseline farm input information.
            scenario_farms (DataFrame): Data containing scenario farm input information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        dissagregated_animal_emissions = self.climate_change_livestock_dissagregated(
            baseline_animals, scenario_animals, baseline_farms, scenario_farms
        )

        emissions_groups = (
            self.goblin_data_manager_class.get_climate_change_livestock_emissions_categories()
        )

        AR_values = self.goblin_data_manager_class.get_AR_values()

        conversion_groups = (
            self.goblin_data_manager_class.get_climate_change_livestock_conversion_groups()
        )

        ar_dict = {"N2O": AR_values["N2O"], "CH4": AR_values["CH4"]}

        for gas in conversion_groups.keys():
            for category in conversion_groups[gas]:
                if gas in ar_dict.keys():
                    dissagregated_animal_emissions.loc[:, category] *= ar_dict[gas]

        total_animal_emissions = pd.DataFrame(
            columns=emissions_groups.keys(), index=dissagregated_animal_emissions.index
        )

        for col in total_animal_emissions.columns:
            try:
                total_animal_emissions[col] = (
                    dissagregated_animal_emissions[emissions_groups[col][0]].values
                    + dissagregated_animal_emissions[emissions_groups[col][1]].values
                )
            except IndexError:
                total_animal_emissions[col] = dissagregated_animal_emissions[
                    emissions_groups[col][0]
                ].values

        return total_animal_emissions


class ClimateChangeCrop:
    """
    A class for assessing the impact of crops on climate change. It calculates emissions
    from crops for both past and future scenarios, considering various emission categories.

    Attributes:
        ef_country (str): emission factor country.
        crop_climate_change_class: A class for calculating emissions for each category.
        common_class (CommonParams): A class for managing various data and constants.
        default_urea_proportion (float): The proportion of fertiliser inputs that is urea.
        default_urea_abated_porpotion (float): The proportion of urea that is abated urea.

    Methods:
        climate_change_crop_past(crop_dataframe):
            Calculates past emissions based on baseline data for animals and farm inputs.
        climate_change_crop_future(crop_dataframe, scenario_dataframe):
            Projects future emissions based on scenario data for animals and farm inputs.
        climate_change_crops_dissagregated(crop_dataframe, scenario_dataframe):
            Provides detailed emissions data combining past and future scenarios.
        climate_change_crops_categories_as_co2e(crop_dataframe, scenario_dataframe):
            Provides emissions data combining past and future scenarios, converted to CO2 equivalents.

    """

    def __init__(
        self, ef_country, default_urea=None, default_urea_abated=None, AR_VALUE="AR5"
    ):
        self.common_class = CommonParams()
        self.goblin_data_manager_class = GoblinDataManager(AR_VALUE=AR_VALUE)
        self.ef_country = ef_country

        self.crop_climate_change_class = CropClimateChangeTotals(ef_country)

        self.default_urea_proportion = default_urea
        self.default_urea_abated_porpotion = default_urea_abated

    def climate_change_crop_past(self, crop_dataframe):
        """
        Calculates past emissions based on baseline data for animals and farm inputs.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.

        Returns:
            dict: A dictionary of emissions data categorized by emission type.

        """
        baseline_index = self.common_class.baseline_index
        kg_to_kt = self.common_class.kg_to_kt

        crop_emissions_dict = (
            self.crop_climate_change_class.create_emissions_dictionary([baseline_index])
        )

        data_frame = pd.DataFrame(crop_dataframe)

        # proportion of fertiliser inputs that is urea
        urea_proportion = self.default_urea_proportion
        urea_abated_proportion = self.default_urea_abated_porpotion
        # generate results and store them in the dictionary

        data = load_crop_farm_data(data_frame)

        base = list(data.keys())[0]

        crop_emissions_dict["crop_residue_direct"][baseline_index] += (
            self.crop_climate_change_class.total_residue_per_crop_direct(
                data[base],
            )
        ) * kg_to_kt

        crop_emissions_dict["N_direct_fertiliser"][baseline_index] += (
            self.crop_climate_change_class.total_fertiliser_direct(
                data[base],
                urea_proportion,
                urea_abated_proportion,
            )
        ) * kg_to_kt

        crop_emissions_dict["N_indirect_fertiliser"][baseline_index] += (
            self.crop_climate_change_class.total_fertiliser_indirect(
                data[base],
                urea_proportion,
                urea_abated_proportion,
            )
        ) * kg_to_kt

        crop_emissions_dict["soils_N2O"][baseline_index] += (
            crop_emissions_dict["crop_residue_direct"][baseline_index]
            + crop_emissions_dict["N_direct_fertiliser"][baseline_index]
            + crop_emissions_dict["N_indirect_fertiliser"][baseline_index]
        )

        crop_emissions_dict["soils_CO2"][baseline_index] += (
            self.crop_climate_change_class.urea_co2(
                data[base],
                urea_proportion,
                urea_abated_proportion,
            )
        ) * kg_to_kt

        return crop_emissions_dict

    def climate_change_crop_future(self, crop_dataframe, scenario_dataframe):
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

        crop_emissions_dict = (
            self.crop_climate_change_class.create_emissions_dictionary(scenarios)
        )

        data = load_crop_farm_data(data_frame)

        for sc in scenarios:
            mask = urea_data["Scenarios"] == sc
            urea_proportion = urea_data.loc[mask, "Urea proportion"].item()
            urea_abated_proportion = urea_data.loc[
                mask, "Urea abated proportion"
            ].item()

            crop_emissions_dict["crop_residue_direct"][sc] += (
                self.crop_climate_change_class.total_residue_per_crop_direct(
                    data[sc],
                )
            ) * kg_to_kt

            crop_emissions_dict["N_direct_fertiliser"][sc] += (
                self.crop_climate_change_class.total_fertiliser_direct(
                    data[sc],
                    urea_proportion,
                    urea_abated_proportion,
                )
            ) * kg_to_kt

            crop_emissions_dict["N_indirect_fertiliser"][sc] += (
                self.crop_climate_change_class.total_fertiliser_indirect(
                    data[sc],
                    urea_proportion,
                    urea_abated_proportion,
                )
            ) * kg_to_kt

            crop_emissions_dict["soils_N2O"][sc] += (
                crop_emissions_dict["crop_residue_direct"][sc]
                + crop_emissions_dict["N_direct_fertiliser"][sc]
                + crop_emissions_dict["N_indirect_fertiliser"][sc]
            )

            crop_emissions_dict["soils_CO2"][sc] += (
                self.crop_climate_change_class.urea_co2(
                    data[sc],
                    urea_proportion,
                    urea_abated_proportion,
                )
            ) * kg_to_kt

        return crop_emissions_dict

    def climate_change_crops_dissagregated(self, crop_dataframe, scenario_dataframe):
        """
        Combine past and future emissions data to provide a comprehensive view of crop impact on climate change.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.
            scenario_dataframe (DataFrame): Data containing scenario information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        past_data = pd.DataFrame.from_dict(
            self.climate_change_crop_past(crop_dataframe)
        )

        future_data = pd.DataFrame.from_dict(
            self.climate_change_crop_future(crop_dataframe, scenario_dataframe)
        )

        return pd.concat([past_data, future_data])

    def climate_change_crops_categories_as_co2e(
        self, crop_dataframe, scenario_dataframe
    ):
        """
        Combine past and future emissions data to provide a comprehensive view of crop impact on climate change,
        converted to CO2 equivalents.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.
            scenario_dataframe (DataFrame): Data containing scenario information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.
        """
        dissagregated_crop_emissions = self.climate_change_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        emissions_groups = (
            self.goblin_data_manager_class.get_climate_change_crops_emissions_groups()
        )

        AR_values = self.goblin_data_manager_class.get_AR_values()

        conversion_groups = (
            self.goblin_data_manager_class.get_climate_change_crop_conversion_groups()
        )

        ar_dict = {"N2O": AR_values["N2O"]}

        for gas in conversion_groups.keys():
            for category in conversion_groups[gas]:
                if gas in ar_dict.keys():
                    dissagregated_crop_emissions.loc[:, category] *= ar_dict[gas]

        total_crop_emissions = pd.DataFrame(
            columns=emissions_groups.keys(), index=dissagregated_crop_emissions.index
        )

        for col in total_crop_emissions.columns:
            total_crop_emissions[col] = dissagregated_crop_emissions[
                emissions_groups[col][0]
            ].values

        total_crop_emissions["soils"] = total_crop_emissions.sum(axis=1)

        return total_crop_emissions


    def climate_change_crops_aggregated(self, crop_dataframe, scenario_dataframe):
        """
        Combine past and future emissions data to provide a comprehensive view of crop impact on climate change
        for various GHG categories.

        Parameters:
            crop_dataframe (DataFrame): Data containing baseline crop information.
            scenario_dataframe (DataFrame): Data containing scenario information.

        Returns:
            DataFrame: A combined dataframe of past and future emissions data.

        """
        AR_values = self.goblin_data_manager_class.get_AR_values()

        dissagregated_crop_emissions = self.climate_change_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        emissions_groups = (
            self.goblin_data_manager_class.get_climate_change_crops_emissions_groups()
        )

        total_crop_emissions = pd.DataFrame(
            columns=emissions_groups.keys(), index=dissagregated_crop_emissions.index
        )

        total_crop_emissions["CH4"] = 0
        total_crop_emissions["CO2"] = dissagregated_crop_emissions["soils_CO2"]
        total_crop_emissions["N2O"] = dissagregated_crop_emissions["soils_N2O"]
        total_crop_emissions["CO2e"] = (
            total_crop_emissions["N2O"].values * AR_values["N2O"]
        ) + (total_crop_emissions["CO2"].values)

        return total_crop_emissions
    


class ClimateChangeTotal:
    """
    A class for assessing the total impact of land use change, livestock and crops on climate change. It calculates emissions
    from land use change, livestock and crops for both past and future scenarios, considering various emission categories.
    
    Attributes:
        common_class (CommonParams): A class for managing various data and constants.

    Methods:
        total_climate_change_emissions(calibration_year, target_year, scenario_dataframe, dataframe_dict):
            Calculates total emissions for each scenario.

    """
    def __init__(self):
        self.common_class = CommonParams()

    def total_climate_change_emissions(
        self, calibration_year, target_year, scenario_dataframe, dataframe_dict
    ):
        """
        Calculates climate change total emissions for each scenario.

        Parameters:
            calibration_year (int): The year for which calibration data is available.
            target_year (int): The year for which scenario ends.
            scenario_dataframe (DataFrame): Data containing scenario information.
            dataframe_dict (dict): A dictionary of dataframes containing baseline and scenario information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.

        """

        baseline_index = self.common_class.baseline_index

        animal_data = dataframe_dict["animal"]
        land_use_data = dataframe_dict["land"]

        total_climate_change_emissions_dataframe = animal_data.copy(deep=True)

        land_use_dataframe = land_use_data.copy(deep=True)

        scenario_list = [baseline_index]
        scenario_list.extend(list(scenario_dataframe["Scenarios"].unique()))

        for sc in scenario_list:
            for gas in total_climate_change_emissions_dataframe.columns:
                if sc >= 0:
                    land_mask = (
                        (land_use_dataframe.index == sc)
                        & (land_use_dataframe["land_use"] == "total")
                        & (land_use_dataframe["year"] == target_year)
                    )
                else:
                    land_mask = (
                        (land_use_dataframe.index == sc)
                        & (land_use_dataframe["land_use"] == "total")
                        & (land_use_dataframe["year"] == calibration_year)
                    )

                total_climate_change_emissions_dataframe.loc[
                    sc, gas
                ] += land_use_dataframe.loc[land_mask, gas].item()

        return total_climate_change_emissions_dataframe