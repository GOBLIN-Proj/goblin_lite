from goblin_lite.resource_manager.data_fetcher import DataFetcher
import os 

def main():
    
    DATABASE ="./data/DATABASE/instance_1.db"
    fetcher_class = DataFetcher(DATABASE)
    
    os.makedirs("fetch_test_data")

    _data_path = "./fetch_test_data/"

    fetcher_class.dump_tables(_data_path)

    for filename in os.listdir(_data_path):
        file_path = os.path.join(_data_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)

    os.rmdir(_data_path)

if __name__ == "__main__":
    main()