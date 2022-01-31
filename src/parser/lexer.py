import ply.lex as lex



class AnalizadorLexico(object):
    tokens = [
        'IDENT',
        'COEFICIENTE',
        'NUMERO',
        'DOSPUNTOS',
        'IGUAL',
        'PNUMERO',
        'CNUMERO',
        'PUNTOYCOMA'
    ]


    reserved = {
        'PROPOSICIONES' : 'PROPOSICIONES',
        'REGLAS' : 'REGLAS',
        'THEN' : 'THEN',
        'AND' : 'AND',
        'OR' : 'OR',
        'IF' : 'IF',
    }
    tokens = tokens +list(reserved.values())
    t_PNUMERO = r'¬?P[0-9]+'
    t_CNUMERO = r'C[0-9]+'
    t_DOSPUNTOS = r':'
    t_PUNTOYCOMA = r';'
    t_IGUAL = r'='
    t_ignore = r' '
    

    def t_IDENT(self,t):
        r'[a-zA-Z\’][a-zA-Z\’]*(?![0-9])' #CUALQUIER PALABRA QUE NO TENGA UN NUMERO JUSTO DETRAS
        t.type = self.reserved.get(t.value, 'IDENT') #SI SE DETECTA UNA PALABRA RESERVADA SE CAMBIA SU TIPO
        return t

    def t_NUMERO(self,t):
        r'(?<![\d.])[0-9]+(?![\d.])' #CUALQUIER NUMERO SIN COMA FLOTANTE
        t.value = int(t.value)
        return t

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
            
# lexer = AnalizadorLexico()
# lexer.build()
# f = open('../test/sistema', 'r', encoding= 'utf8')
# data = f.read()
# f.close()
# lexer.analyse(data)