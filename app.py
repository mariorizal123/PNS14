import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Simulator Bisnis", page_icon="✨", layout="centered")

# ==========================================
# LOGIKA MATEMATIKA & MODEL
# ==========================================
@st.cache_resource
def load_model():
    # Memuat model replika dari file pkl
    return joblib.load('model_praktikum_14.pkl')

def run_simulation(model, iklan, diskon):
    """
    Menghitung prediksi What-If secara terpisah dari UI.
    """
    # Baseline (Iklan 10 Juta, Diskon 10%)
    baseline_input = np.array([[10, 10]])
    baseline_pred = model.predict(baseline_input)[0]
    
    # Skenario Intervensi
    intervention_input = np.array([[iklan, diskon]])
    prediction = model.predict(intervention_input)[0]
    
    # Delta
    delta = prediction - baseline_pred
    return baseline_pred, prediction, delta

# ==========================================
# LOGIKA UI (STREAMLIT)
# ==========================================

model = load_model()

# --- HEADER ---
st.title("✨ Simulator Keputusan Bisnis")

# Info Mahasiswa di Tengah
st.markdown("""
<div style='
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    padding: 20px; 
    border-radius: 15px; 
    margin-bottom: 25px; 
    box-shadow: 0 10px 20px rgba(0, 114, 255, 0.3);
'>
    <h3 style='margin:0; color: #ffffff; font-weight: 800; letter-spacing: 0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>👨‍💼 M. Mario Rizal Efendi</h3>
    <div style='margin-top: 12px; display: flex; gap: 10px; flex-wrap: wrap;'>
        <span style='background: rgba(255, 255, 255, 0.25); color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 14px; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>🏫 Kelas: 3A</span>
        <span style='background: rgba(255, 255, 255, 0.25); color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 14px; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>🆔 NPM: 2313020029</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #7f8c8d; font-size: 16px;'>Uji coba berbagai skenario untuk melihat dampak intervensi (Iklan & Diskon) terhadap keuntungan secara real-time.</p>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR KONTROL ---
with st.sidebar:
    st.markdown("**Nama:** M. Mario Rizal Efendi")
    st.markdown("**Kelas:** 3A")
    st.markdown("**NPM:** 2313020029")
    st.divider()

    st.header("⚙️ Parameter Kontrol")
    st.write("Sesuaikan strategi Anda:")
    
    # Menggunakan slider
    iklan_slider = st.slider("Anggaran Iklan (Jt)", min_value=0, max_value=50, value=10, step=1)
    diskon_slider = st.slider("Besaran Diskon (%)", min_value=0, max_value=20, value=5, step=1)

# --- EKSEKUSI ---
baseline_pred, prediksi, delta = run_simulation(model, iklan_slider, diskon_slider)

# --- PANEL METRIK ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Kondisi Saat Ini", f"Rp {baseline_pred:.1f} Jt")
    
with col2:
    st.metric("Proyeksi Skenario", f"Rp {prediksi:.1f} Jt", f"{delta:.1f} Jt")

with col3:
    # Menghitung Persentase Pertumbuhan agar lebih manajerial
    pertumbuhan = (delta / baseline_pred) * 100 if baseline_pred != 0 else 0
    st.metric("Pertumbuhan Laba", f"{pertumbuhan:.1f}%")

st.write("") # (whitespace)

# --- STORYTELLING MINIMALIS ---
if delta > 0:
    st.success(f"**Tren Positif (+Rp {delta:.1f} Jt)**  \nSkenario ini diproyeksikan menguntungkan. Intervensi berhasil meningkatkan efisiensi dan mengoptimalkan margin laba.")
elif delta < 0:
    st.error(f"**Tren Negatif (-Rp {abs(delta):.1f} Jt)**  \nSkenario ini berisiko. Biaya yang dikeluarkan untuk pemasaran atau diskon berpotensi menekan profitabilitas inti.")
else:
    st.info("**Kondisi Stabil**  \nIntervensi tidak memberikan perubahan signifikan terhadap keuntungan jika dibandingkan dengan kondisi awal.")

st.write("") 
st.markdown("##### 📈 Komparasi Visual")

fig, ax = plt.subplots(figsize=(7, 3.5))

warna_baseline = '#bdc3c7'
warna_skenario = '#2ecc71' if delta >= 0 else '#e74c3c'

bars = ax.bar(['Baseline', 'Skenario Baru'], [baseline_pred, prediksi], color=[warna_baseline, warna_skenario], width=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#ecf0f1') # Garis bawah tipis
ax.tick_params(left=False, labelleft=False) # Hilangkan label angka panjang di sumbu kiri

# Menaruh angka nominal langsung mengambang di atas bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + (max(baseline_pred, prediksi)*0.03), 
            f"Rp {yval:.1f} Jt", ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2c3e50')

# Menyesuaikan warna teks sumbu X
ax.tick_params(axis='x', colors='#34495e')

st.pyplot(fig)