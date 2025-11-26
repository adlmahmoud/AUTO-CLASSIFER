"""
Implémentation des algorithmes de tri avec statistiques
"""

import time
from typing import List, Dict, Any, Tuple


class StatistiquesTri:
    """Stocke les statistiques d'exécution du tri"""
    
    def __init__(self):
        self.temps = 0.0
        self.comparaisons = 0
        self.permutations = 0
        self.algorithme = ""
        self.ordre = ""
    
    def __str__(self) -> str:
        return (f"Algorithme: {self.algorithme}\n"
                f"Ordre: {self.ordre}\n"
                f"Temps: {self.temps:.6f}s\n"
                f"Comparaisons: {self.comparaisons}\n"
                f"Permutations: {self.permutations}")


class TriInsertion:
    """Implémentation du tri par insertion"""
    
    @staticmethod
    def trier(donnees: List[Dict[str, Any]], cle: str, croissant: bool = True) -> Tuple[List[Dict[str, Any]], StatistiquesTri]:
        """Tri par insertion avec statistiques"""
        stats = StatistiquesTri()
        stats.algorithme = "Tri par Insertion"
        stats.ordre = "Croissant" if croissant else "Décroissant"
        
        if not donnees:
            return donnees, stats
        
        donnees_triees = donnees.copy()
        debut = time.time()
        
        for i in range(1, len(donnees_triees)):
            element = donnees_triees[i]
            j = i - 1
            
            while j >= 0:
                stats.comparaisons += 1
                
                valeur_j = donnees_triees[j][cle]
                valeur_element = element[cle]
                
                # Gestion des types différents
                try:
                    if croissant:
                        condition = valeur_j > valeur_element
                    else:
                        condition = valeur_j < valeur_element
                except TypeError:
                    # Si comparaison impossible, on convertit en string
                    if croissant:
                        condition = str(valeur_j) > str(valeur_element)
                    else:
                        condition = str(valeur_j) < str(valeur_element)
                
                if condition:
                    stats.permutations += 1
                    donnees_triees[j + 1] = donnees_triees[j]
                    j -= 1
                else:
                    break
            
            donnees_triees[j + 1] = element
        
        stats.temps = time.time() - debut
        return donnees_triees, stats


class TriBulles:
    """Implémentation du tri à bulles"""
    
    @staticmethod
    def trier(donnees: List[Dict[str, Any]], cle: str, croissant: bool = True) -> Tuple[List[Dict[str, Any]], StatistiquesTri]:
        """Tri à bulles avec statistiques"""
        stats = StatistiquesTri()
        stats.algorithme = "Tri à Bulles"
        stats.ordre = "Croissant" if croissant else "Décroissant"
        
        if not donnees:
            return donnees, stats
        
        donnees_triees = donnees.copy()
        n = len(donnees_triees)
        debut = time.time()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                stats.comparaisons += 1
                
                valeur_j = donnees_triees[j][cle]
                valeur_j1 = donnees_triees[j + 1][cle]
                
                try:
                    if croissant:
                        condition = valeur_j > valeur_j1
                    else:
                        condition = valeur_j < valeur_j1
                except TypeError:
                    if croissant:
                        condition = str(valeur_j) > str(valeur_j1)
                    else:
                        condition = str(valeur_j) < str(valeur_j1)
                
                if condition:
                    stats.permutations += 1
                    donnees_triees[j], donnees_triees[j + 1] = donnees_triees[j + 1], donnees_triees[j]
        
        stats.temps = time.time() - debut
        return donnees_triees, stats


class GestionnaireAlgorithmes:
    """Gestionnaire des algorithmes de tri disponibles"""
    
    ALGORITHMES = {
        "insertion": ("Tri par Insertion", TriInsertion.trier),
        "bulles": ("Tri à Bulles", TriBulles.trier)
    }
    
    @classmethod
    def obtenir_algorithmes(cls):
        """Retourne la liste des algorithmes disponibles"""
        return cls.ALGORITHMES
    
    @classmethod
    def trier(cls, algo_id: str, donnees: List[Dict[str, Any]], cle: str, croissant: bool = True):
        """Exécute l'algorithme de tri spécifié"""
        if algo_id not in cls.ALGORITHMES:
            raise ValueError(f"Algorithme inconnu: {algo_id}")
        
        nom, fonction = cls.ALGORITHMES[algo_id]
        return fonction(donnees, cle, croissant)