#!/usr/bin/env python3
"""
Programme de Tri de Données
Point d'entrée principal
"""

from interface import ApplicationTri

def main():
    """Lance l'application de tri"""
    app = ApplicationTri()
    app.demarrer()

if __name__ == "__main__":
    main()