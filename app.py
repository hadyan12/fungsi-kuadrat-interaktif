import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="📐 Temukan Rumus Fungsi Kuadrat", page_icon="📐")

st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")

st.markdown("""
Selamat datang di ruang eksplorasi fungsi kuadrat!  
Di sini kamu akan mencoba, mengamati, dan **menemukan sendiri** rumus fungsi kuadrat.  

---  

## 🎯 Tujuan
- Melakukan percobaan nilai
- Menebak titik puncak fungsi kuadrat
- Mengubah ke bentuk kuadrat sempurna  
- Menguatkan pemahaman melalui *eksperimen, bukan hafalan!*

""")

# Fungsi kuadrat tersembunyi: f(x) = (x - 2)^2 - 3 = x^2 - 4x + 1
def fungsi_asli(x):
    return x**2 - 4*x + 1  # titik puncak: (2, -3)

# Simpan data sesi
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.langkah_2 = False
    st.session_state.tebakan_salah = 0
    st.session_state.bantuan_ditampilkan = False
    st.session_state.langkah_3 = False
    st.session_state.tebakan_benar = False

### LANGKAH 1
with st.expander("🔍 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    st.write("Coba beberapa nilai x dan lihat hasil f(x).")
    x = st.number_input("Masukkan nilai x:", value=0, step=1, key="x_input")
    if st.button("➕ Tambahkan", key="tambah_x"):
        if x not in st.session_state.x_list:
            st.session_state.x_list.append(x)
            st.session_state.fx_list.append(fungsi_asli(x))
        else:
            st.warning("❗ Nilai x ini sudah pernah kamu coba.")

    if st.session_state.x_list:
        st.markdown("### Data Percobaan")
        data = {"x": st.session_state.x_list, "f(x)": st.session_state.fx_list}
        st.table(data)

        x_vals = st.session_state.x_list
        y_vals = st.session_state.fx_list
        x_min, x_max = min(x_vals), max(x_vals)
        margin = max(1, int((x_max - x_min) * 0.3))

        fig, ax = plt.subplots()
        ax.scatter(x_vals, y_vals, color="blue")
        ax.set_title("Titik-titik (x, f(x))")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.set_xlim(x_min - margin, x_max + margin)
        st.pyplot(fig)

        if len(x_vals) >= 3:
            if st.button("➡ Lanjut ke Langkah 2", key="next_step"):
                st.session_state.langkah_2 = True
                st.rerun()

### LANGKAH 2
if st.session_state.langkah_2 and not st.session_state.langkah_3:
    with st.expander("🎯 Langkah 2: Tebak Titik Puncak", expanded=True):
        st.markdown("""
        Coba tebak koordinat titik puncak dari grafik:
        \[
        f(x) = a(x - h)^2 + k
        \]
        Masukkan tebakanmu untuk \( x \) dan \( f(x) \) pada titik puncak.
        """)

        tebak_x = st.number_input("Tebakan x titik puncak (h):", value=0, step=1)
        tebak_y = st.number_input("Tebakan f(x) titik puncak (k):", value=0, step=1)

        if st.button("🔍 Cek Tebakan"):
            if tebak_x == 2 and tebak_y == -3:
                st.success("✅ Betul! Kamu telah menemukan titik puncaknya: (2, -3)")
                st.session_state.tebakan_benar = True
                st.session_state.langkah_3 = True
            else:
                st.session_state.tebakan_salah += 1
                st.error("❌ Belum tepat. Coba lagi.")
                if st.session_state.tebakan_salah >= 3:
                    st.session_state.bantuan_ditampilkan = True

        if st.session_state.bantuan_ditampilkan and not st.session_state.tebakan_benar:
            st.warning("💡 Bantuan: Menemukan Titik Puncak")
            st.markdown("""
            Berikut langkah-langkah menemukan titik puncak dari data:

            1. **Pilih 3 titik** dari tabel: misalnya (0, f(0)), (1, f(1)), (2, f(2))  
            2. Cocokkan dengan bentuk umum:  
            \[
            f(x) = ax^2 + bx + c
            \]
            3. Gunakan sistem persamaan atau regresi (bisa manual/kalkulator) untuk cari \( a, b, c \)
            4. Gunakan rumus titik puncak:
            \[
            x = \\frac{-b}{2a}
            \]
            5. Masukkan x ke rumus f(x) untuk dapat \( y \)
            """)
            st.info("Contoh hasil: x = 2, f(x) = -3")

### LANGKAH 3
if st.session_state.langkah_3 and st.session_state.tebakan_benar:
    with st.expander("🧠 Langkah 3: Bentuk Kuadrat Sempurna", expanded=True):
        st.markdown("""
        Kita ubah rumus fungsi yang kamu temukan ke bentuk **kuadrat sempurna**:
        """)
        st.latex(r"f(x) = a(x - h)^2 + k")

        st.markdown("Dari eksperimen kita:")
        st.latex(r"f(x) = x^2 - 4x + 1")

        st.markdown("Ubah ke bentuk kuadrat sempurna:")
        st.latex(r"f(x) = (x - 2)^2 - 3")

        st.success("Jadi: Titik puncaknya ada di (2, -3)")

        # Grafik fungsi lengkap
        st.subheader("📊 Grafik Fungsi Lengkap")
        x_range = np.linspace(2 - 10, 2 + 10, 400)
        y_range = fungsi_asli(x_range)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_range, y_range, label="f(x) = x² - 4x + 1", color="blue")
        ax.axvline(2, color="red", linestyle="--", label="Sumbu Simetri (x=2)")
        ax.plot(2, -3, "ro", label="Titik Puncak (2, -3)")
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="green", label="Titik Data")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
