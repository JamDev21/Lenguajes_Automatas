# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:23:23 2025

@author: Jonathan
"""
import ply.lex as lex
import ply.yacc as yacc

# === Definición de tokens ===
tokens = ('DECIMAL_DOS',)

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

def t_DECIMAL_DOS(t):
    r'[+-]?\d+\.\d{2}'  # Expresión regular estricta: número con exactamente 2 decimales
    return t

def t_error(t):
    print("Entrada no válida")
    t.lexer.skip(len(t.value))

# === Construcción del analizador léxico ===
lexer = lex.lex()

# === Definición de la gramática ===
def p_input(p):
    '''input : DECIMAL_DOS'''
    print("Número válido con dos decimales")

def p_error(p):
    print("Entrada no válida")

# === Construcción del analizador sintáctico ===
parser = yacc.yacc()

# === Prueba del analizador ===
def main():
    while True:
        try:
            entrada = input("Ingrese un número con dos decimales: ").strip()
            
            # Validación manual para asegurar que la entrada es EXACTA
            if not entrada or not entrada.replace(".", "").replace("-", "").replace("+", "").isdigit():
                print("Entrada no válida")
                continue
            
            # Procesar la entrada
            resultado = parser.parse(entrada)
            if resultado is None:
                print("Entrada no válida")
        except EOFError:
            break

if __name__ == "__main__":
    main()
