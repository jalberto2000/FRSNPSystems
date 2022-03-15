import ply.yacc as yacc

#TOKENS DEFINIDOS EN EL ANALIZADOR LEXICO
from lexer_training import Lexer


class Parser(object):
        def build(self, lexer):
            self.lexer = lexer
            self.tokens = lexer.tokens
            self._parser = yacc.yacc(module=self)
        def p_fichero(self, p):
            '''
            fichero : results
            '''
            p[0] = p[1]
            
        def p_results(self , p):
            '''
            results : results result 
                         | result
            '''
            if len(p) == 2:
                p[0] = [p[1],]
            else:
                p[0] = p[1] + [p[2],]
        def p_result(self, p):
            '''
            result : ci GUION PNUMERO PUNTOYCOMA
            '''
            p[0] = (p[1], p[3])

        def p_ci(self, p):
            '''
            ci : ci COMA PNUMERO DOSPUNTOS COEFICIENTE
                | PNUMERO DOSPUNTOS COEFICIENTE
            '''
            if len(p) == 4:
                p[0] = [(int(p[1][1::]), int(p[3][1::]))]
            else:
                p[0] = p[1] + [(int(p[3][1::]), int(p[5][1::]))]
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
            print(res)
            return res
            


lexer = Lexer()
lexer.build()
parser = Parser()
parser.build(lexer)
f = open('data/output_test', 'r', encoding = 'utf8')
parser.parsing(f)
f.close()
