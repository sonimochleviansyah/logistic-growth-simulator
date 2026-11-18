<div align="center">

# 🦠 Logistic Growth Simulator

### Simulasi Sistem Dinamik: Pertumbuhan Bakteri dengan Model Logistik

**Euler · Runge-Kutta 4 · SciPy `solve_ivp` · What-If Analysis · Streamlit App**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-ODE%20Solver-8CAAE6?logo=scipy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## ✨ Tentang Proyek

Proyek **Tugas Akhir 07 – Pemodelan dan Simulasi (Modul 7: Dynamic System Simulation)**. Pertumbuhan populasi bakteri dimodelkan sebagai sistem dinamik dengan persamaan diferensial logistik, disimulasikan dengan tiga metode numerik, dikalibrasi terhadap data riil, lalu diuji lewat skenario _What-If_.

$$\frac{dP}{dt} = r\,P\left(1-\frac{P}{K}\right)$$

| Simbol | Arti                                                    |
| ------ | ------------------------------------------------------- |
| `P`    | Populasi bakteri (stock)                                |
| `r`    | Laju pertumbuhan (feedback positif)                     |
| `K`    | Kapasitas dukung / carrying capacity (feedback negatif) |

## 🎯 Fitur

- 📊 **EDA** dataset time-series (89 titik, tanpa missing value)
- 🧮 **3 metode numerik:** Euler, RK4, `scipy.integrate.solve_ivp`
- 🎛️ **Kalibrasi otomatis** `r` dan `K` dengan `curve_fit` + metrik RMSE
- 🔀 **What-If:** ubah `r` dan `K`, bandingkan dengan baseline
- 🔬 **Analisis step size:** galat Euler (orde 1) vs RK4 (orde 4)
- 🌐 **Web app interaktif** berbasis Streamlit + unduh hasil CSV

## 📈 Hasil Utama

| Metrik                            | Nilai               |
| --------------------------------- | ------------------- |
| `r` terkalibrasi                  | **0,308 / jam**     |
| `K` terkalibrasi                  | **0,631**           |
| RMSE vs data                      | **0,040**           |
| Galat Euler (h = 5 jam → 0,1 jam) | 0,0099 → **0,0002** |

<p align="center">
  <img src="images/fig5.png" width="48%" alt="Data vs simulasi">
  <img src="images/fig3.png" width="48%" alt="Perbandingan metode">
</p>

### 🔀 Skenario What-If

| Skenario      | Populasi akhir | Efek                                    |
| ------------- | -------------- | --------------------------------------- |
| Baseline      | 0,626          | Kurva S normal                          |
| `r` turun 50% | 0,525          | Jauh lebih lambat, 90% K belum tercapai |
| `K` naik 20%  | 0,749          | Plateau lebih tinggi                    |
| `K` turun 20% | 0,502          | Plateau lebih rendah                    |

<p align="center"><img src="images/fig4.png" width="70%" alt="What-If"></p>

> **Insight:** `r` mengatur _kecepatan_ pertumbuhan, `K` mengatur _batas atas_.

## ⚠️ Keterbatasan

Model logistik murni tidak menangkap **fase lag** di awal dan **penurunan setelah puncak (±13 jam)** pada data nyata, sehingga RMSE tidak bisa nol. Pengembangan: model Gompertz/Baranyi atau penambahan laju kematian.

## 🚀 Cara Menjalankan

```bash
git clone https://github.com/USERNAME/logistic-growth-simulator.git
cd logistic-growth-simulator
pip install -r requirements.txt
streamlit run app.py
```

Atau buka notebook di Google Colab: `TA07_Simulasi_Logistik.ipynb` (unggah `bacterial_growth.csv` terlebih dahulu).

## 📁 Struktur Repositori

```
├── app.py                        # Aplikasi Streamlit
├── TA07_Simulasi_Logistik.ipynb  # Notebook simulasi lengkap
├── TA07_Laporan_Template.pdf     # Laporan analisis
├── bacterial_growth.csv          # Dataset
├── requirements.txt
└── images/                       # Grafik hasil simulasi
```

## 📚 Referensi

- Dataset: [Py4Life/TAU2016 – bacterial_growth.csv](https://github.com/Py4Life/TAU2016/blob/master/bacterial_growth.csv)
- Fikri, R. (2023). _Exploratory Data Analysis (EDA)_. Medium.
- Islam, N. (n.d.). _Comprehensive Guide to Time Series Data Analytics and Forecasting with Python_. Medium.
- Anggara, M. B. (2026). _Modul Praktikum Pemodelan dan Simulasi – Modul 7_.

## 👤 Author

**[Soni Moch Leviansyah]** · NIM [301240030] · [Program Studi, Universitas]

<div align="center">⭐ Kalau bermanfaat, jangan lupa kasih star ya! ⭐</div>
