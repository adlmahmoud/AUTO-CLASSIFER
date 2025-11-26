"""
Définition des algorithmes de compression
"""

import pickle
import zlib
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
import heapq


class CompressionAlgorithm(ABC):
    """Interface abstraite pour les algorithmes de compression"""
    
    @abstractmethod
    def compress(self, text: str) -> bytes:
        """Compresse le texte et retourne les données binaires"""
        pass
    
    @abstractmethod
    def decompress(self, compressed_data: bytes) -> str:
        """Décompresse les données et retourne le texte original"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retourne le nom de l'algorithme"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Retourne la description de l'algorithme"""
        pass


class HuffmanNode:
    """Nœud pour l'arbre de Huffman"""
    
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self, other):
        return self.freq == other.freq


class HuffmanCompression(CompressionAlgorithm):
    """Implémentation de l'algorithme de compression Huffman"""
    
    def __init__(self):
        self.codes: Dict[str, str] = {}
    
    def get_name(self) -> str:
        return "Huffman"
    
    def get_description(self) -> str:
        return "Compression basée sur les fréquences des caractères - optimal pour le texte"
    
    def _build_frequency_dict(self, text: str) -> Dict[str, int]:
        """Construit le dictionnaire de fréquences des caractères"""
        frequency: Dict[str, int] = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency
    
    def _build_priority_queue(self, frequency: Dict[str, int]) -> List[Tuple[int, HuffmanNode]]:
        """Construit la file de priorité (tas min)"""
        heap: List[Tuple[int, HuffmanNode]] = []
        for char, freq in frequency.items():
            heapq.heappush(heap, (freq, HuffmanNode(char, freq)))
        return heap
    
    def _build_huffman_tree(self, heap: List[Tuple[int, HuffmanNode]]) -> Optional[HuffmanNode]:
        """Construit l'arbre de Huffman"""
        while len(heap) > 1:
            # Prend les deux nœuds avec les plus petites fréquences
            freq1, node1 = heapq.heappop(heap)
            freq2, node2 = heapq.heappop(heap)
            
            # Crée un nouveau nœud parent
            merged_node = HuffmanNode(None, freq1 + freq2)
            merged_node.left = node1
            merged_node.right = node2
            
            heapq.heappush(heap, (merged_node.freq, merged_node))
        
        return heap[0][1] if heap else None
    
    def _generate_codes(self, node: Optional[HuffmanNode], current_code: str):
        """Génère récursivement les codes binaires pour chaque caractère"""
        if node is None:
            return
        
        # Si c'est une feuille, stocke le code
        if node.char is not None:
            self.codes[node.char] = current_code
            return
        
        # Parcourt l'arbre récursivement
        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")
    
    def _encode_text(self, text: str) -> str:
        """Encode le texte en utilisant les codes de Huffman"""
        encoded_bits = []
        for char in text:
            if char not in self.codes:
                raise ValueError(f"Caractère '{char}' non trouvé dans les codes Huffman")
            encoded_bits.append(self.codes[char])
        return ''.join(encoded_bits)
    
    def _bits_to_bytes(self, bit_string: str) -> Tuple[bytes, int]:
        """Convertit une chaîne de bits en bytes avec padding"""
        # Ajoute du padding si nécessaire
        padding_length = 8 - (len(bit_string) % 8)
        if padding_length == 8:
            padding_length = 0
        
        bit_string += '0' * padding_length
        
        # Convertit en bytes
        bytes_list = []
        for i in range(0, len(bit_string), 8):
            byte_str = bit_string[i:i+8]
            bytes_list.append(int(byte_str, 2))
        
        return bytes(bytes_list), padding_length
    
    def _bytes_to_bits(self, data: bytes, padding_length: int) -> str:
        """Convertit les bytes en chaîne de bits"""
        bit_string = ''.join(format(byte, '08b') for byte in data)
        
        # Retire le padding
        if padding_length > 0:
            bit_string = bit_string[:-padding_length]
        
        return bit_string
    
    def compress(self, text: str) -> bytes:
        """Compresse le texte en utilisant l'algorithme de Huffman"""
        if not text:
            return b''
        
        # Réinitialise les codes
        self.codes = {}
        
        # Étape 1: Analyse des fréquences
        frequency = self._build_frequency_dict(text)
        
        # Étape 2: Construction de l'arbre de Huffman
        heap = self._build_priority_queue(frequency)
        root = self._build_huffman_tree(heap)
        
        # Étape 3: Génération des codes
        self._generate_codes(root, "")
        
        # Étape 4: Encodage du texte
        encoded_bits = self._encode_text(text)
        
        # Étape 5: Conversion en bytes
        compressed_data, padding_length = self._bits_to_bytes(encoded_bits)
        
        # Étape 6: Préparation des métadonnées
        metadata: Dict[str, Any] = {
            'codes': self.codes,
            'padding': padding_length,
            'algorithm': 'huffman'
        }
        
        # Combinaison des métadonnées et des données compressées
        result = pickle.dumps(metadata) + b'|||' + compressed_data
        return result
    
    def decompress(self, compressed_data: bytes) -> str:
        """Décompresse les données en utilisant l'algorithme de Huffman"""
        if not compressed_data:
            return ""
        
        try:
            # Séparation des métadonnées et des données
            parts = compressed_data.split(b'|||', 1)
            if len(parts) != 2:
                raise ValueError("Format de données compressées invalide")
            
            metadata_bytes, data_bytes = parts
            metadata = pickle.loads(metadata_bytes)
            
            # Vérification de l'algorithme
            if metadata.get('algorithm') != 'huffman':
                raise ValueError("Algorithme de compression incompatible")
            
            codes = metadata['codes']
            padding_length = metadata['padding']
            
            # Reconstruction du texte
            bit_string = self._bytes_to_bits(data_bytes, padding_length)
            
            # Création du mapping inverse
            reverse_codes = {v: k for k, v in codes.items()}
            
            # Décodage bit par bit
            current_bits = ""
            decoded_chars = []
            
            for bit in bit_string:
                current_bits += bit
                if current_bits in reverse_codes:
                    decoded_chars.append(reverse_codes[current_bits])
                    current_bits = ""
            
            # Vérification des bits restants
            if current_bits:
                raise ValueError("Données compressées corrompues - bits restants non décodés")
            
            return ''.join(decoded_chars)
        
        except Exception as e:
            raise ValueError(f"Erreur lors de la décompression Huffman: {str(e)}")


