# Fungsi Kuadrat Interaktif
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ----------------- KONFIGURASI -----------------
st.set_page_config(page_title="📐 Temukan Rumus Fungsi Kuadrat", page_icon="📐")

# ----------------- HEADER -----------------
st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")
st.markdown("""
Selamat datang di ruang eksplorasi fungsi kuadrat!

🧠 Hari ini kamu akan belajar **bukan dengan rumus langsung**, tapi dengan *menemukan sendiri* pola dari data.

---

## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum persamaan kuadrat dari data
- Menentukan akar-akar dari persamaan kuadrat

## 🇮🇩 Profil Pelajar Pancasila
- Bernalar kritis dan mandiri
- Kreatif dalam menemukan pola
- Bertanggung jawab atas proses belajar

---
""")

# ----------------- INISIALISASI -----------------
def fungsi_rahasia(x):
    return 2 * (x - 2)**2 - 3  # bentuk kuadrat sempurna → a=2, h=2, k=-3

if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.salah_puncak = 0
    st.session_state.puncak_benar = False
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.langkah_4 = False

# ----------------- LANGKAH 1 -----------------
with st.expander("🟩 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    x_input = st.number_input("Masukkan nilai x:", value=0, step=1, key="x_input")
    if st.button("➕ Tambahkan", key="btn_tambah_x"):
        if x_input not in st.session_state.x_list:
            st.session_state.x_list.append(x_input)
            st.session_state.fx_list.append(fungsi_rahasia(x_input))
        else:
            st.warning("Nilai x ini sudah dicoba. Coba nilai lain.")

    if st.session_state.x_list:
        st.write("### 📋 Tabel Hasil Percobaan")
        st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue')
        ax.set_title("Plot Titik-titik f(x)")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.set_xlim(min(st.session_state.x_list)-2, max(st.session_state.x_list)+2)
        ax.set_ylim(min(st.session_state.fx_list)-5, max(st.session_state.fx_list)+5)
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 5:
            if st.button("➡ Lanjut ke Langkah 2", key="lanjut_2"):
                st.session_state.langkah_2 = True
                st.rerun()

# ----------------- LANGKAH 2 -----------------
if st.session_state.langkah_2:
    with st.expander("🟦 Langkah 2: Tebak Titik Puncak", expanded=not st.session_state.puncak_benar):
        st.markdown("""
        Dari grafik dan tabel, coba tebak:

        """)
