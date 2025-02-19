# Importación de librerías PLY para construir el lexer y parser
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# =============================================================================
# 1. ANALIZADOR LÉXICO (LEXER)
# =============================================================================

# Definición de tokens (unidades léxicas que reconocerá el lexer)
tokens = [
    'NUMBER',    # Números enteros o decimales
    'PLUS',      # Operador suma (+)
    'MINUS',     # Operador resta (-)
    'TIMES',     # Operador multiplicación (*)
    'DIVIDE',    # Operador división (/)
    'LPAREN',    # Paréntesis izquierdo (
    'RPAREN',    # Paréntesis derecho )
    'ID'         # Identificadores (texto no válido en este contexto)
]

# Expresiones regulares para tokens simples (operadores y paréntesis)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Función para reconocer identificadores (ej: variables como 'texto')
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Cualquier palabra que empiece con letra o _
    print(f"Error léxico: Identificador no válido '{t.value}'")
    t.lexer.skip(len(t.value))  # Omite el identificador completo para evitar múltiples errores
    return None  # No retorna token válido

# Función para reconocer números (enteros o decimales)
def t_NUMBER(t):
    r'\d+\.?\d*'  # Ej: 123, 45.67
    # Convierte el valor a int o float según corresponda
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Caracteres a ignorar (espacios, tabs, saltos de línea)
t_ignore = ' \t\n'

# Manejo de errores léxicos (caracteres no reconocidos)
def t_error(t):
    print(f"Error léxico: Carácter no válido '{t.value[0]}'")
    t.lexer.skip(1)  # Omite el carácter problemático

# Construcción del lexer
lexer = lex.lex()

# =============================================================================
# 2. ANALIZADOR SINTÁCTICO/SEMÁNTICO (PARSER) Y AST
# =============================================================================

# Clases para representar el Árbol de Sintaxis Abstracta (AST)
class BinOp:
    """Nodo para operaciones binarias """
    def __init__(self, left, op, right):
        self.left = left   # Subárbol izquierdo
        self.op = op       # Operador (+, -, *, /)
        self.right = right # Subárbol derecho

class Number:
    """Nodo para valores numéricos."""
    def __init__(self, value):
        self.value = value  # Valor numérico (int o float)

# Reglas de precedencia y asociatividad de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),   # + y - tienen menor precedencia y son asociativos por la izquierda
    ('left', 'TIMES', 'DIVIDE'), # * y / tienen mayor precedencia y son asociativos por la izquierda
)

# Reglas gramaticales para construir el AST
def p_expression_binop(p):
    '''
   expression : expression PLUS term
              | expression MINUS term
   '''
    # Construye nodo BinOp para operaciones + y -
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_term(p):
    'expression : term'
    # Un término simple es también una expresión
    p[0] = p[1]

def p_term_binop(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
    '''
    # Construye nodo BinOp para operaciones * y /
    p[0] = BinOp(p[1], p[2], p[3])

def p_term_factor(p):
    'term : factor'
    # Un factor simple es también un término
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    # Construye nodo Number para valores numéricos
    p[0] = Number(p[1])

def p_factor_parens(p):
    'factor : LPAREN expression RPAREN'
    # Los paréntesis devuelven la expresión interna directamente
    p[0] = p[2]

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico: la expresión está incompleta")
    parser.success = False  # Indica que hay un error

# Construcción del parser
parser = yacc.yacc()

# =============================================================================
# 3. FUNCIONES PARA MANIPULAR EL AST
# =============================================================================

def print_ast(node, level=0):
    """Imprime el AST con formato de árbol."""
    indent = '  ' * level
    if isinstance(node, BinOp):
        print(f"{indent}BinOp({node.op})")
        print_ast(node.left, level + 1)   # Subárbol izquierdo
        print_ast(node.right, level + 1)  # Subárbol derecho
    elif isinstance(node, Number):
        print(f"{indent}Number({node.value})")

def evaluate_ast(node):
    """Evalúa recursivamente el AST y retorna el resultado numérico."""
    if isinstance(node, BinOp):
        left = evaluate_ast(node.left)
        right = evaluate_ast(node.right)
        # Realiza la operación según el tipo
        if node.op == '+': return left + right
        elif node.op == '-': return left - right
        elif node.op == '*': return left * right
        elif node.op == '/': return left / right
    elif isinstance(node, Number):
        return node.value  # Valor numérico directo


def build_graphical_ast(node, parent=None):
    """Convierte el AST en una estructura de anytree para visualización."""
    if isinstance(node, BinOp):
        current_node = Node(f"BinOp({node.op})", parent=parent)
        build_graphical_ast(node.left, parent=current_node)
        build_graphical_ast(node.right, parent=current_node)
    elif isinstance(node, Number):
        Node(f"Number({node.value})", parent=parent)
    return current_node if parent is None else None

import os
import subprocess
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"
def plot_ast(root_node, filename="ast"):
    
    """Genera un archivo PNG del AST usando Graphviz."""
    from anytree.exporter import DotExporter
    
    print("Generando AST en formato .dot...")
    
    dot_filename = f"{filename}.dot"
    png_filename = f"{filename}.png"

    # Genera el archivo .dot
    DotExporter(root_node,
                nodeattrfunc=lambda node: f'label="{node.name}"',
                edgeattrfunc=lambda parent, child: "dir=none"
    ).to_dotfile(dot_filename)

    print(f"Archivo .dot generado en: {dot_filename}")

    # Ejecuta Graphviz manualmente
    try:
        subprocess.run(["dot", dot_filename, "-Tpng", "-o", png_filename], check=True)
        print(f"¡AST generado como archivo '{png_filename}'!")
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar Graphviz:", e)

# =============================================================================
# 4. EJEMPLO DE USO
# =============================================================================

data = "6 + 4 * 2"  # Expresión 

# Proceso de análisis léxico
lexer.input(data)
print("=== Tokens reconocidos ===")
try:
    for token in lexer:
        print(token)  # Imprime cada token reconocido
except lex.LexError:
    pass  # Los errores ya fueron manejados por t_error

# Proceso de análisis sintáctico/semántico
parser.success = True  # Suponemos éxito inicialmente
ast = parser.parse(data, lexer=lexer)  # Construye el AST

# Impresión del AST (solo si no hay errores)
print("\n=== Árbol de Sintaxis Abstracta (AST) ===")
if parser.success and ast is not None:
    print_ast(ast)
else:
    print("No se pudo construir el AST debido a errores.")

# Evaluación de la expresión (solo si el AST es válido)
print("\n=== Resultado de la operación ===")
if parser.success and ast is not None:
    result = evaluate_ast(ast)
    print(f"{data} = {result}")
    # Generar representación gráfica
    graphical_ast_root = build_graphical_ast(ast)
    plot_ast(graphical_ast_root)
    print("\n¡AST generado como archivo 'ast.png'!")
else:
    print(f"Operación no válida: '{data}' contiene errores léxicos/sintácticos.")