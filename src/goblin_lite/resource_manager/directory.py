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

    def create_goblin_directory_strucutre(self):
        self.create_database_directory()
        self.create_cbm_directory()