class ZLibCompression(CompressionAlgorithm):
    """Implémentation de la compression utilisant zlib"""
    
    def get_name(self) -> str:
        return "ZLib"
    
    def get_description(self) -> str:
        return "Compression standard utilisant la bibliothèque zlib - rapide et efficace"
    
    def compress(self, text: str) -> bytes:
        """Compresse le texte en utilisant zlib"""
        if not text:
            return b''
        
        try:
            compressed = zlib.compress(text.encode('utf-8'), level=9)
            # Ajoute un en-tête pour identifier l'algorithme
            return b'ZLIB' + compressed
        except Exception as e:
            raise ValueError(f"Erreur de compression ZLib: {str(e)}")
    
    def decompress(self, compressed_data: bytes) -> str:
        """Décompresse les données en utilisant zlib"""
        if not compressed_data:
            return ""
        
        try:
            # Vérifie l'en-tête
            if not compressed_data.startswith(b'ZLIB'):
                raise ValueError("Format ZLib invalide - en-tête manquant")
            
            # Retire l'en-tête et décompresse
            data_without_header = compressed_data[4:]
            decompressed = zlib.decompress(data_without_header)
            return decompressed.decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Erreur de décompression ZLib: {str(e)}")


class CompressionManager:
    """Gestionnaire principal des opérations de compression"""
    
    def __init__(self):
        self.algorithms: Dict[str, CompressionAlgorithm] = {}
        self.current_algorithm: Optional[str] = None
        self._initialize_algorithms()
    
    def _initialize_algorithms(self):
        """Initialise les algorithmes disponibles"""
        self.add_algorithm(HuffmanCompression())
        self.add_algorithm(ZLibCompression())
        
        # Définit Huffman comme algorithme par défaut
        if self.algorithms:
            self.current_algorithm = next(iter(self.algorithms.keys()))
    
    def add_algorithm(self, algorithm: CompressionAlgorithm):
        """Ajoute un nouvel algorithme de compression"""
        self.algorithms[algorithm.get_name().lower()] = algorithm
    
    def set_algorithm(self, algorithm_name: str) -> bool:
        """Définit l'algorithme de compression actuel"""
        algo_key = algorithm_name.lower()
        if algo_key in self.algorithms:
            self.current_algorithm = algo_key
            return True
        return False
    
    def get_current_algorithm(self) -> CompressionAlgorithm:
        """Retourne l'algorithme de compression actuel"""
        if self.current_algorithm and self.current_algorithm in self.algorithms:
            return self.algorithms[self.current_algorithm]
        raise ValueError("Aucun algorithme de compression sélectionné")
    
    def get_available_algorithms(self) -> List[str]:
        """Retourne la liste des noms d'algorithmes disponibles"""
        return list(self.algorithms.keys())
    
    def get_algorithm_info(self, algorithm_name: str) -> Dict[str, str]:
        """Retourne les informations sur un algorithme spécifique"""
        algo_key = algorithm_name.lower()
        if algo_key in self.algorithms:
            algo = self.algorithms[algo_key]
            return {
                'name': algo.get_name(),
                'description': algo.get_description()
            }
        return {}
    
    def compress_text(self, text: str) -> Tuple[bytes, float]:
        """Compresse le texte et calcule le taux de compression"""
        if not text:
            return b'', 0.0
        
        algorithm = self.get_current_algorithm()
        compressed_data = algorithm.compress(text)
        
        # Calcul du taux de compression
        original_size = len(text.encode('utf-8'))
        compressed_size = len(compressed_data)
        compression_rate = max(0, (1 - compressed_size / original_size) * 100)
        
        return compressed_data, compression_rate
    
    def decompress_data(self, compressed_data: bytes) -> str:
        """Décompresse les données"""
        if not compressed_data:
            return ""
        
        # Pour ZLib, on peut détecter par l'en-tête
        if compressed_data.startswith(b'ZLIB'):
            algorithm = self.algorithms.get('zlib')
        else:
            # Pour Huffman, on utilise l'algorithme courant ou on essaie de détecter
            algorithm = self.get_current_algorithm()
        
        return algorithm.decompress(compressed_data)
    
    def get_compression_stats(self, original_text: str, compressed_data: bytes) -> Dict[str, Any]:
        """Retourne des statistiques détaillées sur la compression"""
        original_size = len(original_text.encode('utf-8'))
        compressed_size = len(compressed_data)
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_rate': (1 - compressed_size / original_size) * 100,
            'savings': original_size - compressed_size,
            'algorithm': self.current_algorithm
        }