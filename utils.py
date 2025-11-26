"""
Fonctions utilitaires
"""

def formater_nombre(n: int) -> str:
    """Formate un nombre avec séparateurs"""
    return f"{n:,}".replace(",", " ")

def valider_cle(donnees: list, cle: str) -> bool:
    """Vérifie si la clé existe dans les données"""
    return bool(donnees) and cle in donnees[0]