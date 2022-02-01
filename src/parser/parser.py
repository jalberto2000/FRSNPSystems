import ply.yacc as yacc

#TOKENS DEFINIDOS EN EL ANALIZADOR LEXICO
import lexer


class Parser(object):
        def build(self, lexer):
            self.lexer = lexer
            self.tokens = lexer.tokens
            self._parser = yacc.yacc(module=self)
        def p_fichero(self, p):
            '''
            fichero : PROPOSICIONES propositions REGLAS rules
            '''
            p[0] = (p[2], p[4])
            
        def p_propositions(self , p):
            '''
            propositions : propositions proposition 
                         | proposition
            '''
            if len(p) == 2:
                p[0] = [p[1],]
            else:
                p[0] = p[1] + [p[2],]
        def p_proposition(self, p):
            '''
            proposition : text DOSPUNTOS PNUMERO IGUAL COEFICIENTE PUNTOYCOMA
                        | text PUNTOYCOMA
            '''
            if len(p) == 3:
                p[0] = (p[1],)
            else:
                p[0] = (p[1], p[3], p[5])

        def p_text(self, p):
            '''
            text : text IDENT 
                 | IDENT
            '''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = p[1] +" " +p[2]
        def p_rules(self, p):
            '''
            rules : rules rule
                  | rule
            '''
            if len(p) == 2:
                p[0] = [p[1],]
            else:
                p[0] = p[1] + [p[2],]
        def p_rule(self, p):
            '''
            rule : IF union THEN PNUMERO DOSPUNTOS CNUMERO IGUAL COEFICIENTE PUNTOYCOMA
            '''
            p[0] = (p[2]+(p[4],), p[6], float(p[8]))
        
        def p_union(self, p):
            '''
            union : andunion
                  | orunion
                  | PNUMERO
            '''
            if type(p[1]) != tuple:
                p[0] = (p[1],)
            else:
                p[0] = p[1]
        def p_andunion(self, p):
            
            '''
            andunion : andunion AND andunion
                     | PNUMERO
            '''
            if len(p) == 4:
                if type(p[3])  == tuple:
                    if 'AND' not in p[3]:
                        p[0] = ('AND',p[1]) + p[3]
                    else:
                        p[0] = p[3] + (p[1],) 
                else:
                    if 'AND' not in p[1]:
                        p[0] = ('AND', p[1], p[3])
                    else:
                        p[0] = (p[1], p[3])
            else:
                p[0] = p[1]
        
        def p_orunion(self, p):
            '''
            orunion : orunion OR orunion
                    | PNUMERO
            '''
            if len(p) == 4:
                if type(p[3])  == tuple:
                    if 'OR' not in p[3]:
                        p[0] = ('OR',p[1]) + p[3]
                    else:
                        p[0] = p[3] + (p[1],) 
                else:
                    if 'OR' not in p[1]:
                        p[0] = ('OR', p[1], p[3])
                    else:
                        p[0] = (p[1], p[3])
            else:
                p[0] = p[1]

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
lexer = lexer.AnalizadorLexico()
lexer.build()
parser = Parser()
parser.build(lexer)
f = open('../test/sistema', 'r', encoding = 'utf8')
parser.parsing(f)
