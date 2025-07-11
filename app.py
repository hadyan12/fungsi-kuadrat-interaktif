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
    return (x - 2)*(x - 4) - 1  # y = x^2 - 6x + 7

fungsi_pilihan = {
    "f1": (lambda x: x**2 - 6*x + 7),
    "f2": (lambda x: x**2 - 5*x + 6),
    "f3": (lambda x: x**2 - 4*x + 3)
}
fungsi_latex = {
    "f1": "y = x^{2} - 6x + 7",
    "f2": "y = x^{2} - 5x + 6",
    "f3": "y = x^{2} - 4x + 3"
}
faktorisasi_dict = {
    "f1": ["(x - 2)(x - 4)", 2, 4],
    "f2": ["(x - 2)(x - 3)", 2, 3],
    "f3": ["(x - 1)(x - 3)", 1, 3]
}

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.input_manual = []
    st.session_state.langkah = 1
    st.session_state.tebakan_abc = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_abc = 0
    st.session_state.salah_faktorisasi = 0
    st.session_state.sudah_eliminasi = False
    st.session_state.tebakan_fungsi = ""
    st.session_state.fungsi_tersisa = []
    st.session_state.salah_input_x1x2 = 0
    st.session_state.tiga_titik = []

# ---------------------------- LANGKAH 1 ----------------------------
st.header("🟩 Langkah 1: Masukkan Titik-titik")
st.markdown("Masukkan nilai x antara -2 sampai 7 untuk melihat nilai y")

x_input = st.number_input("Nilai x:", min_value=-2, max_value=7, step=1, key="x_input")
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

    if len(st.session_state.data_titik) >= 5:
        if st.button("➡ Lanjut ke Langkah 2"):
            st.session_state.langkah = 2
            st.rerun()

# ---------------------------- LANGKAH 2 ----------------------------
if st.session_state.langkah >= 2:
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
    st.markdown("Gunakan 3 titik dari tebakan benar untuk membentuk sistem persamaan kuadrat.")

    titik = st.session_state.tiga_titik
    for x, y, *_ in titik:
        st.latex(f"({x}, {y})")

    st.markdown("### Substitusi ke \( y = ax^{2} + bx + c \):")
    for x, y, *_ in titik:
        st.latex(f"{y} = a \cdot {x}^{{2}} + b \cdot {x} + c")

    if not st.session_state.sudah_eliminasi:
        if st.button("✍️ Saya sudah eliminasi"):
            st.session_state.sudah_eliminasi = True
            st.rerun()
    else:
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
                        st.info("Hint: coba eliminasi ulang satu pasang persamaan saja terlebih dahulu.")
            except:
                st.error("Masukkan harus berupa bilangan bulat")

# ---------------------------- LANGKAH 4 ----------------------------
if st.session_state.langkah >= 4:
    st.header("🟧 Langkah 4: Pilih Fungsi")
    st.markdown("Pilih salah satu fungsi kuadrat berikut untuk kamu faktorkan:")

    for k, rumus in fungsi_latex.items():
        st.latex(rumus)

    st.session_state.tebakan_fungsi = st.radio("Pilih salah satu:", list(fungsi_latex.keys()), key="radio_pilih_fungsi")

    if st.button("Cek Pilihan Fungsi"):
        st.session_state.fungsi_tersisa = [f for f in fungsi_latex if f != st.session_state.tebakan_fungsi]
        st.session_state.langkah = 5
        st.rerun()

# ---------------------------- LANGKAH 5 ----------------------------
if st.session_state.langkah >= 5:
    st.header("🟪 Langkah 5: Faktorisasi Fungsi Pilihan")
    kode = st.session_state.tebakan_fungsi
    st.latex(fungsi_latex[kode])
    st.markdown("Apa faktorisasi dari fungsi ini?")

    pilihan = st.radio("Pilih faktorisasi yang benar:", [faktorisasi_dict[kode][0], "(x - 1)(x - 7)", "(x - 3)^2"])

    if st.button("Cek Faktorisasi"):
        if pilihan == faktorisasi_dict[kode][0]:
            st.success("✅ Benar! Sekarang kerjakan dua fungsi tersisa di buku tulis!")
            st.session_state.langkah = 6
            st.rerun()
        else:
            st.session_state.salah_faktorisasi += 1
            st.error("❌ Masih salah")
            if st.session_state.salah_faktorisasi >= 3:
                st.info("Hint: Perhatikan koefisien tengah dan konstanta.")

# ---------------------------- LANGKAH 6 ----------------------------
if st.session_state.langkah >= 6:
    st.header("🟥 Langkah 6: Akar dari Fungsi yang Difaktorkan")
    st.markdown("Masukkan akar-akar dari fungsi tersebut.")

    kode = st.session_state.tebakan_fungsi
    x1 = st.number_input("x₁:", key="x1")
    x2 = st.number_input("x₂:", key="x2")

    if st.button("Cek Akar"):
        benar_x1 = faktorisasi_dict[kode][1]
        benar_x2 = faktorisasi_dict[kode][2]
        if sorted([x1, x2]) == sorted([benar_x1, benar_x2]):
            st.success("✅ Selamat! Akar-akarnya benar!")
        else:
            st.session_state.salah_input_x1x2 += 1
            st.error("❌ Salah")
            if st.session_state.salah_input_x1x2 >= 3:
                st.info(f"Hint: Gunakan $ {faktorisasi_dict[kode][0]} = 0 $, lalu cari nilai x.")
