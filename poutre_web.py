# poutre_web.py – VERSION WEB 100 % FONCTIONNELLE (sans tkinter)
import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

st.set_page_config(page_title="Poutre BA EC2", page_icon="Construction", layout="wide")
st.title("Construction Calcul Poutre BA avec Consoles")
st.markdown("**Eurocode 2 – Fonctionne à 100 % en ligne**")

# --- Sidebar ---
with st.sidebar:
    st.header("Paramètres")
    L_str = st.text_input("Portées (m)", value="1.5, 5.0, 6.0, 5.0, 1.5")
    b = st.number_input("Largeur b (m)", 0.20, 1.00, 0.30, 0.05)
    h = st.number_input("Hauteur h (m)", 0.30, 2.00, 0.70, 0.05)
    c_nom = st.number_input("Enrobage (m)", 0.02, 0.06, 0.03, 0.005)
    fck = st.selectbox("Classe béton", [25,30,35,40,45,50], index=1)
    g = st.number_input("g (kN/m)", 5.0, 50.0, 15.0, 1.0)
    q = st.number_input("q (kN/m)", 0.0, 50.0, 12.0, 1.0)

    if st.button("CALCULER", type="primary", use_container_width=True):
        st.session_state.go = True
    else:
        st.session_state.go = False

# --- Calcul ---
if st.session_state.get("go", False):
    try:
        L = [float(x.strip()) for x in L_str.split(",")]
        if len(L) < 3:
            st.error("Minimum 3 portées")
            st.stop()

        d = h - c_nom - 0.015
        q_elu = 1.35*g + 1.50*q
        fcd = fck/1.5
        fyd = 500/1.15

        sections = []
        sections.append(("Console G", -0.5*q_elu*L[0]**2))
        for i in range(1,len(L)-1):
            sections.append((f"Appui {i}", -0.6*q_elu*L[i]**2/8))
            sections.append((f"Travée {i}", +0.5*q_elu*L[i]**2/8))
        sections.append(("Console D", -0.5*q_elu*L[-1]**2))

        data = []
        for nom, M in sections:
            M = round(M, 2)
            if abs(M) < 1: M = 0

            if M == 0:
                As = 0
            else:
                K = abs(M)*1e6 / (b*1000*d**2*fcd)
                if K > 0.167:
                    st.warning(f"{nom} : section limite → augmentez h")
                    z = d * 0.82
                else:
                    z = d * (0.5 + math.sqrt(0.25 - K/1.134))
                As = abs(M)*1e6 / (0.9*z*fyd) * 100

            As_min = max(0.26*(fck/500)**0.5, 0.0013)*b*1000*d
            As_final = max(As, As_min)

            diam = [40,32,25,20,16,14,12]
            barres = []
            reste = As_final
            for d in diam:
                n = int(reste // (math.pi*(d/2)**2))
                if n >= 1:
                    barres.append(f"{n}HA{d}")
                    reste -= n*math.pi*(d/2)**2
                if reste < 200: break
            if not barres: barres = ["2HA12"]

            data.append({
                "Section": nom,
                "M_ed (kN.m)": M,
                "As (mm²)": int(round(As_final)),
                "Ferraillage": " + ".join(barres)
            })

        df = pd.DataFrame(data)
        st.success("CALCUL TERMINÉ !")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Tableau de ferraillage")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("CSV", df.to_csv(index=False), "poutre_ba.csv", "text/csv")

        with col2:
            st.subheader("Schéma")
            fig, ax = plt.subplots(figsize=(10,4))
            total = sum(L)
            ax.add_patch(Rectangle((0,0),total,h,facecolor="#f4e8d8",edgecolor="black",lw=2))
            x = 0
            for i in range(len(L)):
                if i > 0:
                    ax.add_patch(Rectangle((x-0.15,-0.25),0.3,0.25,facecolor="gray"))
                    ax.text(x,-0.35,f"A{i}",ha="center",fontweight="bold")
                x += L[i]
            ax.set_xlim(-0.5,total+0.5)
            ax.set_ylim(-0.5,h+0.3)
            ax.set_title(f"Poutre {b*100:.0f}×{h*100:.0f} cm")
            ax.axis("off")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur : {e}")

else:
    st.info("Paramètres à gauche → CALCULER")

st.caption("Version 100 % web – fonctionne partout")
