# -*- coding: utf-8 -*-

"""
Created on Tue Feb  4 10:27:11 2025

@author: Jonathan
"""
import ply.lex as lex
import ply.yacc as yacc

# === Definición de tokens ===
tokens = ('ENTERO', 'ERROR')

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

def t_ENTERO(t):
    r'[+-]?\d+'  # Expresión regular para números enteros con signo opcional
    return t

def t_ERROR(t):
    r'.+'  # Cualquier otra entrada inválida
    print("Entrada no válida")
    t.lexer.skip(len(t.value))

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caracter no válido:", t.value[0])
    t.lexer.skip(1)

# === Construcción del analizador léxico ===
lexer = lex.lex()

# === Definición de la gramática ===
def p_input(p):
    '''input : ENTERO'''
    print("Número entero válido")

def p_error(p):
    print("Entrada no válida")

# === Construcción del analizador sintáctico ===
parser = yacc.yacc()

# === Prueba del analizador ===
def main():
    while True:
        try:
            entrada = input("Ingrese un número entero: ")
            parser.parse(entrada)
        except EOFError:
            break

if __name__ == "__main__":
    main()
