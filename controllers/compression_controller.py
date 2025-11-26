"""
Contrôleur principal de l'application de compression
"""

import os
import base64
from typing import Optional, Tuple
from tkinter import filedialog, messagebox

from models.compression_algorithms import CompressionManager
from models.file_manager import FileManager


class CompressionController:
    """Contrôle les opérations entre la vue et les modèles"""
    
    def __init__(self):
        self.compression_manager = CompressionManager()
        self.file_manager = FileManager()
        self.current_compressed_data: Optional[bytes] = None
        self.current_file_path: Optional[str] = None
    
    # === Gestion des algorithmes ===
    
    def get_available_algorithms(self):
        """Retourne la liste des algorithmes disponibles"""
        return self.compression_manager.get_available_algorithms()
    
    def set_algorithm(self, algorithm_name: str) -> bool:
        """Définit l'algorithme de compression actuel"""
        return self.compression_manager.set_algorithm(algorithm_name)
    
    def get_algorithm_info(self, algorithm_name: str):
        """Retourne les informations sur un algorithme"""
        return self.compression_manager.get_algorithm_info(algorithm_name)
    
    def get_current_algorithm_name(self) -> str:
        """Retourne le nom de l'algorithme actuel"""
        return self.compression_manager.current_algorithm
    
    # === Opérations sur les fichiers ===
    
    def load_text_file(self) -> Tuple[bool, str, str]:
        """Charge un fichier texte depuis le système de fichiers"""
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner un fichier texte",
                filetypes=[
                    ("Fichiers texte", "*.txt"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if not file_path:
                return False, "", "Aucun fichier sélectionné"
            
            # Validation du fichier
            if not self.file_manager.is_valid_text_file(file_path):
                return False, "", "Le fichier sélectionné n'est pas un fichier texte valide"
            
            # Lecture du fichier
            content = self.file_manager.read_text_file(file_path)
            self.current_file_path = file_path
            
            file_name = os.path.basename(file_path)
            return True, content, f"Fichier chargé: {file_name}"
        
        except Exception as e:
            return False, "", f"Erreur lors du chargement: {str(e)}"
    
    def save_compressed_file(self, compressed_data: bytes) -> Tuple[bool, str]:
        """Sauvegarde les données compressées dans un fichier"""
        try:
            if not compressed_data:
                return False, "Aucune donnée à sauvegarder"
            
            # Suggestion de nom de fichier basé sur le fichier original
            default_name = ""
            if self.current_file_path:
                base_name = os.path.splitext(self.current_file_path)[0]
                algo_name = self.get_current_algorithm_name()
                default_name = f"{base_name}_{algo_name}.comp"
            
            file_path = filedialog.asksaveasfilename(
                title="Sauvegarder les données compressées",
                defaultextension=".comp",
                initialfile=default_name,
                filetypes=[
                    ("Fichiers compressés", "*.comp"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if not file_path:
                return False, "Sauvegarde annulée"
            
            self.file_manager.write_binary_file(file_path, compressed_data)
            file_name = os.path.basename(file_path)
            return True, f"Fichier sauvegardé: {file_name}"
        
        except Exception as e:
            return False, f"Erreur lors de la sauvegarde: {str(e)}"
    
    def load_compressed_file(self) -> Tuple[bool, bytes, str]:
        """Charge un fichier compressé"""
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner un fichier compressé",
                filetypes=[
                    ("Fichiers compressés", "*.comp"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if not file_path:
                return False, b'', "Aucun fichier sélectionné"
            
            compressed_data = self.file_manager.read_binary_file(file_path)
            self.current_compressed_data = compressed_data
            
            file_name = os.path.basename(file_path)
            return True, compressed_data, f"Fichier compressé chargé: {file_name}"
        
        except Exception as e:
            return False, b'', f"Erreur lors du chargement: {str(e)}"
    
    def save_decompressed_text(self, text: str) -> Tuple[bool, str]:
        """Sauvegarde le texte décompressé"""
        try:
            if not text:
                return False, "Aucun texte à sauvegarder"
            
            file_path = filedialog.asksaveasfilename(
                title="Sauvegarder le texte décompressé",
                defaultextension=".txt",
                filetypes=[
                    ("Fichiers texte", "*.txt"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if not file_path:
                return False, "Sauvegarde annulée"
            
            self.file_manager.write_text_file(file_path, text)
            file_name = os.path.basename(file_path)
            return True, f"Texte sauvegardé: {file_name}"
        
        except Exception as e:
            return False, f"Erreur lors de la sauvegarde: {str(e)}"
    
    # === Opérations de compression/décompression ===
    
    def compress_text(self, text: str) -> Tuple[bool, bytes, float, str]:
        """Compresse le texte"""
        try:
            if not text:
                return False, b'', 0.0, "Veuillez entrer du texte à compresser"
            
            compressed_data, compression_rate = self.compression_manager.compress_text(text)
            self.current_compressed_data = compressed_data
            
            # Préparation d'un aperçu
            preview = self._get_data_preview(compressed_data)
            
            message = f"Compression réussie! Taux: {compression_rate:.2f}%"
            return True, compressed_data, compression_rate, message
        
        except Exception as e:
            return False, b'', 0.0, f"Erreur de compression: {str(e)}"
    
    def decompress_data(self, compressed_data: bytes) -> Tuple[bool, str, str]:
        """Décompresse les données"""
        try:
            if not compressed_data:
                return False, "", "Aucune donnée à décompresser"
            
            decompressed_text = self.compression_manager.decompress_data(compressed_data)
            return True, decompressed_text, "Décompression réussie!"
        
        except Exception as e:
            return False, "", f"Erreur de décompression: {str(e)}"
    
    def get_compression_stats(self, original_text: str, compressed_data: bytes) -> dict:
        """Retourne les statistiques de compression"""
        if not original_text or not compressed_data:
            return {}
        
        return self.compression_manager.get_compression_stats(original_text, compressed_data)
    
    # === Méthodes utilitaires ===
    
    def _get_data_preview(self, data: bytes, max_length: int = 100) -> str:
        """Génère un aperçu des données binaires"""
        if not data:
            return ""
        
        if len(data) <= max_length:
            preview_data = data
            suffix = ""
        else:
            preview_data = data[:max_length]
            suffix = "..."
        
        try:
            # Essaie d'encoder en base64 pour l'affichage
            preview_base64 = base64.b64encode(preview_data).decode('utf-8')
            return f"base64: {preview_base64}{suffix}"
        except:
            # Fallback: affichage hexadécimal
            preview_hex = preview_data.hex()
            return f"hex: {preview_hex}{suffix}"
    
    def get_text_stats(self, text: str) -> dict:
        """Retourne des statistiques sur le texte"""
        if not text:
            return {'length': 0, 'size_bytes': 0, 'lines': 0}
        
        return {
            'length': len(text),
            'size_bytes': len(text.encode('utf-8')),
            'lines': text.count('\n') + 1,
            'words': len(text.split())
        }