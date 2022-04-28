import ply.yacc as yacc

#TOKENS DEFINIDOS EN EL ANALIZADOR LEXICO
from lexer_exec import LexerExec


class ParserExec(object):
        def build(self, lexer):
            self.lexer = lexer
            self.tokens = lexer.tokens
            self._parser = yacc.yacc(module=self)
        def p_fichero(self, p):
            '''
            fichero : values END
            '''
            p[0] = p[1]
            
        def p_values(self , p):
            '''
            values : value_exec NEXT values 
                    | value_exec
            '''
            aux1 = [p[1]]
            if len(p) == 4:
                aux2 = []
                print(p[3])
                for l in p[3]:
                    if type(l) == tuple:
                        aux2.append(l)
                    else:
                        aux1.append(l)

                aux1.append(aux2)
                aux1.append(l)  
                p[0] = aux1
            else:
                p[0] = p[1]
        def p_value_exec(self, p):
            '''
            value_exec : neuron_value PUNTOYCOMA value_exec
                        | neuron_value PUNTOYCOMA
            '''
            if len(p) == 4:
                p[0] = [p[1]] + p[3]
            else:
                p[0] = [p[1]]

        def p_neuron_value(self, p):
            '''
            neuron_value : PNUMERO DOSPUNTOS COEFICIENTE
            '''
            p[0] = (int(p[1][1::]), float(p[3]))

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
            


lexer = LexerExec()
lexer.build()
parser = ParserExec()
parser.build(lexer)
f = open('../test/neurons_values', 'r', encoding = 'utf8')
r = parser.parsing(f)
print(r)
f.close()
