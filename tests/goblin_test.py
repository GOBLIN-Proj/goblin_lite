import unittest
import os
import shutil
from goblin_lite.goblin import ScenarioRunner
from goblin_lite.data_grapher import DataGrapher


class TestGoblin(unittest.TestCase):
    def setUp(self):
        self.goblin_config = "./data/config.json"
        self.cbm_config = "./data/cbm_factory.yaml"
        self.ef_country = "ireland"
        self.baseline_year = 2020
        self.target_year = 2050
        self.data_path = "./temp_data"

        # Create the temp_data directory if it doesn't exist
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # Run the scenarios
        runner_class = ScenarioRunner(
            self.ef_country,
            self.baseline_year,
            self.target_year,
            self.goblin_config,
            self.cbm_config,
        )
        runner_class.run_scenarios()

        # Initialize the graph class
        self.graph_class = DataGrapher()

    def tearDown(self):
        # Clean up the output path after each test
        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)

    def test_output_files_exist(self):
        # Call all the graphing methods
        self.graph_class.plot_animal_lca_emissions_by_category(self.data_path)
        self.graph_class.plot_land_use_emissions(self.data_path)
        self.graph_class.plot_forest_flux(self.data_path, detail=True)
        self.graph_class.plot_forest_aggregate(self.data_path)
        self.graph_class.plot_forest_flux_subplot(self.data_path)
        self.graph_class.plot_crop_lca_emissions_by_category(self.data_path)
        self.graph_class.plot_crop_livestock_lca_emissions_by_category(self.data_path)

        target = 0.02
        gas = "CO2e"

        self.graph_class.rank_chart(target, gas, self.data_path)

        # List all files in the data_path directory
        files_in_directory = os.listdir(self.data_path)

        # List all the expected files you want to check for existence
        expected_files = [
            "climate_change_land_use.png",
            "Crop_and_Livestock_LCA.png",
            "forest_carbon_flux.png",
            "forest_carbon_aggregate.png",
            "forest_flux_subplot.png",
            "Crop_LCA.png",
            "Livestock_LCA.png",
            "scenario_rank_chart.png",
        ]

        # Check if all expected files are present in the directory
        for expected_file in expected_files:
            self.assertIn(expected_file, files_in_directory)


if __name__ == "__main__":
    unittest.main()
