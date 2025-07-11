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
    return x**2 - 6*x + 7  # y = (x - 2)(x - 4)

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
    st.session_state.langkah = 1
    st.session_state.input_tebakan = []
    st.session_state.tebakan_bentuk = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_bentuk = 0
    st.session_state.sudah_eliminasi = False
    st.session_state.tiga_titik = []
    st.session_state.tebakan_fungsi = ""
    st.session_state.fungsi_tersisa = []
    st.session_state.salah_faktorisasi = 0
    st.session_state.salah_input_x1x2 = 0

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
        ax.text(x, y, f"({x},{y})", fontsize=8, ha='right')
    ax.set_title("Grafik Titik-titik")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(range(-2, 8))
    ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
    ax.grid(False)
    st.pyplot(fig)

    if len(st.session_state.data_titik) >= 5:
        if st.button("➡ Lanjut ke Langkah 2"):
            st.session_state.langkah = 2
            st.rerun()

# ---------------------------- LANGKAH 2 ----------------------------
if st.session_state.langkah >= 2:
    st.header("🟦 Langkah 2: Tebak Nilai y")
    st.markdown("Masukkan nilai x dan nilai y (hasil dari fungsi kuadrat) untuk dicocokkan dengan fungsi sebenarnya.")

    col1, col2 = st.columns(2)
    with col1:
        x_tebak = st.number_input("x:", min_value=-2, max_value=7, step=1, key="x_tebak")
    with col2:
        y_tebak = st.text_input("y:", key="y_tebak")

    if st.button("Cek Nilai"):
        try:
            y_val = int(y_tebak)
            y_benar = fungsi_rahasia(x_tebak)
            hasil = "✅ Benar" if y_val == y_benar else "❌ Salah"
            st.session_state.input_tebakan.append((x_tebak, y_val, hasil))
        except:
            st.session_state.input_tebakan.append((x_tebak, y_tebak, "⚠️ Bukan bilangan bulat"))

    if st.session_state.input_tebakan:
        st.write("### Tabel Cek Nilai y")
        df = pd.DataFrame(st.session_state.input_tebakan, columns=["x", "y Tebakan", "Status"])
        df.index += 1
        st.dataframe(df)

        benar_terakhir = [baris for baris in st.session_state.input_tebakan if baris[2] == "✅ Benar"]
        if len(benar_terakhir) >= 3:
            if st.button("➡ Lanjut ke Langkah 3"):
                st.session_state.langkah = 3
                st.session_state.tiga_titik = benar_terakhir[-3:]
                st.rerun()

# ---------------------------- LANGKAH 3 ----------------------------
if st.session_state.langkah >= 3:
    st.header("🟨 Langkah 3: Substitusi dan Eliminasi")
    st.markdown("Gunakan 3 titik yang benar untuk disubstitusikan ke bentuk umum \( y = ax^2 + bx + c \).")

    for x, y, _ in st.session_state.tiga_titik:
        st.latex(f"({x}, {y})")
    st.markdown("### Substitusi ke \( y = ax^2 + bx + c \):")
    for x, y, _ in st.session_state.tiga_titik:
        st.latex(f"{y} = a({x})^2 + b({x}) + c")

    if not st.session_state.sudah_eliminasi:
        if st.button("✍️ Saya sudah eliminasi"):
            st.session_state.sudah_eliminasi = True
            st.rerun()
    else:
        a = st.text_input("a =", value=st.session_state.tebakan_bentuk["a"])
        b = st.text_input("b =", value=st.session_state.tebakan_bentuk["b"])
        c = st.text_input("c =", value=st.session_state.tebakan_bentuk["c"])

        if st.button("Cek Hasil Eliminasi"):
            st.session_state.tebakan_bentuk = {"a": a, "b": b, "c": c}
            try:
                if int(a) == 1 and int(b) == -6 and int(c) == 7:
                    st.success("✅ Jawaban benar! Bentuk umum fungsi kuadrat berhasil ditemukan.")
                    st.session_state.fungsi_dipilih = "Fungsi 1"
                    st.session_state.langkah = 4
                    st.rerun()
                else:
                    st.session_state.salah_tebakan_bentuk += 1
                    st.error("❌ Belum tepat. Coba lagi.")
                    if st.session_state.salah_tebakan_bentuk >= 3:
                        st.info("Hint: Ulangi eliminasi dua persamaan saja lebih dulu.")
            except:
                st.error("⚠️ Masukkan harus bilangan bulat")

# ---------------------------- LANGKAH 4 ----------------------------
if st.session_state.langkah >= 4:
    st.header("🟧 Langkah 4: Tampilkan Fungsi dan Grafik")
    st.markdown("Berikut ini adalah bentuk umum fungsi kuadrat yang telah kamu temukan:")
    kode = st.session_state.fungsi_dipilih
    st.latex(fungsi_latex[kode])

    x = np.linspace(-10, 10, 400)
    y = fungsi_kuadrat_dict[kode](x)

    fig, ax = plt.subplots()
    ax.plot(x, y, color='orange', linewidth=2)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_facecolor('white')
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig)

    if st.button("Lanjut ke Langkah 5"):
        st.session_state.langkah = 5
        st.rerun()

# ---------------------------- LANGKAH 5 ----------------------------
if st.session_state.langkah >= 5:
    st.header("🟪 Langkah 5: Faktorisasi Fungsi")
    st.markdown("Pilih salah satu fungsi kuadrat berikut untuk kamu faktorkan:")

    for k, rumus in fungsi_latex.items():
        st.latex(f"{k}: {rumus}")

    st.session_state.tebakan_fungsi = st.radio("Pilih salah satu:", list(fungsi_latex.keys()))

    if st.button("Cek Pilihan Fungsi"):
        st.session_state.fungsi_tersisa = [f for f in fungsi_latex if f != st.session_state.tebakan_fungsi]
        st.rerun()

    kode = st.session_state.tebakan_fungsi
    st.latex(fungsi_latex[kode])

    opsi_faktorisasi = [
        faktorisasi_dict[kode][0],
        "(x - 1)(x - 7)",
        "(x - 3)^2",
        "(x + 1)(x - 5)",
        "(x - 2)^2"
    ]
    random.shuffle(opsi_faktorisasi)

    pilihan = st.radio("Pilih faktorisasi yang benar:", opsi_faktorisasi)

    if st.button("Cek Faktorisasi"):
        if pilihan == faktorisasi_dict[kode][0]:
            st.success("✅ Betul! Inilah penjelasannya:")
            st.latex(f"y = {fungsi_latex[kode].split('=')[1]}")
            st.markdown("Carilah dua bilangan yang hasil kalinya sama dengan konstanta dan jumlahnya sama dengan koefisien tengah.")
            st.session_state.langkah = 6
            st.rerun()
        else:
            st.session_state.salah_faktorisasi += 1
            st.error("❌ Masih salah")
            if st.session_state.salah_faktorisasi >= 3:
                st.info("Hint: Perhatikan hasil kali dan jumlah dua bilangan faktor.")

# ---------------------------- LANGKAH 6 ----------------------------
if st.session_state.langkah >= 6:
    st.header("🟥 Langkah 6: Tentukan Akar Dua Fungsi Lainnya")
    st.markdown("Masukkan akar-akar dari dua fungsi kuadrat yang belum kamu pilih sebelumnya.")

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
                    st.info(f"Hint: Gunakan \( {faktorisasi_dict[fungsi_sisa][0]} = 0 \), lalu cari nilai x.")
