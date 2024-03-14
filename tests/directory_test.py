import os 
from goblin_lite.resource_manager.directory import Directories

def main():

    os.makedirs("./data/directory_test/", exist_ok=True)

    # class instances
    dir_class = Directories("./data/directory_test/", gen_baseline=True, gen_validation=False)

    # create directory structure
    dir_class.create_goblin_directory_strucutre(10)

if __name__ == "__main__":
    main()
