import os

class GetFile():
    def __init__(self, is_lexicon: bool, root_directory: str = "./files/"):
        self.__root_directory = root_directory
        self.__is_lexicon = is_lexicon
    
    def run(self) -> list[str] | bool:
        try:
            items_in_dir = os.listdir(path=self.__root_directory)
            
            files = []
            for item in items_in_dir:
                if self.__is_lexicon:
                    if os.path.isfile(os.path.join(self.__root_directory, item)) and item.endswith(".txt") and "-lexico-saida.txt" not in item and "-sintatico-saida.txt" not in item:
                        files.append(item)
                else:
                    if os.path.isfile(os.path.join(self.__root_directory, item)) and item.endswith("-lexico-saida.txt"):
                        files.append(item)

        except FileNotFoundError:
            print(f"The directory {self.__root_directory} not found.")
            return False
        except Exception as e:
            print(f"An error was occurred while get the file names:    {e}")
            return False
        return files
