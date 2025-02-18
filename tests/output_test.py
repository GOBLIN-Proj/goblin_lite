import unittest
import os
from goblin_lite.goblin import ScenarioRunner
from goblin_lite.resource_manager.goblin_data_manager import GoblinDataManager
from goblin_lite.resource_manager.data_fetcher import DataFetcher
import pandas as pd
import numpy as np

class TestOutput(unittest.TestCase):
    def setUp(self):
        self.goblin_config = "./data/config.json"
        self.cbm_config = "./data/cbm_factory.yaml"
        self.ef_country = "ireland"
        self.baseline_year = 2020
        self.target_year = 2050

        self.test_data_path = "./data/output_test/"

        self.test_data = pd.read_csv(os.path.join(self.test_data_path, "climate_change_totals.csv"), index_col=0)
        
        # create goblin data manager
        goblin_data_manger = GoblinDataManager(
            ef_country = self.ef_country,
            calibration_year= self.baseline_year,
            target_year= self.target_year,
            configuration_path= self.goblin_config,
            cbm_configuration_path= self.cbm_config,
        )

            # Run the scenarios
        runner_class = ScenarioRunner(
            goblin_data_manger
        )
        runner_class.run_scenarios()

        # Initialize the fetch class
        self.fetch_class = DataFetcher()

        self.generated_data = self.fetch_class.get_climate_change_emission_totals()


    def test_output_percentage_difference(self):
        for col in self.generated_data.columns:
            for i in self.generated_data.index:
                generated_val = self.generated_data.loc[i, col]
                test_val = self.test_data.loc[i, col]
                # Calculate the absolute percentage difference
                percentage_diff = np.abs((generated_val - test_val) / test_val) * 100
                
                print(f"Generated value for {col} at index {i}: {generated_val}")
                print(f"Test value for {col} at index {i}: {test_val}")
                print(f"Percentage difference for {col} at index {i}: {percentage_diff}")
                print("\n")

                # Assert that the difference is within 5%
                self.assertTrue(percentage_diff <= 5, f"{col} values for index {i} are not within 5% of the test data")

                
if __name__ == "__main__":
    unittest.main()
