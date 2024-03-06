from goblin_lite.resource_manager.data_fetcher import DataFetcher
import os 

def main():
    fetcher_class = DataFetcher()
    
    os.makedirs("fetch_test_data")

    _data_path = "./fetch_test_data/"

    fetcher_class.get_air_quality_animal_emissions_by_category().to_csv(os.path.join(_data_path, "air_quality_animal_emissions.csv")) #1
    fetcher_class.get_air_quality_crop_emissions_by_category().to_csv(os.path.join(_data_path, "air_quality_crop_emissions.csv")) #2
    fetcher_class.get_air_quality_emission_totals().to_csv(os.path.join(_data_path, "air_quality_emissions_totals.csv")) #3


    fetcher_class.get_climate_change_animal_emissions_aggregated().to_csv(os.path.join(_data_path, "climate_change_animal_emissions_aggregated.csv")) #4
    fetcher_class.get_climate_change_crop_emissions_aggregated().to_csv(os.path.join(_data_path, "climate_change_crop_emissions_aggregated.csv")) #5
    fetcher_class.get_climate_change_emission_totals().to_csv(os.path.join(_data_path, "climate_change_emissions_totals.csv")) #6
    fetcher_class.get_climate_change_animal_emissions_by_category().to_csv(os.path.join(_data_path, "climate_change_animal_emissions_by_category.csv")) #7
    fetcher_class.get_climate_change_crop_emissions_by_category().to_csv(os.path.join(_data_path, "climate_change_crop_emissions_by_category.csv")) #8


    fetcher_class.get_crop_national_inputs().to_csv(os.path.join(_data_path, "crop_catchment_inputs.csv")) #9
    fetcher_class.get_crop_emissions_by_category_co2e().to_csv(os.path.join(_data_path, "crop_emissions_by_category_co2e.csv")) # 10
    fetcher_class.get_crop_farm_input_applied().to_csv(os.path.join(_data_path, "crop_farm_input_applied.csv")) #11


    fetcher_class.get_eutrophication_emission_totals().to_csv(os.path.join(_data_path, "eutrophication_emission_totals.csv")) #12
    fetcher_class.get_eutrophication_crop_emissions_by_category().to_csv(os.path.join(_data_path, "eutrophication_crop_emissions_by_category.csv")) #13
    fetcher_class.get_eutrophication_animal_emissions_by_category().to_csv(os.path.join(_data_path, "eutrophication_animal_emissions_by_category.csv")) #14


    fetcher_class.get_baseline_livestock_data().to_csv(os.path.join(_data_path, "baseline_livestock_data.csv")) #15
    fetcher_class.get_scenario_livestock_data().to_csv(os.path.join(_data_path, "scenario_livestock_data.csv")) #16
    fetcher_class.get_livestock_output_summary().to_csv(os.path.join(_data_path, "livestock_output_summary.csv")) #17

    fetcher_class.get_landuse_areas().to_csv(os.path.join(_data_path, "landuse_areas.csv")) #18
    fetcher_class.get_landuse_emissions_totals().to_csv(os.path.join(_data_path, "landuse_emissions_totals.csv")) #19

    fetcher_class.get_total_afforested().to_csv(os.path.join(_data_path, "total_afforested.csv")) #20
    fetcher_class.get_total_grassland_area().to_csv(os.path.join(_data_path, "total_grassland_area.csv")) #21
    fetcher_class.get_transition_matrix().to_csv(os.path.join(_data_path, "transition_matrix.csv")) #22

    fetcher_class.get_grassland_spared_area_by_soil_group().to_csv(os.path.join(_data_path, "grassland_spared_area_by_soil_group.csv")) #23
    fetcher_class.get_grassland_scenario_farm_inputs().to_csv(os.path.join(_data_path, "grassland_scenario_farm_inputs.csv")) #24
    fetcher_class.get_grassland_baseline_farm_inputs().to_csv(os.path.join(_data_path, "grassland_baseline_farm_inputs.csv")) #25 


    fetcher_class.get_scenario_inputs().to_csv(os.path.join(_data_path, "scenario_inputs.csv")) #26
    fetcher_class.get_stocking_rate_per_ha().to_csv(os.path.join(_data_path, "stocking_rate_per_ha.csv")) #27



    fetcher_class.get_forest_aggregate().to_csv(os.path.join(_data_path, "forest_aggregate.csv")) #28
    fetcher_class.get_forest_flux().to_csv(os.path.join(_data_path, "forest_flux.csv")) #29

    fetcher_class.get_total_spared_area().to_csv(os.path.join(_data_path, "total_spared_area.csv")) #30

    fetcher_class.get_animal_emissions_by_category_co2e().to_csv(os.path.join(_data_path, "animal_emissions_by_category_co2e.csv")) #31

    for filename in os.listdir(_data_path):
        file_path = os.path.join(_data_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)

    os.rmdir(_data_path)

if __name__ == "__main__":
    main()