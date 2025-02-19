# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:44:29 2025

@author: Jonathan
"""

import ply.lex as lex
import ply.yacc as yacc

# === Definición de tokens ===
tokens = ('EMAIL',)

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

# Expresión regular para un correo electrónico válido
def t_EMAIL(t):
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return t

def t_error(t):
    t.lexer.skip(len(t.value))  # Saltar caracteres inválidos

# === Construcción del analizador léxico ===
lexer = lex.lex()

# === Definición de la gramática ===
def p_input_email(p):
    '''input : EMAIL'''
    p[0] = "Correo electrónico válido"

def p_error(p):
    p[0] = "Entrada no válida"

# === Construcción del analizador sintáctico ===
parser = yacc.yacc()

# === Prueba del analizador ===
def main():
    while True:
        try:
            entrada = input("Ingrese un correo electrónico: ").strip()
            
            # Validación manual rápida antes de yacc (para evitar errores de sintaxis)
            if "@" not in entrada or "." not in entrada.split("@")[-1]:
                print("Entrada no válida")
                continue
            
            # Procesar con el analizador sintáctico
            resultado = parser.parse(entrada)
            if resultado:
                print(resultado)
        except EOFError:
            break

if __name__ == "__main__":
    main()
