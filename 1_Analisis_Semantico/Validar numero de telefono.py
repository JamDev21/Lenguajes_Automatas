# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:51:54 2025

@author: Jonathan
"""

import ply.lex as lex
import ply.yacc as yacc

# === Definición de tokens ===
tokens = ('PHONE',)

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

# Expresión regular para un número de teléfono válido (10 dígitos o con prefijo +52)
def t_PHONE(t):
    r'(\+52)?\d{8}$'
    return t

def t_error(t):
    t.lexer.skip(len(t.value))  # Saltar caracteres inválidos

# === Construcción del analizador léxico ===
lexer = lex.lex()

# === Definición de la gramática ===
def p_input_phone(p):
    '''input : PHONE'''
    print("Número de teléfono válido")

def p_error(p):
    print("Entrada no válida")  # Evita errores de TypeError

# === Construcción del analizador sintáctico ===
parser = yacc.yacc()

# === Prueba del analizador ===
def main():
    while True:
        try:
            entrada = input("Ingrese un número de teléfono: ").strip()
            
            # Validación previa para evitar caracteres inválidos
            if not entrada.replace("+52", "").isdigit():
                print("Entrada no válida")
                continue

            # Procesar con el analizador sintáctico
            parser.parse(entrada)
        except EOFError:
            break

if __name__ == "__main__":
    main()
