import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

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
    return (x - 2)*(x - 4) - 1 # y = x^2 - 6x + 7

fungsi_pilihan = {
    "Fungsi 1": (lambda x: x**2 - 6*x + 7),
    "Fungsi 2": (lambda x: x**2 - 5*x + 6),
    "Fungsi 3": (lambda x: x**2 - 4*x + 3)
}
fungsi_latex = {
    "Fungsi 1": "y = x^{2} - 6x + 7",
    "Fungsi 2": "y = x^{2} - 5x + 6",
    "Fungsi 3": "y = x^{2} - 4x + 3"
}
faktorisasi_dict = {
    "Fungsi 1": ["(x - 2)(x - 4)", 2, 4],
    "Fungsi 2": ["(x - 2)(x - 3)", 2, 3],
    "Fungsi 3": ["(x - 1)(x - 3)", 1, 3]
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
        ax.axvline(x, ymax=(y+2)/(max(y_vals)+3), linestyle="dotted", color="gray")
        ax.axhline(y, xmax=(x+2)/10, linestyle="dotted", color="gray")
        ax.text(x, y, f"({x},{y})", fontsize=8, ha='right')
    ax.set_title("Titik-titik (x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(range(-2, 8))
    ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
    
    # Remove grid and set plain background
    ax.grid(False)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

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
            st.session_state.input_manual.append((x_manual, y_manual_val, hasil))
        except ValueError: # Catch ValueError specifically for non-integer input
            st.session_state.input_manual.append((x_manual, y_manual, "⚠ Input tidak valid"))
            st.error("Masukkan harus berupa bilangan bulat untuk y.") # Moved error message here

    if st.session_state.input_manual:
        st.write("### Tabel Hasil Tebakanmu")
        df2 = pd.DataFrame(st.session_state.input_manual, columns=["x", "y Tebakan", "Status"])
        df2.index = df2.index + 1
        st.dataframe(df2)

        benar_terakhir = [row for row in st.session_state.input_manual if row[2] == "✅ Benar"]
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

    st.markdown("### Substitusi ke $y = ax^2 + bx + c$:")
    for x, y, *_ in titik:
        st.latex(f"{y} = a({x})^2 + b({x}) + c") # Changed to use LaTeX for substitution

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
            except ValueError: # Catch ValueError for non-integer input here too
                st.error("Masukkan a, b, dan c harus berupa bilangan bulat.")

# ---------------------------- LANGKAH 4 ----------------------------
if st.session_state.langkah >= 4:
    st.header("🟧 Langkah 4: Pilih Fungsi")
    st.markdown("Pilih salah satu fungsi kuadrat berikut untuk kamu faktorkan:")
    for k, rumus in fungsi_latex.items():
        st.latex(f"{k}: {rumus}")
    st.session_state.tebakan_fungsi = st.radio("Pilih salah satu:", list(fungsi_latex.keys()))
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
    
    # Generate options and randomize their order
    opsi_faktorisasi = [
        faktorisasi_dict[kode][0],
        "(x - 1)(x - 7)",
        "(x - 3)^2",
        "(x + 1)(x - 5)",
        "(x - 2)^2"
    ]
    random.shuffle(opsi_faktorisasi) # Randomize the order

    pilihan = st.radio("Pilih faktorisasi yang benar:", opsi_faktorisasi)
    if st.button("Cek Faktorisasi"):
        if pilihan == faktorisasi_dict[kode][0]:
            st.success("✅ Benar! Mari kita bahas pembahasannya:")
            st.markdown(f"""
            Untuk memfaktorkan fungsi kuadrat $y = {fungsi_latex[kode].split('=')[1]}$, kita perlu mencari **dua bilangan** yang memenuhi dua kondisi:
            1.  Jika kedua bilangan tersebut **dikalikan**, hasilnya harus sama dengan nilai **konstanta** (istilah 'c' dalam $ax^2 + bx + c$).
            2.  Jika kedua bilangan tersebut **dijumlahkan**, hasilnya harus sama dengan nilai **koefisien dari x** (istilah 'b' dalam $ax^2 + bx + c$).

            Untuk **Fungsi {kode}**:
            """)
            if kode == "Fungsi 1":
                st.markdown(r"""
                Fungsi yang dipilih adalah $y = x^2 - 6x + 7$.
                Kita mencari dua bilangan yang jika dikalikan hasilnya 7 dan jika dijumlahkan hasilnya -6.
                Bilangan tersebut adalah **-2 dan -4**.
                Karena $(-2) \times (-4) = 8$ dan $(-2) + (-4) = -6$.
                Jadi, faktorisasinya adalah **$(x - 2)(x - 4)$**.
                """)
            elif kode == "Fungsi 2":
                st.markdown(r"""
                Fungsi yang dipilih adalah $y = x^2 - 5x + 6$.
                Kita mencari dua bilangan yang jika dikalikan hasilnya 6 dan jika dijumlahkan hasilnya -5.
                Bilangan tersebut adalah **-2 dan -3**.
                Karena $(-2) \times (-3) = 6$ dan $(-2) + (-3) = -5$.
                Jadi, faktorisasinya adalah **$(x - 2)(x - 3)$**.
                """)
            elif kode == "Fungsi 3":
                st.markdown(r"""
                Fungsi yang dipilih adalah $y = x^2 - 4x + 3$.
                Kita mencari dua bilangan yang jika dikalikan hasilnya 3 dan jika dijumlahkan hasilnya -4.
                Bilangan tersebut adalah **-1 dan -3**.
                Karena $(-1) \times (-3) = 3$ dan $(-1) + (-3) = -4$.
                Jadi, faktorisasinya adalah **$(x - 1)(x - 3)$**.
                """)
            st.session_state.langkah = 6
            st.rerun()
        else:
            st.session_state.salah_faktorisasi += 1
            st.error("❌ Masih salah")
            if st.session_state.salah_faktorisasi >= 3:
                st.info("Hint: Perhatikan koefisien tengah dan konstanta. Ingat, $(x-p)(x-q) = x^2 - (p+q)x + pq$.")

# ---------------------------- LANGKAH 6 ----------------------------
if st.session_state.langkah >= 6:
    st.header("🟥 Langkah 6: Akar dari Dua Fungsi Lainnya")
    st.markdown("Masukkan akar-akar dari dua fungsi kuadrat yang belum kamu pilih.")
    for fungsi_sisa in st.session_state.fungsi_tersisa:
        st.latex(fungsi_latex[fungsi_sisa])
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input(f"x₁ untuk {fungsi_sisa}", key=f"x1_{fungsi_sisa}")
        with col2:
            x2 = st.number_input(f"x₂ untuk {fungsi_sisa}", key=f"x2_{fungsi_sisa}")

        if st.button(f"Cek Akar {fungsi_sisa}"):
            benar_x1 = faktorisasi_dict[fungsi_sisa][1]
            benar_x2 = faktorisasi_dict[fungsi_sisa][2]
            if sorted([x1, x2]) == sorted([benar_x1, benar_x2]):
                st.success(f"✅ Akar-akarnya benar untuk {fungsi_sisa}!")
            else:
                st.session_state.salah_input_x1x2 += 1
                st.error("❌ Salah")
                if st.session_state.salah_input_x1x2 >= 3:
                    st.info(f"Hint: Gunakan $ {faktorisasi_dict[fungsi_sisa][0]} = 0 $, lalu cari nilai x.")
