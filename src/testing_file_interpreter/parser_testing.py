import ply.yacc as yacc

#TOKENS DEFINIDOS EN EL ANALIZADOR LEXICO
from testing_file_interpreter.lexer_testing import LexerTesting
# from lexer_testing import LexerTesting


class ParserTesting(object):
        def build(self, lexer):
            self.lexer = lexer
            self.tokens = lexer.tokens
            self._parser = yacc.yacc(module=self)
        def p_fichero(self, p):
            '''
            fichero : coeficiente range_values
            '''
            p[0] = (p[1], p[2])
        
        def p_coeficiente(self, p):
            '''
            coeficiente : COEFICIENTE PUNTOYCOMA
            '''
            p[0] = int(p[1])
        def p_range_values(self , p):
            '''
            range_values : range_value range_values 
                    | range_value
            '''

            if len(p) == 3:
                p[0]= [p[1]] + p[2]
            else:
                p[0] = [p[1]]


        def p_range_value(self, p):
            '''
            range_value : PNUMERO DOSPUNTOS COEFICIENTE GUION COEFICIENTE PUNTOYCOMA
            '''
            p[0] = (int(p[1][1::]), (float(p[3]), float(p[5])))


        def p_error(self, p):
            print(p)
            print("Error de sintaxis en el archivo")


        def parsing(self, file):
            def get_token():
                while True:
                    tok = self.lexer.lexer.token()
                    if tok is not None: return tok
                    try:
                        line = next(file)
                        self.lexer.lexer.input(line)
                    except StopIteration:
                        return None
            res = self._parser.parse("", lexer=self.lexer.lexer, tokenfunc = get_token)
            return res
            


# lexer = LexerTesting()
# lexer.build()
# parser = ParserTesting()
# parser.build(lexer)
# f = open('../test/testing_values', 'r', encoding = 'utf8')
# r = parser.parsing(f)
# print("final")
# print(r)
# f.close()
