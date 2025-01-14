from goblin_lite.data_processing.landuse_data_generator import LandUseDataGenerator
import pandas as pd
import os

def main():

    #Data path 
    input_path = "../data/integration/input/"
    output_path = "../data/integration/output/"

    # Load data
    scenario_input_dataframe = pd.read_csv(os.path.join(input_path, "scenario_input_dataframe.csv"))
    total_grassland_area = pd.read_csv(os.path.join(input_path, "total_grassland_area.csv"))
    total_spared_area = pd.read_csv(os.path.join(input_path, "total_spared_area.csv"))
    total_spared_area_by_soil_group = pd.read_csv(os.path.join(input_path, "total_spared_area_by_soil_group.csv"))

    # Configuration
    baseline_year = 2020
    target_year = 2050



    # Land use data
    landuse_data_generator = LandUseDataGenerator(baseline_year, 
                                                  target_year, 
                                                  scenario_input_dataframe, 
                                                  total_grassland_area, 
                                                  total_spared_area, 
                                                  total_spared_area_by_soil_group)

    transition_matrix = landuse_data_generator.generate_transition_matrix()

    landuse_data = landuse_data_generator.generate_landuse_data()

    cbm_afforestation_data = landuse_data_generator.generate_afforestation_data()


    # Save data
    transition_matrix.to_csv(os.path.join(output_path, "transition_matrix.csv"), index=False)
    landuse_data.to_csv(os.path.join(output_path, "landuse_data.csv"), index=False)
    cbm_afforestation_data.to_csv(os.path.join(output_path, "cbm_afforestation_data.csv"), index=False)
    

if __name__ == "__main__":
    main()