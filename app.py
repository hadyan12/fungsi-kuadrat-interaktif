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

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.input_manual = []
    st.session_state.langkah = 1
    st.session_state.tebakan_abc = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_abc = 0
    st.session_state.salah_faktorisasi = 0
    st.session_state.sudah_eliminasi = False

# ---------------------------- LANGKAH 1 ----------------------------
st.header("🟩 Langkah 1: Masukkan Titik-titik")
st.markdown("Masukkan nilai x antara -2 sampai 7 untuk melihat nilai y")

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
        ax.axvline(x, linestyle="dotted", color="gray")
        ax.axhline(y, linestyle="dotted", color="gray")
        ax.text(x, y, f"({x},{y})", fontsize=8, ha='right')
    ax.set_title("Titik-titik (x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(range(-2, 8))
    ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
    ax.grid(True)
    st.pyplot(fig)

# ---------------------------- LANGKAH 2 ----------------------------
st.header("🟦 Langkah 2: Tebak y dari Nilai x")
st.markdown("Masukkan **nilai x dan y** yang kamu tebak. Sistem akan mencocokkan dengan fungsi yang tersembunyi.")

col1, col2 = st.columns(2)
with col1:
    x_manual = st.number_input("Tebak nilai x:", min_value=-2, max_value=7, key="manual_x")
with col2:
    y_manual = st.text_input("Tebak nilai y:", key="manual_y")

if st.button("Cek Tebakan"):
    try:
        y_manual_val = int(y_manual)
        y_benar = fungsi_rahasia(x_manual)
        hasil = "✅ Benar" if y_manual_val == y_benar else "❌ Salah"
        st.session_state.input_manual.append((x_manual, y_manual_val, y_benar, hasil))
    except:
        st.session_state.input_manual.append((x_manual, y_manual, "?", "⚠ Input tidak valid"))

if st.session_state.input_manual:
    st.write("### Tabel Hasil Tebakanmu")
    df2 = pd.DataFrame(st.session_state.input_manual, columns=["x", "y Tebakan", "y Sebenarnya", "Status"])
    st.dataframe(df2)

    benar_terakhir = [row for row in st.session_state.input_manual if row[3] == "✅ Benar"]
    if len(benar_terakhir) >= 3:
        if st.button("➡ Lanjut ke Langkah 3"):
            st.session_state.langkah = 3
            st.session_state.tiga_titik = benar_terakhir[-3:]
            st.rerun()

# ---------------------------- LANGKAH 3 ----------------------------
if st.session_state.langkah >= 3:
    st.header("🟨 Langkah 3: Substitusi dan Eliminasi")
    st.markdown("Kita gunakan 3 titik dari Langkah 2 yang benar untuk membentuk sistem persamaan.")

    titik = st.session_state.tiga_titik
    for x, y, *_ in titik:
        st.latex(f"({x}, {y})")

    st.markdown("### Substitusi ke \( y = ax^2 + bx + c \):")
    for x, y, *_ in titik:
        st.latex(f"{y} = a({x})^2 + b({x}) + c")

    if not st.session_state.sudah_eliminasi:
        if st.button("✍️ Saya sudah eliminasi"):
            st.session_state.sudah_eliminasi = True
            st.rerun()
    else:
        st.success("Silakan masukkan hasil nilai a, b, dan c dari eliminasi tadi.")
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
                        st.info("Hint: coba cek kembali hasil eliminasi. Salah satu dari a, b, atau c mungkin salah.")
                    if st.session_state.salah_tebakan_abc >= 5:
                        st.warning("Bantuan: coba asumsikan a = 1 dulu, lalu cari b dan c dari titik lainnya.")
            except:
                st.error("Masukkan harus berupa bilangan bulat")

# ---------------------------- LANGKAH 4 ----------------------------
if st.session_state.langkah >= 4:
    st.header("🟧 Langkah 4: Bentuk Umum dan Grafik")
    st.markdown("Bentuk umum fungsi kuadrat yang kamu temukan:")
    st.latex("y = x^2 - 6x + 7")

    fig4, ax4 = plt.subplots()
    x_vals = np.linspace(-2, 8, 200)
    y_vals = x_vals**2 - 6*x_vals + 7
    ax4.plot(x_vals, y_vals, label="y = x² - 6x + 7", color="blue")
    ax4.grid(True)
    ax4.set_title("Grafik Fungsi Kuadrat")
    ax4.set_xlabel("x")
    ax4.set_ylabel("y")
    st.pyplot(fig4)

    if st.button("➡ Lanjut ke Langkah 5"):
        st.session_state.langkah = 5
        st.rerun()

# ---------------------------- LANGKAH 5 ----------------------------
if st.session_state.langkah >= 5:
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
if st.session_state.langkah == 6:
    st.header("🟥 Langkah 6: Akar-akar Persamaan Kuadrat")
    st.markdown("Sekarang kita lihat akar-akarnya dari faktorisasi tadi:")

    st.latex("(x - 2)(x - 4) = 0")
    st.latex("x = 2 \\quad atau \\quad x = 4")

    st.success("✅ Selamat! Kamu telah menemukan akar-akar fungsi kuadrat dengan eksplorasi mandiri.")
