import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import Optional

class CompresseurHuffman:
    """Algorithme de compression Huffman"""
    
    def __init__(self):
        self.codes = {}
    
    class Noeud:
        def __init__(self, char: str, freq: int):
            self.char = char
            self.freq = freq
            self.gauche = None
            self.droite = None
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    def _construire_frequences(self, texte: str) -> dict:
        """Calcule les fréquences des caractères"""
        frequences = {}
        for char in texte:
            frequences[char] = frequences.get(char, 0) + 1
        return frequences
    
    def _construire_arbre(self, frequences: dict):
        """Construit l'arbre de Huffman"""
        import heapq
        tas = []
        
        for char, freq in frequences.items():
            heapq.heappush(tas, (freq, self.Noeud(char, freq)))
        
        while len(tas) > 1:
            freq1, noeud1 = heapq.heappop(tas)
            freq2, noeud2 = heapq.heappop(tas)
            
            noeud_fusion = self.Noeud(None, freq1 + freq2)
            noeud_fusion.gauche = noeud1
            noeud_fusion.droite = noeud2
            
            heapq.heappush(tas, (noeud_fusion.freq, noeud_fusion))
        
        return tas[0][1] if tas else None
    
    def _generer_codes(self, noeud, code_actuel: str):
        """Génère les codes binaires"""
        if noeud is None:
            return
        
        if noeud.char is not None:
            self.codes[noeud.char] = code_actuel
            return
        
        self._generer_codes(noeud.gauche, code_actuel + "0")
        self._generer_codes(noeud.droite, code_actuel + "1")
    
    def compresser(self, texte: str) -> tuple:
        """Compresse le texte"""
        if not texte:
            return "", 0
        
        self.codes = {}
        frequences = self._construire_frequences(texte)
        racine = self._construire_arbre(frequences)
        self._generer_codes(racine, "")
        
        # Encoder le texte
        texte_encode = ''.join(self.codes[char] for char in texte)
        
        # Calculer le taux de compression
        taille_originale = len(texte.encode('utf-8')) * 8  # en bits
        taille_compressee = len(texte_encode)
        taux_compression = (1 - taille_compressee / taille_originale) * 100
        
        return texte_encode, max(0, taux_compression)
    
    def decompresser(self, texte_binaire: str, codes: dict) -> str:
        """Décompresse le texte"""
        codes_inverses = {v: k for k, v in codes.items()}
        texte_original = ""
        buffer = ""
        
        for bit in texte_binaire:
            buffer += bit
            if buffer in codes_inverses:
                texte_original += codes_inverses[buffer]
                buffer = ""
        
        return texte_original

