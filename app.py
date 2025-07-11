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
    return (x - 2)*(x - 4) - 1  # Titik puncak di x = 3, y = -1 (bulat)

def bentuk_eksplisit(x):
    return x**2 - 6*x + 7

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.langkah = 1
    st.session_state.tebakan_y = []
    st.session_state.salah_y = []
    st.session_state.tebakan_abc = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_abc = 0
    st.session_state.salah_faktorisasi = 0

# ---------------------------- LANGKAH 1 ----------------------------
if st.session_state.langkah == 1:
    st.header("🟩 Langkah 1: Masukkan Titik-titik")
    st.markdown("Masukkan nilai x antara -2 sampai 7 untuk melihat nilai y")

    x_input = st.number_input("Nilai x:", min_value=-2, max_value=7, step=1)
    if st.button("Tambah Titik"):
        if x_input not in [x for x, _ in st.session_state.data_titik]:
            y_val = fungsi_rahasia(x_input)
            st.session_state.data_titik.append((x_input, y_val))
            st.session_state.tebakan_y.append("")
            st.session_state.salah_y.append(None)

    if st.session_state.data_titik:
        df = pd.DataFrame(st.session_state.data_titik, columns=["x", "y"])
        st.write("### Tabel Titik")
        st.dataframe(df)

        fig, ax = plt.subplots()
        x_vals, y_vals = zip(*st.session_state.data_titik)
        ax.scatter(x_vals, y_vals, color="green")
        ax.set_title("Titik-titik (x, y)")
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
    st.header("🟦 Langkah 2: Tebak Nilai y dari Titik")
    st.markdown("Masukkan tebakan nilai **y** dari tiap titik yang sudah kamu coba.")

    salah_total = 0
    hasil_tabel = []
    for i, (x, y) in enumerate(st.session_state.data_titik):
        tebakan = st.text_input(f"x = {x}, y = ", value=st.session_state.tebakan_y[i], key=f"y_input_{i}")
        st.session_state.tebakan_y[i] = tebakan

        try:
            if tebakan.strip() != "":
                if int(tebakan) == y:
                    st.session_state.salah_y[i] = False
                    hasil_tabel.append([x, tebakan, "✅ Benar"])
                else:
                    st.session_state.salah_y[i] = True
                    hasil_tabel.append([x, tebakan, "❌ Salah"])
                    salah_total += 1
        except:
            st.session_state.salah_y[i] = True
            hasil_tabel.append([x, tebakan, "⚠ Bukan angka"])
            salah_total += 1

    st.write("### Hasil Tebakan")
    df_hasil = pd.DataFrame(hasil_tabel, columns=["x", "Tebakan y", "Hasil"])
    st.dataframe(df_hasil)

    warna = "green" if salah_total == 0 else "red"
    fig, ax = plt.subplots()
    x_vals, y_vals = zip(*st.session_state.data_titik)
    ax.scatter(x_vals, y_vals, color=warna)
    ax.set_title("Grafik Data")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    st.pyplot(fig)

    if salah_total == 0:
        st.success("Semua tebakan benar!")
        if st.button("➡ Lanjut ke Langkah 3"):
            st.session_state.langkah = 3
            st.rerun()
    else:
        st.warning("Masih ada tebakan yang salah. Coba lagi ya!")

    if salah_total >= 3:
        st.info("""
        🔍 **Hint:**
        - Ini fungsi kuadrat: berbentuk \( y = ax^2 + bx + c \)
        - Perhatikan perubahan y ketika x naik.
        - Gunakan pola simetri atau titik puncak.
        """)
    if salah_total >= 5:
        st.warning("""
        ❗ Sudah 5 kali salah. Yuk kita bantu perlahan:

        1. Ambil 3 titik, misalnya (x₁, y₁), (x₂, y₂), (x₃, y₃)
        2. Substitusikan ke rumus: \( y = ax^2 + bx + c \)
        3. Dapatkan 3 persamaan
        4. Eliminasi di kertas untuk dapatkan nilai a, b, c
        """)

