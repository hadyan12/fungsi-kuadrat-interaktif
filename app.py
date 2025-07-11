# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Temukan Rumus Fungsi Kuadrat", page_icon="📐")
st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")

st.markdown("""
Selamat datang di *laboratorium mini* fungsi kuadrat!

Hari ini kamu akan:
- 🔍 Melakukan eksperimen nilai `x` dan mengamati hasil `f(x)`
- 🧠 Menebak koordinat titik puncak parabola
- ✏ Menebak rumus fungsi kuadrat sendiri
- 🧪 Menguji apakah rumusmu cocok dengan data
- 📐 Mengubah bentuk ke *kuadrat sempurna*

---
""")

# Fungsi rahasia (target)
def fungsi_asli(x):
    return 2 * x**2 + 3 * x + 1

# Inisialisasi session_state
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.tebakan_puncak = 0
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.langkah_4 = False
    st.session_state.salah_tebakan = 0
    st.session_state.berhasil = False

# Langkah 1: Eksperimen nilai x
with st.expander("🔍 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    x_input = st.number_input("Masukkan nilai x:", value=0, step=1, key="x_input")
    if st.button("➕ Tambahkan", key="tambah_x"):
        if x_input not in st.session_state.x_list:
            st.session_state.x_list.append(x_input)
            st.session_state.fx_list.append(fungsi_asli(x_input))
        else:
            st.warning("Nilai x ini sudah dicoba.")

    if st.session_state.x_list:
        st.subheader("📋 Tabel Nilai f(x)")
        tabel = {"x": st.session_state.x_list, "f(x)": st.session_state.fx_list}
        st.table(tabel)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="blue")
        ax.set_title("Grafik Titik (x, f(x))")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.set_xlim(min(st.session_state.x_list)-1, max(st.session_state.x_list)+1)
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 3:
            if st.button("➡ Lanjut ke Langkah 2", key="ke_langkah_2"):
                st.session_state.langkah_2 = True
                st.rerun()

# Langkah 2: Tebak Titik Puncak
if st.session_state.langkah_2 and not st.session_state.langkah_3:
    with st.expander("🎯 Langkah 2: Tebak Titik Puncak", expanded=True):
        st.markdown("""
        Dari grafik yang kamu buat, kira-kira di nilai x berapa fungsi mencapai titik terendah (titik puncak)?
        Masukkan tebakan nilai x untuk titik puncaknya:
        """)
        x_puncak_tebakan = st.number_input("Tebak nilai x titik puncak:", value=0, step=1, key="x_puncak")
        if st.button("🔍 Cek Puncak", key="cek_puncak"):
            x_asli = -3 / (2 * 2)  # -b / 2a
            if abs(x_puncak_tebakan - x_asli) < 0.1:
                st.success("✅ Betul! Titik puncak mendekati x = {:.2f}".format(x_asli))
                st.session_state.langkah_3 = True
            else:
                st.warning("❌ Belum tepat. Coba lagi dengan memperhatikan grafik.")

# Langkah 3: Tebak Rumus
if st.session_state.langkah_3 and not st.session_state.langkah_4:
    with st.expander("✏ Langkah 3: Tebak Rumus Fungsi Kuadrat", expanded=True):
        st.markdown("""
        Berdasarkan tabel dan grafik, coba tebak rumus fungsi kuadrat dalam bentuk:
        
        \[
        f(x) = ax^2 + bx + c
        \]
        """)

        a = st.number_input("Tebak nilai a:", value=1, step=1)
        b = st.number_input("Tebak nilai b:", value=1, step=1)
        c = st.number_input("Tebak nilai c:", value=0, step=1)

        def f_tebakan(x): return a * x**2 + b * x + c

        if st.button("🔎 Uji Rumus", key="cek_tebakan"):
            cocok = all(abs(f_tebakan(x) - y) < 0.01 for x, y in zip(st.session_state.x_list, st.session_state.fx_list))
            if cocok:
                st.success("✅ Hebat! Rumus kamu cocok dengan semua data!")
                st.session_state.langkah_4 = True
                st.session_state.berhasil = True
            else:
                st.session_state.salah_tebakan += 1
                st.error("❌ Rumus belum cocok. Coba perbaiki.")
                if st.session_state.salah_tebakan >= 3:
                    st.info("💡 Petunjuk: Coba gunakan titik puncak dan salah satu titik lain untuk menyusun sistem persamaan.")

# Langkah 4: Kuadrat Sempurna
if st.session_state.langkah_4 and st.session_state.berhasil:
    with st.expander("📐 Langkah 4: Bentuk Kuadrat Sempurna", expanded=True):
        h = -b / (2 * a)
        k = a * h**2 + b * h + c
        st.latex(f"f(x) = {a}x^2 + {b}x + {c}")
        st.markdown("Bentuk kuadrat sempurna:")
        st.latex(rf"f(x) = {a}(x {'-' if h >= 0 else '+'}{abs(h):.2f})^2 + {k:.2f}")

        # Grafik akhir
        x_vals = np.linspace(h - 5, h + 5, 400)
        y_vals = fungsi_asli(x_vals)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x_vals, y_vals, label="f(x) asli", color="blue")
        ax.axvline(h, color="red", linestyle="--", label="Sumbu simetri")
        ax.plot(h, k, "ro", label="Titik puncak")
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="green", label="Data kamu")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        st.success("🎉 Selamat! Kamu berhasil menemukan dan mengubah bentuk fungsi kuadrat.")
