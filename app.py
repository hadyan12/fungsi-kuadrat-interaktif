# Fungsi Kuadrat Interaktif - Versi Eksploratif Lengkap
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------- SETUP AWAL ----------------------------
st.set_page_config(page_title="📐 Eksplorasi Fungsi Kuadrat", page_icon="📐")
st.title("📐 Eksplorasi Mandiri Fungsi Kuadrat")

st.markdown("""
Selamat datang di eksplorasi fungsi kuadrat! 🎓

Kamu akan belajar lewat percobaan, analisis data, dan berpikir kritis. Bukan sekadar rumus, tapi *proses menemukan*.

---
## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum fungsi kuadrat dari data
- Menentukan akar-akar dengan metode faktorisasi

---
## 🇮🇩 Profil Pelajar Pancasila
- Bernalar kritis dan mandiri
- Kreatif dalam menemukan pola
- Bertanggung jawab atas proses belajar
---
""")

# ---------------------------- INISIALISASI ----------------------------
def fungsi_rahasia(x):
    return (x - 1)*(x - 3)  # f(x) = x^2 - 4x + 3

def bentuk_eksplisit(x):
    return x**2 - 4*x + 3

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.langkah = 1
    st.session_state.salah_input_y = 0
    st.session_state.jawaban_y = []
    st.session_state.a = 1
    st.session_state.b = -4
    st.session_state.c = 3
    st.session_state.faktorisasi_benar = False

# ---------------------------- LANGKAH 1 ----------------------------
if st.session_state.langkah == 1:
    st.header("🟩 Langkah 1: Coba Masukkan Nilai x")
    st.markdown("Masukkan beberapa nilai x (antara -5 sampai 7) dan amati nilai y = f(x)")
    x_input = st.number_input("Nilai x:", min_value=-5, max_value=7, step=1)
    if st.button("Tambah Titik"):
        if x_input not in [x for x, y in st.session_state.data_titik]:
            y_val = fungsi_rahasia(x_input)
            st.session_state.data_titik.append((x_input, y_val))
            st.session_state.jawaban_y.append("")

    if st.session_state.data_titik:
        df = pd.DataFrame(st.session_state.data_titik, columns=["x", "y = f(x)"])
        st.write("### 📊 Tabel Titik yang Diuji")
        st.dataframe(df)

        fig, ax = plt.subplots()
        x_vals, y_vals = zip(*st.session_state.data_titik)
        ax.scatter(x_vals, y_vals, color="green")
        ax.set_title("Titik-titik f(x)")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        st.pyplot(fig)

        if len(st.session_state.data_titik) >= 5:
            if st.button("Lanjut ke Langkah 2"):
                st.session_state.langkah = 2
                st.rerun()

# ---------------------------- LANGKAH 2 ----------------------------
elif st.session_state.langkah == 2:
    st.header("🟦 Langkah 2: Coba Tebak Nilai y")
    st.markdown("Masukkan tebakan nilai **y** untuk setiap nilai **x** yang telah kamu coba.")

    salah_total = 0
    for i, (x_val, y_true) in enumerate(st.session_state.data_titik):
        tebakan = st.text_input(f"x = {x_val}, tebak y:", value=st.session_state.jawaban_y[i], key=f"y_tebak_{i}")
        st.session_state.jawaban_y[i] = tebakan

        if tebakan.strip() != "":
            try:
                if int(tebakan) != y_true:
                    salah_total += 1
                    st.markdown(f"❌ Salah. y untuk x = {x_val} seharusnya bukan {tebakan}.")
                else:
                    st.markdown("✅ Benar")
            except:
                salah_total += 1
                st.markdown("⚠ Masukkan harus berupa angka bulat.")

    if salah_total >= 1:
        st.warning("Masih ada jawaban yang salah. Grafik akan ditandai merah.")
        fig, ax = plt.subplots()
        x_vals, y_vals = zip(*st.session_state.data_titik)
        ax.scatter(x_vals, y_vals, color="red")
        ax.set_title("Titik Salah")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.success("Semua tebakan benar!")
        if st.button("➡ Lanjut ke Langkah 3"):
            st.session_state.langkah = 3
            st.rerun()

    if salah_total >= 3:
        st.info("""
        🔍 **Petunjuk:**
        - Ingat bahwa ini fungsi kuadrat.
        - Lihat apakah perubahan y konsisten saat x naik 1 satuan.
        - Gunakan pola kuadrat: y = ax² + bx + c
        """)

    if salah_total >= 5:
        st.warning("""
        ❗ Kamu sudah 5 kali salah.

        Sekarang coba ambil 3 titik, misalnya:
        (x₁, y₁), (x₂, y₂), (x₃, y₃)

        Masukkan ke:
        \[
        y = ax^2 + bx + c
        \]

        Gunakan substitusi → dapat 3 persamaan.
        Eliminasi → selesaikan di kertas ya!
        """)

# ---------------------------- LANGKAH SELANJUTNYA ----------------------------
# Langkah 3–6 akan ditambahkan bertahap setelah konfirmasi langkah 1 & 2
# (berisi eliminasi manual, input hasil, faktorisasi, dan cek akar)

if st.session_state.langkah >= 3:
    st.info("📌 Langkah 3 sampai 6 sedang dalam proses pembangunan tahap berikutnya.")
