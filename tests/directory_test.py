import os 
from goblin_lite.resource_manager.directory import Directories
import shutil

def main():

    os.makedirs("./data/directory_test/", exist_ok=True)

    # class instances
    

    # create directory structure
    for i in range(10):
        os.mkdir(f"./data/directory_test/{i}")
        path = os.path.join("./data/directory_test/", str(i)+"/")

        print(f"Creating directory structure for {path}")
        dir_class = Directories(path)
        dir_class.create_goblin_directory_structure()

    # delete the directory
    shutil.rmtree("./data/directory_test/")

    print("Directory test passed.")

if __name__ == "__main__":
    main()
