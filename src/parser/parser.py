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
            rule : IF PNUMERO THEN PNUMERO DOSPUNTOS CNUMERO IGUAL COEFICIENTE PUNTOYCOMA 
                 | IF PNUMERO union THEN PNUMERO DOSPUNTOS CNUMERO IGUAL COEFICIENTE PUNTOYCOMA
            '''
            if len(p) == 10:
                p[0] = ((p[2],), p[4], float(p[8]))
            else:
                p[0] = ((p[2],)+p[3], p[5], float(p[9]))
        
        def p_union(self, p):
            '''
            union : andunion
                 | orunion
            '''
            p[0] = p[1]
        def p_andunion(self, p):
            '''
            andunion : AND PNUMERO andunion 
                     | AND PNUMERO
                     | AND PNUMERO orunion
            '''
            if len(p) == 3:
                p[0] = (p[1],p[2],)
            else:
                p[0] = (p[1],p[2],) + p[3]
        
        def p_orunion(self, p):
            '''
            orunion : OR PNUMERO orunion
                    | OR PNUMERO
                    | OR PNUMERO andunion
            '''
            if len(p) == 3:
                p[0] = (p[1],p[2],)
            else:
                p[0] = (p[1],p[2],) + p[3]
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
