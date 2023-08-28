
class GetContent():
    def __init__(self, root_directory: str = "./files/"):
        self.__root_directory = root_directory
    
    def run(self, filename: str) -> str:
        content = ""
        try:
            with open(self.__root_directory + filename, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"An error was occurred when get the file content: {e}")
        finally:
            return content