# ---------------------------- LANGKAH 3 ----------------------------
elif st.session_state.langkah == 3:
    st.header("🟨 Langkah 3: Substitusi dan Eliminasi")
    st.markdown("Sekarang kamu akan mencari nilai a, b, dan c dari \( y = ax^2 + bx + c \) berdasarkan titik.")

    st.markdown("Gunakan 3 titik yang sudah kamu ambil tadi dan masukkan ke bentuk \( y = ax^2 + bx + c \) untuk membentuk 3 persamaan. Silakan hitung di kertas.")

    st.markdown("### 🔢 Sekarang masukkan hasilmu")
    a = st.text_input("a =", value=st.session_state.tebakan_abc["a"])
    b = st.text_input("b =", value=st.session_state.tebakan_abc["b"])
    c = st.text_input("c =", value=st.session_state.tebakan_abc["c"])

    if st.button("Cek Jawaban Bentuk Umum"):
        st.session_state.tebakan_abc = {"a": a, "b": b, "c": c}
        try:
            if int(a) == 1 and int(b) == -6 and int(c) == 7:
                st.success("✅ Jawaban benar!")
                st.session_state.langkah = 4
                st.rerun()
            else:
                st.session_state.salah_tebakan_abc += 1
                st.error("❌ Jawaban belum tepat")
                if st.session_state.salah_tebakan_abc >= 3:
                    st.info("Coba gunakan kembali eliminasi. Salah satu dari a, b, atau c mungkin keliru.")
                if st.session_state.salah_tebakan_abc >= 5:
                    st.warning("""
                    ⚠ Kamu sudah 5 kali salah.

                    Kita bantu sedikit:
                    - Coba mulai dari a = 1 dulu
                    - Lalu hitung ulang untuk b dan c dari salah satu titik
                    """)
        except:
            st.error("Masukkan harus berupa bilangan bulat")

# ---------------------------- LANGKAH 4 ----------------------------
elif st.session_state.langkah == 4:
    st.header("🟧 Langkah 4: Bentuk Umum dan Grafik")
    st.markdown("Kita sudah punya nilai a, b, dan c. Bentuk umum fungsi kuadrat adalah:")

    st.latex("y = x^2 - 6x + 7")

    fig, ax = plt.subplots()
    x_vals = np.linspace(-2, 8, 200)
    y_vals = x_vals**2 - 6*x_vals + 7
    ax.plot(x_vals, y_vals, label="y = x² - 6x + 7", color="blue")
    ax.grid(True)
    ax.set_title("Grafik Fungsi Kuadrat")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)

    if st.button("➡ Lanjut ke Langkah 5"):
        st.session_state.langkah = 5
        st.rerun()

# ---------------------------- LANGKAH 5 ----------------------------
elif st.session_state.langkah == 5:
    st.header("🟪 Langkah 5: Faktorisasi")
    st.markdown("Sekarang kita faktorkan bentuk \( y = x^2 - 6x + 7 \)")

    pilihan = st.radio("Manakah bentuk faktorisasi yang benar?", [
        "(x - 1)(x - 7)",
        "(x - 2)(x - 4)",
        "(x - 3)^2",
        "(x - 3)(x - 3) + 2",
    ])

    if st.button("Cek Faktorisasi"):
        if pilihan == "(x - 2)(x - 4)":
            st.success("✅ Faktorisasi benar!")
            st.session_state.langkah = 6
            st.rerun()
        else:
            st.session_state.salah_faktorisasi += 1
            st.error("❌ Masih salah")
            if st.session_state.salah_faktorisasi >= 3:
                st.info("Hint: Perkalian dua bilangan hasilnya 7, jumlahnya 6?")

# ---------------------------- LANGKAH 6 ----------------------------
elif st.session_state.langkah == 6:
    st.header("🟥 Langkah 6: Akar-akar Persamaan Kuadrat")
    st.markdown("Sekarang kita lihat akar-akarnya.")

    st.latex("(x - 2)(x - 4) = 0")
    st.latex("x = 2 \quad atau \quad x = 4")

    st.success("✅ Selamat! Kamu telah menemukan akar-akar fungsi kuadrat dengan eksplorasi mandiri.")
