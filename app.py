# Fungsi Kuadrat Interaktif - Versi Eksploratif Faktorisasi
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi dasar
st.set_page_config(page_title="🧮 Eksplorasi Fungsi Kuadrat", page_icon="🧮")

# Header
st.title("🧮 Temukan Akar dan Bentuk Umum Fungsi Kuadrat!")
st.markdown("""
Mari kita eksplorasi fungsi kuadrat dari data dan grafik.

---

## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum persamaan kuadrat dari data
- Menentukan akar-akar persamaan kuadrat dengan faktorisasi

## 🇮🇩 Profil Pelajar Pancasila
- Bernalar kritis dan mandiri
- Kreatif dalam menyusun bentuk faktorisasi

---
""")

# Fungsi rahasia: f(x) = (x - 2)(x - 3) = x^2 - 5x + 6
def fungsi_rahasia(x):
    return x**2 - 5*x + 6

# Inisialisasi sesi
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.salah_akar = 0

# LANGKAH 1: Eksplorasi data
with st.expander("🟩 Langkah 1: Coba-coba nilai x", expanded=not st.session_state.langkah_2):
    x_input = st.number_input("Masukkan nilai x:", value=0, step=1)
    if st.button("➕ Tambahkan", key="tambah_x"):
        if x_input not in st.session_state.x_list:
            st.session_state.x_list.append(x_input)
            st.session_state.fx_list.append(fungsi_rahasia(x_input))
        else:
            st.warning("Nilai ini sudah dicoba.")

    if st.session_state.x_list:
        st.write("### 📊 Tabel x dan f(x)")
        st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue')
        ax.axhline(0, color='gray', linestyle='--')
        ax.set_title("Plot f(x) terhadap x")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 5:
            if st.button("➡ Lanjut ke Langkah 2"):
                st.session_state.langkah_2 = True
                st.rerun()

# LANGKAH 2: Cari akar dan bentuk faktorisasi
if st.session_state.langkah_2:
    with st.expander("🟦 Langkah 2: Temukan Akar-akarnya", expanded=not st.session_state.langkah_3):
        st.markdown("""
        Dari tabel, coba cari nilai-nilai x yang menghasilkan f(x) = 0.
        Masukkan dua akar tersebut di bawah ini:
        """)

        akar1 = st.number_input("Tebakan akar pertama:", key="akar1")
        akar2 = st.number_input("Tebakan akar kedua:", key="akar2")

        if st.button("🔍 Cek Faktorisasi"):
            def hasil_tebakan(x):
                return (x - akar1)*(x - akar2)

            cocok = True
            for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
                if abs(hasil_tebakan(x) - fx) > 1e-6:
                    cocok = False
                    break

            if cocok:
                st.success("✅ Akar kamu benar!")
                st.latex(f"f(x) = (x - {akar1})(x - {akar2})")
                a = 1
                b = - (akar1 + akar2)
                c = akar1 * akar2
                st.markdown("### 🧾 Bentuk Umum:")
                st.latex(f"f(x) = x^2 + ({b})x + ({c})")
                st.session_state.langkah_3 = True
            else:
                st.session_state.salah_akar += 1
                st.error("❌ Akar belum tepat, coba lagi.")

                if st.session_state.salah_akar >= 3:
                    st.warning("Sudah 3 kali salah. Yuk kita pelajari caranya!")
                    st.markdown(r'''
### 💡 Petunjuk Menemukan Akar
1. Perhatikan dari tabel, nilai x yang membuat f(x) = 0
2. Biasanya ada dua titik yang menyentuh sumbu x
3. Jika f(2) = 0 dan f(3) = 0, maka akar-akarnya adalah 2 dan 3
4. Maka bentuk faktorisasi:
\[
f(x) = (x - 2)(x - 3)
\]
Lalu kembangkan bentuknya jadi bentuk umum.
''')

# LANGKAH 3: Penutup
if st.session_state.langkah_3:
    with st.expander("🟨 Langkah 3: Grafik Lengkap dan Simpulan", expanded=True):
        st.markdown("""
        📈 Berikut adalah grafik lengkap dari fungsi kuadrat:
        """)
        x_vals = np.linspace(min(st.session_state.x_list)-2, max(st.session_state.x_list)+2, 400)
        y_vals = fungsi_rahasia(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="f(x)", color='green')
        ax.axhline(0, color='gray', linestyle='--')
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue', label="Data kamu")
        ax.set_title("Grafik Fungsi Kuadrat")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.success("Keren! Kamu sudah berhasil menemukan akar dan bentuk umum fungsi kuadrat! 🎉")
