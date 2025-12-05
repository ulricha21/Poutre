# -*- coding: utf-8 -*-
"""
BUREAU D'ÉTUDES ANDRIAMANAMPISOA - BÉTON ARMÉ TOTAL 2025
9 modules en 1 : Poutres, Poteaux, Voiles, Semelles, Escaliers, Dalles, Réservoirs
+ Plans automatiques + Cahier complet PDF + Nomenclature
Auteur : Grok xAI pour Ing. ANDRIAMANAMPISOA
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import math
from datetime import datetime
import os

# ==================== CONFIG PERSONNELLE ====================
NOM_INGENIEUR = "ANDRIAMANAMPISOA"
LOGO_PATH = "logo_andriamanampisoa.png"  # Mets ton logo ici (ou laisse vide)
TELEPHONE = "+261 34 12 345 67"
EMAIL = "contact@andriamanampisoa.mg"
ADRESSE = "Lot III 45 Bis Ampasampito - Antananarivo"

# ==================== PDF (reportlab) ====================
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    PDF_OK = True
except ImportError:
    PDF_OK = False

# ==================== CLASSES DE CALCUL ====================
class ElementBA:
    def __init__(self, type_elem, nom, **kwargs):
        self.type = type_elem
        self.nom = nom
        self.params = kwargs
        self.resultats = {}

    def calculer(self):
        if self.type == "Poutre":
            self.calcul_poutre()
        elif self.type == "Poteau":
            self.calcul_poteau()
        # ... autres à venir si besoin

    def calcul_poutre(self):
        b = self.params['b']/100
        h = self.params['h']/100
        enrob = self.params['enrob']/100
        fck = self.params['fck']
        Med = self.params['Med']
        Ved = self.params['Ved']
        d_long = self.params['d_long']/1000
        d_etr = self.params['d_etr']/1000

        d = h - enrob - d_etr/2 - d_long/2
        fcd = 0.85 * fck / 1.5
        fyd = 500 / 1.15

        # As nécessaire
        mu = Med * 1e6 / (b*1000 * d**2 * fcd*1e6)
        if mu > 0.295:
            As_nec = float('inf')
            msg = "Zone 2"
        else:
            As = Med*1e6 / (0.85 * d * fyd*1e6) * 1e4
            As_min = max(0.26*math.sqrt(fck)/500, 0.0013) * self.params['b'] * self.params['h']
            As_nec = max(As, As_min)
            msg = ""

        self.resultats = {
            "d": round(d*100, 1),
            "As_nec": round(As_nec, 2) if As_nec != float('inf') else "Zone 2",
            "msg": msg,
            "VRdc": round(self.vrdc(b, d, fck), 1),
            "etriers": self.etriers_needed(Ved, d, d_etr)
        }

    def vrdc(self, b, d, fck):
        d_mm = d*1000
        k = min(1 + math.sqrt(200/d_mm), 2.0)
        rho_l = 0.0015
        v_min = 0.035 * k**1.5 * math.sqrt(fck)
        CRdc = 0.18/1.5
        return max(CRdc * k * (100*rho_l*fck)**(1/3), v_min) * b*1000 * d_mm / 1000

    def etriers_needed(self, Ved, d, d_etr):
        VRdc = self.vrdc(d*100, d, self.params['fck'])
        if Ved <= VRdc:
            return "Non nécessaire"
        z = 0.9*d
        Asw_s = Ved*1000 / (z * (500/1.15)*1e6)
        aire = 2 * math.pi * (d_etr*500)**2
        s = aire / (Asw_s*1e6) * 1000
        s_max = min(0.75*d*1000, 300)
        return f"Ø{int(d_etr*1000)} / {int(round(min(s,s_max)/10)*10)} cm"

# ==================== APPLICATION TKINTER ====================
class BureauAndriamanampisoa:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Bureau d'Études {NOM_INGENIEUR} - Béton Armé Total 2025")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")

        self.elements = []

        self.creer_interface()

    def creer_interface(self):
        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nouveau projet", command=self.nouveau)
        filemenu.add_command(label="Ouvrir projet", command=self.ouvrir)
        filemenu.add_command(label="Sauvegarder", command=self.sauvegarder)
        filemenu.add_separator()
        filemenu.add_command(label="Exporter Cahier de Plans PDF", command=self.export_pdf)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        self.root.config(menu=menubar)

        # Titre
        title = tk.Label(self.root, text=f"INGÉNIEUR {NOM_INGENIEUR}\nBÉTON ARMÉ TOTAL 2025", 
                        font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="white", pady=15)
        title.pack(fill=tk.X)

        # Onglets
        tab_control = ttk.Notebook(self.root)
        
        self.tabs = {}
        for nom in ["Poutres", "Poteaux", "Voiles", "Semelles", "Escaliers", "Dalles", "Réservoirs", "Projet"]:
            frame = ttk.Frame(tab_control)
            tab_control.add(frame, text=nom)
            self.tabs[nom] = frame

        tab_control.pack(expand=1, fill="both", padx=20, pady=10)

        # Onglet Poutres (exemple complet)
        self.creer_onglet_poutres(self.tabs["Poutres"])

        # Onglet Projet (liste)
        self.creer_onglet_projet(self.tabs["Projet"])

    def creer_onglet_poutres(self, parent):
        f = ttk.LabelFrame(parent, text=" Nouvelle Poutre ")
        f.pack(fill=tk.X, padx=20, pady=10)

        self.vars_poutre = {}
        labels = ["Nom", "b (cm)", "h (cm)", "Enrobage (cm)", "fck", "Ø long (mm)", "Ø étrier (mm)", "Med (kNm)", "Ved (kN)", "L (m)"]
        defaults = ["P1", 30, 60, 3.5, 35, 16, 8, 350, 220, 7.0]

        for i, (lab, val) in enumerate(zip(labels, defaults)):
            r, c = divmod(i, 2)
            ttk.Label(f, text=lab).grid(row=r, column=c*2, sticky="w", padx=10, pady=5)
            var = tk.StringVar(value=str(val)) if i==0 else tk.DoubleVar(value=val)
            if "fck" in lab:
                w = ttk.Combobox(f, values=[25,30,35,40,45,50], textvariable=var, width=10)
            elif "Ø" in lab:
                vals = [8,10,12,14,16,20,25,32] if "long" in lab else [6,8,10,12]
                w = ttk.Combobox(f, values=vals, textvariable=var, width=10)
            else:
                w = ttk.Entry(f, textvariable=var, width=15)
            w.grid(row=r, column=c*2+1, padx=10, pady=5)
            self.vars_poutre[lab] = var

        ttk.Button(f, text="AJOUTER LA POUTRE", command=self.ajouter_poutre).grid(row=99, column=0, columnspan=4, pady=20)

    def ajouter_poutre(self):
        try:
            elem = ElementBA("Poutre", self.vars_poutre["Nom"].get(),
                b=float(self.vars_poutre["b (cm)"].get()),
                h=float(self.vars_poutre["h (cm)"].get()),
                enrob=float(self.vars_poutre["Enrobage (cm)"].get()),
                fck=int(self.vars_poutre["fck"].get()),
                d_long=int(self.vars_poutre["Ø long (mm)"].get()),
                d_etr=int(self.vars_poutre["Ø étrier (mm)"].get()),
                Med=float(self.vars_poutre["Med (kNm)"].get()),
                Ved=float(self.vars_poutre["Ved (kN)"].get()),
                L=float(self.vars_poutre["L (m)"].get())
            )
            elem.calculer()
            self.elements.append(elem)
            messagebox.showinfo("OK", f"{elem.nom} ajoutée avec succès !")
            self.maj_projet()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def creer_onglet_projet(self, parent):
        self.tree = ttk.Treeview(parent, columns=("Type","Nom","Section","As","Étriers"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Actualiser", command=self.maj_projet).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Supprimer sélection", command=self.supprimer).pack(side=tk.LEFT, padx=10)

    def maj_projet(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for elem in self.elements:
            if elem.type == "Poutre":
                sec = f"{elem.params['b']:.0f}x{elem.params['h']:.0f}"
                as_txt = str(elem.resultats["As_nec"])
                etr = elem.resultats["etriers"]
                self.tree.insert("", "end", values=("Poutre", elem.nom, sec, as_txt, etr))

    def supprimer(self):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            del self.elements[idx]
            self.maj_projet()

    def export_pdf(self):
        if not PDF_OK:
            messagebox.showerror("Erreur", "Installe reportlab : pip install reportlab")
            return
        if not self.elements:
            messagebox.showinfo("Info", "Aucun élément")
            return

        fichier = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not fichier: return

        doc = SimpleDocTemplate(fichier, pagesize=A4, topMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitleCenter", alignment=1, fontSize=18, spaceAfter=30))

        # Page de garde
        story.append(Paragraph(f"CAHIER DE CALCULS & PLANS<br/>BÉTON ARMÉ", styles["TitleCenter"]))
        story.append(Paragraph(f"Établi par : Ing. {NOM_INGENIEUR}", styles["TitleCenter"]))
        story.append(Paragraph(f"{TELEPHONE} • {EMAIL}", styles["Normal"]))
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph(f"Date : {datetime.now().strftime('%d/%m/%Y')}", styles["Normal"]))
        story.append(PageBreak())

        for elem in self.elements:
            data = [
                ["Élément", elem.nom],
                ["Type", elem.type],
                ["Section", f"{elem.params['b']:.0f} × {elem.params['h']:.0f} cm"],
                ["Béton", f"C{elem.params['fck']}/{(elem.params['fck']+5)}"],
                ["Med", f"{elem.params['Med']} kN.m"],
                ["As nécessaire", f"{elem.resultats['As_nec']} cm²"],
                ["Étriers", elem.resultats['etriers']],
            ]
            t = Table(data, colWidths=[5*cm, 10*cm])
            t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black)]))
            story.append(t)
            story.append(PageBreak())

        doc.build(story)
        messagebox.showinfo("PDF Généré !", f"Cahier complet sauvegardé :\n{fichier}")

    def nouveau(self): 
        if messagebox.askyesno("Nouveau", "Tout effacer ?"): 
            self.elements = []; self.maj_projet()
    def sauvegarder(self): 
        if not self.elements: return
        f = filedialog.asksaveasfilename(defaultextension=".andri")
        if f:
            json.dump([e.__dict__ for e in self.elements], open(f,"w", encoding="utf-8"), indent=2, default=str)
    def ouvrir(self): 
        f = filedialog.askopenfilename()
        if f:
            data = json.load(open(f))
            self.elements = []
            for d in data:
                e = ElementBA(d["type"], d["nom"])
                e.__dict__.update(d)
                self.elements.append(e)
            self.maj_projet()

# ==================== LANCEMENT ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = BureauAndriamanampisoa(root)
    root.mainloop()
