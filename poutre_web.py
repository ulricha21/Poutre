# -*- coding: utf-8 -*-
"""
CALCUL POUTRE BA AVEC CONSOLES - VERSION WEB (Streamlit)
Conforme Eurocode 2 - NF EN 1992-1-1 + Annexe Nationale France
Auteur : xAI / Grok - 2025
"""

import streamlit as st
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from fpdf import FPDF
from datetime import datetime
import base64

# ====================== CONFIGURATION PAGE ======================
st.set_page_config(
    page_title="Calcul Poutre BA - EC2",
    page_icon="Construction",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Construction Calcul Poutre en Béton Armé avec Consoles")
st.markdown("**Eurocode 2 – NF EN 1992-1-1 + Annexe Nationale France**")

# ====================== FONCTIONS DE CALCUL ======================
def calcul_ferraillage(M_ed, d, b, fcd, fyd):
    """Ferraillage longitudinal optimisé (retourne liste de (nb, diam)"""
    diametres = [40, 32, 25, 20, 16, 14, 12, 10, 8]

    if abs(M_ed) < 1e-3:  # très faible moment
        As_min = max(0.26 * (fck/fyk)**0.5 * b*1000*d, 0.0013*b*1000*d)
        return [(2, 12)], 0, As_min

    K = M_ed / (b*1000*d**2*fcd)
    if K > 0.167:
        return None, None, None  # section insuffisante

    z = d * (0.5 + math.sqrt(0.25 - K/1.134))
    As_req = M_ed / (0.9*z*fyd) * 100

    As_min = max(0.26 * (fck/fyk)**0.5 * b*1000*d, 0.0013*b*1000*d)
    As_final = max(As_req, As_min)

    barres = []
    reste = As_final
    for diam in diametres:
        if diam/1000 >= d/4:  # diamètre trop gros
            continue
        aire = math.pi*(diam/2)**2
        n = int(reste // aire)
        if n > 0:
            barres.append((n, diam))
            reste -= n * aire
        if reste < aire*0.1:
            break
    if not barres:
        barres = [(2, 12)]

    As_posee = sum(n*math.pi*(d/2)**2 for n, d in barres)
    return barres, As_req, As_min

def formater_ferraillage(barres):
    return " + ".join([f"{n}HA{diam}" for n, diam in barres]) if barres else "—"

def calcul_etriers(V_ed, b, d, fcd, fyd, As_long):
    """Retourne texte étriers + espacement (m)"""
    VRd_c = max(
        0.18/1.5 * (100*(As_long/(b*1000*d))*fck)**(1/3) * b*1000*d,
        0.035*(fck**(1/3))*b*1000*d
    )
    if V_ed <= VRd_c:
        return "Pas d'étriers nécessaires (béton seul suffit)", None

    diam_etriers = [12, 10, 8, 6]
    for diam in diam_etriers:
        A_sw = math.pi*(diam/2)**2
        VRd_s_branche = A_sw * fyd * (d*1000)/1000   # 1 branche
        s_req = (2*VRd_s_branche) / ((V_ed - 0.5*VRd_c)/1000) / 1000  # 2 branches
        s_max = min(0.75*d, 0.60)
        s = min(s_req, s_max)
        if s >= 0.10:
            return f"Étriers ø{diam} c/{s*100:.0f} cm (2 branches)", s
    return "Étriers insuffisants", 0.20

def verification_fleche(L_travées, q_els, b, h, As_inf, As_sup):
    L_max = max(L_travées)
    rho = As_inf / (b*1000*h)
    rho0 = math.sqrt(fck)*1e-3
    K = 1.0 if rho <= rho0 else max(1.0, 1.5 - 0.5*(rho/rho0))
    Ecm = 22*((fck+8)/10)**0.3 * 1000
    I = b*h**3/12
    f_calc = K * (q_els * L_max**4 * 1000) / (Ecm * I) * 1000   # mm
    f_lim = L_max*1000 / 250
    return f_calc <= f_lim, round(f_calc,1), round(f_lim,1)

def generer_schema(L, b, h, c_nom, resultats, s_etriers):
    fig, ax = plt.subplots(figsize=(14,5))
    total = sum(L)
    ax.add_patch(Rectangle((0,0), total, h, facecolor="#f0e0d0", edgecolor="black", linewidth=2))

    # Appuis
    x = 0
    for i, l in enumerate(L):
        if i > 0:
            ax.add_patch(Rectangle((x-0.15,-0.25),0.3,0.25,facecolor="#555",edgecolor="black"))
            ax.text(x,-0.35,f"A{i}",ha="center",fontweight="bold")
        x += l

    # Positions sections
    pos = {}
    x = 0
    pos["Console G"] = 0
    x += L[0]
    for i in range(1,len(L)):
        if i < len(L)-1:
            pos[f"Appui {i}"] = x
            pos[f"Travée {i}"] = x + L[i]/2
        else:
            pos["Console D"] = x + L[i]
        x += L[i]

    y_inf = c_nom + 0.03
    y_sup = h - c_nom - 0.03

    # Aciers inférieurs (travées)
    for r in resultats:
        if "Travée" in r["section"]:
            p = pos[r["section"]]
            for j, (n,d) in enumerate(r["ferraillage"]):
                ax.plot([p-1,p+1],[y_inf+j*0.045,y_inf+j*0.045],"red",lw=3)
            ax.text(p+1.2, y_inf + (len(r["ferraillage"])-1)*0.045,
                    formater_ferraillage(r["ferraillage"][:1]), color="red", fontweight="bold")

    # Aciers supérieurs (appuis & consoles)
    for r in resultats:
        if "Appui" in r["section"] or "Console" in r["section"]:
            p = pos[r["section"]]
            for j, (n,d) in enumerate(r["ferraillage"]):
                ax.plot([p-1,p+1],[y_sup-j*0.045,y_sup-j*0.045],"blue",lw=3)
            ax.text(p+1.2, y_sup - (len(r["ferraillage"])-1)*0.045,
                    formater_ferraillage(r["ferraillage"][:1]), color="blue", fontweight="bold")

    # Étriers
    if s_etriers:
        for x in np.arange(0.3, total, s_etriers):
            ax.plot([x,x],[0.08,h-0.08],"green",ls="--",lw=1)

    ax.set_xlim(-1, total+2)
    ax.set_ylim(-0.5, h+0.4)
    ax.set_title("Schéma de ferraillage - Vue en élévation", fontsize=14, fontweight="bold")
    ax.set_xlabel("Longueur (m)")
    ax.legend(["Aciers inférieurs","Aciers supérieurs","Étriers"], loc="upper right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig

# ====================== SIDEBAR - SAISIE ======================
with st.sidebar:
    st.header("Paramètres d'entrée")

    L_str = st.text_input("Portées (m)", "2.0,5.0,6.0,5.0,2.0",
                          help="Séparées par des virgules – consoles aux extrémités")
    b = st.number_input("Largeur b (m)", 0.20, 1.00, 0.30, 0.05)
    h = st.number_input("Hauteur h (m)", 0.30, 1.50, 0.60, 0.05)
    c_nom = st.number_input("Enrobage nominal (m)", 0.02, 0.06, 0.03, 0.005)

    st.markdown("---")
    fck = st.selectbox("Classe béton", [25,30,35,40,45,50], index=1)
    fyk = st.selectbox("Acier", [500], index=0)

    g = st.number_input("Charge permanente g (kN/m)", 5.0, 50.0, 15.0, 1.0)
    q = st.number_input("Charge d’exploitation q (kN/m)", 0.0, 50.0, 12.0, 1.0)

    st.markdown("---")
    gamma_g = st.number_input("γG", value=1.35, step=0.05)
    gamma_q = st.number_input("γQ", value=1.50, step=0.05)
    psi2 = st.number_input("ψ₂ (quasi-permanent)", value=0.3, step=0.1)

    if st.button("CALCULER", type="primary", use_container_width=True):
        st.session_state["calculé"] = True

# ====================== CALCUL PRINCIPAL ======================
if st.session_state.get("calculé", False):
    try:
        L = [float(x) for x in L_str.split(",")]
        if len(L) < 3:
            st.error("Minimum 3 portées (console + travée + console)")
            st.stop()

        d = h - c_nom - 0.015
        q_elu = gamma_g*g + gamma_q*q
        q_els = g + psi2*q
        fcd = fck / 1.5
        fyd = fyk / 1.15

        # Sections critiques (méthode forfaitaire EC2)
        sections = []
        x = 0
        sections.append(("Console G", -0.5*q_elu*L[0]**2, x))
        x += L[0]
        for i in range(1, len(L)-1):
            M_appui = -0.6*q_elu*(L[i]**2)/8
            M_travée = 0.5*q_elu*(L[i]**2)/8
            sections.append((f"Appui {i}", M_appui, x))
            sections.append((f"Travée {i}", M_travée, x + L[i]/2))
            x += L[i]
        sections.append(("Console D", -0.5*q_elu*L[-1]**2, x))

        resultats = []
        for nom, M_kNm, pos in sections:
            M_ed = M_kNm * 1e6
            fer, As_req, As_min = calcul_ferraillage(M_ed, d, b, fcd, fyd)
            if fer is None:
                st.error(f"Section insuffisante en **{nom}** → augmentez h ou b")
                st.stop()
            As_posee = sum(n*math.pi*(diam/2)**2 for n,diam in fer)
            taux = As_posee/(b*1000*d)*100
            resultats.append({
                "section": nom,
                "M_ed": round(M_kNm,2),
                "As_req": round(As_req),
                "As_min": round(As_min),
                "ferraillage": fer,
                "ferraillage_str": formater_ferraillage(fer),
                "As_posee": round(As_posee),
                "taux": round(taux,2),
                "status": "OK" if As_posee >= As_req else "Min"
            })

        # Effort tranchant max & étriers
        V_max = max(0.6*q_elu*max(L[1:-1]), q_elu*max(L[0],L[-1])) * 1000
        As_long_max = max(r["As_posee"] for r in resultats if "Appui" in r["section"])
        etriers_txt, s_etriers = calcul_etriers(V_max, b, d, fcd, fyd, As_long_max)

        # Flèche
        travées_centrales = [L[i] for i in range(1,len(L)-1)]
        As_inf = next((r["As_posee"] for r in resultats if "Travée" in r["section"]), 1000)
        As_sup = next((r["As_posee"] for r in resultats if "Appui" in r["section"]), 1000)
        fleche_ok, f_calc, f_lim = verification_fleche(travées_centrales, q_els, b, h, As_inf, As_sup)

        # ====================== AFFICHAGE RÉSULTATS ======================
        col1, col2 = st.columns([1.1, 1])

        with col1:
            st.subheader("Tableau de ferraillage")
            df = pd.DataFrame(resultats)[["section","M_ed","As_req","As_min","ferraillage_str","As_posee","taux","status"]]
            df.columns = ["Section","M_ed (kN.m)","As req","As min","Ferraillage","As posé","Taux (%)","Statut"]
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown("### Résultats complémentaires")
            st.info(f"**V_ed max** : {V_max/1000:.1f} kN → {etriers_txt}")
            st.info(f"**Flèche** : {f_calc} mm ≤ {f_lim} mm → {'OK' if fleche_ok else 'KO'}")

        with col2:
            st.subheader("Schéma de ferraillage")
            fig = generer_schema(L, b, h, c_nom, resultats, s_etriers)
            st.pyplot(fig)

        # ====================== EXPORT ======================
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            csv = df.to_csv(index=False, sep=";").encode()
            st.download_button("CSV Tableau", csv, "ferraillage.csv", "text/csv")
        with c2:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
            buf.seek(0)
            st.download_button("PNG Schéma", buf.getvalue(), "schema.png", "image/png")
        with c3:
            # PDF simple (texte + tableau + image)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0,10,"CALCUL POUTRE BA - EC2", ln=1, align="C")
            pdf.set_font("Arial", "",10)
            pdf.ln(5)
            pdf.cell(0,8,f"Portées : {L_str} m | Section : {b*100:.0f}×{h*100:.0f} cm | C{fck}/37 - B{fyk}", ln=1)
            pdf.ln(5)
            # tableau (simplifié)
            pdf.set_font("Arial","B",9)
            for i, col in enumerate(df.columns):
                pdf.cell(25,8,col,1)
            pdf.ln()
            pdf.set_font("Arial","",9)
            for _, row in df.iterrows():
                for val in row:
                    pdf.cell(25,8,str(val),1)
                pdf.ln()
            pdf.output("rapport.pdf")
            with open("rapport.pdf","rb") as f:
                st.download_button("PDF Rapport", f.read(), "rapport_poutre.pdf", "application/pdf")

        st.success("Calcul terminé – tout est prêt !")

    except Exception as e:
        st.error(f"Erreur : {e}")

else:
    st.info("Saisissez les paramètres à gauche puis cliquez sur **CALCULER**")

# ====================== LIEN DE DÉPLOIEMENT GRATUIT ======================
st.sidebar.markdown("---")
st.sidebar.markdown("### Déploiement gratuit")
st.sidebar.markdown("[Streamlit Cloud → 3 clics](https://share.streamlit.io/deploy)")