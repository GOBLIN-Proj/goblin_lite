"""
Directories Module
==================
This module is used to create the directory structure for the CBM-Runner model. This is primarily
used to create the directory structure for the SIT when attempting concurrent runs of the model.
"""
import os 
from goblin_cbm_runner.resource_manager.paths import Paths


class Directories:
    """
    Directories class is used to create the directory structure for the CBM-Runner model. This is primarily
    used to create the directory structure for the SIT when attempting concurrent runs of the model.

    Args:
    -----
    path: str
        The path to the directory where the directory structure will be created.

    Attributes:
    -----------
    path: str
        The path to the directory where the directory structure will be created.
    paths_class: Paths
        An instance of the Paths class from the cbm_runner package.

    Methods:
    --------
    create_database_directory(self):
        Create the directory for the database.

    create_cbm_directory(self):
        Create the directory for the CBM-Runner model.
    
    cbm_generated_input_directories(self, scenarios):
        Create the directory for the generated input data for the CBM-Runner model.

    create_goblin_directory_strucutre(self, scenarios):
        Create the directory structure for the CBM-Runner model.

    """
    def __init__(self, path):
        self.path = os.path.dirname(path)
        self.paths_class = Paths(path, gen_baseline=True)
       

    def create_database_directory(self):
        """
        Create the directory for the database.

        Args:
        -----
        None

        Returns:
        --------
        None
        """
        os.makedirs(self.path, exist_ok=True)

    def create_cbm_directory(self):
        """
        Create the directory for the CBM-Runner model.

        Args:
        -----
        None

        Returns:
        --------
        None
        """
        self.paths_class.setup_runner_paths(self.path)


    def cbm_generated_input_directories(self, scenarios):
        """
        Create the directory for the generated input data for the CBM-Runner model.

        Args:
        -----
        scenarios: int
            The number of scenarios to create directories for.

        Returns:
        --------
        None
        """
        generated_input_cbm_dir  = self.paths_class.get_generated_input_data_path()

        os.makedirs(os.path.join(generated_input_cbm_dir,"-1"), exist_ok=True)

        for sc in range(scenarios):
            os.makedirs(os.path.join(generated_input_cbm_dir,str(sc)), exist_ok=True)


    def create_goblin_directory_structure(self):
        """
        Create the directory structure for the CBM-Runner model.

        Args:
        -----
        scenarios: int
            The number of scenarios to create directories for.
        """
        self.create_database_directory()
        self.create_cbm_directory()

        #goblin_cbm_runner creates these directories
        #self.cbm_generated_input_directories(scenarios)