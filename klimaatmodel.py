import streamlit as st
import numpy as np
import pandas as pd

st.title("Klimaatmodel – Direct Berekenen")

st.header("Input Parameters")

# INPUTS
Y0 = st.number_input("Y(0): NEGEER DIT! Inkomen in basisjaar", value=100.0, step=1.0, key="Y0_input")
beta0 = st.number_input("NEGEER DIT! β0", value=1.0, step=0.1, format="%.1f", key="beta0_input")
T0 = st.number_input("T(0): Temperatuur in basisjaar", value=0.56, step=0.01, format="%.2f", key="T0")
NGHG0 = st.number_input("NGHG(0): Emissies in basisjaar", value=340.0, step=0.1, key="NGHG0")
delta = st.number_input("δ: schadeparameter", value=0.25, step=0.01, format="%.2f", key="delta")
beta2 = st.number_input("1-β2: Innovatie en populatie parameter", value=0.5, step=0.01, format="%.2f", key="beta2")
g = st.number_input("g: groeifactor", value=0.015, step=0.001, format="%.3f", key="g")
k = st.number_input("K: klimaatrespons op emissies", value=0.45, step=0.01, format="%.2f", key="k")
beta1 = st.number_input("β1: Innovatie en populatie parameter", value=0.035, step=0.001, format="%.3f", key="beta1")

# Tijd variabele
t_single = st.slider("t (jaren) voor een enkel punt", min_value=0, max_value=200, value=40, key="t_single")

st.divider()

# Functie om de formule T*(t) te berekenen (gevectoriseerd)
def bereken_temperatuur(t_waarden, T0, NGHG0, beta1, beta2, g, delta, k):
    try:
        X = (1.0 - beta2) * g - beta1
        
        if X == 0 or delta * (1.0 - beta2) == 0:
            return None, "Een noemer is nul, controleer parameters."

        BreukTerm = (delta * (1.0 - beta2)) / X
        FactorVoorLn = 1.0 / (delta * (1.0 - beta2))
        
        # Factor C is: k * NGHG0 (op basis van eerdere instructies)
        C_factor = k * NGHG0
        
        InhoudBlokhaken = C_factor * BreukTerm * (np.exp(X * t_waarden) - 1.0)
        InhoudLn = 1.0 + InhoudBlokhaken
        
        if np.any(InhoudLn <= 0):
            return None, "Logaritme van een niet-positief getal."

        T_ster_t = T0 + FactorVoorLn * np.log(InhoudLn)
        
        return T_ster_t, None

    except Exception as e:
        return None, f"Fout: {e}"

# Verzamel de parameters voor de functie-aanroep
params = [T0, NGHG0, beta1, beta2, g, delta, k]


# =========================================================================
# 1. BEREKENING VOOR EEN ENKEL PUNT
# =========================================================================

T_ster_single_result, foutmelding_single = bereken_temperatuur(np.array([t_single]), *params)

st.subheader("Resultaten")

if foutmelding_single:
    st.error(foutmelding_single)
else:
    # Bereken GHG basiswaarde
    GHG = beta0 * Y0**beta2
    
    st.success(f"De berekende temperatuur $T^*(t)$ in jaar {t_single} is:")
    st.markdown(f"## **{T_ster_single_result[0]:.3f} °C**")
    st.markdown(f"Basis GHG-waarde: **{GHG:.1f}**")
    st.caption("De initiële constante is vereenvoudigd tot $\\kappa \\cdot NGHG(0)$.")


# =========================================================================
# 2. GRAFIEK OVER DE VOLLEDIGE PERIODE
# =========================================================================

st.header("Dynamiek van $T^*(t)$ over de tijd")

# Bepaal het bereik voor de grafiek
t_range = np.arange(0, t_single + 1 if t_single > 0 else 201, 1)

# Bereken de reeks T*(t) waarden met de functie
T_ster_series, foutmelding_series = bereken_temperatuur(t_range, *params)

if foutmelding_series:
    st.error(f"Fout bij het genereren van de grafiek: {foutmelding_series}")
else:
    # Maak een Pandas DataFrame
    df = pd.DataFrame({
        'Jaar': t_range,
        'Temperatuur (°C)': T_ster_series
    })
    
    # Plot de grafiek
    st.line_chart(df, x='Jaar', y='Temperatuur (°C)')

