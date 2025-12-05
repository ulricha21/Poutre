
"""
CALCUL POUTRE AVEC CONSOLES - EUROCODE 2 (EC2)
Version professionnelle avec tableau détaillé de ferraillage
Auteur : xAI / Grok - 2024
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
from datetime import datetime

class PoutreBAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcul Poutre BA avec Consoles - EC2")
        self.root.geometry("1300x950")

        # Configuration des matériaux disponibles
        self.diam_aciers = [8, 10, 12, 14, 16, 20, 25, 32, 40]
        self.diam_etriers = [6, 8, 10, 12]

        # Variables Tkinter
        self.create_variables()
        self.create_interface()

    def create_variables(self):
        """Crée toutes les variables Tkinter"""
        self.L = tk.StringVar(value="2.0,5.0,6.0,5.0,2.0")  # Portées avec consoles
        self.b = tk.DoubleVar(value=0.30)                   # Largeur (m)
        self.h = tk.DoubleVar(value=0.60)                   # Hauteur totale (m)
        self.c_nom = tk.DoubleVar(value=0.03)               # Enrobage nominal (m)
        
        # Matériaux
        self.fck = tk.IntVar(value=30)                      # Résistance béton (MPa)
        self.fyk = tk.IntVar(value=500)                     # Limite élastique acier (MPa)
        
        # Charges
        self.g = tk.DoubleVar(value=15.0)                   # Charge permanente (kN/m)
        self.q = tk.DoubleVar(value=12.0)                   # Charge exploitation (kN/m)
        
        # Coefficients
        self.gamma_g = tk.DoubleVar(value=1.35)
        self.gamma_q = tk.DoubleVar(value=1.50)
        self.gamma_c = tk.DoubleVar(value=1.50)
        self.gamma_s = tk.DoubleVar(value=1.15)
        self.psi2 = tk.DoubleVar(value=0.3)

        # Résultats calculs
        self.resultats = []
        self.etriers_result = ""
        self.fleche_result = ""

    def create_interface(self):
        """Crée l'interface utilisateur complète"""
        # Notebook principal
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Onglet Saisie
        saisie_frame = ttk.Frame(notebook)
        notebook.add(saisie_frame, text="Saisie des données")
        self.create_saisie_frame(saisie_frame)

        # Onglet Résultats
        resultats_frame = ttk.Frame(notebook)
        notebook.add(resultats_frame, text="Résultats")
        self.create_resultats_frame(resultats_frame)

    def create_saisie_frame(self, frame):
        """Crée le cadre de saisie des données"""
        # === Géométrie ===
        geom_frame = ttk.LabelFrame(frame, text="Géométrie", padding=10)
        geom_frame.pack(fill=tk.X, padx=5, pady=5)

        # Portées
        ttk.Label(geom_frame, text="Portées (m) :").grid(row=0, column=0, sticky="e", padx=(0, 10))
        portees_entry = ttk.Entry(geom_frame, textvariable=self.L, width=45, font=('Arial', 10))
        portees_entry.grid(row=0, column=1, sticky="w")
        ttk.Label(geom_frame, text="Ex: 2.0,5.0,6.0,5.0,2.0 (consoles aux extrémités)", 
                 font=('Arial', 8, 'italic')).grid(row=1, column=1, sticky="w")

        # Dimensions
        dimensions_frame = ttk.Frame(geom_frame)
        dimensions_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(dimensions_frame, text="Largeur b =").pack(side=tk.LEFT)
        ttk.Entry(dimensions_frame, textvariable=self.b, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(dimensions_frame, text="m").pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(dimensions_frame, text="Hauteur h =").pack(side=tk.LEFT)
        ttk.Entry(dimensions_frame, textvariable=self.h, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(dimensions_frame, text="m").pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(dimensions_frame, text="Enrobage =").pack(side=tk.LEFT)
        ttk.Entry(dimensions_frame, textvariable=self.c_nom, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(dimensions_frame, text="m").pack(side=tk.LEFT)

        # === Matériaux ===
        mat_frame = ttk.LabelFrame(frame, text="Matériaux", padding=10)
        mat_frame.pack(fill=tk.X, padx=5, pady=5)

        materials_frame = ttk.Frame(mat_frame)
        materials_frame.pack()

        ttk.Label(materials_frame, text="Béton C").pack(side=tk.LEFT)
        ttk.Entry(materials_frame, textvariable=self.fck, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(materials_frame, text="/37").pack(side=tk.LEFT, padx=(0, 30))

        ttk.Label(materials_frame, text="Acier B").pack(side=tk.LEFT)
        ttk.Entry(materials_frame, textvariable=self.fyk, width=8).pack(side=tk.LEFT, padx=(5, 10))

        # === Charges ===
        charge_frame = ttk.LabelFrame(frame, text="Charges", padding=10)
        charge_frame.pack(fill=tk.X, padx=5, pady=5)

        charges_frame = ttk.Frame(charge_frame)
        charges_frame.pack()

        ttk.Label(charges_frame, text="Charge permanente g =").pack(side=tk.LEFT)
        ttk.Entry(charges_frame, textvariable=self.g, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(charges_frame, text="kN/m").pack(side=tk.LEFT, padx=(0, 30))

        ttk.Label(charges_frame, text="Charge exploitation q =").pack(side=tk.LEFT)
        ttk.Entry(charges_frame, textvariable=self.q, width=8).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(charges_frame, text="kN/m").pack(side=tk.LEFT)

        # === Coefficients ===
        coeff_frame = ttk.LabelFrame(frame, text="Coefficients de sécurité", padding=10)
        coeff_frame.pack(fill=tk.X, padx=5, pady=5)

        coeffs_frame = ttk.Frame(coeff_frame)
        coeffs_frame.pack()

        ttk.Label(coeffs_frame, text="γg =").pack(side=tk.LEFT)
        ttk.Entry(coeffs_frame, textvariable=self.gamma_g, width=6).pack(side=tk.LEFT, padx=(5, 15))

        ttk.Label(coeffs_frame, text="γq =").pack(side=tk.LEFT)
        ttk.Entry(coeffs_frame, textvariable=self.gamma_q, width=6).pack(side=tk.LEFT, padx=(5, 15))

        ttk.Label(coeffs_frame, text="ψ2 =").pack(side=tk.LEFT)
        ttk.Entry(coeffs_frame, textvariable=self.psi2, width=6).pack(side=tk.LEFT, padx=(5, 15))

        # === Bouton Calcul ===
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="🚀 CALCULER", command=self.calculer, 
                  style='Accent.TButton').pack(padx=20, pady=10)

    def create_resultats_frame(self, frame):
        """Crée le cadre des résultats avec tableau et schéma"""
        # === Tableau des résultats ===
        table_frame = ttk.LabelFrame(frame, text="Tableau de ferraillage", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar pour le tableau
        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Tableau Treeview
        columns = ('Section', 'M_ed', 'As_req', 'As_min', 'Ferraillage', 'As_pos', 'Taux', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', 
                                yscrollcommand=tree_scroll.set, height=12)

        # Configuration des colonnes
        col_widths = [100, 80, 80, 80, 180, 80, 60, 80]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=width, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)

        # === Schéma de ferraillage ===
        schema_frame = ttk.LabelFrame(frame, text="Schéma de ferraillage", padding=5)
        schema_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.figure = plt.Figure(figsize=(12, 5), facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figure, master=schema_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # === Boutons d'export ===
        export_frame = ttk.Frame(frame)
        export_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(export_frame, text="📄 Exporter PDF", 
                  command=self.exporter_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="📊 Exporter CSV", 
                  command=self.exporter_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="🔄 Nouveau calcul", 
                  command=self.nouveau_calcul).pack(side=tk.RIGHT, padx=5)

    def calculer(self):
        """Effectue tous les calculs de la poutre"""
        try:
            # Validation des entrées
            L = [float(x.strip()) for x in self.L.get().split(',')]
            if len(L) < 3:
                messagebox.showerror("Erreur", "Minimum 3 portées requises (console-travée-console)")
                return

            # Récupération des paramètres
            b = self.b.get()
            h = self.h.get()
            c_nom = self.c_nom.get()
            fck = self.fck.get()
            fyk = self.fyk.get()
            g = self.g.get()
            q = self.q.get()
            gamma_g = self.gamma_g.get()
            gamma_q = self.gamma_q.get()
            gamma_c = self.gamma_c.get()
            gamma_s = self.gamma_s.get()
            psi2 = self.psi2.get()

            # Vérifications basiques
            if b <= 0 or h <= 0 or c_nom <= 0:
                messagebox.showerror("Erreur", "Les dimensions doivent être positives")
                return
            if c_nom >= h/2:
                messagebox.showerror("Erreur", "L'enrobage ne peut pas être supérieur à h/2")
                return

            # Calculs préliminaires
            d = h - c_nom - 0.015  # Hauteur utile (approximation)
            qd_elu = gamma_g * g + gamma_q * q
            qd_els = g + psi2 * q
            fcd = fck / gamma_c
            fyd = fyk / gamma_s

            # Détermination des sections critiques
            sections = self.determiner_sections_critiques(L, qd_elu)

            # Nettoyage du tableau
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Calcul du ferraillage pour chaque section
            self.resultats = []
            for section_info in sections:
                nom_section, M_ed_kNm, position = section_info
                M_ed = M_ed_kNm * 1e6  # Conversion en N.mm
                
                ferraillage, As_req, As_min = self.calcul_ferraillage(M_ed, d, b, fcd, fyd)
                
                if ferraillage is None:
                    messagebox.showerror("Erreur", f"Section insuffisante en {nom_section}!\nAugmentez h ou b.")
                    return

                ferraillage_str = self.formater_ferraillage(ferraillage)
                As_pos = sum(n * math.pi * (diam/2)**2 for n, diam in ferraillage)
                taux = (As_pos / (b * 1000 * d)) * 100
                status = "✅ OK" if As_pos >= As_req else "⚠️ Min"

                self.resultats.append({
                    'section': nom_section,
                    'M_ed': M_ed_kNm,
                    'As_req': As_req,
                    'As_min': As_min,
                    'ferraillage': ferraillage,
                    'ferraillage_str': ferraillage_str,
                    'As_pos': As_pos,
                    'taux': taux,
                    'status': status,
                    'position': position
                })

                # Ajout au tableau
                self.tree.insert('', 'end', values=(
                    nom_section,
                    f"{M_ed_kNm:.2f}",
                    f"{As_req:.0f}",
                    f"{As_min:.0f}",
                    ferraillage_str,
                    f"{As_pos:.0f}",
                    f"{taux:.2f}",
                    status
                ))

            # Calcul des étriers
            V_ed_max = self.calculer_effort_tranchant_max(L, qd_elu)
            As_long_ref = max(r['As_pos'] for r in self.resultats if 'Appui' in r['section'])
            self.etriers_result, s_etriers = self.calcul_etriers(V_ed_max, b, d, fcd, fyd, As_long_ref)

            # Vérification de la flèche
            travée_centrale = next((r for r in self.resultats if 'Travée 2' in r['section']), None)
            appui_central = next((r for r in self.resultats if 'Appui 2' in r['section']), None)
            
            if travée_centrale and appui_central:
                As_inf = travée_centrale['As_pos']
                As_sup = appui_central['As_pos']
                Ecm = 22 * ((fck + 8) / 10)**0.3 * 1000
                flèche_ok, fleche_calc, fleche_limite = self.verification_fleche(
                    L[1:-1], qd_els, b, h, As_inf, As_sup, Ecm, fck)
                self.fleche_result = {
                    'ok': flèche_ok,
                    'calc': fleche_calc,
                    'limite': fleche_limite
                }
            else:
                self.fleche_result = {'ok': True, 'calc': 0, 'limite': float('inf')}

            # Génération du schéma
            self.generer_schema(L, b, h, c_nom, s_etriers)

            messagebox.showinfo("Succès", "Calcul terminé avec succès!")

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", "Veuillez vérifier les valeurs entrées.\n" + str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue :\n{str(e)}")

    def determiner_sections_critiques(self, L, qd_elu):
        """Détermine les sections critiques pour une poutre avec consoles"""
        sections = []
        total_length = 0
        
        # Console gauche
        sections.append(("Console G", -0.5 * qd_elu * L[0]**2, 0))
        total_length += L[0]
        
        # Appuis et travées internes
        for i in range(1, len(L)-1):
            # Appui
            if i == 1:
                M_appui = -0.6 * qd_elu * (L[i]**2) / 8
            elif i == len(L)-2:
                M_appui = -0.6 * qd_elu * (L[i]**2) / 8
            else:
                M_appui = -0.6 * qd_elu * (max(L[i], L[i+1])**2) / 8
            sections.append((f"Appui {i}", M_appui, total_length))
            
            # Travée
            M_travee = 0.5 * qd_elu * (L[i]**2) / 8
            sections.append((f"Travée {i}", M_travee, total_length + L[i]/2))
            
            total_length += L[i]
        
        # Console droite
        sections.append(("Console D", -0.5 * qd_elu * L[-1]**2, total_length))
        
        return sections

    def calcul_ferraillage(self, M_ed, d, b, fcd, fyd):
        """Calcule le ferraillage longitudinal optimisé"""
        if M_ed <= 0:  # Compression - cas rare pour poutres
            As_req = 0
            As_min = 0.0013 * b * 1000 * d
            return [(2, 12)], As_req, As_min

        K = M_ed / (b * 1000 * d**2 * fcd)
        K_max = 0.167  # ξ = 0.45 (pas de redistribution)

        if K > K_max:
            return None, None, None

        z = d * (0.5 + math.sqrt(0.25 - K / 1.134))
        As_req = M_ed / (0.9 * z * fyd) * 100  # mm²

        # Ferraillage minimal (EC2 §9.2.1.1)
        As_min1 = 0.26 * (self.fck.get() / self.fyk.get())**0.5 * b * 1000 * d
        As_min2 = 0.0013 * b * 1000 * d
        As_min = max(As_min1, As_min2, 100)  # Minimum absolu

        As_final = max(As_req, As_min)
        barres = []

        # Optimisation du choix des barres
        for diam in sorted(self.diam_aciers, reverse=True):
            if diam/1000 >= d/4:  # Vérification du diamètre max
                continue
            area_diam = math.pi * (diam/2)**2
            n = int(As_final // area_diam)
            if n > 0:
                barres.append((n, diam))
                As_final -= n * area_diam
                if As_final <= area_diam * 0.1:  # Tolérance de 10%
                    break

        # Si aucune barre trouvée, utiliser la plus petite
        if not barres:
            barres = [(2, min(self.diam_aciers))]

        return barres, As_req, As_min

    def formater_ferraillage(self, ferraillage):
        """Formate le ferraillage pour l'affichage"""
        if not ferraillage:
            return "Aucun"
        
        parties = []
        for n, diam in ferraillage:
            if n > 0:
                parties.append(f"{int(n)}HA{diam}")
        
        return " + ".join(parties) if parties else "2HA12"

    def calcul_etriers(self, V_ed, b, d, fcd, fyd, As_long):
        """Calcule les étriers optimisés"""
        VRd_c = 0.18 / self.gamma_c.get() * (100 * (As_long / (b * 1000 * d)) * self.fck.get())**(1/3) * b * 1000 * d
        VRd_c = max(VRd_c, 0.035 * (self.fck.get()**(1/3)) * b * 1000 * d)

        if V_ed <= VRd_c:
            return "Pas d'étriers nécessaires (béton seul suffit)", None

        for diam in sorted(self.diam_etriers, reverse=True):
            A_sw = math.pi * (diam/2)**2  # mm² par branche
            VRd_s = 2 * A_sw * fyd * (d * 1000) / 1000  # N (2 branches)
            s_req = VRd_s / ((V_ed - 0.5 * VRd_c) / 1000) / 1000  # m
            s_final = min(s_req, min(0.75 * d, 0.60))  # Espacement max

            if s_final >= 0.10:  # Espacement minimum 10 cm
                return f"Étriers ø{diam} c/{s_final*100:.0f} cm (2 branches)", s_final

        return "Étriers insuffisants avec diamètres disponibles", 0.15

    def calculer_effort_tranchant_max(self, L, qd_elu):
        """Calcule l'effort tranchant maximal"""
        V_max = 0
        for i in range(len(L)):
            if i == 0:  # Console gauche
                V = qd_elu * L[i]
            elif i == len(L)-1:  # Console droite
                V = qd_elu * L[i]
            else:  # Appuis internes
                V = 0.6 * qd_elu * max(L[i], L[i+1] if i+1 < len(L) else 0)
            V_max = max(V_max, V)
        return V_max * 1000  # Conversion en N

    def verification_fleche(self, L, qd_els, b, h, As_inf, As_sup, Ecm, fck):
        """Vérifie la flèche selon EC2 méthode simplifiée"""
        if len(L) == 0:
            return True, 0, float('inf')
            
        L_d = max(L)  # Portée maximale
        K = 1.0
        rho = As_inf / (b * 1000 * h)
        rho_0 = math.sqrt(fck) * 1e-3

        if rho > rho_0:
            K = max(1.0, 1.5 - 0.5 * (rho / rho_0))

        fleche_limite = L_d * 1000 / 250  # L/250
        I = b * h**3 / 12
        fleche_calc = K * (qd_els * L_d**4 * 1000) / (Ecm * I) * 1000

        return fleche_calc <= fleche_limite, fleche_calc, fleche_limite

    def generer_schema(self, L, b, h, c_nom, s_etriers):
        """Génère le schéma de ferraillage"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Dessin de la poutre
        total_length = sum(L)
        ax.add_patch(Rectangle((0, 0), total_length, h, facecolor='#E8D5B5', edgecolor='black', linewidth=2))

        # Dessin des appuis
        x_appui = 0
        for i, l in enumerate(L):
            if i > 0:
                ax.add_patch(Rectangle((x_appui-0.15, -0.25), 0.3, 0.25, facecolor='#666666', edgecolor='black'))
                ax.text(x_appui, -0.35, f'Appui {i}', ha='center', fontsize=9, weight='bold')
            x_appui += l

        # Positions des sections critiques
        positions = {}
        x_pos = 0
        positions["Console G"] = 0
        x_pos += L[0]
        positions["Appui 1"] = x_pos
        
        for i in range(1, len(L)-1):
            positions[f"Travée {i}"] = x_pos + L[i]/2
            x_pos += L[i]
            positions[f"Appui {i+1}"] = x_pos
            
        positions["Console D"] = total_length

        # Dessin des aciers longitudinaux
        y_inf = c_nom + 0.02
        y_sup = h - c_nom - 0.02

        # Aciers inférieurs (travées)
        for section in self.resultats:
            if "Travée" in section['section']:
                pos = positions[section['section']]
                ferraillage = section['ferraillage']
                for j, (n, diam) in enumerate(ferraillage):
                    y_pos = y_inf + j * 0.04
                    ax.plot([pos-0.8, pos+0.8], [y_pos, y_pos], 'red', linewidth=3, solid_capstyle='round')
                # Label
                if ferraillage:
                    label = self.formater_ferraillage([ferraillage[0]])
                    ax.text(pos+0.9, y_inf + (len(ferraillage)-1)*0.04, label, 
                           color='red', fontsize=8, weight='bold', va='center')

        # Aciers supérieurs (appuis et consoles)
        for section in self.resultats:
            if "Appui" in section['section'] or "Console" in section['section']:
                pos = positions[section['section']]
                ferraillage = section['ferraillage']
                for j, (n, diam) in enumerate(ferraillage):
                    y_pos = y_sup - j * 0.04
                    ax.plot([pos-0.8, pos+0.8], [y_pos, y_pos], 'blue', linewidth=3, solid_capstyle='round')
                # Label
                if ferraillage:
                    label = self.formater_ferraillage([ferraillage[0]])
                    ax.text(pos+0.9, y_sup - (len(ferraillage)-1)*0.04, label, 
                           color='blue', fontsize=8, weight='bold', va='center')

        # Dessin des étriers
        if s_etriers and s_etriers > 0:
            for x in np.arange(0.5, total_length, s_etriers):
                ax.plot([x, x], [0.1, h-0.1], 'green', linestyle='--', linewidth=1)
                # Barres horizontales des étriers
                ax.plot([x, x+0.15], [0.1, 0.1], 'green', linewidth=1)
                ax.plot([x, x+0.15], [h-0.1, h-0.1], 'green', linewidth=1)

        # Légende
        legend_elements = [
            plt.Line2D([0], [0], color='red', linewidth=3, label='Aciers inférieurs (travées)'),
            plt.Line2D([0], [0], color='blue', linewidth=3, label='Aciers supérieurs (appuis/consoles)'),
            plt.Line2D([0], [0], color='green', linestyle='--', linewidth=1, label='Étriers')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

        # Configuration du graphique
        ax.set_xlim(-0.5, total_length + 2.0)
        ax.set_ylim(-0.5, h + 0.3)
        ax.set_title("Schéma de ferraillage - Vue en élévation", fontsize=12, weight='bold')
        ax.set_xlabel("Longueur (m)", fontsize=10)
        ax.set_ylabel("Hauteur (m)", fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('auto')

        self.canvas.draw()

    def exporter_pdf(self):
        """Exporte les résultats en PDF professionnel"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # En-tête
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "CALCUL DE POUTRE EN BÉTON ARMÉ AVEC CONSOLES", ln=1, align="C")
            pdf.set_font("Arial", "I", 12)
            pdf.cell(0, 8, "Conforme à l'Eurocode 2 (NF EN 1992-1-1)", ln=1, align="C")
            pdf.ln(10)

            # Données d'entrée
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "1. DONNÉES D'ENTRÉE", ln=1)
            pdf.set_font("Arial", "", 10)

            pdf.cell(0, 8, f"• Géométrie : Portées = {self.L.get()} m", ln=1)
            pdf.cell(0, 8, f"• Section transversale : {self.b.get()*100:.0f} × {self.h.get()*100:.0f} cm", ln=1)
            pdf.cell(0, 8, f"• Enrobage nominal : {self.c_nom.get()*1000:.0f} mm", ln=1)
            pdf.cell(0, 8, f"• Matériaux : Béton C{self.fck.get()}/37 - Acier B{self.fyk.get()}", ln=1)
            pdf.cell(0, 8, f"• Charges : g = {self.g.get():.1f} kN/m, q = {self.q.get():.1f} kN/m", ln=1)
            pdf.ln(5)

            # Tableau de ferraillage
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "2. TABLEAU DE FERRAILLAGE", ln=1)
            pdf.set_font("Arial", "", 9)

            # En-têtes du tableau
            headers = ["Section", "M_ed\n(kN.m)", "As req\n(mm²)", "As min\n(mm²)", 
                      "Ferraillage", "As posé\n(mm²)", "Taux\n(%)", "Statut"]
            widths = [25, 18, 18, 18, 40, 18, 15, 18]

            # Ligne d'en-tête
            for header, width in zip(headers, widths):
                pdf.cell(width, 10, header, border=1, align='C')
            pdf.ln(10)

            # Contenu du tableau
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                for value, width in zip(values, widths):
                    pdf.cell(width, 8, str(value), border=1, align='C')
                pdf.ln(8)

            # Résultats complémentaires
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "3. RÉSULTATS COMPLÉMENTAIRES", ln=1)
            pdf.set_font("Arial", "", 10)

            pdf.cell(0, 8, f"• Effort tranchant maximal : {self.calculer_effort_tranchant_max([float(x) for x in self.L.get().split(',')], self.gamma_g.get()*self.g.get()+self.gamma_q.get()*self.q.get())/1000:.1f} kN", ln=1)
            pdf.cell(0, 8, f"• Étriers : {self.etriers_result}", ln=1)
            
            if hasattr(self, 'fleche_result'):
                fleche_status = "✅ OK" if self.fleche_result['ok'] else "❌ KO"
                pdf.cell(0, 8, f"• Flèche : {self.fleche_result['calc']:.1f} mm / {self.fleche_result['limite']:.1f} mm ({fleche_status})", ln=1)

            # Schéma de ferraillage
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "4. SCHÉMA DE FERRAILLAGE", ln=1)
            
            # Sauvegarde temporaire du schéma
            self.figure.savefig("temp_schema.png", dpi=150, bbox_inches='tight', 
                               facecolor='white', edgecolor='none')
            pdf.image("temp_schema.png", x=10, w=190)

            # Pied de page
            pdf.ln(10)
            pdf.set_font("Arial", "I", 8)
            pdf.cell(0, 10, f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", 
                    ln=1, align='C')

            # Sauvegarde
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                title="Enregistrer le rapport de calcul"
            )

            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Succès", f"Rapport PDF enregistré avec succès !\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erreur PDF", f"Impossible de générer le PDF :\n{str(e)}")

    def exporter_csv(self):
        """Exporte le tableau en CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichiers CSV", "*.csv")],
                title="Enregistrer le tableau de ferraillage"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # En-têtes
                    headers = ["Section", "M_ed (kN.m)", "As req (mm²)", "As min (mm²)", 
                              "Ferraillage", "As posé (mm²)", "Taux (%)", "Statut"]
                    f.write(";".join(headers) + "\n")
                    
                    # Données
                    for item in self.tree.get_children():
                        values = self.tree.item(item)['values']
                        f.write(";".join(str(v) for v in values) + "\n")

                messagebox.showinfo("Succès", f"Tableau CSV enregistré avec succès !\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erreur CSV", f"Impossible de générer le CSV :\n{str(e)}")

    def nouveau_calcul(self):
        """Réinitialise l'interface pour un nouveau calcul"""
        if messagebox.askyesno("Nouveau calcul", "Voulez-vous réinitialiser tous les paramètres ?"):
            self.L.set("2.0,5.0,6.0,5.0,2.0")
            self.b.set(0.30)
            self.h.set(0.60)
            self.c_nom.set(0.03)
            self.fck.set(30)
            self.fyk.set(500)
            self.g.set(15.0)
            self.q.set(12.0)
            self.gamma_g.set(1.35)
            self.gamma_q.set(1.50)
            self.psi2.set(0.3)
            
            # Nettoyer le tableau et le schéma
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.figure.clear()
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Style moderne
    style = ttk.Style()
    style.theme_use('clam')
    
    app = PoutreBAApp(root)
    root.mainloop()

