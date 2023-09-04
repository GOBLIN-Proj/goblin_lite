from cattle_lca.models import load_livestock_data, load_farm_data
from cattle_lca.lca import ClimateChangeTotals as CattleClimateChangeTotals
from sheep_lca.lca import ClimateChangeTotals as SheepClimateChangeTotals
from cattle_lca.lca import EutrophicationTotals as CattleEutrophicationTotals
from sheep_lca.lca import EutrophicationTotals as SheepEutrophicationTotals
from cattle_lca.lca import AirQualityTotals as CattleAirQualityTotals
from sheep_lca.lca import AirQualityTotals as SheepAirQualityTotals
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import ClimateChangeTotals as CropClimateChangeTotals
from crop_lca.lca import EutrophicationTotals as CropEutrophicationTotals
from crop_lca.lca import AirQualityTotals as CropAirQualityTotals
import landcover_lca.lca_emission as landuse_lca
import landcover_lca.models as landuse_models
from goblin_lite.goblin_data_manager import GoblinDataManager
import pandas as pd


class CommonParams:
    def __init__(self) -> None:
        self.baseline_index = -1
        self.kg_to_kt = 1e-6
        self.t_to_kt = 1e-3


class ClimateChangeLandUse:
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

        past_forest_mask = (forest_data["Year"] == baseline) & (
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
                + landuse_lca.horticulture_co2_peat_export(
                    ef_country, baseline, baseline
                )
            )
            * kg_to_kt
        ) + (
            forest_data.loc[past_forest_mask, "Total Ecosystem"].item()
            * t_to_kt
            * self.goblin_data_manager_class.AR_values["CO2e"]
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
            + landuse_lca.horticulture_co2_peat_export(ef_country, baseline, baseline)
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
        ] = (
            landuse_lca.total_co2_emission_forest(
                land_use_data[base],
                land_use_data[base],
                transition_matrix[base],
                ef_country,
            )
            * kg_to_kt
        ) + (
            forest_data.loc[past_forest_mask, "Total Ecosystem"].item()
            * t_to_kt
            * self.goblin_data_manager_class.AR_values["CO2e"]
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
            + (emission_df["CH4"] * self.goblin_data_manager_class.AR_values["CH4"])
            + (emission_df["N2O"] * self.goblin_data_manager_class.AR_values["N2O"])
        )

        return emission_df

    def climate_change_landuse_future(self):
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
                    + landuse_lca.horticulture_co2_peat_export(
                        ef_country, target_year, baseline
                    )
                )
                * kg_to_kt
            ) + (
                forest_data.loc[future_forest_mask, "Total Ecosystem"].item()
                * t_to_kt
                * self.goblin_data_manager_class.AR_values["CO2e"]
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
                + landuse_lca.horticulture_co2_peat_export(
                    ef_country, target_year, baseline
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
                * self.goblin_data_manager_class.AR_values["CO2e"]
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
            + (emission_df["CH4"] * self.goblin_data_manager_class.AR_values["CH4"])
            + (emission_df["N2O"] * self.goblin_data_manager_class.AR_values["N2O"])
        )

        return emission_df

    def climate_change_landuse(self):
        past_data = self.climate_change_landuse_past()

        future_data = self.climate_change_landuse_future()

        return pd.concat([past_data, future_data])


class ClimateChangeLivestock:
    def __init__(self, ef_country, AR_VALUE="AR5"):
        self.common_class = CommonParams()
        self.cattle_climate_change_class = CattleClimateChangeTotals(ef_country)
        self.sheep_climate_change_class = SheepClimateChangeTotals(ef_country)
        self.goblin_data_manager_class = GoblinDataManager(AR_VALUE=AR_VALUE)

    def climate_change_livestock_past(self, baseline_animals, baseline_farms):
        baseline_index = self.common_class.baseline_index
        kg_to_kt = self.common_class.kg_to_kt

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
                baseline_farms[past_farm_loc].total_urea,
                baseline_farms[past_farm_loc].total_urea_abated,
                baseline_farms[past_farm_loc].total_n_fert,
            )
            * kg_to_kt
        )

        emissions_dict["N_indirect_fertiliser"][baseline_index] += (
            self.cattle_climate_change_class.N2O_fertiliser_indirect(
                baseline_farms[past_farm_loc].total_urea,
                baseline_farms[past_farm_loc].total_urea_abated,
                baseline_farms[past_farm_loc].total_n_fert,
            )
            * kg_to_kt
        )
        emissions_dict["soils_CO2"][baseline_index] += (
            self.cattle_climate_change_class.CO2_soils_GWP(
                baseline_farms[past_farm_loc].total_urea,
                baseline_farms[past_farm_loc].total_urea_abated,
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
        scenario_animals_dataframe = scenario_animals

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
                    scenario_farms[sc].total_urea,
                    scenario_farms[sc].total_urea_abated,
                    scenario_farms[sc].total_n_fert,
                )
                * kg_to_kt
            )

            emissions_dict["N_indirect_fertiliser"][sc] += (
                self.cattle_climate_change_class.N2O_fertiliser_indirect(
                    scenario_farms[sc].total_urea,
                    scenario_farms[sc].total_urea_abated,
                    scenario_farms[sc].total_n_fert,
                )
                * kg_to_kt
            )
            emissions_dict["soils_CO2"][sc] += (
                self.cattle_climate_change_class.CO2_soils_GWP(
                    scenario_farms[sc].total_urea,
                    scenario_farms[sc].total_urea_abated,
                )
                * kg_to_kt
            )

            # Add the totals
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
        self, basline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        past_data = pd.DataFrame.from_dict(
            self.climate_change_livestock_past(basline_animals, baseline_farms)
        )

        future_data = pd.DataFrame.from_dict(
            self.climate_change_livestock_future(scenario_animals, scenario_farms)
        )

        return pd.concat([past_data, future_data])

    def climate_change_livestock_aggregated(
        self, basline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        dissagregated_animal_emissions = self.climate_change_livestock_dissagregated(
            basline_animals, scenario_animals, baseline_farms, scenario_farms
        )

        emissions_groups = (
            self.goblin_data_manager_class.climate_change_livestock_emissions_groups
        )
        AR_values = self.goblin_data_manager_class.AR_values

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
        self, basline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        dissagregated_animal_emissions = self.climate_change_livestock_dissagregated(
            basline_animals, scenario_animals, baseline_farms, scenario_farms
        )

        emissions_groups = (
            self.goblin_data_manager_class.climate_change_livestock_emissions_categories
        )

        AR_values = self.goblin_data_manager_class.AR_values

        conversion_groups = (
            self.goblin_data_manager_class.climate_change_livestock_conversion_groups
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


class EutrophicationLivestock:
    def __init__(self, ef_country):
        self.common_class = CommonParams()
        self.cattle_eutrophication_class = CattleEutrophicationTotals(ef_country)
        self.sheep_eutrophication_class = SheepEutrophicationTotals(ef_country)

    def eutrophication_livestock_past(self, baseline_animals, baseline_farms):
        baseline_index = self.common_class.baseline_index
        kg_to_kt = self.common_class.kg_to_kt

        eutrophication_dict = (
            self.cattle_eutrophication_class.create_emissions_dictionary(
                [baseline_index]
            )
        )

        baseline_animals = load_livestock_data(baseline_animals)
        baseline_farms = load_farm_data(baseline_farms)

        past_farm_loc = list(baseline_farms.keys())[0]
        past_animals_loc = list(baseline_animals.keys())[0]

        eutrophication_dict["manure_management"][baseline_index] += (
            self.cattle_eutrophication_class.total_manure_NH3_EP(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        eutrophication_dict["soils"][baseline_index] += (
            self.cattle_eutrophication_class.total_fertilser_soils_EP(
                baseline_farms[past_farm_loc].total_urea,
                baseline_farms[past_farm_loc].total_urea_abated,
                baseline_farms[past_farm_loc].total_n_fert,
                baseline_farms[past_farm_loc].total_p_fert,
            )
            * kg_to_kt
        )
        eutrophication_dict["soils"][baseline_index] += (
            self.cattle_eutrophication_class.total_grazing_soils_EP(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        # Past Sheep
        eutrophication_dict["manure_management"][baseline_index] += (
            self.sheep_eutrophication_class.total_manure_NH3_EP(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )
        eutrophication_dict["soils"][baseline_index] += (
            self.sheep_eutrophication_class.total_grazing_soils_EP(
                baseline_animals[past_animals_loc]["animals"],
            )
            * kg_to_kt
        )

        return eutrophication_dict

    def eutrophication_livestock_future(self, scenario_animals, scenario_farms):
        scenario_animals_dataframe = scenario_animals
        index = [int(i) for i in scenario_animals_dataframe.Scenarios.unique()]

        scenario_animals = load_livestock_data(scenario_animals)
        scenario_farms = load_farm_data(scenario_farms)

        kg_to_kt = self.common_class.kg_to_kt

        # create emissions dictionary

        eutrophication_dict = (
            self.cattle_eutrophication_class.create_emissions_dictionary(index)
        )

        for sc in index:
            for farm_id in scenario_animals_dataframe.farm_id[
                scenario_animals_dataframe["Scenarios"] == sc
            ].unique():
                eutrophication_dict["manure_management"][sc] += (
                    self.cattle_eutrophication_class.total_manure_NH3_EP(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )

                eutrophication_dict["soils"][sc] += (
                    self.cattle_eutrophication_class.total_grazing_soils_EP(
                        scenario_animals[farm_id]["animals"],
                    )
                    * kg_to_kt
                )

                eutrophication_dict["manure_management"][sc] += (
                    self.sheep_eutrophication_class.total_manure_NH3_EP(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )
                eutrophication_dict["soils"][sc] += (
                    self.sheep_eutrophication_class.total_grazing_soils_EP(
                        scenario_animals[farm_id]["animals"]
                    )
                    * kg_to_kt
                )

            eutrophication_dict["soils"][sc] += (
                self.cattle_eutrophication_class.total_fertilser_soils_EP(
                    scenario_farms[sc].total_urea,
                    scenario_farms[sc].total_urea_abated,
                    scenario_farms[sc].total_n_fert,
                    scenario_farms[sc].total_p_fert,
                )
                * kg_to_kt
            )

        return eutrophication_dict

    def eutrophication_livestock_dissagregated(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        past_data = pd.DataFrame.from_dict(
            self.eutrophication_livestock_past(baseline_animals, baseline_farms)
        )

        future_data = pd.DataFrame.from_dict(
            self.eutrophication_livestock_future(scenario_animals, scenario_farms)
        )

        return pd.concat([past_data, future_data])


class AirQualityLivestock:
    def __init__(self, ef_country):
        self.common_class = CommonParams()
        self.cattle_air_quality_class = CattleAirQualityTotals(ef_country)
        self.sheep_air_quality_class = SheepAirQualityTotals(ef_country)

    def air_quality_livestock_past(self, baseline_animals, baseline_farms):
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
                baseline_farms[past_farm_loc].total_urea,
                baseline_farms[past_farm_loc].total_urea_abated,
                baseline_farms[past_farm_loc].total_n_fert,
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
            )
            * kg_to_kt
        )

        return ammonia_dict

    def air_quality_livestock_future(self, scenario_animals, scenario_farms):
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
                    scenario_farms[sc].total_urea,
                    scenario_farms[sc].total_urea_abated,
                    scenario_farms[sc].total_n_fert,
                )
                * kg_to_kt
            )

        return ammonia_dict

    def air_quality_livestock_dissagregated(
        self, baseline_animals, scenario_animals, baseline_farms, scenario_farms
    ):
        past_data = pd.DataFrame.from_dict(
            self.air_quality_livestock_past(baseline_animals, baseline_farms)
        )

        future_data = pd.DataFrame.from_dict(
            self.air_quality_livestock_future(scenario_animals, scenario_farms)
        )

        return pd.concat([past_data, future_data])


class ClimateChangeCrop:
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
        baseline_index = self.common_class.baseline_index
        # base = self.baseline
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
        dissagregated_crop_emissions = self.climate_change_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        emissions_groups = (
            self.goblin_data_manager_class.climate_change_crops_emissions_groups
        )

        AR_values = self.goblin_data_manager_class.AR_values

        conversion_groups = (
            self.goblin_data_manager_class.climate_change_crop_conversion_groups
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
        AR_values = self.goblin_data_manager_class.AR_values

        dissagregated_crop_emissions = self.climate_change_crops_dissagregated(
            crop_dataframe, scenario_dataframe
        )

        emissions_groups = (
            self.goblin_data_manager_class.climate_change_crops_emissions_groups
        )

        AR_values = self.goblin_data_manager_class.AR_values

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


class EurtrophicationCrop:
    def __init__(self, ef_country, default_urea=None, default_urea_abated=None):
        self.common_class = CommonParams()
        self.ef_country = ef_country

        self.crop_etrophication_class = CropEutrophicationTotals(ef_country)

        self.default_urea_proportion = default_urea
        self.default_urea_abated_porpotion = default_urea_abated

    def eutrophication_crops_past(self, crop_dataframe):
        baseline_index = self.common_class.baseline_index
        # base = self.baseline
        kg_to_kt = self.common_class.kg_to_kt

        crop_eutrophication_dict = (
            self.crop_etrophication_class.create_emissions_dictionary([baseline_index])
        )

        data_frame = pd.DataFrame(crop_dataframe)

        # proportion of fertiliser inputs that is urea
        urea_proportion = self.default_urea_proportion
        urea_abated_proportion = self.default_urea_abated_porpotion
        # generate results and store them in the dictionary

        data = load_crop_farm_data(data_frame)

        base = list(data.keys())[0]

        crop_eutrophication_dict["soils"][baseline_index] += (
            self.crop_etrophication_class.total_soils_EP(
                data[base], urea_proportion, urea_abated_proportion
            )
        ) * kg_to_kt

        return crop_eutrophication_dict

    def eutrophication_crops_future(self, crop_dataframe, scenario_dataframe):
        kg_to_kt = self.common_class.kg_to_kt

        data_frame = pd.DataFrame(crop_dataframe)

        urea_data = scenario_dataframe[
            ["Scenarios", "Urea proportion", "Urea abated proportion"]
        ].drop_duplicates()

        scenarios = list(urea_data["Scenarios"].values)

        crop_eutrophication_dict = (
            self.crop_etrophication_class.create_emissions_dictionary(scenarios)
        )

        data = load_crop_farm_data(data_frame)

        for sc in scenarios:
            mask = urea_data["Scenarios"] == sc
            urea_proportion = urea_data.loc[mask, "Urea proportion"].item()
            urea_abated_proportion = urea_data.loc[
                mask, "Urea abated proportion"
            ].item()

            crop_eutrophication_dict["soils"][sc] += (
                self.crop_etrophication_class.total_soils_EP(
                    data[sc], urea_proportion, urea_abated_proportion
                )
            ) * kg_to_kt

        return crop_eutrophication_dict

    def eutrophication_crops_dissagregated(self, crop_dataframe, scenario_dataframe):
        past_data = pd.DataFrame.from_dict(
            self.eutrophication_crops_past(crop_dataframe)
        )

        future_data = pd.DataFrame.from_dict(
            self.eutrophication_crops_future(crop_dataframe, scenario_dataframe)
        )

        return pd.concat([past_data, future_data])


class AirQualityCrop:
    def __init__(self, ef_country, default_urea=None, default_urea_abated=None):
        self.common_class = CommonParams()
        self.ef_country = ef_country

        self.crop_air_quality_class = CropAirQualityTotals(ef_country)

        self.default_urea_proportion = default_urea
        self.default_urea_abated_porpotion = default_urea_abated

    def air_quality_crops_past(self, crop_dataframe):
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
        past_data = pd.DataFrame.from_dict(self.air_quality_crops_past(crop_dataframe))

        future_data = pd.DataFrame.from_dict(
            self.air_quality_crops_future(crop_dataframe, scenario_dataframe)
        )

        return pd.concat([past_data, future_data])


class ClimateChangeTotal:
    def __init__(self):
        self.common_class = CommonParams()

    def total_climate_change_emissions(
        self, calibration_year, target_year, scenario_dataframe, dataframe_dict
    ):
        baseline_index = self.common_class.baseline_index

        animal_data = dataframe_dict["animal"]
        crop_data = dataframe_dict["crop"]
        land_use_data = dataframe_dict["land"]

        total_climate_change_emissions_dataframe = animal_data.copy(deep=True)

        land_use_dataframe = land_use_data.copy(deep=True)

        crop_dataframe = crop_data.copy(deep=True)

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
                ] += crop_dataframe.loc[sc, gas].item()
                total_climate_change_emissions_dataframe.loc[
                    sc, gas
                ] += land_use_dataframe.loc[land_mask, gas].item()

        return total_climate_change_emissions_dataframe


class EutrophicationTotal:
    def __init__(self):
        self.common_class = CommonParams()

    def total_eutrophication_emissions(self, scenario_dataframe, dataframe_dict):
        baseline_index = self.common_class.baseline_index

        livestock_data = dataframe_dict["animal"]
        crop_data = dataframe_dict["crop"]

        total_livestock_and_crop_eutrophication_emissions = livestock_data.copy(
            deep=True
        )

        crop_eutrophication_emissions = crop_data.copy(deep=True)

        scenario_list = [baseline_index]
        scenario_list.extend(list(scenario_dataframe["Scenarios"].unique()))

        for sc in scenario_list:
            for category in total_livestock_and_crop_eutrophication_emissions.columns:
                if category in crop_eutrophication_emissions.columns:
                    # try:
                    total_livestock_and_crop_eutrophication_emissions.loc[
                        sc, category
                    ] += crop_eutrophication_emissions.loc[sc, category]

        total_livestock_and_crop_eutrophication_emissions[
            "Total"
        ] = total_livestock_and_crop_eutrophication_emissions.sum(axis=1)

        return total_livestock_and_crop_eutrophication_emissions


class AirQualityTotal:
    def __init__(self):
        self.common_class = CommonParams()

    def total_air_quality_emissions(self, scenario_dataframe, dataframe_dict):
        baseline_index = self.common_class.baseline_index

        livestock_data = dataframe_dict["animal"]
        crop_data = dataframe_dict["crop"]

        total_animal_and_crop_air_quality_emissions = livestock_data.copy(deep=True)
        crop_air_quality_emissions = crop_data.copy(deep=True)

        scenario_list = [baseline_index]
        scenario_list.extend(list(scenario_dataframe["Scenarios"].unique()))

        for sc in scenario_list:
            for category in total_animal_and_crop_air_quality_emissions.columns:
                if category in crop_air_quality_emissions.columns:
                    total_animal_and_crop_air_quality_emissions.loc[
                        sc, category
                    ] += crop_air_quality_emissions.loc[sc, category]

        total_animal_and_crop_air_quality_emissions[
            "Total"
        ] = total_animal_and_crop_air_quality_emissions.sum(axis=1)

        return total_animal_and_crop_air_quality_emissions
