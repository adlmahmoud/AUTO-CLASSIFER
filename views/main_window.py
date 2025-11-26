"""
Interface graphique principale de l'application
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import tkinter.messagebox as messagebox

from controllers.compression_controller import CompressionController


class CompressionApp:
    """Fenêtre principale de l'application de compression"""
    
    def __init__(self, root):
        self.root = root
        self.controller = CompressionController()
        
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
        
        # État de l'application
        self.current_compressed_data = None
    
    def setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title("Compresseur de Texte Avancé")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Style
        self.setup_styles()
    
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        
        # Configuration des styles de base
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Arial', 9))
        style.configure('TButton', font=('Arial', 9))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Stats.TLabel', font=('Arial', 9, 'bold'))
        
        # Style pour les zones de texte
        self.root.option_add('*Text.Background', 'white')
        self.root.option_add('*Text.Foreground', 'black')
        self.root.option_add('*Text.Font', ('Arial', 9))
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration de la grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)  # Zone de sortie
        
        # === En-tête ===
        header_label = ttk.Label(main_frame, text="Compresseur de Texte", 
                                style='Header.TLabel')
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # === Sélection d'algorithme ===
        algo_frame = ttk.LabelFrame(main_frame, text="Paramètres de Compression", padding="10")
        algo_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        algo_frame.columnconfigure(1, weight=1)
        
        ttk.Label(algo_frame, text="Algorithme:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.algorithm_var = tk.StringVar()
        self.algorithm_combo = ttk.Combobox(algo_frame, 
                                          textvariable=self.algorithm_var,
                                          state="readonly")
        self.algorithm_combo['values'] = self.controller.get_available_algorithms()
        self.algorithm_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.algorithm_combo.set(self.controller.get_current_algorithm_name())
        
        # Description de l'algorithme
        self.algo_description_var = tk.StringVar()
        algo_desc_label = ttk.Label(algo_frame, textvariable=self.algo_description_var,
                                   wraplength=400, foreground='#666666')
        algo_desc_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.update_algorithm_description()
        
        # === Zone de texte d'entrée ===
        input_frame = ttk.LabelFrame(main_frame, text="Texte à Compresser", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, width=80, height=12,
                                                   font=('Consolas', 9))
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Boutons de contrôle ===
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Boutons de fichier
        file_buttons = [
            ("Charger Fichier Texte", self.load_text_file),
            ("Sauvegarder Texte", self.save_text),
        ]
        
        for i, (text, command) in enumerate(file_buttons):
            ttk.Button(control_frame, text=text, command=command).grid(
                row=0, column=i, padx=5)
        
        # Boutons de compression
        compression_buttons = [
            ("Compresser", self.compress_text),
            ("Décompresser", self.decompress_data),
        ]
        
        for i, (text, command) in enumerate(compression_buttons, start=len(file_buttons)):
            ttk.Button(control_frame, text=text, command=command).grid(
                row=0, column=i, padx=5)
        
        # Boutons de fichiers compressés
        compressed_file_buttons = [
            ("Sauvegarder Compressé", self.save_compressed_file),
            ("Charger Compressé", self.load_compressed_file),
        ]
        
        for i, (text, command) in enumerate(compressed_file_buttons, start=len(file_buttons) + len(compression_buttons)):
            ttk.Button(control_frame, text=text, command=command).grid(
                row=0, column=i, padx=5)
        
        # === Statistiques ===
        stats_frame = ttk.LabelFrame(main_frame, text="Statistiques", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configuration de la grille des statistiques
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # Labels de statistiques
        self.stats_vars = {
            'original': tk.StringVar(value="Taille originale: -"),
            'compressed': tk.StringVar(value="Taille compressée: -"),
            'rate': tk.StringVar(value="Taux de compression: -"),
            'savings': tk.StringVar(value="Économie: -")
        }
        
        ttk.Label(stats_frame, textvariable=self.stats_vars['original'], 
                 style='Stats.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.stats_vars['compressed'], 
                 style='Stats.TLabel').grid(row=0, column=1, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.stats_vars['rate'], 
                 style='Stats.TLabel').grid(row=0, column=2, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.stats_vars['savings'], 
                 style='Stats.TLabel').grid(row=0, column=3, sticky=tk.W)
        
        # === Zone de texte de sortie ===
        output_frame = ttk.LabelFrame(main_frame, text="Résultat", padding="10")
        output_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=12,
                                                    font=('Consolas', 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Barre de statut ===
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, style='TLabel')
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def setup_bindings(self):
        """Configure les liaisons d'événements"""
        self.algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_changed)
        
        # Mise à jour des statistiques du texte en temps