import ply.lex as lex



class LexerTraining(object):
    tokens = [
        'COEFICIENTE',
        'DOSPUNTOS',
        'PNUMERO',
        'PUNTOYCOMA',
        'GUION',
        'COMA'
    ]

    tokens = tokens
    t_PNUMERO = r'P[0-9]+'
    t_DOSPUNTOS = r':'
    t_PUNTOYCOMA = r';'
    t_ignore = r' '
    t_COMA = r','
    t_GUION = r'-'


    def t_COEFICIENTE(self,t):
        r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?' #CUALQUIER NUMERO CON COMA FLOTANTE
        t.value = float(t.value)
        return t

    def t_error(self,t):
        print("Illegal character '%s' at line %d" % (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)
    
    def t_newline(self,t):
         r'\n+'
         t.lexer.lineno += len(t.value)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    def analyse(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)
            
# lexer = Lexer()
# lexer.build()
# f = open('data/output_test', 'r', encoding= 'utf8')
# data = f.read()
# f.close()
# lexer.analyse(data)