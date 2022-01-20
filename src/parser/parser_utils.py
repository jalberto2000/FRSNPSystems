from .formatError import *
from typing import Tuple, List
def parse_file(file:str) -> Tuple[List[str], List[str]]:
    propositions = list()
    rules = list()
    in_rules = 0
    with open(file, 'r', encoding="utf8") as f:
        if f.readline().rstrip() != 'PROPOSICIONES':
            raise formatError("No se encuentra PROPOSICIONES en el archivo")
        for line in f.readlines():
            
            if not line.isspace():
                line = line.rstrip()
                if line == "REGLAS":
                    in_rules += 1
                    if in_rules > 1:
                        raise formatError("Se ha encontrado REGLAS en mas de una ocasion")
                else:
                    if not in_rules:
                        propositions.append(parse_proposition(line))
                    else:
                        rules.append(parse_rule(line))
        if in_rules == 0:
            raise formatError("No se ha encontrado REGLAS en el archivo")
    return (propositions, rules)

#FUNCION QUE RECIBE UNA POSIBLE PROPOSICION Y DEVUELVE LA PROPOSICION Y EL VALOR DE CONFIANZA
def parse_proposition(proposition:str) -> Tuple[str, ...]:
    parts = proposition.split(':')
    if len(parts) == 2: #LA PROPOSICION ES DE ENTRADA Y CONTIENE UN VALOR DE CONFIANZA
        valor = parts[1].split("=")[1].strip()
        try:
            valor = float(valor)
        except ValueError:
            raise ValueError("El valor %s no es válido"%valor)
        return (parts[0], valor)
    elif len(parts) == 1: #LA PROPOSICION NO ES DE ENTRADA
        return tuple(parts)
    else: #LA PROPOSICION NO ESTA FORMATEAD CORRECTAMENTE
        raise formatError('la proposicion "%s" no esta bien formateada '%proposition)

#FUNCION QUE RECIBE UNA POSIBLE REGLA Y DEVUELVE LAS PROPOSICIONES IMPLICADAS Y EL VALOR DE CONFIANZA
def parse_rule(rule:str) -> Tuple[str, float]:
    parts = rule.split(':')
    if len(parts) == 2:
        valor = parts[1].split("=")[1].strip()
        try:
            valor = float(valor)
        except ValueError:
            raise ValueError("El valor %s no es válido" %valor)
        antecedent, consequent = parts[0].split("THEN")
        return (parts[0], valor)
    else: #LA PROPOSICION NO ESTA FORMATEADA CORRECTAMENTE
        raise formatError('la regla "%s" no esta bien formateada'%rule)
        