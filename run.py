from modules.SaveFile import SaveFile
from modules.GetFile import GetFile
from modules.GetContent import GetContent
from modules.Analyzer import Analyzer

ROOT_DIR = "./files/"

files = GetFile(ROOT_DIR).run()

if files and len(files) > 0:
	for file in files:
		content = GetContent(ROOT_DIR).run(file)
		if content == "":
			print(f"Nenhum conteudo no arquivo '{ROOT_DIR + file}'")
		else:
			try:
				tokens, errors = Analyzer().run(content)
			except Exception as e:
				print(f"An error was occurred when tokenize the content: {e}")
			SaveFile(ROOT_DIR).run(filename=file, tokens=tokens, errors=errors)
			
else:
	print(f"Nenhum arquivo encontrado na pasta raíz '{ROOT_DIR}'")