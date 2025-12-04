import streamlit as st
import numpy as np

st.title("Klimaatmodel – Direct Berekenen")

st.header("Input Parameters")
#INPUTS NGHG FORMULA

Y0 = st.number_input("Y(0): Inkomen in basisjaar", value=100, step=0.01, format="%.2f", key="Y0")
beta0 = st.number_input("β0", value=1, step=0.1, format="%.1f", key="beta0")

# INPUTS
T0 = st.number_input("T(0): Temperatuur in basisjaar", value=0.56, step=0.01, format="%.2f", key="T0")
NGHG0 = st.number_input("NGHG(0): Emissies in basisjaar", value=340.0, key="NGHG0")
delta = st.number_input("δ: schadeparameter", value=0.25, step=0.01, format="%.2f", key="delta")
beta2 = st.number_input("1-β2: Innovatie en populatie parameter", value=0.5, step=0.01, format="%.2f", key="beta2")
g = st.number_input("g: groeifactor", value=0.015, step=0.001, format="%.3f", key="g")
k = st.number_input("K: klimaatrespons op emissies", value=0.45, step=0.01, format="%.2f", key="k")
beta1 = st.number_input("β1: Innovatie en populatie parameter", value=0.035, step=0.001, format="%.3f", key="beta1")

# Tijd variabele
t = st.slider("t (jaren)", min_value=0, max_value=200, value=40, key="t")

st.divider()

st.subheader("Berekening van $T^*(t)$")


        GHG = beta0 * Y0**beta2
        st.markdown(f"## **{GHG:.3f}")

# BEREKENING VAN T*(t)
try:
    # 1. Bereken de exponent 'X' en de noemer in de tweede breuk
    # X = ((1 - beta2) * g - beta1)
    X = (1.0 - beta2) * g - beta1
    
    # Controle op delen door nul
    if X == 0:
        st.error("Fout: De term ((1-β2)g - β1) is 0. De formule is niet gedefinieerd in deze vorm.")
    elif delta * (1.0 - beta2) == 0:
         st.error("Fout: De term δ(1-β2) is 0.")
    else:
        # 2. Bereken de tweede breuk in de logaritme
        # BreukTerm = (delta * (1 - beta2)) / X
        BreukTerm = (delta * (1.0 - beta2)) / X
        
        # 3. Bereken de inhoud van de blokhaken
        # HIER GEBRUIKEN WE UW VEREENVOUDIGING: 
        # C = NGHG(0) in plaats van de complexe breuk.
        # InhoudBlokhaken = NGHG(0) * BreukTerm * (e^(X*t) - 1)
        InhoudBlokhaken = k * NGHG0 * BreukTerm * (np.exp(X * t) - 1.0)
        
        # 4. Bereken de totale inhoud van de natuurlijke logaritme (ln)
        InhoudLn = 1.0 + InhoudBlokhaken
        
        # 5. Bereken T*(t)
        # FactorVoorLn = 1 / (delta * (1 - beta2))
        FactorVoorLn = 1.0 / (delta * (1.0 - beta2))
        
        T_ster_t = T0 + FactorVoorLn * np.log(InhoudLn)
    
        # Resultaat weergeven
        st.success(f"De berekende temperatuur $T^*(t)$ in jaar {t} is:")
        st.markdown(f"## **{T_ster_t:.3f} °C**")
        st.caption("Gebaseerd op de interpretatie dat de initiële constante $\\frac{\\kappa \\beta_{0}(Y(0))^{1-\\beta_{2}}}{NGHG(0)}$ wordt vervangen door de input $NGHG(0)$.")

except ZeroDivisionError:
    st.error("Fout bij delen door nul. Controleer de parameters.")

except Exception as e:
    st.error(f"Er is een onverwachte fout opgetreden: {e}")
    st.error("Controleer of de berekeningen positieve waarden geven voor de logaritme.")







