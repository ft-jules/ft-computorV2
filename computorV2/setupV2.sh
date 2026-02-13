#!/bin/zsh

# --- CONFIGURATION ---
ENV_NAME="computorV2"
PYTHON_VER="3.10"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
RESET='\033[0m'

# --- DÉTECTION DU CHEMIN ---
if [[ -d "/goinfre/$USER" ]]; then
    MODE="ECOLE"
    INSTALL_PATH="/goinfre/$USER/miniconda3"
else
    MODE="PERSO"
    INSTALL_PATH="$HOME/miniconda3"
fi

# --- MODE NETTOYAGE ---
if [[ "$1" == "clean" ]]; then
    echo -e "${RED}=== NETTOYAGE $ENV_NAME ($MODE) ===${RESET}"
    echo -n "Tu es sur le point de supprimer l'environnement. Continuer ? (y/N) "
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Annulé."
        exit 0
    fi

    source "$INSTALL_PATH/etc/profile.d/conda.sh" 2>/dev/null
    conda deactivate 2>/dev/null

    if [[ "$MODE" == "ECOLE" ]]; then
        # École : Suppression radicale
        if [[ -d "$INSTALL_PATH" ]]; then
            echo "Suppression totale de Miniconda dans /goinfre..."
            rm -rf "$INSTALL_PATH"
            echo -e "${GREEN}Nettoyage complet effectué (Quota libéré).${RESET}"
        else
            echo "Rien à supprimer."
        fi
    else
        # Perso : Suppression sélective
        echo "Suppression de l'environnement $ENV_NAME..."
        conda remove --name "$ENV_NAME" --all -y
        echo "Nettoyage du cache..."
        conda clean --all -y
        echo -e "${GREEN}Environnement supprimé. Miniconda est resté intact.${RESET}"
    fi
    exit 0
fi

# --- MODE INSTALLATION ---
echo -e "${BLUE}=== Setup ComputorV2 (Linux/Zsh) ===${RESET}"

if [[ "$(uname -s)" != "Linux" ]]; then
    echo -e "${RED}Erreur : Linux uniquement.${RESET}"
    exit 1
fi

if [[ "$MODE" == "ECOLE" ]]; then
    echo -e "${YELLOW}Mode École détecté : Installation dans /goinfre${RESET}"
else
    echo -e "${GREEN}Mode Perso : Installation dans $HOME${RESET}"
fi

if ! command -v conda &> /dev/null; then
    if [[ -d "$INSTALL_PATH" ]]; then
        echo "Dossier trouvé, chargement..."
        source "$INSTALL_PATH/etc/profile.d/conda.sh"
    else
        echo "Téléchargement et installation de Miniconda..."
        if command -v wget &> /dev/null; then
            wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
        else
            curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        fi
        bash miniconda.sh -b -p "$INSTALL_PATH"
        rm miniconda.sh
        source "$INSTALL_PATH/etc/profile.d/conda.sh"
        conda init zsh
    fi
else
    echo -e "${GREEN}Conda déjà installé.${RESET}"
fi

source "$INSTALL_PATH/etc/profile.d/conda.sh" 2>/dev/null || true
if conda info --envs | grep -q "$ENV_NAME"; then
    echo -e "L'environnement ${BLUE}$ENV_NAME${RESET} existe déjà."
else
    conda create --name "$ENV_NAME" python="$PYTHON_VER" -y
fi

echo "Installation outils complets..."
conda run -n "$ENV_NAME" pip install black flake8 mypy pytest numpy

echo -e "\n${GREEN}=== PRÊT ===${RESET}"
echo -e "Activer : ${BLUE}conda activate $ENV_NAME${RESET}"
echo -e "Nettoyer : ${YELLOW}./setup_v2.sh clean${RESET}"