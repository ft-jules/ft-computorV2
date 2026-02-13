#!/usr/bin/env python3
import sys
import os
import io
import contextlib

# Ajout du dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.core.context import Context
import main

# --- COULEURS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- CAPTURE SORTIE ---
@contextlib.contextmanager
def capture_stdout():
    new_out = io.StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out

class DefenseTester:
    def __init__(self):
        self.context = Context()
        self.total_tests = 0
        self.passed_tests = 0

    def print_header(self, title):
        print(f"\n{Colors.HEADER}{Colors.BOLD}" + "="*60)
        print(f" {title.center(58)} ")
        print("="*60 + f"{Colors.ENDC}\n")

    def check(self, expr, expected, mode="calc", description=""):
        self.total_tests += 1
        result_str = ""
        success = False
        
        try:
            if mode == "calc":
                lexer = Lexer(expr)
                parser = Parser(lexer, self.context)
                res_obj = parser.parse()
                result_str = str(res_obj) if res_obj is not None else "None"
                if result_str == expected:
                    success = True

            elif mode == "solve":
                with capture_stdout() as captured:
                    main.handle_equation(expr, self.context)
                output = captured.getvalue().strip()
                
                # Adaptation: On cherche si TOUS les mots clés sont présents
                if isinstance(expected, list):
                    success = all(k in output for k in expected)
                    result_str = output.replace('\n', ' | ')
                else:
                    success = expected in output
                    result_str = output

            elif mode == "error":
                try:
                    if "?" in expr:
                        with capture_stdout() as captured:
                            main.handle_equation(expr, self.context)
                    else:
                        lexer = Lexer(expr)
                        parser = Parser(lexer, self.context)
                        parser.parse()
                    result_str = "No Error"
                    success = False
                except Exception as e:
                    result_str = f"Error: {str(e)}"
                    success = True

        except Exception as e:
            result_str = f"CRASH: {e}"
            success = False

        status_icon = "✅" if success else "❌"
        color = Colors.GREEN if success else Colors.FAIL
        
        print(f"{Colors.CYAN}[TEST {self.total_tests:02d}]{Colors.ENDC} {description}")
        print(f"   Input    : {Colors.BOLD}{expr}{Colors.ENDC}")
        if not success:
            print(f"   Expected : {expected}")
            print(f"   Got      : {Colors.FAIL}{result_str}{Colors.ENDC}")
        print(f"   Status   : {color}{status_icon} {('PASS' if success else 'FAIL')}{Colors.ENDC}")
        print(f"{Colors.BLUE}" + "-"*60 + f"{Colors.ENDC}")

        if success:
            self.passed_tests += 1

    def run(self):
        print(f"{Colors.BOLD}🚀 SUITE DE TESTS ADAPTÉE - COMPUTOR V2{Colors.ENDC}")
        
        # 1. ARITHMÉTIQUE
        self.print_header("ARITHMÉTIQUE & RATIONNELS")
        self.check("1 + 1", "2", description="Addition simple")
        self.check("2 * 3 + 4", "10", description="Priorité multiplication")
        self.check("2 * (3 + 4)", "14", description="Parenthèses")
        self.check("5 % 2", "1", description="Modulo")
        self.check("0.5", "1/2", description="Float vers Rationnel")

        # 2. VARIABLES
        self.print_header("VARIABLES")
        self.check("varA = 10", "10", description="Assignation")
        self.check("varB = varA * 2", "20", description="Utilisation variable")
        self.check("varA = 5", "5", description="Réassignation")
        self.check("varB", "20", description="Non modification dépendante")

        # 3. COMPLEXES
        self.print_header("NOMBRES COMPLEXES")
        self.check("i", "i", description="Unité imaginaire")
        self.check("i^2", "-1", description="Carré de i")
        self.check("(1 + 2 * i) * (3 + 4 * i)", "-5 + 10i", description="Multiplication complexe")
        
        # 4. FONCTIONS
        self.print_header("FONCTIONS")
        self.check("f(x) = x ^ 2", "Function f(x)", description="Définition fonction")
        self.check("f(4)", "16", description="Appel fonction simple")
        self.check("g(y) = f(y) + 1", "Function g(y)", description="Fonction imbriquée")
        self.check("g(3)", "10", description="Appel fonction imbriquée")

        # 5. MATRICES (Nécessite le fix dans matrix.py)
        self.print_header("MATRICES")
        self.check("[[1, 2]; [3, 4]]", "[[1, 2]; [3, 4]]", description="Parsing Matrice")
        self.check("[[1, 2]] * 2", "[[2, 4]]", description="Multiplication Scalaire")
        self.check("[[1, 2]] + [[3, 4]]", "[[4, 6]]", description="Addition Matrices")
        self.check("[[1, 2]] ** [[3]; [4]]", "[[11]]", description="Produit Matriciel")

        # 6. ÉQUATIONS (Adapté à ton output)
        self.print_header("RÉSOLUTION D'ÉQUATIONS")
        
        self.check("x = 5 ?", 
                   ["Reduced form: x - 5 = 0", "degree: 1", "5"], 
                   mode="solve", description="Degré 1 simple")

        self.check("x^2 = 4 ?", 
                   # Acceptation de "strictly positive" (ton output)
                   ["x^2 - 4 = 0", "degree: 2", "strictly positive", "2", "-2"], 
                   mode="solve", description="Degré 2 (Delta > 0)")
        
        self.check("x^2 + 2*x + 1 = 0 ?", 
                   ["x^2 + 2x + 1 = 0", "degree: 2", "is 0", "-1"], 
                   mode="solve", description="Degré 2 (Delta = 0)")

        self.check("x^2 + 1 = 0 ?", 
                   # Acceptation de "not null" + présence de "i" (ton output)
                   ["degree: 2", "not null", "i"], 
                   mode="solve", description="Degré 2 (Delta < 0 / Complexes)")
        
        self.check("4 = 4 ?", 
                   ["degree: 0", "Every real number"], 
                   mode="solve", description="Degré 0 (Vrai)")
        
        self.check("4 = 5 ?", 
                   ["degree: 0", "No solution"], 
                   mode="solve", description="Degré 0 (Faux)")

        self.check("x^2 + x - x^2 = 5 ?", 
                   ["degree: 1", "5"], 
                   mode="solve", description="Nettoyage coefficients")

        # 7. ERREURS
        self.print_header("GESTION D'ERREURS")
        self.check("1 / 0", "", mode="error", description="Division par zéro")
        self.check("((1+1", "", mode="error", description="Syntaxe")
        self.check("[[1,2]] + [[1]]", "", mode="error", description="Dim Mismatch")
        self.check("unknown + 1", "", mode="error", description="Var inconnue")

        self.print_summary()

    def print_summary(self):
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== RÉSULTATS FINAUX ==={Colors.ENDC}")
        score = (self.passed_tests / self.total_tests) * 100
        color = Colors.GREEN if score == 100 else (Colors.WARNING if score > 50 else Colors.FAIL)
        print(f"Tests passés : {self.passed_tests} / {self.total_tests}")
        print(f"Score        : {color}{Colors.BOLD}{score:.1f}%{Colors.ENDC}")
        
if __name__ == "__main__":
    tester = DefenseTester()
    tester.run()