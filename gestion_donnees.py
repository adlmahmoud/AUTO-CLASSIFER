"""
Gestion du chargement et sauvegarde des données
"""

import csv
import json
import os
from typing import List, Dict, Any


class GestionnaireDonnees:
    """Gère toutes les opérations sur les données"""
    
    @staticmethod
    def charger_csv(chemin: str) -> List[Dict[str, Any]]:
        """Charge les données depuis un fichier CSV"""
        try:
            with open(chemin, 'r', encoding='utf-8') as fichier:
                lecteur = csv.DictReader(fichier)
                return [dict(ligne) for ligne in lecteur]
        except FileNotFoundError:
            raise Exception(f"Fichier non trouvé: {chemin}")
        except Exception as e:
            raise Exception(f"Erreur CSV: {str(e)}")
    
    @staticmethod
    def charger_json(chemin: str) -> List[Dict[str, Any]]:
        """Charge les données depuis un fichier JSON"""
        try:
            with open(chemin, 'r', encoding='utf-8') as fichier:
                data = json.load(fichier)
                return data if isinstance(data, list) else [data]
        except FileNotFoundError:
            raise Exception(f"Fichier non trouvé: {chemin}")
        except json.JSONDecodeError:
            raise Exception("Fichier JSON invalide")
        except Exception as e:
            raise Exception(f"Erreur JSON: {str(e)}")
    
    @staticmethod
    def analyser_donnees(donnees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse les données et retourne les métadonnées"""
        if not donnees:
            return {"cles": [], "total": 0}
        
        return {
            "cles": list(donnees[0].keys()),
            "total": len(donnees),
            "exemple": donnees[0] if donnees else {}
        }
    
    @staticmethod
    def formater_tableau(donnees: List[Dict[str, Any]], limite: int = 20) -> str:
        """Formate les données en tableau lisible"""
        if not donnees:
            return "Aucune donnée à afficher"
        
        entetes = list(donnees[0].keys())
        lignes = []
        
        # Ligne d'en-tête
        ligne_entete = " | ".join(f"{entete:>15}" for entete in entetes)
        lignes.append(ligne_entete)
        lignes.append("-" * len(ligne_entete))
        
        # Lignes de données
        for item in donnees[:limite]:
            ligne = " | ".join(f"{str(item.get(entete, '')):>15}" for entete in entetes)
            lignes.append(ligne)
        
        if len(donnees) > limite:
            lignes.append(f"... et {len(donnees) - limite} autres lignes")
        
        return "\n".join(lignes)