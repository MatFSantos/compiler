from src.modules.SaveFile import SaveFile
from src.modules.GetFile import GetFile
from src.modules.GetContent import GetContent
from src.modules.Lexicon import Lexicon
from src.modules.SyntacticSemantic import SyntacticSemantic
import sys

params = sys.argv
try:
	index_name = params.index('--name')
except:
	index_name = 0

if	(index_name > 0 and not (
	(
		('--lexico' in params or '-l' in params)
		and
		('--syntactic' not in params or '-sy' not in params)
	) or (
		('--lexico' not in params or '-l' not in params)
		and
		('--syntactic' in params or '-sy' in params)
	)
)):
	raise ValueError("Parametro --name exige que indique qual analisador irá usar")
if __name__ == "__main__":
	ROOT_DIR = "./files/"

	if len(params) <= 1 or '--lexico' in params or '-l' in params:
		print("Running lexical analyser...")
		if index_name >= 1:
			content = GetContent(root_directory=ROOT_DIR).run(params[index_name + 1])
			if content == "":
				print(f"Nenhum conteudo no arquivo '{ROOT_DIR + params[index_name + 1]}'")
			else:
				try:
					tokens, errors = Lexicon().run(content)
				except Exception as e:
					print(f"An error was occurred while tokenize the content: {e}")
				SaveFile(concat_name="-lexico-saida.txt", root_directory=ROOT_DIR).run(filename=params[index_name + 1], tokens=tokens, errors=errors)
		else:
			files = GetFile(is_lexicon=True, root_directory=ROOT_DIR).run()
			if not files:
				print(f"An error was occurred while getting files in '{ROOT_DIR}'")
			elif len(files) > 0:
				for file in files:
					content = GetContent(root_directory=ROOT_DIR).run(file)
					if content == "":
						print(f"Nenhum conteudo no arquivo '{ROOT_DIR + file}'")
					else:
						try:
							tokens, errors = Lexicon().run(content)
						except Exception as e:
							print(f"An error was occurred while tokenize the content: {e}")
						SaveFile(concat_name="-lexico-saida.txt", root_directory=ROOT_DIR).run(filename=file, tokens=tokens, errors=errors)			
			else:
				print(f"Nenhum arquivo encontrado na pasta raíz '{ROOT_DIR}'")
		print("Finished.")
	if len(params) <= 1 or '--syntactic' in params or '-sy' in params:
		print("Running syntactical analyser...")
		if index_name >= 1:
			content = GetContent(root_directory=ROOT_DIR).run(filename=params[index_name + 1])
			if content == "":
				print(f"Nenhum conteudo no arquivo '{ROOT_DIR + params[index_name + 1]}'")
			else:
				try:
					errors, erros_sem = SyntacticSemantic(string_tokens=content).run()
					for e in errors:
						print(e)
					if len(errors) == 0:
						print('Sem erros sintáticos')
					for e in erros_sem:
						print(e)
					if len(erros_sem) == 0:
						print('Sem erros semânticos')
				except Exception as e:
					print(f"An error was occurred while tokenize the content: {e}")
				SaveFile(concat_name='-sintatico-saida.txt').run(filename=params[index_name + 1].replace("-lexico-saida", ""),tokens=content.splitlines(), errors=errors)
				SaveFile(concat_name='-semantico-saida.txt').run(filename=params[index_name + 1].replace("-lexico-saida", ""),tokens=content.splitlines(), errors=erros_sem)
		else:
			files = GetFile(is_lexicon=False, root_directory=ROOT_DIR).run()
			for file in files:
				content = GetContent(root_directory=ROOT_DIR).run(filename=file)
				if content == "":
					print(f"Nenhum conteudo no arquivo '{ROOT_DIR + file}'")
				else:
					try:
						errors, erros_sem = SyntacticSemantic(string_tokens=content).run()
						for e in errors:
							print(f"\nErros sintáticos no arquivo '{ROOT_DIR + file}:'")
							print(e)
						if len(errors) == 0:
							print(f"\nSem erros sintáticos no arquivo '{ROOT_DIR + file}'")
						for e in erros_sem:
							print(f"\nErros semânticos no arquivo '{ROOT_DIR + file}:'")
							print(e)
						if len(erros_sem) == 0:
							print(f"\nSem erros semânticos no arquivo '{ROOT_DIR + file}'")
					except Exception as e:
						print(f"An error was occurred while tokenize the content: {e}")
					SaveFile(concat_name='-sintatico-saida.txt').run(filename=file.replace("-lexico-saida", ""),tokens=content.splitlines(), errors=errors)
					SaveFile(concat_name='-semantico-saida.txt').run(filename=file.replace("-lexico-saida", ""),tokens=content.splitlines(), errors=erros_sem)
		print("Finished.")