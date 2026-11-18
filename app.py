import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit

st.set_page_config(page_title="Simulator Logistik Bakteri", page_icon="🦠", layout="wide")
st.title("🦠 Simulator Pertumbuhan Logistik Bakteri")
st.caption("TA-07 Pemodelan dan Simulasi | Model: dP/dt = r·P·(1 − P/K) | Metode: Euler, RK4, solve_ivp")

# ---------- Data ----------
@st.cache_data
def load_data(file):
    raw = pd.read_csv(file)
    row = raw.iloc[0]
    df = pd.DataFrame({"Time": row.index.astype(float), "Population": row.values})
    df["Jam"] = df["Time"] / 3600
    return df

up = st.sidebar.file_uploader("Upload bacterial_growth.csv (opsional)", type="csv")
df = load_data(up if up else "bacterial_growth.csv")
P0 = float(df.Population.iloc[0])
T = float(df.Jam.max())

# ---------- Model ----------
def f(t, P, r, K):
    return r * P * (1 - P / K)

def euler(h, r, K):
    n = int(round(T / h)); t = np.linspace(0, n * h, n + 1); y = np.zeros(n + 1); y[0] = P0
    for i in range(n):
        y[i + 1] = y[i] + h * f(t[i], y[i], r, K)
    return t, y

def rk4(h, r, K):
    n = int(round(T / h)); t = np.linspace(0, n * h, n + 1); y = np.zeros(n + 1); y[0] = P0
    for i in range(n):
        k1 = f(t[i], y[i], r, K); k2 = f(t[i], y[i] + h / 2 * k1, r, K)
        k3 = f(t[i], y[i] + h / 2 * k2, r, K); k4 = f(t[i], y[i] + h * k3, r, K)
        y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return t, y

def ivp(r, K):
    tt = np.linspace(0, T, 400)
    s = solve_ivp(f, (0, T), [P0], args=(r, K), t_eval=tt, rtol=1e-8, atol=1e-10)
    return s.t, s.y[0]

def simulate(method, h, r, K):
    if method == "Euler": return euler(h, r, K)
    if method == "RK4": return rk4(h, r, K)
    return ivp(r, K)

def rmse(t, y):
    return float(np.sqrt(np.mean((np.interp(df.Jam, t, y) - df.Population) ** 2)))

@st.cache_data
def calibrate():
    logi = lambda t, r, K: K / (1 + (K - P0) / P0 * np.exp(-r * t))
    (r, K), _ = curve_fit(logi, df.Jam, df.Population, p0=[0.3, 0.62])
    return float(r), float(K)

r_fit, K_fit = calibrate()

# ---------- Sidebar ----------
st.sidebar.header("Parameter")
if st.sidebar.button("Gunakan hasil kalibrasi (curve_fit)"):
    st.session_state["r"], st.session_state["K"] = r_fit, K_fit
r = st.sidebar.slider("Laju pertumbuhan r (per jam)", 0.01, 1.5, st.session_state.get("r", round(r_fit, 3)), 0.005, key="r")
K = st.sidebar.slider("Kapasitas dukung K", 0.3, 1.2, st.session_state.get("K", round(K_fit, 3)), 0.005, key="K")
method = st.sidebar.selectbox("Metode numerik", ["Euler", "RK4", "solve_ivp"])
h = st.sidebar.select_slider("Step size h (jam)", [0.1, 0.25, 0.5, 1.0, 2.0, 5.0], value=1.0,
                             disabled=(method == "solve_ivp"))
st.sidebar.header("Skenario What-If")
r_pct = st.sidebar.slider("Perubahan r (%)", -80, 100, -50, 5)
K_pct = st.sidebar.slider("Perubahan K (%)", -50, 100, 0, 5)

# ---------- Output ----------
t_b, y_b = simulate(method, h, r, K)
r_s, K_s = r * (1 + r_pct / 100), K * (1 + K_pct / 100)
t_s, y_s = simulate(method, h, r_s, K_s)

c1, c2, c3, c4 = st.columns(4)
c1.metric("RMSE baseline vs data", f"{rmse(t_b, y_b):.4f}")
c2.metric("Populasi akhir (baseline)", f"{y_b[-1]:.3f}")
c3.metric("Populasi akhir (skenario)", f"{y_s[-1]:.3f}", f"{y_s[-1]-y_b[-1]:+.3f}")
c4.metric("Kalibrasi terbaik", f"r={r_fit:.3f}, K={K_fit:.3f}")

tab1, tab2, tab3 = st.tabs(["📈 Data vs Simulasi", "🔀 What-If", "🔬 Pengaruh Step Size"])

with tab1:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df.Jam, df.Population, "o", ms=3, color="gray", label="Data asli")
    ax.plot(t_b, y_b, "r", label=f"Simulasi {method}")
    ax.set_xlabel("Waktu (jam)"); ax.set_ylabel("Populasi"); ax.grid(alpha=.3); ax.legend()
    st.pyplot(fig)
    st.info("Model logistik murni tidak memuat fase lag di awal dan penurunan setelah puncak (±13 jam), sehingga RMSE tidak bisa nol.")
    out = pd.DataFrame({"Jam": t_b, "Populasi_simulasi": y_b})
    st.download_button("Unduh hasil simulasi (CSV)", out.to_csv(index=False), "hasil_simulasi.csv", "text/csv")

with tab2:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df.Jam, df.Population, "o", ms=3, color="gray", label="Data asli")
    ax.plot(t_b, y_b, "r", label=f"Baseline (r={r:.3f}, K={K:.3f})")
    ax.plot(t_s, y_s, "b--", label=f"Skenario (r={r_s:.3f}, K={K_s:.3f})")
    ax.set_xlabel("Waktu (jam)"); ax.set_ylabel("Populasi"); ax.grid(alpha=.3); ax.legend()
    st.pyplot(fig)
    st.write(f"Perubahan r sebesar **{r_pct:+d}%** dan K sebesar **{K_pct:+d}%** mengubah populasi akhir dari "
             f"**{y_b[-1]:.3f}** menjadi **{y_s[-1]:.3f}**. r mengatur kecepatan, K mengatur batas atas.")

with tab3:
    exact = lambda t: K / (1 + (K - P0) / P0 * np.exp(-r * t))
    rows = []
    for hh in [5, 2, 1, 0.5, 0.1]:
        te, ye = euler(hh, r, K); tr, yr = rk4(hh, r, K)
        rows.append([hh, abs(ye[-1] - exact(te[-1])), abs(yr[-1] - exact(tr[-1]))])
    st.dataframe(pd.DataFrame(rows, columns=["h (jam)", "Galat Euler", "Galat RK4"]).style.format({"Galat Euler": "{:.6f}", "Galat RK4": "{:.8f}"}),
                 hide_index=True)
    st.caption("Galat diukur terhadap solusi analitik pada t akhir. Euler orde 1 (galat ∝ h), RK4 orde 4 (galat ∝ h⁴).")
