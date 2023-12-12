
class SaveFile():
    def __init__(self, concat_name: str = '-saida.txt', root_directory: str = "./files/"):
        self.__concat_name = concat_name
        self.__root_directory = root_directory
    
    def run(self, filename: str, tokens: list[str], errors: list[str]) -> bool:
        try:
            with open(self.__root_directory + filename.replace(".txt", self.__concat_name), "w") as f:
                f.write(tokens[0])
                for t in tokens[1:]:
                    f.write("\n" + t)
                if len(errors) > 0:
                    f.write("\n---------- ERRORS --------")
                elif "sintatico" in self.__concat_name:
                    f.write("\n\nSEM ERROS SINTÁTICOS")
                for e in errors:
                    f.write("\n" + e)
            return True
        except Exception as e:
            print(f"An error was occured while save the file: {e}")
            return False