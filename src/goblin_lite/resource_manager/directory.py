import os 
from cbm_runner.resource_manager.paths import Paths


class Directories:
    def __init__(self, path, gen_baseline = True, gen_validation = False):
        self.path = path
        self.paths_class = Paths(path, gen_baseline, gen_validation)
       

    def create_database_directory(self):
        os.makedirs(self.path, exist_ok=True)

    def create_cbm_directory(self):
         self.paths_class.setup_runner_paths(self.path)


    def cbm_generated_input_directories(self, scenarios):
        generated_input_cbm_dir  = self.paths_class.get_generated_input_data_path()

        os.makedirs(os.path.join(generated_input_cbm_dir,"-1"), exist_ok=True)

        for sc in range(scenarios):
            os.makedirs(os.path.join(generated_input_cbm_dir,str(sc)), exist_ok=True)


    def create_goblin_directory_strucutre(self, scenarios):
        self.create_database_directory()
        self.create_cbm_directory()
        self.cbm_generated_input_directories(scenarios)