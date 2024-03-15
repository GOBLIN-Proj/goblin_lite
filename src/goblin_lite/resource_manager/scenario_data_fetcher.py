"""
Scenario Data Fetcher Documentation
====================================

The ``ScenarioDataFetcher`` class is designed to extract specific pieces of information from a scenario dataset. 

"""
import pandas as pd

class ScenarioDataFetcher:
    """
    The ScenarioDataFetcher class is designed to extract specific pieces of information from a scenario dataset.

    This class provides methods to retrieve various information from a scenario dataset.

    Methods:
        __init__(scenario_data):
            Initializes an instance of the `ScenarioDataFetcher` class.
            
        get_column_index(column_name):
            Retrieves the index of a specified column in the scenario data.
            
        get_afforestation_end_year():
            Retrieves the end year for afforestation activities for a specified scenario.
            
        get_catchment_name():
            Retrieves the name of the catchment area defined in the scenario data.
            
        get_scenario_list():
            Retrieves a list of all scenarios present in the scenario data.
            
        get_afforest_scenario_index():
            Retrieves a list of afforestation scenario indices, with -1 indicating a special scenario, followed by the indices of all available scenarios.

        get_urea_proportions():
            Retrieves the urea proportions for each scenario.

    """
    def __init__(self, scenario_data):
        self.scenario_data = scenario_data
    

    def get_column_index(self, column_name):
        """
        Retrieves the index of a specified column in the scenario data.

        Args:
            column_name (str): The name of the column to retrieve.

        Returns:
            int: The index of the column.
        """
        lower_case_columns = [col.lower() for col in self.scenario_data.columns]
        try:
            column_index = lower_case_columns.index(column_name)
            return column_index
        
        except ValueError:

            return None
        

    def get_afforestation_end_year(self):
        """
        Retrieves the end year for afforestation activities for a specified scenario.

        Returns:
            int: The afforestation end year.
        """
        column_index = self.get_column_index("afforest year")

        matching_column_name = self.scenario_data.columns[column_index]

        return self.scenario_data[matching_column_name].unique().item()
   
    
    def get_catchment_name(self):
        """
        Retrieves the name of the catchment area defined in the scenario data.

        Returns:
            str: The catchment name.
        """
        column_index = self.get_column_index("catchment")
        matching_column_name = self.scenario_data.columns[column_index]

        return self.scenario_data[matching_column_name].unique().item()

    
    def get_scenario_list(self):
        """
        Retrieves a list of all scenarios present in the scenario data.

        Returns:
            list: A list of scenario identifiers.
        """
        column_index = self.get_column_index("scenarios")
        matching_column_name = self.scenario_data.columns[column_index]

        return self.scenario_data[matching_column_name].unique().tolist()
    
    
    def get_total_scenarios(self):
        """
        Retrieves the total number of scenarios present in the scenario data.

        Returns:
            int: The total number of scenarios.
        """
        scenario_list = self.get_scenario_list()

        return len(scenario_list)
    

    def get_scenario_index(self):
        
        """
        Retrieves a list of afforestation scenario indices, with -1 indicating a special scenario,
        followed by the indices of all available scenarios.

        Returns:
            list: A list containing -1 followed by all scenario indices.
        """
        # Create a list with -1 as the first element
        scenarios = [-1]
        # Extend the list with the scenario indices obtained from get_scenario_list method
        scenarios.extend(self.get_scenario_list())
        
        return scenarios
            
    def get_urea_proportions(self):
        """
        Retrieves the urea proportions for each scenario.

        Returns:
           pandas.DataFrame: A DataFrame containing urea proportions for each scenario.
        """
  
        urea_index = self.get_column_index("urea proportion")
        urea_abated_index = self.get_column_index("urea abated proportion")
        scenario_index = self.get_column_index("scenarios")

        urea_column_name = self.scenario_data.columns[urea_index]
        urea_abated_column_name = self.scenario_data.columns[urea_abated_index]
        scenario_column_name = self.scenario_data.columns[scenario_index]

        return self.scenario_data[[scenario_column_name, urea_column_name, urea_abated_column_name]].drop_duplicates()
