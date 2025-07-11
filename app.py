# 📘 Fungsi Kuadrat Interaktif - Pertemuan 1
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------ KONFIGURASI HALAMAN ------------------
st.set_page_config(page_title="📐 Temukan Fungsi Kuadrat", page_icon="📐")

# ------------------ HEADER ------------------
st.title("📐 Temukan Sendiri Fungsi Kuadrat!")
st.markdown(r'''
Selamat datang di ruang eksplorasi fungsi kuadrat! 🤓

🔍 Hari ini kamu akan belajar *menemukan sendiri* bentuk umum fungsi kuadrat melalui data.

---

## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum fungsi kuadrat dari data
- Menentukan akar-akar persamaan kuadrat dengan faktorisasi

## 🇮🇩 Profil Pelajar Pancasila
- Bernalar kritis dan mandiri
- Kreatif dalam menemukan pola
- Bertanggung jawab atas proses belajar

---
''')

# ------------------ INISIALISASI ------------------
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.tebakan_a = 0
    st.session_state.tebakan_b = 0
    st.session_state.tebakan_c = 0
    st.session_state.tebakan_salah = 0
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False

# Fungsi rahasia
def fungsi_rahasia(x):
    return (x - 2)*(x - 3)  # akar: 2 dan 3 → f(x) = x^2 - 5x + 6

def fungsi_eksplisit(x):
    return x**2 - 5*x + 6

# ------------------ LANGKAH 1: Coba Titik ------------------
with st.expander("🟩 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    x_input = st.number_input("Masukkan nilai x:", value=0, step=1)
    if st.button("➕ Tambahkan", key="tambah_x"):
        if x_input not in st.session_state.x_list:
            st.session_state.x_list.append(x_input)
            st.session_state.fx_list.append(fungsi_rahasia(x_input))
        else:
            st.warning("Nilai x sudah pernah dicoba. Pilih nilai lain.")

    if st.session_state.x_list:
        st.subheader("📊 Tabel Nilai x dan f(x)")
        st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue')
        ax.set_title("Plot Titik-titik f(x)")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 4:
            if st.button("➡ Lanjut ke Langkah 2"):
                st.session_state.langkah_2 = True
                st.rerun()

# ------------------ LANGKAH 2: Lengkapi Bentuk Umum ------------------
if st.session_state.langkah_2:
    with st.expander("🟦 Langkah 2: Lengkapi Fungsi Umum", expanded=not st.session_state.langkah_3):
        st.markdown(r'''
Coba lengkapi bentuk umum:
\[
f(x) = ax^2 + bx + c
\]
Isi tebakan kamu berdasarkan data.
''')
        a = st.number_input("Tebakan nilai a:", value=1)
        b = st.number_input("Tebakan nilai b:", value=0)
        c = st.number_input("Tebakan nilai c:", value=0)

        def fungsi_tebakan(x):
            return a * x**2 + b * x + c

        if st.button("🔍 Cek Jawaban"):
            benar = True
            for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
                if fungsi_tebakan(x) != fx:
                    benar = False
                    break

            if benar:
                st.success("✅ Tepat! Fungsi kamu cocok dengan semua titik!")
                st.session_state.tebakan_a = a
                st.session_state.tebakan_b = b
                st.session_state.tebakan_c = c
                st.session_state.langkah_3 = True
            else:
                st.session_state.tebakan_salah += 1
                st.error("❌ Belum cocok. Coba lagi!")

                if st.session_state.tebakan_salah >= 3:
                    st.warning("🔍 Yuk kita belajar cara menentukan a, b, dan c!")
                    st.markdown(r'''
### 💡 Cara Menentukan a, b, dan c:
1. Ambil tiga titik dari tabel.
2. Substitusi ke bentuk:
\[
y = ax^2 + bx + c
\]
3. Buat sistem persamaan.
4. Selesaikan dengan eliminasi atau substitusi.
''')

# ------------------ LANGKAH 3: Akar dengan Faktorisasi ------------------
if st.session_state.langkah_3:
    with st.expander("🟥 Langkah 3: Temukan Akar dengan Faktorisasi", expanded=True):
        a = st.session_state.tebakan_a
        b = st.session_state.tebakan_b
        c = st.session_state.tebakan_c

        st.markdown(f"""
        Bentuk umum:
        \[
        f(x) = {a}x^2 + ({b})x + ({c})
        \]
        
        Coba cari dua bilangan yang jumlahnya {b * -1} dan hasil kalinya {c}
        """)

        m = st.number_input("Tebakan akar pertama:", key="akar1")
        n = st.number_input("Tebakan akar kedua:", key="akar2")

        if st.button("✅ Cek Faktorisasi"):
            if a == 1 and -m - n == b and m * n == c:
                st.success(f"🎉 Betul! Faktorisasi: (x - {int(m)})(x - {int(n)})")
                st.markdown(f"""
                Maka akar-akarnya:
                \[
                x = {int(m)} \quad \text{{dan}} \quad x = {int(n)}
                \]
                """)
            else:
                st.error("❌ Masih salah. Coba lagi!")
                st.markdown(r'''
### 💡 Petunjuk:
- Misal bentuk: \( x^2 - 5x + 6 \)
- Cari dua bilangan:
    - jumlahnya 5
    - hasil kalinya 6
- Jawabannya: 2 dan 3
- Maka: \( (x - 2)(x - 3) \)
''')
