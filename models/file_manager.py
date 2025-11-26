"""
Gestionnaire de fichiers pour les opérations d'entrée/sortie
"""

import os
import json
from typing import Optional, Dict, Any


class FileManager:
    """Gère les opérations de lecture/écriture de fichiers"""
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Lit un fichier texte"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return content
        
        except UnicodeDecodeError:
            # Essai avec un encodage différent
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise IOError(f"Impossible de lire le fichier: {str(e)}")
        
        except Exception as e:
            raise IOError(f"Erreur lors de la lecture du fichier: {str(e)}")
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> bool:
        """Écrit du texte dans un fichier"""
        try:
            # Crée le répertoire parent si nécessaire
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return True
        
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture du fichier: {str(e)}")
    
    @staticmethod
    def read_binary_file(file_path: str) -> bytes:
        """Lit un fichier binaire"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas")
            
            with open(file_path, 'rb') as file:
                return file.read()
        
        except Exception as e:
            raise IOError(f"Erreur lors de la lecture du fichier binaire: {str(e)}")
    
    @staticmethod
    def write_binary_file(file_path: str, data: bytes) -> bool:
        """Écrit des données binaires dans un fichier"""
        try:
            # Crée le répertoire parent si nécessaire
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as file:
                file.write(data)
            
            return True
        
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture du fichier binaire: {str(e)}")
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
        """Retourne des informations sur un fichier"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'is_file': os.path.isfile(file_path),
                'extension': os.path.splitext(file_path)[1]
            }
        
        except Exception:
            return None
    
    @staticmethod
    def is_valid_text_file(file_path: str) -> bool:
        """Vérifie si un fichier est un fichier texte valide"""
        try:
            info = FileManager.get_file_info(file_path)
            if not info or not info['is_file']:
                return False
            
            # Vérifie la taille (évite les fichiers trop gros)
            if info['size'] > 10 * 1024 * 1024:  # 10 MB max
                return False
            
            # Essaie de lire les premiers bytes pour vérifier le texte
            with open(file_path, 'rb') as file:
                sample = file.read(1024)
                # Vérification basique de texte
                try:
                    sample.decode('utf-8')
                    return True
                except UnicodeDecodeError:
                    return False
        
        except Exception:
            return False