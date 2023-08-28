
class SaveFile():
    def __init__(self, root_directory: str = "./files/"):
        self.__root_directory = root_directory
    
    def run(self, filename, tokens, errors) -> bool:
        try:
            with open(self.__root_directory + filename.replace(".txt", "-saida.txt"), "w") as f:
                for t in tokens:
                    f.write(t + "\n")
                if len(errors) > 0:
                    f.write("---------- ERRORS --------")
                for e in errors:
                    f.write(e + "\n")
            return True
        except Exception as e:
            print(f"An error was occured when save the file: {e}")
            return False