from typing import Tuple

NONDECLARADE = "IDE Não declarado"
INCOPTYPE = "Tipo incompatível"
DUPLICATE = "Duplicado"
INVALIDATT = "Atribuição inválida"

class SyntacticSemantic():
    def __init__(self, string_tokens: str = []):
        self.__string_tokens = string_tokens
        self.__pointer = 0
        self.__tokens = []
        self.__tokens_len = 0
        self.__syntactical_errors = []
        self.__scopes = []
        self.__scope_table = {} # { [identificador]: { type: ...,  category: ...,  parameter: ..., instantiated: ..., extends: ..., array: ..., scope: { ... } } }
        self.__semantic_errors = []
        self.__var_temp = {}
        self.__method_temp = {}
        self.__is_dec_method = False
        self.__is_dec = False
        self.__is_access = False
        self.__obj_access = False
        self.__is_read = False

    """
        Função que inicia o analizador sintático
    """
    def run(self) -> Tuple[list[str], list[str]]:
        self.__parser_tokens()
        self.__program()
        # print("tabela de escopo:\n")
        # for k, v in self.__scope_table.items():   
        #     print(f"{k}: {v}")
        #     print()
        # print("erros:\n")
        # for e in self.__semantic_errors:
        #     print(e)
        return self.__syntactical_errors, self.__semantic_errors

    def __program(self) -> None:
        self.__consts_block()
        self.__variables_block()
        self.__class_block()

    def __variables_block(self) -> None:
        token = self.__next(expected='variables')
        if token['value'] == 'variables':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__variables()
            else:
                self.__syntactical_error(token, '{')
        else:
            self.__syntactical_error(token, 'variables')
    
    def __variables(self) -> None:
        self.__var_temp['category'] = 'variables'
        self.__is_dec = True
        token = self.__next(expected='}')
        if not token['value'] == '}':
            self.__pointer -= 1
            self.__variable()
            self.__variables()
        else:
            self.__var_temp = {}
            self.__is_dec = False
        
    def __variable(self) -> None:
        self.__var_temp['category'] = 'variable'
        self.__is_dec = True
        self.__type()
        self.__dec_var()
        self.__multiple_variables_line()
    
    def __type(self) -> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string']")
        if token['key'] == 'PRE':
            if token['value'] in ['int', 'real', 'boolean', 'string']:
                if self.__is_dec:
                    self.__var_temp['type'] = token['value']
                elif self.__is_dec_method:
                    self.__method_temp['type'] = token['value']
                return
        self.__syntactical_error(found=token, expected="['int', 'real', 'boolean', 'string']")

    def __dec_var(self) -> None:    
        token = self.__next(expected="IDE")
        if token['key'] == 'IDE':
            self.__var_temp['ide'] = token['value']
            if self.__is_dec:
                self.__add_ide(self.__var_temp['ide'], False, token['line'], type=self.__var_temp['type'], category=self.__var_temp['category'], parameter=False, extends=False)
            elif self.__obj_access:
                    
                if 'token' in self.__var_temp.keys() and self.__var_temp['token']['category'] != 'object':
                    self.__semantic_error(token['line'], INCOPTYPE, self.__var_temp['ide'])
                else:
                    if self.__var_temp['scope']:
                        ide = self.__verify_specific_ide(scope=self.__var_temp['scope'])
                    else:
                        ide = self.__verify_specific_ide(scope=self.__var_temp['token']['type'])

                    if token['value'] in ide.keys():
                        self.__var_temp['token'] = ide[token['value']]
                        self.__var_temp['scope'] = None
                    else:
                        self.__semantic_error(token['line'], NONDECLARADE, token['value'])
            else:
                ide = self.__verify_specific_ide(token['value'])
                if not ide:
                    self.__semantic_error(token['line'], NONDECLARADE, token['value'])
            self.__dimensions()
        else:
            self.__syntactical_error(found=token, expected="IDE")

    def __dimensions(self) -> None:
        token = self.__next(expected='[')
        if token['value'] == '[':
            if self.__is_dec:
                self.__add_ide(self.__var_temp['ide'], True, token['line'], array=True)
            else:
                if 'token' not in self.__var_temp.keys():
                    self.__semantic_error(token['line'], type=INCOPTYPE + f'. identificador não é um array.', ide= self.__var_temp['scope'] if 'ide' not in self.__var_temp.keys() else self.__var_temp['ide'])
                elif 'array' not in self.__var_temp['token'].keys():
                    self.__semantic_error(token['line'], type=INCOPTYPE + f'. identificador não é um array.', ide= self.__var_temp['scope'] if 'ide' not in self.__var_temp.keys() else self.__var_temp['ide'] )
            self.__size_dimension()
            token = self.__next(expected=']')
            if token['value'] == ']':
                self.__dimensions()
            else:
                self.__syntactical_error(found=token, expected=']')
        else:
            self.__pointer -= 1

    def __size_dimension(self) -> None:
        token = self.__next(expected='[NRO, IDE]')
        if token['key'] not in ['NRO', 'IDE']:
            self.__syntactical_error(found=token, expected='[NRO, IDE]')
        elif token['key'] == 'NRO':
            if '.' in token['value']:
                self.__semantic_error(line=token['line'], type=INCOPTYPE + f". Esperava int, recebeu real", ide=token['value'])
        elif token['key'] == 'IDE':
            table = self.__verify_specific_ide(token['value'])
            if table:
                if table['type'] != 'int':
                    self.__semantic_error(line=token['line'], type=INCOPTYPE + f". Esperava int, recebeu {table['type']}", ide=token['value'])
            else:
                self.__semantic_error(line=token['line'], type=NONDECLARADE, ide=token['value'])

    def __multiple_variables_line(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__dec_var()
            self.__multiple_variables_line()
        elif not token['value'] == ';':
            self.__var_temp = {}
            self.__is_dec = False
            self.__syntactical_error(found=token, expected="[',', ';']")
        

    def __class_block(self) -> None:
        token = self.__next(expected='class')
        if token['value'] == 'class':
            self.__ide_class()
        else:
            self.__syntactical_error(token, 'class')
    
    def __ide_class(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__var_temp['ide'] = token['value']
            self.__add_ide(ide=token['value'], update=False, line=token['line'], type="class", category="class", parameter=False, extends=False, scope={})
            self.__scopes.append(token['value'])
            self.__extends()
        else:
            self.__var_temp['ide'] = token['value']
            self.__add_ide(ide=token['value'], update=False, line=token['line'], type="class", category="class", parameter=False, extends=False, scope={})
            self.__scopes.append(token['value'])
            self.__pointer -= 1
            self.__main()

    def __extends(self) -> None:
        token = self.__next(expected='extends')
        if token['value'] == 'extends':
            token = self.__next(expected='IDE')
            if token['key'] == 'IDE':
                if self.__verify_ide(token['value'], token['line']):
                    self.__add_ide(ide=self.__var_temp['ide'], level=1, update=True, line=token['line'], extends=token['value'])
            else:
                self.__syntactical_error(token, 'extends')
        else:
            self.__pointer -= 1
        self.__start_class_block()

    def __start_class_block(self) -> None:
        token = self.__next(expected='{')
        if token['value'] == '{':
            self.__init_class()
        else:
            self.__syntactical_error(token, '{')
    
    def __init_class(self) -> None:
        self.__body_blocks()
        self.__methods_block()
        self.__constructor()
    
    def __methods_block(self) -> None:
        token = self.__next(expected='methods')
        if token['value'] == 'methods':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__methods()
                token = self.__next(expected='}')
                if not token['value'] == '}':
                    self.__syntactical_error(found=token, expected='}')
                else:
                    self.__method_temp = {}
            else:
                self.__syntactical_error(found=token, expected='{')
        else:
            self.__syntactical_error(found=token, expected='methods')

    def __methods(self) -> None:
        token = self.__next(expected="['}', 'void', 'int', 'real', 'boolean', 'string', IDE]")
        self.__pointer -= 1
        if token['value'] in ['void', 'int', 'real', 'boolean', 'string'] or token['key'] == 'IDE':
            self.__method()
            self.__methods()

    def __method(self) -> None:
        self.__is_dec_method = True
        self.__types()
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__add_ide(ide=token['value'],update=False, line=token['line'], type=self.__method_temp['type'], category='method', parameter=False, extends=False, scope={})
            self.__scopes.append(token['value'])
            self.__method_temp = {}
            self.__is_dec_method = False
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__is_dec = True
                self.__dec_parameters()
            else:
                self.__syntactical_error(found=token, expected='(')
        else:
            self.__syntactical_error(found=token, expected='(')
    
    def __types(self) -> None:
        token = self.__next(expected="['void', 'int', 'real', 'boolean', 'string', IDE]")
        if not token['value'] == 'void':
            self.__pointer -= 1
            self.__type_variables()
        else:
            self.__method_temp['type'] = token['value']
    
    def __type_variables(self) -> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string', IDE]")
        if not token['key'] == 'IDE':
            self.__pointer -= 1
            self.__type()
        elif self.__is_dec_method:
            self.__method_temp['type'] = token['value']
        elif self.__is_dec:
            self.__var_temp['type'] = token['value']
            if token['value'] in self.__scope_table.keys():
                if self.__scope_table[token['value']]['type'] != 'class':
                    self.__semantic_error(line=token['line'], type=INCOPTYPE + f". Esperava class, encontrou {self.__scope_table[token['value']]['type']}", ide=token['value'])
            else:
                self.__semantic_error(line=token['line'], type=NONDECLARADE, ide=token['value'])

    def __dec_parameters(self) -> None:
        token = self.__next(expected="['int', 'real', 'boolean','string', IDE]")
        self.__pointer -= 1
        if token['value'] in ['int', 'real', 'boolean','string']:
            self.__variable_param()
        elif token['key'] == 'IDE':
            self.__object_param()
        self.__mult_dec_parameters()
    
    def __mult_dec_parameters(self) -> None:
        token = self.__next(expected="[',', ')']")
        if token['value'] == ',':
            self.__type_variables()
            token = self.__next(expected='IDE')
            if token['key'] == 'IDE':
                self.__add_ide(token['value'], update=False, line= token['line'], type=self.__var_temp['type'], category='variable', parameter=True, extends=False)
                self.__mult_dec_parameters()
            else:
                self.__syntactical_error(found=token, expected='IDE')
        else:
            self.__pointer -= 1
            self.__end_dec_parameters()
    
    def __end_dec_parameters(self) -> None:
        self.__is_dec = False
        self.__var_temp = {}
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__method_body()
            else:
                self.__syntactical_error(found=token, expected='{')
        else:
            self.__syntactical_error(found=token, expected=')')
    
    def  __method_body(self) -> None:
        self.__variables_block()
        self.__objects_block()
        self.__commands_method_body()

    def __commands_method_body(self) -> None:
        self.__commands()
        token = self.__next(expected='return')
        if token['value'] == 'return':
            self.__return()
            token = self.__next(expected=';')
            if token['value'] == ';':
                token = self.__next(expected='}')
                if not token['value'] == '}':
                    self.__syntactical_error(found=token, expected='}')
                else:
                    if self.__scopes:
                        self.__scopes.pop()
                    self.__is_dec_method = False
            else:
                self.__syntactical_error(found=token, expected=';')
        else:
            self.__syntactical_error(found=token, expected='return')
    
    def __return(self) -> None:
        token = self.__next(expected='')
        self.__pointer -= 1
        if token['key'] in ['NRO', 'IDE', 'CAC'] or token['value'] in ['!', '[', '(', 'true', 'false']:
            self.__value()

    def __commands(self) -> None:
        token = self.__next(expected="['print', 'read', 'if', 'for', IDE]")
        self.__pointer -= 1
        if token['value'] in ['print', 'read', 'if', 'for', 'this'] or token['key'] == 'IDE':
            self.__command()
            self.__commands()
    
    def __command(self) -> None:
        token = self.__next(expected="['print', 'read', 'if', 'for', IDE]")
        self.__pointer -= 1
        if token['value'] == 'print':
            self.__print_begin()
        elif token['value'] == 'read':
            self.__read_begin()
        elif token['key'] == 'IDE' or token['value'] == 'this':
            self.__object_access_or_assigment()
            token = self.__next(expected=';')
            if not token['value'] == ';':
                self.__syntactical_error(found=token, expected=';')
        elif token['value'] == 'if':
            self.__if()
        elif token['value'] == 'for':
            self.__for_block()
        else:
            self.__pointer += 1
            self.__syntactical_error(found=token, expected="['print', 'read', 'if', 'for', IDE]")

    def __for_block(self) -> None:
        self.__begin_for()
        self.__for_increment()
        self.__end_for()


    def __begin_for(self) -> None:
        token = self.__next(expected='for')
        if token['value'] == 'for':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__object_access_or_assigment()
                token = self.__next(expected=';')
                if token['value'] == ';':
                    self.__conditional_expression()
                    token = self.__next(expected=';')
                    if not token['value'] == ';':
                        self.__syntactical_error(found=token, expected=';')
                else:
                    self.__syntactical_error(found=token, expected=';')
            else:
                self.__syntactical_error(found=token, expected='(')
        else:
            self.__syntactical_error(found=token, expected='for')
    
    def __conditional_expression(self) -> None:
        token = self.__next(expected="[NRO, IDE, CAC, '(']")
        if token['value'] == '(':
            self.__relational_expression()
        elif token['key'] in ['NRO', 'IDE', 'CAC']:
            self.__pointer -= 1 
            self.__relational_expression()
        else:
            self.__syntactical_error(found=token, expected="[NRO, IDE, CAC, '(']")

    def __relational_expression(self) -> None:
        self.__relational_expression_value()
        token  = self.__next(expected='REL')
        if token['key'] == 'REL':
            self.__relational_expression_value()
        else:
            self.__syntactical_error(found=token, expected='REL')

    def __for_increment(self) -> None:
        self.__dec_object_atribute_access()
        self.__assignment()
    
    def __assignment(self) -> None:
        token = self.__next(expected="[ART_DOUBLE, '=']")
        if token['value'] == '=':
            self.__value()
        elif token['value'] not in ['++', '--']:
            self.__syntactical_error(found=token, expected="[ART_DOUBLE, '=']")
    
    def __end_for(self) -> None:
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__commands()
                token = self.__next(expected='}')
                if not token['value'] == '}':
                    self.__syntactical_error(found=token, expected='}')
            else:
                self.__syntactical_error(found=token, expected='{')
        else:
            self.__syntactical_error(found=token, expected=')')

    def __print_begin(self) -> None:
        token = self.__next(expected='print')
        if token['value'] == 'print':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__print_end()
            else:
                self.__syntactical_error(found=token, expected='(')
        else:
            self.__syntactical_error(found=token, expected='print')
    
    def __print_end(self) -> None:
        self.__print_parameter()
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected=';')
            if not token['value'] == ';':
                self.__syntactical_error(found=token, expected=';')
        else:
            self.__syntactical_error(found=token, expected=')')
    
    def __print_parameter(self) -> None:
        token = self.__next(expected='[CAC, NRO, IDE]')
        if token['key'] not in ['CAC', 'NRO']:
            if token['key'] == 'IDE' or token['value'] == 'this':
                if token['value'] != "this":
                    ide = self.__verify_specific_ide(ide=token['value'])
                    if ide['category'] not in ['variable', 'object', 'const']:
                        self.__semantic_error(token['line'], INCOPTYPE + f". Esparava ['variable', 'object', 'const'], recebeu {ide['category']} ", token['value'])
                self.__pointer -= 1
                self.__dec_object_atribute_access()
            else:
                self.__syntactical_error(found=token, expected='[CAC, NRO, IDE]')
    
    def __read_begin(self) -> None:
        token = self.__next(expected='read')
        if token['value'] == 'read':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__read_end()
            else:
                self.__syntactical_error(found=token, expected='(')
        else:
            self.__syntactical_error(found=token, expected='read')
    
    def __read_end(self) -> None:
        self.__dec_object_atribute_access()
        token = self.__next(expected=')')
        if token['value'] == ')':
            if 'token' in self.__var_temp.keys() and self.__var_temp['token']['type'] not in ['int','real', 'string', 'boolean']:
                self.__semantic_error(token['line'], INCOPTYPE, ide=self.__var_temp['ide'] if 'ide' in self.__var_temp.keys() else self.__var_temp['scope'])
            token = self.__next(expected=';')
            if not token['value'] == ';':
                self.__syntactical_error(found=token, expected=';')
        else:
            self.__syntactical_error(found=token, expected=')')
    
    def __object_access_or_assigment(self) -> None:
        self.__dec_object_atribute_access()
        self.__object_access_or_assigment_end()
    
    def __object_access_or_assigment_end(self) -> None:
        token = self.__next(expected='=')
        if token['value'] == '=':
            self.__value()
        elif token['value'] in ['++', '--']:
            if 'token' in self.__var_temp.keys() and self.__var_temp['token']['type'] not in ['int','real']:
                self.__semantic_error(line=token['line'], type=INCOPTYPE, ide=self.__var_temp['ide'] )
        else:
            self.__pointer -= 1
            self.__object_method_access_end()
    
    def __value(self) -> None:
        token = self.__next(expected="[NRO, CAC, '!', '[', '(', IDE, 'true', 'false']")
        if token['key'] == 'NRO':
            self.__simple_or_double_arithimetic_expression_optional()
        elif token['value'] == '!':
            self.__logical_expression_begin()
            self.__logical_expression_end()
        elif token['value'] == '[':
            self.__pointer -= 1
            self.__vector_assign_block()
        elif token['key'] == 'IDE':
            self.__pointer -= 1
            self.__init_expression()
        elif token['value'] == '(':
            self.__pointer -= 1
            self.__arithimetic_or_logical_expression_with_parentheses()
        elif not (token['value'] in ['true', 'false'] or token['key'] == 'CAC'):
            self.__syntactical_error(found=token, expected="[NRO, CAC, '!', '[', '(', IDE, 'true', 'false']")

    def __arithimetic_or_logical_expression_with_parentheses(self) -> None:
        self.__parentheses_begin()

    def __parentheses_begin(self) -> None:
        token = self.__next(expected='(')
        if token['value'] == '(':
            self.__expression()
            self.__parentheses_end()
        else:
            self.__syntactical_error(found=token, expected='(')

    def __parentheses_end(self) -> None:
        token = self.__next(expected=')')
        if token['value'] == ')':
            self.__expressions_without_parentheses_end()
        else:
            self.__syntactical_error(found=token, expected=')')
    
    def __expressions_without_parentheses_end(self) -> None:
        token = self.__next(expected="[ART, LOG]")
        if token['value'] in ['+', '-', '*', '/']:
           self.__pointer -= 1
           self.__end_expression()
        elif token['key'] == 'LOG':
            self.__logical_expression_begin()
            self.__logical_expression_end()
        else:
            self.__pointer -= 1 

    def __expression(self) -> None:
        token = self.__next(expected="['(']")
        self.__pointer -= 1
        if token['value'] == '(':
            self.__parentheses_begin()
        elif token['key'] == 'NRO':
            self.__simple_expression_without_parentheses()
        elif token['value'] in ['true', 'false', '!']:
            self.__logical_expression_without_parentheses()
        elif token['key'] == 'IDE':
            self.__simple_or_logical_ide_begin()

    def __simple_or_logical_ide_begin(self) -> None:
        self.__dec_object_atribute_access()
        self.__simple_or_logical_ide_end()

    def __simple_or_logical_ide_end(self) -> None:
        token = self.__next(expected="[ART, '->', REL, LOG]")
        self.__pointer -= 1
        if token['value'] == '->' or token['key'] in ['REL', 'LOG']:
            self.__optional_object_method_access()
            self.__log_rel_optional()
            self.__logical_expression_end()
        elif token['value'] in ['+', '-', '*', '/']:
            self.__end_expression()
        else:
            self.__syntactical_error(found=token, expected="[ART, '->', REL, LOG]")

    def __logical_expression_without_parentheses(self) -> None:
        token = self.__next(expected="['true', 'false', '!']")
        if token['value'] in ['true', 'false']:
            self.__logical_expression_begin()
        elif token['value'] == '!':
            self.__logical_expression_begin()
            self.__logical_expression_end()

    def __simple_expression_without_parentheses(self) -> None:
        token = self.__next(expected='NRO')
        if token['key'] == 'NRO':
            self.__end_expression()
        else:
            self.__syntactical_error(found=token, expected='NRO')

    def __init_expression(self) -> None:
        self.__dec_object_atribute_access()
        self.__arithimetic_or_logical_expression()

    def __arithimetic_or_logical_expression(self) -> None:
        token = self.__next(expected="[ART, '->', REL, LOG]")
        self.__pointer -= 1
        if token['value'] == '->' or token['key'] in ['REL', 'LOG']:
            self.__optional_object_method_access()
            self.__log_rel_optional()
            self.__logical_expression_end()
        elif token['key'] == 'ART':
            self.__simple_or_double_arithimetic_expression()

    def __vector_assign_block(self) -> None:
        token = self.__next(expected='[')
        if token['value'] == '[':
            self.__elements_assign()
            token = self.__next(expected=']')
            if not token['value'] == ']':
                self.__syntactical_error(found=token, expected=']')
        else:
            self.__syntactical_error(found=token, expected='[')
    
    def __elements_assign(self) -> None:
        self.__element_assign()
        self.__multiple_elements_assign()
    
    def __element_assign(self) -> None:
        token = self.__next(expected="[IDE, CAC, NRO, '[']")
        if token['value'] == '[':
            self.__pointer -= 1
            self.__n_dimensions_assign()
        elif token['key'] not in ['CAC', 'IDE', 'NRO']:
            self.__syntactical_error(found=token, expected="[IDE, CAC, NRO, '[']")
    
    def __n_dimensions_assign(self) -> None:
        token = self.__next(expected='[')
        if token['value'] == '[':
            self.__elements_assign()
            token = self.__next(expected=']')
            if not token['value'] == ']':
                self.__syntactical_error(found=token, expected=']')
        else:
            self.__pointer -= 1

    def __multiple_elements_assign(self) -> None:
        token = self.__next(expected=",")
        if token['value'] == ',':
            self.__element_assign()
            self.__multiple_elements_assign()
        else:
            self.__pointer -= 1

    def __logical_expression_begin(self) -> None:
        token = self.__next(expected="['(', '!', 'true', 'false', IDE]")
        if token['value'] == '(':
            self.__logical_expression()
            token = self.__next(expected=')')
            if not token['value'] == ')':
                self.__syntactical_error(found=token, expected=')')
        elif token['value'] == '!':
            self.__logical_expression_begin()
        elif token['value'] in ['true', 'false', 'this'] or token['key'] == 'IDE':
            self.__pointer -= 1
            self.__logical_expression_value()
        else:
            self.__syntactical_error(found=token, expected="['(', '!', 'true', 'false', IDE]")

    def __logical_expression(self) -> None:
        self.__logical_expression_begin()
        self.__logical_expression_end()
    
    def __logical_expression_value(self) -> None:
        token = self.__next(expected="['true', 'false', IDE]")
        if token['value'] not in ['true', 'false']:
            if token['key'] == 'IDE' or token['value'] == 'this':
                self.__pointer -= 1
                self.__object_method_or_object_access()
                self.__log_rel_optional()
            else:
                self.__syntactical_error(found=token, expected="['true', 'false', IDE]")

    def __object_method_or_object_access(self) -> None:
        self.__object_method_or_object_access_or_part()
    
    def __log_rel_optional(self) -> None:
        token = self.__next(expected='REL')
        if token['key'] == 'REL':
            self.__relational_expression_value()
        else:
            self.__pointer -= 1
    
    def __relational_expression_value(self) -> None:
        token = self.__next(expected="[NRO, CAC, IDE]")
        if token['key'] == 'IDE':
            self.__pointer -= 1
            self.__object_method_or_object_access()
        elif token['key'] not in ['NRO', 'CAC']:
            self.__syntactical_error(found=token, expected="[NRO, CAC, IDE]")

    def __logical_expression_end(self) -> None:
        token = self.__next(expected="LOG")
        if token['key'] == 'LOG':
            self.__logical_expression_begin()
            self.__logical_expression_end()
        else:
            self.__pointer -= 1
    
    def __simple_or_double_arithimetic_expression_optional(self) -> None:
        token = self.__next(expected="ART")
        self.__pointer -= 1
        if token['key'] == 'ART':
            self.__simple_or_double_arithimetic_expression()
    
    def __simple_or_double_arithimetic_expression(self) -> None:
        token = self.__next(expected="['ART', 'ART_DOUBLE']")
        if token['value'] not in ['++', '--']:
            self.__pointer -= 1
            self.__end_expression()

    def __end_expression(self) -> None:
        token = self.__next(expected='ART')
        if token['value'] in ['+', '-', '*', '/']:
            self.__part_loop()
        else:
            self.__syntactical_error(found=token, expected='ART')
    
    def __part_loop(self) -> None:
        token = self.__next(expected="[IDE, NRO, '(']")
        self.__pointer -= 1
        if token['key'] in ['IDE', 'NRO'] or token['value'] == 'this':
            self.__part()
            self.__end_expression_optional()
        elif token['value'] == '(':
            self.__parentheses_expression()
        else:
            self.__syntactical_error(found=token, expected="[IDE, NRO, '(']")
    
    def __parentheses_expression(self) -> None:
        token = self.__next(expected='(')
        if token['value'] == '(':
            self.__simple_expression()
            token = self.__next(expected=')')
            if token['value'] == ')':
                self.__end_expression_optional()
            else:
                self.__syntactical_error(found=token, expected=')')
        else:
            self.__syntactical_error(found=token, expected='(')
    
    def __simple_expression(self) -> None:
        token = self.__next(expected="[NRO, IDE, '(']")
        self.__pointer -= 1
        if token['key'] in ['NRO', 'IDE']:
            self.__part()
            self.__end_expression()
        elif token['value'] == '(':
            self.__parentheses_expression()
        else:
            self.__syntactical_error(found=token, expected="[NRO, IDE, '(']")

    def __part(self) -> None:
        token = self.__next(expected="[IDE, NRO]")
        if not token['key'] == 'NRO':
            self.__pointer -= 1
            self.__object_method_or_object_access_or_part()

    def __end_expression_optional(self) -> None:
        token = self.__next(expected="ART")
        self.__pointer -= 1
        if token['value'] in ['+', '-', '*', '/']:
            self.__end_expression()
        
    def __object_method_or_object_access_or_part(self) -> None:
        self.__dec_object_atribute_access()
        self.__optional_object_method_access()
    
    def __optional_object_method_access(self) -> None:
        token = self.__next(expected='->')
        self.__pointer -= 1
        if token['value'] == '->':
            self.__object_method_access_end()

    def __object_method_access_end(self) -> None:
        token = self.__next(expected='->')
        if token['value'] == '->':
            self.__ide_or_constructor()
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__parameters()
                token = self.__next(expected=')')
                if not token['value'] == ')':
                    self.__syntactical_error(found=token, expected=')')
            else:
                self.__syntactical_error(found=token, expected='(')
        else:
            self.__syntactical_error(found=token, expected='->')
    
    def __parameters(self) -> None:
        token = self.__next(expected="[NRO, '!', '[', IDE, '(', 'true', 'false', CAC]")
        self.__pointer -= 1
        if token['key'] in ['NRO', 'IDE', 'CAC'] or token['value'] in ['!', '[', '(', 'true', 'false']:
            self.__value()
            self.__mult_parameters()
    
    def __mult_parameters(self) -> None:
        token = self.__next(expected=',')
        if token['value'] == ',':
            self.__value()
            self.__mult_parameters()
        else:
            self.__pointer -= 1

    def __ide_or_constructor(self) -> None:
        token = self.__next(expected="[IDE, 'constructor']")
        if not (token['value'] == 'constructor' or token['key'] == 'IDE'):
            self.__syntactical_error(found=token, expected="[IDE, 'constructor']")

    def __dec_object_atribute_access(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE' or token['value'] == 'this':
            if token['value'] == 'this':
                self.__var_temp['scope'] = self.__scopes[-2]
            else:
                self.__var_temp['ide'] = token['value']
                self.__var_temp['scope'] = None
                ide = self.__verify_specific_ide(token['value'])
                self.__var_temp['token'] = ide
            self.__dimensions()
            self.__end_object_attribute_access()
        else:
            self.__syntactical_error(found=token, expected='IDE')
    
    def __end_object_attribute_access(self) -> None:
        token = self.__next(expected='.')
        if token['value'] == '.':
            self.__multiple_object_attribute_access()
        else:
            if self.__var_temp['scope']:
                self.__semantic_error(token['line'], INCOPTYPE, self.__var_temp['scope'])
            self.__pointer -= 1
    
    def __multiple_object_attribute_access(self) -> None:
        self.__obj_access = True
        self.__dec_var()
        self.__end_object_attribute_access()

    def __objects_block(self) -> None:
        token = self.__next(expected='objects')
        if token['value'] == 'objects':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__objects()
            else:
                self.__syntactical_error(found=token, expected='{')
        else:
            self.__syntactical_error(found=token, expected='objects')
    
    def __objects(self) -> None:
        self.__var_temp['category'] = 'object'
        self.__is_dec = True
        token = self.__next(expected="[IDE, '}']")
        if token['key'] == 'IDE':
            self.__pointer -= 1
            self.__object()
            self.__objects()
        elif not token['value'] == '}':
            self.__syntactical_error(found=token, expected="[IDE, '}']")
        else:
            self.__var_temp = {}
            self.__is_dec = False


    def __object(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            if token['value'] in self.__scope_table.keys():
                if self.__scope_table[token['value']]['type'] != 'class':
                    self.__semantic_error(token['line'], type=INCOPTYPE + f". Esperava class, encontrou {self.__scope_table[token['value']]['type']}", ide=token['value'])
            else:
                self.__semantic_error(token['line'],type=NONDECLARADE, ide=token['value'])
            self.__var_temp['type'] = token['value']
            self.__dec_var()
            self.__multiple_objects()
        else:
            self.__syntactical_error(found=token, expected='IDE')
    
    def __multiple_objects(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__dec_var()
            self.__multiple_objects()
        elif not token['value'] == ';':
            self.__is_dec = False
            self.__var_temp = {}
            self.__syntactical_error(found=token, expected="[',', ';']")
    

    def __variable_param(self) -> None:
        self.__type()
        token = self.__next(expected='IDE')
        if not token['key'] == 'IDE':
            self.__syntactical_error(found=token, expected='IDE')
        elif self.__is_dec:
            self.__add_ide(token['value'], update=False, line= token['line'], type=self.__var_temp['type'], category='variable', parameter=True, extends=False)

    def __object_param(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__var_temp['type'] = token['value']
            if token['value'] in self.__scope_table.keys():
                if self.__scope_table[token['value']]['type'] != 'class':
                    self.__semantic_error(line=token['line'], type=INCOPTYPE + f". Esperava class, encontrou {self.__scope_table[token['value']]['type']}", ide=token['value'])
            else:
                self.__semantic_error(line=token['line'], type=NONDECLARADE, ide=token['value'])
            token = self.__next(expected='IDE')
            if not token['key'] == 'IDE':
                self.__syntactical_error(found=token, expected='IDE')
            elif self.__is_dec:
                self.__add_ide(ide=token['value'], update=False, line=token['line'], type=self.__var_temp['type'], category='variable', parameter=True, extends=False)
        else:
            self.__syntactical_error(found=token, expected='IDE')

    def __constructor(self) -> None:
        token = self.__next(expected='constructor')
        if token['value'] == 'constructor':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__dec_parameters_constructor()
                token = self.__next(expected=')')
                if token['value'] == ')':
                    token = self.__next(expected='{')
                    self.__variables_block()
                    self.__objects_block()
                    self.__commands()
                    token = self.__next(expected='}')
                    if token['value'] == '}':
                        self.__end_class()
                    else:
                        self.__syntactical_error(token, '}')
                else:
                    self.__syntactical_error(token, ')')
            else:
                self.__syntactical_error(token, '(')
    
    def __dec_parameters_constructor(self)-> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string', IDE]")
        self.__pointer -= 1
        if token['value'] in ['int', 'real', 'boolean', 'string'] or token['key'] == 'IDE':
            self.__mult_param_constructor()
            self.__mult_dec_parameters_constructor()
    
    def __mult_param_constructor(self)-> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string', IDE]")
        self.__pointer -= 1
        if token['value'] in ['int', 'real', 'boolean', 'string']:
            self.__variable_param()
        elif token['key'] == 'IDE':
            self.__object_param()
        else:
            self.__syntactical_error(found=token, expected="['int', 'real', 'boolean', 'string', IDE]")
        
    def __mult_dec_parameters_constructor(self)-> None:
        token = self.__next(expected=",")
        if token['value'] == ',':
            self.__mult_param_constructor()
            self.__mult_dec_parameters_constructor()
        else:
            self.__pointer -= 1
        
    def __end_class(self) -> None:
        token = self.__next(expected='}')
        if token['value'] == '}':
            self.__scopes.pop()
            self.__class_block()
        else:
            self.__syntactical_error(token, '}')

    def __main(self) -> None:
        token = self.__next(expected='main')
        if token['value'] == 'main':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__init_main()
            else:
                self.__syntactical_error(token, '{')
        else:
            self.__syntactical_error(token, 'main')

    def __init_main(self) -> None:
        self.__body_blocks()
        self.__main_methods()

    def __body_blocks(self) -> None:
        self.__variables_block()
        self.__objects_block()
    
    def __main_methods(self) -> None:
        token = self.__next(expected='methods')
        if token['value'] == 'methods':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__main_methods_body()
            else:
                self.__syntactical_error(token,'{')
        else:
            self.__syntactical_error(token, 'methods')
    
    def __main_methods_body(self) -> None:
        self.__is_dec_method = True
        self.__main_type()
        token = self.__next(expected='main')
        if token['value'] == 'main':
            self.__add_ide(ide=token['value'],update=False, line=token['line'], type=self.__method_temp['type'], category='method', parameter=False, extends=False, scope={})
            self.__scopes.append(token['value'])
            self.__method_temp = {}
            self.__is_dec_method = False
            token = self.__next(expected='(')
            if token['value'] == '(':
                token = self.__next(expected=')')
                if token['value'] == ')':
                    token = self.__next(expected='{')
                    if token['value'] == '{':
                        self.__method_body()
                        self.__methods()
                    else:
                        self.__syntactical_error(token, '{')
                else:
                    self.__syntactical_error(token, ')')
            else:
                self.__syntactical_error(token, '(')
        else:
            self.__syntactical_error(token, 'main')
    
    def __main_type(self) -> None:
        token = self.__next(expected='PRE')
        if token['value'] == 'void':
            self.__method_temp['type'] = token['value']
            return
        else:
            self.__pointer -= 1
            self.__type()
    
    def __if(self) -> None:
        token = self.__next(expected='if')
        if token['value'] == 'if':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__condition()
                token = self.__next(expected=')')
                if token['value'] == ')':
                    token = self.__next(expected='then')
                    if token['value'] == 'then':
                        token = self.__next(expected='{')
                        if token['value'] == '{':
                            self.__commands()
                            token = self.__next(expected='}')
                            if token['value'] == '}':
                                self.__if_else()
                            else:
                                self.__syntactical_error(token, '}')
                        else:
                            self.__syntactical_error(token, '{')
                    else:
                        self.__syntactical_error(token, 'then')
                else:
                    self.__syntactical_error(token, ')')
            else:
                self.__syntactical_error(token, '(')
        else:
            self.__syntactical_error(token, 'if')
    
    def __if_else(self) -> None:
        if self.__pointer < self.__tokens_len:
            token = self.__next()
            if token['value'] == 'else':
                token = self.__next(expected='{')
                if token['value'] == '{':
                    self.__commands()
                    token = self.__next(expected='}')
                    if token['value'] == '}':
                        return
                    else:
                        self.__syntactical_error(token, '}')
                else:
                    self.__syntactical_error(token, '{')
            else:
                self.__pointer -= 1
    
    def __condition(self) -> None:
        self.__logical_expression()

    def __consts_block(self) -> None:
        token = self.__next(expected='const')
        if token['value'] == 'const':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__consts()
            else:
                self.__syntactical_error(token, '{')
        else:
            self.__syntactical_error(token, 'const')
    
    def __consts(self) -> None:
        self.__is_dec = True
        token = self.__next(expected='}')
        if not token['value'] == '}':
            self.__pointer -= 1
            self.__const()
            self.__consts()
        else:
            self.__is_dec = False
            self.__var_temp = {}
    
    def __const(self) -> None:
        self.__type()
        self.__const_atribution()
        self.__multiple_consts()
    
    def __const_atribution(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__var_temp['ide'] = token['value']
            self.__add_ide(token['value'],False, token['line'], type=self.__var_temp['type'], category='const', parameter=False, extends=False)
            token = self.__next(expected='=')
            if token['value'] == '=':
                self.__atribution()
            else:
                self.__syntactical_error(token, '=')
        else:
            self.__syntactical_error(token, 'IDE')
    
    def __multiple_consts(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__const_atribution()
            self.__multiple_consts()
        elif not token['value'] == ';':
            self.__syntactical_error(token, "[',', ';']")
    
    def __atribution(self) -> None:
        token = self.__next(expected="[NRO, BOOL, CAC]")
        if not (
            token['value'] == 'true' 
                or 
            token['value'] == 'false'
                or
            token['key'] == 'NRO'
                or
            token['key'] == 'CAC'):
            self.__syntactical_error(token, "[NRO, BOOL, CAC]")
        else:
            self.__verify_attribution(self.__var_temp, token)
    """
        Função que faz o papel de guardar o erro assim que ele acontece
    """
    def __syntactical_error(self, found: dict, expected: str) -> None:
        self.__syntactical_errors.append(f"L - {found['line'] if 'line' in found.keys() else 'EOF'}:\t Esperava {expected}, mas encontrou [{found['key']}:{found['value']}].")

    def __semantic_error(self, line: int, type: str, ide: str) -> None:
        self.__semantic_errors.append(f"L - {line}: [IDE: {ide}] {type}")

    """
        Função que avança o ponteiro da lista para o próximo token
        retorna um dicionário e um boleano para indicar se a lista de tokens ainda tem tokens
    """
    def __next(self, expected: str = 'TOKEN') -> dict:
        if self.__pointer > self.__tokens_len:
            self.__syntactical_error(found={'key':'EOF', 'value': 'End Of File'}, expected=expected)
            raise Exception("End of file founded.")
        token = self.__tokens[self.__pointer]
        self.__pointer += 1
        return token

    """
        Transforma a string contendo todos os tokens em uma lista de dicionários no formato:

            {'key': key, 'value': value, 'line': line}

            key -> é o tipo de token
            value -> o valor do token
            line -> a linha em que aquele token está
    """
    def __parser_tokens(self) -> None:
        self.__tokens = []
        self.__tokens_len = -1 # mapeando a lista de tokens de 0 a n - 1

        for line in self.__string_tokens.splitlines():
            aux = line.split('<', 1)
            splitline = aux[1].rsplit('>', 1)[0].split(',', 1)
            n_line = int(aux[0].strip())
            self.__tokens.append({'key': splitline[0].strip(), 'value': splitline[1].strip(), "line": n_line})
            self.__tokens_len += 1

    """
        Adiciona um identificador na tabela de escopo.
    """
    def __add_ide(self, ide: str, update: bool, line: str, level: int = 0, **args) -> None:
        table = self.__get_scope(level)
        if ide in table.keys():
            if not update:
                self.__semantic_error(line, type=DUPLICATE, ide=ide)
                if args['category'] == 'class':
                    table[ide] = args
            else:
                table[ide].update(args)
        else:
            table[ide] = args

    """
        Captura o dicionário correspondente ao escopo de análise atual.
    """
    def __get_scope(self, level: int = 0) -> dict:
        table = self.__scope_table
        if level <= len(self.__scopes):
            scopes = self.__scopes.copy()
            for _ in range(level):
                scopes.pop()
        else:
            scopes = []
        if scopes:
            for s in scopes:
                table = table[s]['scope']
        return table

    """
        Método verifica se um identificador existe na tabela de símbolos, a partir do escopo atual
        até o mais alto escopo possível.
    """
    def __verify_ide(self, ide: str, line: str) -> bool:
        flag = False
        for i in range(len(self.__scopes)):
            table = self.__get_scope(i)
            if ide in table.keys():
                flag = True
        if flag:
            self.__semantic_error(line=line, type=NONDECLARADE, ide=ide)
        return not flag

    def __verify_specific_ide(self, ide:str = None, scope: str = None) -> dict:
        if scope:
            if scope in self.__scope_table.keys():
                return self.__scope_table[scope]['scope']
            else:
                return None
        stop = False
        token = None
        scopes =  self.__scopes.copy()
        while not stop:
            table = self.__scope_table.copy()
            for s in scopes:
                table = table[s]['scope']
            if ide in table.keys():
                token = table[ide]
                stop = True
            else:
                if scopes:
                    scopes.pop()
                else:
                    stop = True
        return token
    
    """
        Método verifica se uma atribuição está sendo feita corretamente
    """
    def __verify_attribution(self, expected: str, token: str) -> None:
        if expected['type'] == 'string':
            if token['key'] == 'CAC':
                return
        elif expected['type'] == 'boolean':
            if token['value'] == 'false' or token['value'] == 'true':
                return
        elif expected['type'] == 'int':
            if token['key'] == 'NRO' and '.' not in token['value']:
                return
        elif expected['type'] == 'real':
            if token['key'] == 'NRO' and '.' in token['value']:
                return
        self.__semantic_error(token['line'], type=INCOPTYPE + f". Esperava '{expected['type']}', recebeu '{token['value']}'", ide=expected['ide'])