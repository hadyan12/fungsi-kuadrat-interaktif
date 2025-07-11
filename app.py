# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ---------- Konfigurasi ----------
st.set_page_config(page_title="📐 Eksplorasi Fungsi Kuadrat", page_icon="📐")

st.title("📐 Eksplorasi Fungsi Kuadrat")
st.markdown("""
Selamat datang! Di sini kamu akan **menemukan sendiri rumus fungsi kuadrat** dari data.  
Jangan khawatir, kamu akan dibimbing secara bertahap 😊

---  
## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum fungsi kuadrat dari data.
- Menentukan akar-akarnya menggunakan faktorisasi.

""")

# ---------- Fungsi Rahasia ----------
def fungsi_rahasia(x):
    return 1 * (x - 2) * (x + 3)  # f(x) = x^2 + x - 6 → a=1, b=1, c=-6

# ---------- Inisialisasi ----------
if "data_x" not in st.session_state:
    st.session_state.data_x = []
    st.session_state.data_fx = []
    st.session_state.salah_tebakan = 0
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False

# ---------- LANGKAH 1 ----------
st.header("🟩 Langkah 1: Masukkan Titik-titik Fungsi")

with st.form("form_input"):
    x_val = st.number_input("Masukkan nilai x (antara -5 dan 5):", min_value=-5, max_value=5, step=1)
    submitted = st.form_submit_button("Tambahkan titik")

    if submitted:
        if x_val in st.session_state.data_x:
            st.warning("❗ Nilai x ini sudah dimasukkan.")
        else:
            st.session_state.data_x.append(x_val)
            st.session_state.data_fx.append(fungsi_rahasia(x_val))

if st.session_state.data_x:
    st.subheader("📋 Tabel Titik")
    st.table({"x": st.session_state.data_x, "f(x)": st.session_state.data_fx})

    # Grafik
    fig, ax = plt.subplots()
    warna = "red" if st.session_state.salah_tebakan >= 3 else "blue"
    ax.scatter(st.session_state.data_x, st.session_state.data_fx, color=warna, s=100)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_title("Grafik Titik f(x)")
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_xlim(-6, 6)
    ax.set_ylim(min(st.session_state.data_fx) - 2, max(st.session_state.data_fx) + 2)
    st.pyplot(fig)

    if len(st.session_state.data_x) >= 5:
        if st.button("➡ Lanjut ke Langkah 2"):
            st.session_state.langkah_2 = True

# ---------- LANGKAH 2 ----------
if st.session_state.langkah_2:
    st.header("🟦 Langkah 2: Cocokkan Titik-titik dengan Fungsi")

    st.markdown("Sekarang coba masukkan kembali titik-titik hasil f(x)-mu. Apakah cocok semua?")
    
    tebakan_x = st.number_input("Coba masukkan nilai x (ulang):", key="tebakan_x")
    tebakan_fx = st.number_input("Apa nilai f(x) menurutmu?", key="tebakan_fx")

    if st.button("✅ Cek Jawaban"):
        benar = fungsi_rahasia(tebakan_x) == tebakan_fx
        if benar:
            st.success("✅ Benar! Titik ini cocok dengan fungsi yang sedang disembunyikan.")
        else:
            st.session_state.salah_tebakan += 1
            st.error("❌ Belum cocok.")
            
            if st.session_state.salah_tebakan == 3:
                st.warning("⚠️ Sudah 3 kali salah. Clue: Perhatikan di mana grafik memotong sumbu-x.")

            if st.session_state.salah_tebakan >= 5:
                st.info("🧠 Bantuan: Gunakan 3 titik yang kamu punya. Masukkan ke bentuk umum:\n\n"
                        r"$f(x) = ax^2 + bx + c$ lalu buat sistem persamaan. Kita akan bantu di langkah selanjutnya.")
                st.session_state.langkah_3 = True

    if st.button("➡ Lanjut ke Langkah 3", key="next3"):
        st.session_state.langkah_3 = True
