#!/bin/bash

# --- Couleurs pour un affichage propre ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

# Nom de ton programme python
PROGRAM="computor.py"

# Fonction pour lancer un test
# Arg 1 : Description du test
# Arg 2 : L'équation
run_test() {
    echo -e "${BLUE}-------------------------------------------------------------${RESET}"
    echo -e "${BOLD}TEST : $1${RESET}"
    echo -e "Equation : ${GREEN}$2${RESET}"
    echo -e "${BLUE}--- Résultat ---${RESET}"
    
    # On lance python et on affiche la sortie
    python3 "$PROGRAM" "$2"
    
    echo "" # Saut de ligne
}

# Vérification que le fichier python existe
if [ ! -f "$PROGRAM" ]; then
    echo -e "${RED}Erreur : Le fichier $PROGRAM est introuvable !${RESET}"
    exit 1
fi

echo -e "${BOLD}=== LANCEMENT DE LA BATTERIE DE TESTS COMPUTOR V1 ===${RESET}\n"

# --- SCÉNARIOS DE TESTS ---

# 1. Exemple du sujet (Delta > 0)
# Attendu : Degré 2, Discriminant positif, 2 solutions (~0.90 et ~-0.47)
run_test "Exemple Sujet (Delta > 0)" "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# 2. Exemple du sujet (Degré 1)
# Attendu : Degré 1, Solution unique (-0.25)
run_test "Exemple Sujet (Degré 1)" "5 * X^0 + 4 * X^1 = 4 * X^0"

# 3. Exemple du sujet (Degré 2, Delta < 0)
# Attendu : Degré 2, Solutions complexes avec 'i'
run_test "Exemple Sujet (Delta < 0)" "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"

# 4. Cas Delta = 0 (Identité remarquable)
# (X+1)^2 = X^2 + 2X + 1. Donc X^2 + 2X + 1 = 0 a une solution double (-1)
# Attendu : Degré 2, Discriminant nul, 1 solution (-1)
run_test "Delta = 0 (Solution unique)" "1 * X^0 + 2 * X^1 + 1 * X^2 = 0"

# 5. Cas Impossible (Degré 0)
# Attendu : Degré 0, Pas de solution
run_test "Impossible (4 = 0)" "4 * X^0 = 0"

# 6. Cas Toujours Vrai (Degré 0)
# Attendu : Degré 0, Tous les réels sont solutions
run_test "Toujours Vrai (0 = 0)" "4 * X^0 = 4 * X^0"

# 7. Cas Degré trop élevé (si tu l'as géré)
# Attendu : Degré 3, Message d'erreur poli
run_test "Degré 3 (Trop haut)" "1 * X^3 + 2 * X^0 = 0"



echo -e "${GREEN}=== FIN DES TESTS ===${RESET}"