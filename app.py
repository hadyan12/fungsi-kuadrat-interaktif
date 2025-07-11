# Fungsi Kuadrat Interaktif - Versi Eksploratif Lengkap (Revisi Total)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    return (x - 2)*(x - 4)  # Titik puncak di x = 3, y = -1

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.langkah = 1
    st.session_state.tebakan_y = {}
    st.session_state.salah_y = {}
    st.session_state.tebakan_abc = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_abc = 0
    st.session_state.salah_faktorisasi = 0

# ---------------------------- LANGKAH 1 ----------------------------
if st.session_state.langkah == 1:
    st.header("🟩 Langkah 1: Masukkan Titik-titik")
    st.markdown("Masukkan nilai x antara -2 sampai 7 (bilangan bulat) untuk melihat nilai y dari fungsi kuadrat.")

    x_input = st.number_input("Nilai x:", min_value=-2, max_value=7, step=1)
    if st.button("Tambah Titik"):
        if x_input not in [x for x, _ in st.session_state.data_titik]:
            y_val = fungsi_rahasia(x_input)
            st.session_state.data_titik.append((x_input, y_val))

    if st.session_state.data_titik:
        df = pd.DataFrame(st.session_state.data_titik, columns=["x", "y"])
        st.write("### Tabel Titik")
        st.dataframe(df)

        fig, ax = plt.subplots()
        x_vals, y_vals = zip(*st.session_state.data_titik)
        ax.scatter(x_vals, y_vals, color="green")
        for x, y in st.session_state.data_titik:
            ax.axvline(x, linestyle='--', color='gray', alpha=0.4)
            ax.axhline(y, linestyle='--', color='gray', alpha=0.4)
        ax.set_xticks(range(-2, 9))
        ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
        ax.grid(True)
        ax.set_title("Grafik Fungsi berdasarkan Titik")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        st.pyplot(fig)

        if len(st.session_state.data_titik) >= 3:
            if st.button("➡ Lanjut ke Langkah 2"):
                st.session_state.langkah = 2
                st.rerun()

# ---------------------------- LANGKAH 2 ----------------------------
elif st.session_state.langkah == 2:
    st.header("🟦 Langkah 2: Tebak Nilai y dari Titik")
    st.markdown("Masukkan tebakan nilai **y** untuk setiap titik x di bawah. Kamu akan melihat mana yang benar dan mana yang belum.")

    hasil_tabel = []
    salah_total = 0
    for x, y in st.session_state.data_titik:
        tebakan = st.text_input(f"x = {x}, y =", value=st.session_state.tebakan_y.get(x, ""), key=f"tebakan_{x}")
        st.session_state.tebakan_y[x] = tebakan
        try:
            if tebakan.strip() != "":
                if int(tebakan) == y:
                    st.session_state.salah_y[x] = False
                    hasil_tabel.append([x, tebakan, "✅ Benar"])
                else:
                    st.session_state.salah_y[x] = True
                    hasil_tabel.append([x, tebakan, "❌ Salah"])
                    salah_total += 1
        except:
            st.session_state.salah_y[x] = True
            hasil_tabel.append([x, tebakan, "⚠ Bukan angka"])
            salah_total += 1

    st.write("### Rekap Tebakan")
    st.dataframe(pd.DataFrame(hasil_tabel, columns=["x", "Tebakan y", "Hasil"]))

    warna = "green" if salah_total == 0 else "red"
    fig, ax = plt.subplots()
    x_vals, y_vals = zip(*st.session_state.data_titik)
    ax.scatter(x_vals, y_vals, color=warna)
    for x, y in st.session_state.data_titik:
        ax.axvline(x, linestyle='--', color='gray', alpha=0.4)
        ax.axhline(y, linestyle='--', color='gray', alpha=0.4)
    ax.set_xticks(range(-2, 9))
    ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
    ax.grid(True)
    ax.set_title("Grafik Fungsi berdasarkan Titik")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)

    if salah_total == 0:
        st.success("✅ Semua tebakan benar!")
        if st.button("➡ Lanjut ke Langkah 3"):
            st.session_state.langkah = 3
            st.rerun()
    else:
        st.warning("Masih ada yang salah. Coba cek kembali.")

    if salah_total >= 3:
        st.info("""
        🔍 **Hint:**
        - Perhatikan simetri grafik.
        - Bentuk umum fungsi kuadrat adalah \( y = ax^2 + bx + c \)
        - Coba lihat nilai y ketika x semakin jauh dari titik tengah.
        """)
    if salah_total >= 5:
        st.warning("""
        ⚠ Sudah 5 kali salah. Yuk kita bantu secara bertahap:

        1. Ambil 3 titik, misalnya (x₁, y₁), (x₂, y₂), (x₃, y₃)
        2. Substitusikan ke rumus: \( y = ax^2 + bx + c \)
        3. Dapatkan 3 persamaan
        4. Eliminasi secara manual di kertas
        """)

# ---------------------------- LANGKAH 3 ----------------------------
elif st.session_state.langkah == 3:
    st.header("🟨 Langkah 3: Substitusi dan Eliminasi")
    st.markdown("""
    Sekarang kamu akan mencari nilai **a**, **b**, dan **c** dari fungsi kuadrat.

    👉 Pilih 3 titik dari data di atas.
    👉 Substitusikan satu per satu ke bentuk \( y = ax^2 + bx + c \)
    👉 Dapatkan 3 persamaan, lalu lakukan eliminasi di kertas
    """)

    st.markdown("Setelah kamu menghitung, silakan masukkan nilai a, b, dan c hasil dari eliminasi:")
    a = st.text_input("a =", value=st.session_state.tebakan_abc["a"])
    b = st.text_input("b =", value=st.session_state.tebakan_abc["b"])
    c = st.text_input("c =", value=st.session_state.tebakan_abc["c"])

    if st.button("Cek Jawaban"):
        st.session_state.tebakan_abc = {"a": a, "b": b, "c": c}
        try:
            if int(a) == 1 and int(b) == -6 and int(c) == 8:
                st.success("✅ Jawaban benar! Lanjut ke bentuk umum.")
                st.session_state.langkah = 4
                st.rerun()
            else:
                st.session_state.salah_tebakan_abc += 1
                st.error("❌ Masih salah. Coba lagi.")
                if st.session_state.salah_tebakan_abc >= 3:
                    st.info("Gunakan eliminasi. Mungkin hanya satu nilai yang salah.")
                if st.session_state.salah_tebakan_abc >= 5:
                    st.warning("Coba mulai dari a = 1 dan cek ulang dengan titik (2,0)")
        except:
            st.error("Masukkan harus berupa angka bulat")

# (Langkah 4, 5, 6 akan menyusul dalam iterasi berikut jika diminta langsung)
