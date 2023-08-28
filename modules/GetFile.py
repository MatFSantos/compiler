import os

class GetFile():
    def __init__(self, root_directory: str = "./files/"):
        self.__root_directory = root_directory
    
    def run(self) -> list[str] | bool:
        
        try:
            items_in_dir = os.listdir(path=self.__root_directory)
            files = [
                item for item in items_in_dir
                if os.path.isfile(os.path.join(self.__root_directory, item)) and item.endswith(".txt") and "-saida.txt" not in item
            ]
        except FileNotFoundError:
            print(f"The directory {self.__root_directory} not found.")
            return False
        except Exception as e:
            print(f"An error was occurred when get the file names:    {e}")
            return False
        return files
