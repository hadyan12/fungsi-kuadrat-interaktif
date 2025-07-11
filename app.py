import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# HARUS di baris pertama
st.set_page_config(page_title="Eksplorasi Fungsi Kuadrat", page_icon="📐")

st.title("📐 Eksplorasi Fungsi Kuadrat: Temukan Titik Puncaknya!")

st.markdown(r"""
Selamat datang, penjelajah matematika!  

Hari ini kamu tidak akan langsung diberi rumus.  
Sebaliknya, kamu akan **melakukan percobaan nilai** dan **mengamati grafik**,  
hingga akhirnya bisa **menemukan sendiri titik puncak fungsi kuadrat!**

---

### 🎯 Tujuan Hari Ini:
- Menemukan **pola dari data** titik-titik \( (x, f(x)) \)  
- **Menebak sendiri titik puncak parabola**  
- Menyimpulkan bentuk umum fungsi kuadrat

---

### 💡 Tips:
- Coba nilai \( x \) yang berurutan (misalnya: -3, -2, ..., 2, 3)  
- Amati: Di mana grafik mencapai nilai terkecil/terbesar?

""")

# Fungsi kuadrat rahasia (bisa diganti)
def fungsi_kuadrat(x):
    return 2 * x**2 + 3 * x + 1

# Session state
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.tebakan_puncak = None

### Langkah 1: Coba Nilai x
with st.expander("🔍 Langkah 1: Eksperimen Nilai \( x \)", expanded=True):
    x_baru = st.number_input("Masukkan nilai \( x \):", value=0, step=1, key="x_input")
    if st.button("➕ Tambahkan", key="tambah_x"):
        if x_baru not in st.session_state.x_list:
            st.session_state.x_list.append(x_baru)
            st.session_state.fx_list.append(fungsi_kuadrat(x_baru))
        else:
            st.warning("Nilai x ini sudah kamu coba.")

    if st.session_state.x_list:
        st.write("📋 Berikut data yang sudah kamu kumpulkan:")
        st.table({
            "x": st.session_state.x_list,
            "f(x)": st.session_state.fx_list
        })

        # Plot grafik
        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue', label="Titik (x, f(x))")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Grafik Titik-titik Hasil Percobaan")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

### Langkah 2: Menebak Titik Puncak
if len(st.session_state.x_list) >= 3:
    with st.expander("🎯 Langkah 2: Tebak Titik Puncak", expanded=True):
        st.markdown(r"""
        Dari grafik titik-titik di atas, kira-kira:
        - Di **nilai \( x \) berapa** fungsi mencapai nilai terkecil?
        - Berapa kira-kira nilai \( f(x) \) pada titik itu?

        ✏️ Masukkan tebakanmu untuk titik puncak:
        """)

        x_puncak_tebakan = st.number_input("Tebakan nilai \( x \) titik puncak:", value=0.0, format="%.2f", key="x_puncak_tebak")
        y_puncak_tebakan = st.number_input("Tebakan nilai \( f(x) \) titik puncak:", value=0.0, format="%.2f", key="y_puncak_tebak")

        if st.button("🔍 Tampilkan Grafik dengan Tebakan", key="cek_puncak"):
            st.session_state.tebakan_puncak = (x_puncak_tebakan, y_puncak_tebakan)

        if st.session_state.tebakan_puncak:
            x_vals = np.linspace(min(st.session_state.x_list)-2, max(st.session_state.x_list)+2, 300)
            y_vals = fungsi_kuadrat(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="Kurva Fungsi Kuadrat", color='lightblue')
            ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue', label="Titik Percobaan")
            ax.plot(st.session_state.tebakan_puncak[0], st.session_state.tebakan_puncak[1], "ro", label="Tebakan Titik Puncak")
            ax.axvline(st.session_state.tebakan_puncak[0], color='red', linestyle='--', label="Garis Vertikal x")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title("Grafik Fungsi + Tebakan Titik Puncak")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            st.success(rf"""
Tebakan kamu:  
\( x = {x_puncak_tebakan} \),  
\( f(x) = {y_puncak_tebakan} \)  
""")

