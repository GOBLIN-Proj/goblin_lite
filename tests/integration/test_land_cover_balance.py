from goblin_lite.data_processing.landuse_data_generator import LandUseDataGenerator
import pandas as pd
import os

def test_landcover_balance():
    # Define paths
    input_path = os.path.abspath("../data/integration/input/")
    output_path = os.path.abspath("../data/integration/output/")

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

    rows = []

    # Identify the baseline scenario (assuming it's the first one in transition_matrix.index)
    baseline_scenario = transition_matrix.index[0]

    # Fetch baseline values for farmable_condition, forest, and wetland
    baseline_farmable_condition = landuse_data.loc[
        (landuse_data["farm_id"] == baseline_scenario) & (landuse_data["land_use"] == "farmable_condition"), 
        "area_ha"
    ].item()

    baseline_forest = landuse_data.loc[
        (landuse_data["farm_id"] == baseline_scenario) & (landuse_data["land_use"] == "forest"), 
        "area_ha"
    ].item()

    baseline_wetland = landuse_data.loc[
        (landuse_data["farm_id"] == baseline_scenario) & (landuse_data["land_use"] == "wetland"), 
        "area_ha"
    ].item()

    # Loop through scenarios
    for sc in transition_matrix.index.unique()[1:]:

        # Calculate adjusted areas (absolute difference from baseline)
        farmable_condition_area = abs(
            landuse_data.loc[
                (landuse_data["farm_id"] == sc) & (landuse_data["land_use"] == "farmable_condition"), 
                "area_ha"
            ].item() - baseline_farmable_condition
        )

        forest_area = abs(
            landuse_data.loc[
                (landuse_data["farm_id"] == sc) & (landuse_data["land_use"] == "forest"), 
                "area_ha"
            ].item() - baseline_forest
        )

        wetland_area = abs(
            landuse_data.loc[
                (landuse_data["farm_id"] == sc) & (landuse_data["land_use"] == "wetland"), 
                "area_ha"
            ].item() - baseline_wetland
        )

        # Create the row
        row = {
            "scenario": sc,
            "transition_area": abs(transition_matrix.loc[sc, "Grassland_to_Grassland"]),
            "farmable_condition_area": farmable_condition_area,
            "forest_area": forest_area,
            "wetland_area": wetland_area,
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    for sc in df["scenario"].unique():
        transition_area = df.loc[sc, "transition_area"].item()
        total_land_use_area = df.loc[sc,["farmable_condition_area", "forest_area", "wetland_area"]].sum()
        assert transition_area == total_land_use_area, f"Transition area mismatch for scenario {sc}: {transition_area} != {total_land_use_area}"


if __name__ == "__main__":
    test_landcover_balance()