class ApplicationCompression:
    """Application de compression avec interface graphique"""
    
    def __init__(self):
        self.fenetre = tk.Tk()
        self.compresseur = CompresseurHuffman()
        self.texte_original = ""
        self.texte_compresse = ""
        self.codes_compression = {}
        
        self.configurer_interface()
    
    def configurer_interface(self):
        """Configure l'interface graphique"""
        self.fenetre.title("Compresseur de Texte - Huffman")
        self.fenetre.geometry("700x600")
        self.fenetre.configure(bg='#f5f5f5')
        
        # Style
        style = ttk.Style()
        style.configure('Titre.TLabel', font=('Arial', 14, 'bold'), background='#f5f5f5')
        style.configure('Stats.TLabel', font=('Arial', 10, 'bold'), background='#f5f5f5')
        
        # Frame principal
        main_frame = ttk.Frame(self.fenetre, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        titre = ttk.Label(main_frame, text="🔐 COMPRESSEUR DE TEXTE", style='Titre.TLabel')
        titre.pack(pady=10)
        
        # === SECTION SAISIE ===
        section_saisie = ttk.LabelFrame(main_frame, text="1. Saisie du Texte", padding="10")
        section_saisie.pack(fill=tk.X, pady=10)
        
        # Boutons de chargement
        frame_boutons = ttk.Frame(section_saisie)
        frame_boutons.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_boutons, text="📁 Charger Fichier", 
                  command=self.charger_fichier).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="🧹 Effacer", 
                  command=self.effacer_texte).pack(side=tk.LEFT, padx=5)
        
        # Zone de texte d'entrée
        self.zone_entree = scrolledtext.ScrolledText(section_saisie, height=8, width=80)
        self.zone_entree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # === SECTION COMPRESSION ===
        section_compression = ttk.LabelFrame(main_frame, text="2. Compression", padding="10")
        section_compression.pack(fill=tk.X, pady=10)
        
        ttk.Button(section_compression, text="🎯 Compresser", 
                  command=self.compresser_texte).pack(pady=5)
        ttk.Button(section_compression, text="🔄 Décompresser", 
                  command=self.decompresser_texte).pack(pady=5)
        
        # === SECTION RÉSULTATS ===
        section_resultats = ttk.LabelFrame(main_frame, text="3. Résultats", padding="10")
        section_resultats.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Statistiques
        frame_stats = ttk.Frame(section_resultats)
        frame_stats.pack(fill=tk.X, pady=5)
        
        self.label_stats = ttk.Label(frame_stats, text="Taux de compression: --%", style='Stats.TLabel')
        self.label_stats.pack()
        
        # Zone de texte des résultats
        self.zone_resultat = scrolledtext.ScrolledText(section_resultats, height=10, width=80)
        self.zone_resultat.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # === SECTION FICHIERS ===
        section_fichiers = ttk.Frame(main_frame)
        section_fichiers.pack(fill=tk.X, pady=10)
        
        ttk.Button(section_fichiers, text="💾 Sauvegarder Compressé", 
                  command=self.sauvegarder_compresse).pack(side=tk.LEFT, padx=5)
        ttk.Button(section_fichiers, text="📤 Charger Compressé", 
                  command=self.charger_compresse).pack(side=tk.LEFT, padx=5)
    
    def charger_fichier(self):
        """Charge un fichier texte"""
        try:
            fichier = filedialog.askopenfilename(
                title="Choisir un fichier texte",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
            )
            
            if fichier:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                self.zone_entree.delete(1.0, tk.END)
                self.zone_entree.insert(1.0, contenu)
                self.texte_original = contenu
                messagebox.showinfo("Succès", f"Fichier chargé: {os.path.basename(fichier)}")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {str(e)}")
    
    def effacer_texte(self):
        """Efface le texte"""
        self.zone_entree.delete(1.0, tk.END)
        self.zone_resultat.delete(1.0, tk.END)
        self.label_stats.config(text="Taux de compression: --%")
        self.texte_original = ""
        self.texte_compresse = ""
    
    def compresser_texte(self):
        """Compresse le texte"""
        texte = self.zone_entree.get(1.0, tk.END).strip()
        
        if not texte:
            messagebox.showwarning("Attention", "Veuillez saisir du texte à compresser")
            return
        
        try:
            # Compression
            texte_binaire, taux = self.compresseur.compresser(texte)
            self.texte_compresse = texte_binaire
            self.codes_compression = self.compresseur.codes.copy()
            
            # Affichage des résultats
            self.zone_resultat.delete(1.0, tk.END)
            self.zone_resultat.insert(1.0, f"TEXTE COMPRESSÉ (binaire):\n{texte_binaire}")
            
            # Statistiques
            taille_originale = len(texte.encode('utf-8'))
            taille_compressee = (len(texte_binaire) + 7) // 8  # Approximation en bytes
            self.label_stats.config(
                text=f"Taux de compression: {taux:.2f}% | "
                     f"Original: {taille_originale} octets | "
                     f"Compressé: ~{taille_compressee} octets"
            )
            
            messagebox.showinfo("Succès", f"Compression réussie! Taux: {taux:.2f}%")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de compression: {str(e)}")
    
    def decompresser_texte(self):
        """Décompresse le texte"""
        if not self.texte_compresse or not self.codes_compression:
            messagebox.showwarning("Attention", "Aucune donnée compressée disponible")
            return
        
        try:
            texte_decompresse = self.compresseur.decompresser(
                self.texte_compresse, self.codes_compression
            )
            
            self.zone_resultat.delete(1.0, tk.END)
            self.zone_resultat.insert(1.0, f"TEXTE DÉCOMPRESSÉ:\n{texte_decompresse}")
            
            messagebox.showinfo("Succès", "Décompression réussie!")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de décompression: {str(e)}")
    
    def sauvegarder_compresse(self):
        """Sauvegarde les données compressées"""
        if not self.texte_compresse:
            messagebox.showwarning("Attention", "Aucune donnée à sauvegarder")
            return
        
        try:
            fichier = filedialog.asksaveasfilename(
                title="Sauvegarder les données compressées",
                defaultextension=".comp",
                filetypes=[("Fichiers compressés", "*.comp"), ("Tous les fichiers", "*.*")]
            )
            
            if fichier:
                # Sauvegarde simplifiée (dans un vrai projet, on sauverait les codes aussi)
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(f"CODES:{str(self.codes_compression)}\n")
                    f.write(f"DONNEES:{self.texte_compresse}")
                
                messagebox.showinfo("Succès", f"Fichier sauvegardé: {os.path.basename(fichier)}")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de sauvegarde: {str(e)}")
    
    def charger_compresse(self):
        """Charge des données compressées"""
        try:
            fichier = filedialog.askopenfilename(
                title="Charger des données compressées",
                filetypes=[("Fichiers compressés", "*.comp"), ("Tous les fichiers", "*.*")]
            )
            
            if fichier:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                # Extraction des codes et données (simplifié)
                if "CODES:" in contenu and "DONNEES:" in contenu:
                    parties = contenu.split("DONNEES:")
                    if len(parties) == 2:
                        self.texte_compresse = parties[1].strip()
                        # Dans un vrai projet, on parserait les codes correctement
                        self.codes_compression = {"a": "0", "b": "1"}  # Exemple simplifié
                        
                        self.zone_resultat.delete(1.0, tk.END)
                        self.zone_resultat.insert(1.0, f"Données compressées chargées:\n{self.texte_compresse[:100]}...")
                        
                        messagebox.showinfo("Succès", "Données compressées chargées!")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {str(e)}")
    
    def demarrer(self):
        """Démarre l'application"""
        self.fenetre.mainloop()