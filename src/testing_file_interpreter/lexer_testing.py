import ply.lex as lex



class LexerTesting(object):
    tokens = [
        'GUION',
        'NUMERO',
        'PNUMERO',
        'DOSPUNTOS',
        'COEFICIENTE',
        'PUNTOYCOMA'
    ]

    tokens = tokens
    t_GUION = r'-'
    t_PNUMERO = r'P[0-9]+'
    t_NUMERO = r'[0-9]+'
    t_DOSPUNTOS = r':'
    t_PUNTOYCOMA = r';'
    t_ignore = r' '

    def t_COEFICIENTE(self,t):
        r'[+]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?' #CUALQUIER NUMERO CON COMA FLOTANTE
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
            
# lexer = LexerTesting()
# lexer.build()
# f = open('../test/testing_values', 'r', encoding= 'utf8')
# data = f.read()
# f.close()
# lexer.analyse(data)