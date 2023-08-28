from tests.modules.AnalyzerTest import Tester as AnalyzerTester
from tests.mock.dataIn import DataIn
from tests.mock.dataOut import token_out, errors_out

####################################################
# teste do Analyzer:
analyzerTester = AnalyzerTester()
i = 0
error = False
for data in DataIn:
    if data != "":
        if not analyzerTester.run(data_in=data, data_out_e=errors_out[i], data_out_t=token_out[i]):
            print(f"Teste {i + 1} concluido com erros")
            error = True
            break
    i += 1
if not error:
    print("Todos os testes do analizador passaram com sucesso")
