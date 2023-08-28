from modules.Analyzer import Analyzer

class Tester():
    def __init__(self) -> None:
        self.__analyzer = Analyzer()
    def run(self, data_in, data_out_t, data_out_e) -> bool:

        tokens, errors = self.__analyzer.run(data_in)
        i = 0
        incorrect = False
        if len(tokens) == len(data_out_t):
            for t in tokens:
                if t != data_out_t[i]:
                    print("token incorreto")
                    print(f"    Esperado: {data_out_t[i]}")
                    print(f"    recebido: {tokens[i]}")
                    incorrect = True
                i += 1
        else:
            print(f"""{"Mais" if len(tokens) > len(data_out_t) else "Menos"} tokens do que o esperado.""")
            print(f"Quantidade de tokens esperados: {len(data_out_t)}")
            print("\n".join(data_out_t))
            print(f"Quantidade de tokens recebidos: {len(tokens)}")
            print("\n".join(tokens))
            incorrect = True
        if len(errors) == len(data_out_e):
            i = 0
            for e in errors:
                if e != data_out_e[i]:
                    print("erro incorreto")
                    print(f"    Esperado: {data_out_e[i]}")
                    print(f"    recebido: {errors[i]}")
                    incorrect = True
                i += 1
        else:
            print(f"""{"Mais" if len(errors) > len(data_out_e) else "Menos"} erros do que o esperado.""")
            print(f"Quantidade de erros esperados: {len(data_out_e)}")
            print("\n".join(data_out_e))
            print(f"Quantidade de erros recebidos: {len(errors)}")
            print("\n".join(errors))

            incorrect = True

        return not incorrect

