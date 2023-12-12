import re

class Lexicon():
    def __init__(self):
        self.__regex_letter = r'[a-zA-Z]'
        self.__regex_number = r'[0-9]'
        self.__regex_symbol = r'(?![A-Za-z0-9"])[ -~]'
        self.__regex_not_a_symbol = r'[^\x00-\x7E]'
        self.__reserved_words = [
            "variables", "const", "class", "methods", "objects", "main",
            "return", "if", "else", "then", "for", "read", "print", "void",
            "int", "real", "boolean", "string", "true", "false", "extends",
            "this", "constructor"
        ]
        self.__separators = ['\n', ';', ',', '.', '(', ')', '[', ']', '{', '}', '-', '+', '*', '/', '!', '=', '<', '>', '&', '|', ' ', '"']
        self.__delimiters = [';', ',', '.', '(', ')', '[', ']', '{', '}']
        self.__aritmetic = ['+', '-', '*', '/']
        self.__logical = ['|', '&', '!']
        self.__relational = ['=', '<', '>', '!']
    def run(self, content: str)-> (list[str], list[str]):
        tokens = []     # lista de tokens
        erros = []      # lista de erros
        lexeme = ""     # palavra analisada
        i = 0           # contador de caracteres
        line = 1        # contador de linhas
        length = len(content)   # quantidade de caracteres dos arquivos
        content = content.replace('\t', ' ') # adiciona espaço no lugar de tabulações


        while i < length:
            # identificador / palavra reservada
            if re.match(self.__regex_letter, content[i]):
                lexeme = content[i]
                i += 1
                valid_id = True
                stop = False
                while i < length and (content[i] not in self.__separators or content[i] in ['&', '|']) and not stop:
                    if content[i] == '&' or content[i] == '|':
                        if i + 1 < length:
                            if content[i] == content[i + 1]:
                                stop = True
                            else:
                                valid_id = False
                        else:
                            valid_id = False
                    if (re.match(self.__regex_symbol, content[i]) and not stop and content[i] != '_') or re.match(self.__regex_not_a_symbol, content[i]):
                        valid_id = False
                    lexeme += content[i]
                    i += 1
                
                if valid_id:
                    if lexeme in self.__reserved_words:
                        tokens.append(f'{line} <PRE, {lexeme}>')
                    else:
                        tokens.append(f'{line} <IDE, {lexeme}>')
                else:
                    erros.append(f'{line} <IMF, {lexeme}>')
                i -= 1
            # numeros
            elif re.match(self.__regex_number, content[i]):
                lexeme = content[i]
                i += 1
                valid_number = True
                stop = False
                while i < length and (content[i] not in self.__separators or content[i] in [ '&', '|']) and not stop:
                    if content[i] == '&' or content[i] == '|':
                        if i + 1 < length:
                            if content[i] == content[i + 1]:
                                stop = True
                            else:
                                valid_number = False
                        else:
                            valid_number = False
                    if not re.match(self.__regex_number, content[i]) and not stop:
                        valid_number = False
                    lexeme += content[i]
                    i += 1
                
                if i < length and content[i] == '.':
                    lexeme += content[i]
                    i += 1
                    if i < length:
                        if re.match(self.__regex_number, content[i]) and valid_number:
                            valid_number = True
                        else:
                            valid_number = False
                        
                        lexeme += content[i]
                        i += 1
                        while i < length and (content[i] not in self.__separators or content[i] in ['.' ,'&', '|']) and not stop:
                            if content[i] == '&' or content[i] == '|':
                                if i + 1 < length:
                                    if content[i] == content[i + 1]:
                                        stop = True
                                    else:
                                        valid_number = False
                                else:
                                    valid_number = False
                            if not re.match(self.__regex_number, content[i]) and not stop:
                                valid_number = False
                            lexeme += content[i]
                            i += 1
                    else:
                        erros.append(f"{line} <NMF, {lexeme}>")
                
                if valid_number:
                    tokens.append(f"{line} <NRO, {lexeme}>")
                else:
                    erros.append(f"{line} <NMF, {lexeme}>")
                i -= 1
            # símbolos
            elif re.match(self.__regex_symbol, content[i]):
                verified = False
                lexeme = content[i]
                # delimitadores
                if content[i] in self.__delimiters or content[i] == '-':
                    if content[i] == '-':
                        if i + 1 < length:
                            if content[i + 1] == '>':
                                i += 1
                                lexeme += content[i]
                                tokens.append(f"{line} <DEL, {lexeme}>")
                                verified = True
                    else:
                        tokens.append(f"{line} <DEL, {lexeme}>")
                        verified = True
                # operadores aritméticos
                if content[i] in self.__aritmetic and not verified:
                    verified = True
                    if content[i] == '/':
                        if i + 1 < length:
                            if content[i + 1] == '/':
                                i += 1
                                while i < length and content[i] != '\n':
                                    lexeme += content[i]
                                    i += 1
                                i -= 1
                            elif content[i + 1] == '*':
                                i += 1
                                lexeme += content[i]
                                line_begin = line
                                close = False
                                valid_coment = False
                                while i < length and not valid_coment:
                                    if content[i] == '*':
                                        close = True
                                    elif content[i] == '/' and close:
                                        valid_coment = True
                                    else:
                                        close = False
                                    if content[i] == '\n':
                                        line += 1
                                    lexeme += content[i]
                                    i += 1
                                i -= 1
                                if not valid_coment:
                                    erros.append(f"{line_begin} <CoMF, >")
                            else:
                                tokens.append(f"{line} <ART, {lexeme}>")
                        else:
                            tokens.append(f"{line} <ART, {lexeme}>")
                    elif content[i] == '+' or content[i] == '-':
                        if i + 1 < length:
                            if content[i + 1] == content[i]:
                                i += 1
                                lexeme += content[i]
                        tokens.append(f"{line} <ART, {lexeme}>")
                    else:
                        tokens.append(f"{line} <ART, {lexeme}>")
                # operadores relacionais
                if content[i] in self.__relational and not verified:
                    if content[i] == '!':
                        if i + 1 < length:
                            if content[i+1] == '=':
                                i += 1
                                lexeme += content[i]
                                tokens.append(f"{line} <REL, {lexeme}>")
                                verified = True
                    else:
                        if i + 1 < length:
                            if content[i + 1] == '=':
                                i += 1
                                lexeme += content[i]
                        tokens.append(f"{line} <REL, {lexeme}>")
                        verified = True
                # operadores lógicos
                if content[i] in self.__logical and not verified:
                    verified = True
                    if content[i] in ['&', '|']:
                        if i + 1 < length:
                            i += 1
                            if content[i] == content[i - 1]:
                                lexeme += content[i]
                                tokens.append(f"{line} <LOG, {lexeme}>")
                            else:
                                stop = False
                                while i < length and (content[i] not in self.__separators or content[i] in ['&', '|']) and not stop:
                                    if content[i] == '&' or content[i] == '|':
                                        if i + 1 < length:
                                            if content[i] == content[i + 1]:
                                                stop = True
                                    lexeme += content[i]
                                    i += 1
                                erros.append(f"{line} <TMF, {lexeme}>")
                                i -= 1
                        else:
                            erros.append(f"{line} <TMF, {lexeme}>")
                    else:
                        tokens.append(f"{line} <LOG, {lexeme}>")
                # símbolos
                if not verified and content[i] != ' ':
                    stop = False
                    i += 1
                    while i < length and (content[i] not in self.__separators or content[i] in ['&', '|']) and not stop:
                        if content[i] == '&' or content[i] == '|':
                            if i + 1 < length:
                                if content[i] == content[i + 1]:
                                    stop = True
                        lexeme += content[i]
                        i += 1
                    erros.append(f"{line} <TMF, {lexeme}>")
                    i -= 1
            # cadeia de caracteres
            elif content[i] == '"':
                lexeme = content[i]
                i += 1
                valid_string = True
                while i < length and content[i] != '\n' and content[i] != '"':
                    if not re.match(self.__regex_symbol, content[i]) and not re.match(self.__regex_letter, content[i]) and not re.match(self.__regex_number, content[i]):
                        valid_string = False
                    lexeme += content[i]
                    i += 1
                
                if content[i] == '"':
                    lexeme += content[i]
                    if valid_string:
                        tokens.append(f"{line} <CAC, {lexeme}>")
                    else:
                        erros.append(f"{line} <CMF, {lexeme}>")
                else:
                    erros.append(f"{line} <CMF, {lexeme}>")
                    i -= 1 if content[i] == '\n' else 0
            # contado de linhas
            elif content[i] == '\n':
                line += 1
            # fora do range de símbolos
            else:
                lexeme = content[i]
                stop = False
                while i < length and (content[i] not in self.__separators or content[i] in ['&', '|']) and not stop:
                    if content[i] == '&' or content[i] == '|':
                        if i + 1 < length:
                            if content[i] == content[i + 1]:
                                stop = True
                    lexeme += content[i]
                    i += 1
                erros.append(f"{line} <TMF, {lexeme}>")
                i -= 1
            i += 1
        return tokens, erros