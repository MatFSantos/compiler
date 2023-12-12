import re

class Syntactic():
    def __init__(self, string_tokens: str = []):
        self.__string_tokens = string_tokens
        self.__pointer = 0
        self.__tokens = []
        self.__tokens_len = 0
        self.__errors = []
    
    """
        Função que inicia o analizador sintático
    """
    def run(self) -> list[str]:
        self.__parser_tokens()
        self.__program()
        return self.__errors        

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
                self.__error(token, '{')
        else:
            self.__error(token, 'variables')
    
    def __variables(self) -> None:
        token = self.__next(expected='}')
        if not token['value'] == '}':
            self.__pointer -= 1
            self.__variable()
            self.__variables()
        
    def __variable(self) -> None:
        self.__type()
        self.__dec_var()
        self.__multiple_variables_line()
    
    def __type(self) -> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string']")
        if token['key'] == 'PRE':
            if token['value'] in ['int', 'real', 'boolean', 'string']:
                return
        self.__error(found=token, expected="['int', 'real', 'boolean', 'string']")

    def __dec_var(self) -> None:    
        token = self.__next(expected="IDE")
        if token['key'] == 'IDE':
            self.__dimensions()
        else:
            self.__error(found=token, expected="IDE")

    def __dimensions(self) -> None:
        token = self.__next(expected='[')
        if token['value'] == '[':
            self.__size_dimension()
            token = self.__next(expected=']')
            if token['value'] == ']':
                self.__dimensions()
            else:
                self.__error(found=token, expected=']')
        else:
            self.__pointer -= 1

    def __size_dimension(self) -> None:
        token = self.__next(expected='[NRO, IDE]')
        if token['key'] not in ['NRO', 'IDE']:
            self.__error(found=token, expected='[NRO, IDE]')

    def __multiple_variables_line(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__dec_var()
            self.__multiple_variables_line()
        elif not token['value'] == ';':
            self.__error(found=token, expected="[',', ';']")
        

    def __class_block(self) -> None:
        token = self.__next(expected='class')
        if token['value'] == 'class':
            self.__ide_class()
        else:
            self.__error(token, 'class')
    
    def __ide_class(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__extends()
        else:
            self.__pointer -= 1
            self.__main()

    def __extends(self) -> None:
        token = self.__next(expected='extends')
        if token['value'] == 'extends':
            token = self.__next(expected='IDE')
            if token['key'] == 'IDE':
                self.__start_class_block()
            else:
                self.__error(token, 'extends')
        else:
            self.__pointer -= 1
            self.__start_class_block()

    def __start_class_block(self) -> None:
        token = self.__next(expected='{')
        if token['value'] == '{':
            self.__init_class()
        else:
            self.__error(token, '{')
    
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
                    self.__error(found=token, expected='}')
            else:
                self.__error(found=token, expected='{')
        else:
            self.__error(found=token, expected='methods')

    def __methods(self) -> None:
        token = self.__next(expected="['}', 'void', 'int', 'real', 'boolean', 'string', IDE]")
        self.__pointer -= 1
        if token['value'] in ['void', 'int', 'real', 'boolean', 'string'] or token['key'] == 'IDE':
            self.__method()
            self.__methods()

    def __method(self) -> None:
        self.__types()
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__dec_parameters()
            else:
                self.__error(found=token, expected='(')
        else:
            self.__error(found=token, expected='(')
    
    def __types(self) -> None:
        token = self.__next(expected="['void', 'int', 'real', 'boolean', 'string', IDE]")
        if not token['value'] == 'void':
            self.__pointer -= 1
            self.__type_variables()
    
    def __type_variables(self) -> None:
        token = self.__next(expected="['int', 'real', 'boolean', 'string', IDE]")
        if not token['key'] == 'IDE':
            self.__pointer -= 1
            self.__type()

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
                self.__mult_dec_parameters()
            else:
                self.__error(found=token, expected='IDE')
        else:
            self.__pointer -= 1
            self.__end_dec_parameters()
    
    def __end_dec_parameters(self) -> None:
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__method_body()
            else:
                self.__error(found=token, expected='{')
        else:
            self.__error(found=token, expected=')')
    
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
                    self.__error(found=token, expected='}')
            else:
                self.__error(found=token, expected=';')
        else:
            self.__error(found=token, expected='return')
    
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
                self.__error(found=token, expected=';')
        elif token['value'] == 'if':
            self.__if()
        elif token['value'] == 'for':
            self.__for_block()
        else:
            self.__pointer += 1
            self.__error(found=token, expected="['print', 'read', 'if', 'for', IDE]")

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
                        self.__error(found=token, expected=';')
                else:
                    self.__error(found=token, expected=';')
            else:
                self.__error(found=token, expected='(')
        else:
            self.__error(found=token, expected='for')
    
    def __conditional_expression(self) -> None:
        token = self.__next(expected="[NRO, IDE, CAC, '(']")
        if token['value'] == '(':
            self.__relational_expression()
        elif token['key'] in ['NRO', 'IDE', 'CAC']:
            self.__pointer -= 1 
            self.__relational_expression()
        else:
            self.__error(found=token, expected="[NRO, IDE, CAC, '(']")

    def __relational_expression(self) -> None:
        self.__relational_expression_value()
        token  = self.__next(expected='REL')
        if token['key'] == 'REL':
            self.__relational_expression_value()
        else:
            self.__error(found=token, expected='REL')

    def __for_increment(self) -> None:
        self.__dec_object_atribute_access()
        self.__assignment()
    
    def __assignment(self) -> None:
        token = self.__next(expected="[ART_DOUBLE, '=']")
        if token['value'] == '=':
            self.__value()
        elif token['value'] not in ['++', '--']:
            self.__error(found=token, expected="[ART_DOUBLE, '=']")
    
    def __end_for(self) -> None:
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__commands()
                token = self.__next(expected='}')
                if not token['value'] == '}':
                    self.__error(found=token, expected='}')
            else:
                self.__error(found=token, expected='{')
        else:
            self.__error(found=token, expected=')')

    def __print_begin(self) -> None:
        token = self.__next(expected='print')
        if token['value'] == 'print':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__print_end()
            else:
                self.__error(found=token, expected='(')
        else:
            self.__error(found=token, expected='print')
    
    def __print_end(self) -> None:
        self.__print_parameter()
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected=';')
            if not token['value'] == ';':
                self.__error(found=token, expected=';')
        else:
            self.__error(found=token, expected=')')
    
    def __print_parameter(self) -> None:
        token = self.__next(expected='[CAC, NRO, IDE]')
        if token['key'] not in ['CAC', 'NRO']:
            if token['key'] == 'IDE':
                self.__pointer -= 1
                self.__dec_object_atribute_access()
            else:
                self.__error(found=token, expected='[CAC, NRO, IDE]')
    
    def __read_begin(self) -> None:
        token = self.__next(expected='read')
        if token['value'] == 'read':
            token = self.__next(expected='(')
            if token['value'] == '(':
                self.__read_end()
            else:
                self.__error(found=token, expected='(')
        else:
            self.__error(found=token, expected='read')
    
    def __read_end(self) -> None:
        self.__dec_object_atribute_access()
        token = self.__next(expected=')')
        if token['value'] == ')':
            token = self.__next(expected=';')
            if not token['value'] == ';':
                self.__error(found=token, expected=';')
        else:
            self.__error(found=token, expected=')')
    
    def __object_access_or_assigment(self) -> None:
        self.__dec_object_atribute_access()
        self.__object_access_or_assigment_end()
    
    def __object_access_or_assigment_end(self) -> None:
        token = self.__next(expected='=')
        if token['value'] == '=':
            self.__value()
        elif token['value'] in ['++', '--']:
            self.__pointer -= 1
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
            self.__error(found=token, expected="[NRO, CAC, '!', '[', '(', IDE, 'true', 'false']")

    def __arithimetic_or_logical_expression_with_parentheses(self) -> None:
        self.__parentheses_begin()

    def __parentheses_begin(self) -> None:
        token = self.__next(expected='(')
        if token['value'] == '(':
            self.__expression()
            self.__parentheses_end()
        else:
            self.__error(found=token, expected='(')

    def __parentheses_end(self) -> None:
        token = self.__next(expected=')')
        if token['value'] == ')':
            self.__expressions_without_parentheses_end()
        else:
            self.__error(found=token, expected=')')
    
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
            self.__error(found=token, expected="[ART, '->', REL, LOG]")

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
            self.__error(found=token, expected='NRO')

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
                self.__error(found=token, expected=']')
        else:
            self.__error(found=token, expected='[')
    
    def __elements_assign(self) -> None:
        self.__element_assign()
        self.__multiple_elements_assign()
    
    def __element_assign(self) -> None:
        token = self.__next(expected="[IDE, CAC, NRO, '[']")
        if token['value'] == '[':
            self.__pointer -= 1
            self.__n_dimensions_assign()
        elif token['key'] not in ['CAC', 'IDE', 'NRO']:
            self.__error(found=token, expected="[IDE, CAC, NRO, '[']")
    
    def __n_dimensions_assign(self) -> None:
        token = self.__next(expected='[')
        if token['value'] == '[':
            self.__elements_assign()
            token = self.__next(expected=']')
            if not token['value'] == ']':
                self.__error(found=token, expected=']')
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
                self.__error(found=token, expected=')')
        elif token['value'] == '!':
            self.__logical_expression_begin()
        elif token['value'] in ['true', 'false', 'this'] or token['key'] == 'IDE':
            self.__pointer -= 1
            self.__logical_expression_value()
        else:
            self.__error(found=token, expected="['(', '!', 'true', 'false', IDE]")

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
                self.__error(found=token, expected="['true', 'false', IDE]")

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
            self.__error(found=token, expected="[NRO, CAC, IDE]")

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
            self.__error(found=token, expected='ART')
    
    def __part_loop(self) -> None:
        token = self.__next(expected="[IDE, NRO, '(']")
        self.__pointer -= 1
        if token['key'] in ['IDE', 'NRO'] or token['value'] == 'this':
            self.__part()
            self.__end_expression_optional()
        elif token['value'] == '(':
            self.__parentheses_expression()
        else:
            self.__error(found=token, expected="[IDE, NRO, '(']")
    
    def __parentheses_expression(self) -> None:
        token = self.__next(expected='(')
        if token['value'] == '(':
            self.__simple_expression()
            token = self.__next(expected=')')
            if token['value'] == ')':
                self.__end_expression_optional()
            else:
                self.__error(found=token, expected=')')
        else:
            self.__error(found=token, expected='(')
    
    def __simple_expression(self) -> None:
        token = self.__next(expected="[NRO, IDE, '(']")
        self.__pointer -= 1
        if token['key'] in ['NRO', 'IDE']:
            self.__part()
            self.__end_expression()
        elif token['value'] == '(':
            self.__parentheses_expression()
        else:
            self.__error(found=token, expected="[NRO, IDE, '(']")

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
                    self.__error(found=token, expected=')')
            else:
                self.__error(found=token, expected='(')
        else:
            self.__error(found=token, expected='->')
    
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
            self.__error(found=token, expected="[IDE, 'constructor']")

    def __dec_object_atribute_access(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE' or token['value'] == 'this':
            self.__dimensions()
            self.__end_object_attribute_access()
        else:
            self.__error(found=token, expected='IDE')
    
    def __end_object_attribute_access(self) -> None:
        token = self.__next(expected='.')
        if token['value'] == '.':
            self.__multiple_object_attribute_access()
        else:
            self.__pointer -= 1
    
    def __multiple_object_attribute_access(self) -> None:
        self.__dec_var()
        self.__end_object_attribute_access()

    def __objects_block(self) -> None:
        token = self.__next(expected='objects')
        if token['value'] == 'objects':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__objects()
            else:
                self.__error(found=token, expected='{')
        else:
            self.__error(found=token, expected='objects')
    
    def __objects(self) -> None:
        token = self.__next(expected="[IDE, '}']")
        if token['key'] == 'IDE':
            self.__pointer -= 1
            self.__object()
            self.__objects()
        elif not token['value'] == '}':
            self.__error(found=token, expected="[IDE, '}']")

    def __object(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            self.__dec_var()
            self.__multiple_objects()
        else:
            self.__error(found=token, expected='IDE')
    
    def __multiple_objects(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__dec_var()
            self.__multiple_objects()
        elif not token['value'] == ';':
            self.__error(found=token, expected="[',', ';']")
    

    def __variable_param(self) -> None:
        self.__type()
        token = self.__next(expected='IDE')
        if not token['key'] == 'IDE':
            self.__error(found=token, expected='IDE')

    def __object_param(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            token = self.__next(expected='IDE')
            if not token['key'] == 'IDE':
                self.__error(found=token, expected='IDE')
        else:
            self.__error(found=token, expected='IDE')

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
                        self.__error(token, '}')
                else:
                    self.__error(token, ')')
            else:
                self.__error(token, '(')
    
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
            self.__error(found=token, expected="['int', 'real', 'boolean', 'string', IDE]")
        
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
            self.__class_block()
        else:
            self.__error(token, '}')

    def __main(self) -> None:
        token = self.__next(expected='main')
        if token['value'] == 'main':
            token = self.__next(expected='{')
            if token['value'] == '{':
                self.__init_main()
            else:
                self.__error(token, '{')
        else:
            self.__error(token, 'main')

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
                self.__error(token,'{')
        else:
            self.__error(token, 'methods')
    
    def __main_methods_body(self) -> None:
        self.__main_type()
        token = self.__next(expected='main')
        if token['value'] == 'main':
            token = self.__next(expected='(')
            if token['value'] == '(':
                token = self.__next(expected=')')
                if token['value'] == ')':
                    token = self.__next(expected='{')
                    if token['value'] == '{':
                        self.__method_body()
                        self.__methods()
                    else:
                        self.__error(token, '{')
                else:
                    self.__error(token, ')')
            else:
                self.__error(token, '(')
        else:
            self.__error(token, 'main')
    
    def __main_type(self) -> None:
        token = self.__next(expected='PRE')
        if token['value'] == 'void':
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
                                self.__error(token, '}')
                        else:
                            self.__error(token, '{')
                    else:
                        self.__error(token, 'then')
                else:
                    self.__error(token, ')')
            else:
                self.__error(token, '(')
        else:
            self.__error(token, 'if')
    
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
                        self.__error(token, '}')
                else:
                    self.__error(token, '{')
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
                self.__error(token, '{')
        else:
            self.__error(token, 'const')
    
    def __consts(self) -> None:
        token = self.__next(expected='}')
        if not token['value'] == '}':
            self.__pointer -= 1
            self.__const()
            self.__consts()
    
    def __const(self) -> None:
        self.__type()
        self.__const_atribution()
        self.__multiple_consts()
    
    def __const_atribution(self) -> None:
        token = self.__next(expected='IDE')
        if token['key'] == 'IDE':
            token = self.__next(expected='=')
            if token['value'] == '=':
                self.__atribution()
            else:
                self.__error(token, '=')
        else:
            self.__error(token, 'IDE')
    
    def __multiple_consts(self) -> None:
        token = self.__next(expected="[',', ';']")
        if token['value'] == ',':
            self.__const_atribution()
            self.__multiple_consts()
        elif not token['value'] == ';':
            self.__error(token, "[',', ';']")
    
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
            self.__error(token, "[NRO, BOOL, CAC]")
    
    """
        Função que faz o papel de guardar o erro assim que ele acontece
    """
    def __error(self, found: dict, expected: str) -> None:
        self.__errors.append(f"L - {found['line'] if 'line' in found.keys() else 'EOF'}:\t Esperava {expected}, mas encontrou [{found['key']}:{found['value']}].")

    """
        Função que avança o ponteiro da lista para o próximo token
        retorna um dicionário e um boleano para indicar se a lista de tokens ainda tem tokens
    """
    def __next(self, expected: str = 'TOKEN') -> dict:
        if self.__pointer > self.__tokens_len:
            self.__error(found={'key':'EOF', 'value': 'End Of File'}, expected=expected)
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