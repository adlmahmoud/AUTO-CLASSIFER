"""
Interface graphique Tkinter pour l'application de tri
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import List, Dict, Any

from gestion_donnees import GestionnaireDonnees
from algorithmes import GestionnaireAlgorithmes


class ApplicationTri:
    """Application principale avec interface graphique"""
    
    def __init__(self):
        self.racine = tk.Tk()
        self.donnees_chargees: List[Dict[str, Any]] = []
        self.donnees_triees: List[Dict[str, Any]] = []
        self.cles_disponibles: List[str] = []
        
        self._configurer_fenetre()
        self._creer_widgets()
    
    def _configurer_fenetre(self):
        """Configure la fenêtre principale"""
        self.racine.title("📊 Application de Tri de Données")
        self.racine.geometry("900x750")
        self.racine.configure(bg='#f8f9fa')
    
    def _creer_widgets(self):
        """Crée tous les widgets de l'interface"""
        style = ttk.Style()
        style.configure('Titre.TLabel', font=('Arial', 16, 'bold'), background='#f8f9fa')
        style.configure('Section.TLabelframe', font=('Arial', 11, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.racine, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== SECTION TITRE =====
        titre = ttk.Label(main_frame, text="🎯 TRI DE DONNÉES", style='Titre.TLabel')
        titre.pack(pady=10)
        
        # ===== SECTION CHARGEMENT =====
        section_chargement = ttk.LabelFrame(main_frame, text="1. Chargement des Données", 
                                          padding=15, style='Section.TLabelframe')
        section_chargement.pack(fill=tk.X, pady=10)
        
        # Boutons de chargement
        frame_boutons = ttk.Frame(section_chargement)
        frame_boutons.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame_boutons, text="📁 CSV", 
                  command=self._charger_csv, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="📄 JSON", 
                  command=self._charger_json, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="✍️ Manuel", 
                  command=self._saisir_manuel, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="🧹 Effacer", 
                  command=self._effacer_donnees, width=12).pack(side=tk.LEFT, padx=5)
        
        # Statut
        self.label_statut = ttk.Label(section_chargement, 
                                     text="Aucune donnée chargée", 
                                     font=('Arial', 10))
        self.label_statut.pack(pady=5)
        
        # Données brutes
        ttk.Label(section_chargement, text="Données chargées:").pack(anchor=tk.W)
        self.texte_donnees = scrolledtext.ScrolledText(section_chargement, height=8, width=100)
        self.texte_donnees.pack(fill=tk.X, pady=5)
        
        # ===== SECTION CONFIGURATION TRI =====
        section_config = ttk.LabelFrame(main_frame, text="2. Configuration du Tri", 
                                      padding=15, style='Section.TLabelframe')
        section_config.pack(fill=tk.X, pady=10)
        
        # Critère
        frame_critere = ttk.Frame(section_config)
        frame_critere.pack(fill=tk.X, pady=5)
        ttk.Label(frame_critere, text="Critère:", width=10).pack(side=tk.LEFT)
        self.combo_critere = ttk.Combobox(frame_critere, state="readonly", width=30)
        self.combo_critere.pack(side=tk.LEFT, padx=5)
        
        # Ordre
        frame_ordre = ttk.Frame(section_config)
        frame_ordre.pack(fill=tk.X, pady=5)
        ttk.Label(frame_ordre, text="Ordre:", width=10).pack(side=tk.LEFT)
        self.ordre_var = tk.StringVar(value="croissant")
        ttk.Radiobutton(frame_ordre, text="Croissant ↗", 
                       variable=self.ordre_var, value="croissant").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_ordre, text="Décroissant ↘", 
                       variable=self.ordre_var, value="decroissant").pack(side=tk.LEFT, padx=10)
        
        # Algorithme
        frame_algo = ttk.Frame(section_config)
        frame_algo.pack(fill=tk.X, pady=5)
        ttk.Label(frame_algo, text="Algorithme:", width=10).pack(side=tk.LEFT)
        self.algo_var = tk.StringVar(value="insertion")
        ttk.Radiobutton(frame_algo, text="Tri par Insertion", 
                       variable=self.algo_var, value="insertion").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_algo, text="Tri à Bulles", 
                       variable=self.algo_var, value="bulles").pack(side=tk.LEFT, padx=10)
        
        # Bouton trier
        ttk.Button(section_config, text="🎯 Lancer le Tri", 
                  command=self._executer_tri, style='Accent.TButton').pack(pady=10)
        
        # ===== SECTION RÉSULTATS =====
        section_resultats = ttk.LabelFrame(main_frame, text="3. Résultats du Tri", 
                                         padding=15, style='Section.TLabelframe')
        section_resultats.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Statistiques
        self.label_stats = ttk.Label(section_resultats, 
                                    text="Aucun tri effectué", 
                                    font=('Arial', 10, 'bold'),
                                    foreground='#2c5aa0')
        self.label_stats.pack(pady=5)
        
        
        # Résultats
        ttk.Label(section_resultats, text="Données triées:").pack(anchor=tk.W)
        self.texte_resultats = scrolledtext.ScrolledText(section_resultats, height=20, width=100)
        self.texte_resultats.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _charger_csv(self):
        """Charge un fichier CSV"""
        try:
            fichier = filedialog.askopenfilename(
                filetypes=[("CSV", "*.csv"), ("Tous", "*.*")]
            )
            if fichier:
                self.donnees_chargees = GestionnaireDonnees.charger_csv(fichier)
                self._mettre_a_jour_interface()
                messagebox.showinfo("Succès", f"CSV chargé: {len(self.donnees_chargees)} enregistrements")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def _charger_json(self):
        """Charge un fichier JSON"""
        try:
            fichier = filedialog.askopenfilename(
                filetypes=[("JSON", "*.json"), ("Tous", "*.*")]
            )
            if fichier:
                self.donnees_chargees = GestionnaireDonnees.charger_json(fichier)
                self._mettre_a_jour_interface()
                messagebox.showinfo("Succès", f"JSON chargé: {len(self.donnees_chargees)} enregistrements")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def _saisir_manuel(self):
        """Ouvre la fenêtre de saisie manuelle"""
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Saisie Manuelle")
        fenetre.geometry("500x400")
        
        ttk.Label(fenetre, text="Format: clé=valeur séparé par des virgules\nEx: nom=Alice,age=20,note=15", 
                 font=('Arial', 10)).pack(pady=10)
        
        texte = scrolledtext.ScrolledText(fenetre, height=20, width=100)
        texte.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def valider():
            contenu = texte.get(1.0, tk.END).strip()
            if contenu:
                self._traiter_saisie_manuelle(contenu)
                fenetre.destroy()
        
        ttk.Button(fenetre, text="Valider", command=valider).pack(pady=10)
    
    def _traiter_saisie_manuelle(self, texte: str):
        """Traite la saisie manuelle"""
        try:
            lignes = [l.strip() for l in texte.split('\n') if l.strip()]
            donnees = []
            
            for ligne in lignes:
                entree = {}
                paires = ligne.split(',')
                for paire in paires:
                    if '=' in paire:
                        cle, valeur = paire.split('=', 1)
                        entree[cle.strip()] = valeur.strip()
                if entree:
                    donnees.append(entree)
            
            self.donnees_chargees = donnees
            self._mettre_a_jour_interface()
            messagebox.showinfo("Succès", f"Saisie manuelle: {len(donnees)} enregistrement(s)")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Saisie invalide: {str(e)}")
    
    def _mettre_a_jour_interface(self):
        """Met à jour l'interface après chargement"""
        if self.donnees_chargees:
            analyse = GestionnaireDonnees.analyser_donnees(self.donnees_chargees)
            self.cles_disponibles = analyse["cles"]
            
            self.combo_critere['values'] = self.cles_disponibles
            if self.cles_disponibles:
                self.combo_critere.set(self.cles_disponibles[0])
            
            self.label_statut.config(
                text=f"✅ {len(self.donnees_chargees)} enregistrements - {len(self.cles_disponibles)} champs"
            )
            
            # Afficher les données
            tableau = GestionnaireDonnees.formater_tableau(self.donnees_chargees)
            self.texte_donnees.delete(1.0, tk.END)
            self.texte_donnees.insert(1.0, tableau)
        else:
            self._effacer_donnees()
    
    def _executer_tri(self):
        """Exécute le tri avec les paramètres choisis"""
        if not self.donnees_chargees:
            messagebox.showwarning("Attention", "Chargez d'abord des données")
            return
        
        if not self.combo_critere.get():
            messagebox.showwarning("Attention", "Choisissez un critère de tri")
            return
        
        try:
            cle = self.combo_critere.get()
            croissant = self.ordre_var.get() == "croissant"
            algo = self.algo_var.get()
            
            # Exécuter le tri
            self.donnees_triees, stats = GestionnaireAlgorithmes.trier(
                algo, self.donnees_chargees, cle, croissant
            )
            
            # Afficher résultats
            tableau_trie = GestionnaireDonnees.formater_tableau(self.donnees_triees)
            self.texte_resultats.delete(1.0, tk.END)
            self.texte_resultats.insert(1.0, tableau_trie)
            
            # Afficher statistiques
            self.label_stats.config(
                text=f"🔧 {stats.algorithme} | {stats.ordre} | "
                     f"⏱️ {stats.temps:.4f}s | "
                     f"🔍 {stats.comparaisons} comparaisons | "
                     f"🔄 {stats.permutations} permutations"
            )
            
            messagebox.showinfo("Succès", "Tri effectué avec succès!")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du tri: {str(e)}")
    
    def _effacer_donnees(self):
        """Réinitialise l'interface"""
        self.donnees_chargees = []
        self.donnees_triees = []
        self.cles_disponibles = []
        
        self.label_statut.config(text="Aucune donnée chargée")
        self.texte_donnees.delete(1.0, tk.END)
        self.texte_resultats.delete(1.0, tk.END)
        self.label_stats.config(text="Aucun tri effectué")
        self.combo_critere.set('')
    
    def demarrer(self):
        """Lance l'application"""
        self.racine.mainloop()