import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# HARUS di baris pertama sebelum komponen lain
st.set_page_config(page_title="Temukan Rumus Fungsi Kuadrat", page_icon="📐")

st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")

st.markdown("""
Hai, selamat datang di *ruang eksplorasi fungsi kuadrat!*  
Hari ini kamu *bukan cuma belajar*, kamu akan *menjadi peneliti matematika*!

🤔 Coba beberapa nilai, amati hasilnya, dan...  
✨ *Temukan sendiri rumus fungsi kuadrat yang tersembunyi di balik angka-angka!*

---

## 🧩 Apa yang akan kamu lakukan?

🔍 Uji nilai-nilai x dan lihat hasil f(x)  
📊 Catat data dalam bentuk tabel dan grafik  
🧠 Coba *menebak rumus* dari pola data  
🧪 Uji tebakanmu — apakah cocok dengan semua titik?  
🏁 Ubah ke bentuk *kuadrat sempurna* setelah menemukan rumusnya!

---

## 🎯 Tujuan Pembelajaran

- Melatih kemampuan *menganalisis pola*
- Memahami *struktur fungsi kuadrat*
- Meningkatkan *logika berpikir mandiri*
- Belajar seperti *ilmuwan sungguhan!*

💡 *Tips dari Pembimbing:*  
> Coba minimal 3–5 nilai x dan jangan takut salah! Justru dari kesalahan kamu akan cepat paham.
""")

# Fungsi kuadrat rahasia
def fungsi_asli(x):
    return 2 * x**2 + 3 * x + 1  # bisa diganti a, b, c sesukamu

# Session state untuk menyimpan progres pengguna
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.cocok = False

### LANGKAH 1: Eksperimen Nilai x
with st.expander("🔍 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    st.write("Masukkan nilai x (boleh negatif/positif), lalu lihat hasil f(x).")
    x = st.number_input("Masukkan nilai x:", value=1, step=1, key="x_input")
    if st.button("➕ Tambahkan ke tabel", key="add_x"):
        if x not in st.session_state.x_list:
            st.session_state.x_list.append(x)
            st.session_state.fx_list.append(fungsi_asli(x))
        else:
            st.warning("Nilai x ini sudah pernah dicoba.")

    if st.session_state.x_list:
        st.write("📋 Data percobaan kamu:")
        data = {"x": st.session_state.x_list, "f(x)": st.session_state.fx_list}
        st.table(data)

        # Plot titik
        fig, ax = plt.subplots()
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue', label='Titik f(x)')
        ax.set_title("Plot Titik (x, f(x))")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 3:
            if st.button("➡ Lanjut ke Tebak Rumus", key="next_tebakan"):
                st.session_state.langkah_2 = True
                st.rerun()

### LANGKAH 2: Tebak Rumus
if st.session_state.langkah_2 and not st.session_state.langkah_3:
    with st.expander("✏ Langkah 2: Tebak Rumus", expanded=True):
        st.markdown(r"""
        Dari data, coba tebak bentuk:
        \[
        f(x) = ax^2 + bx + c
        \]
        """)

        a_tebak = st.number_input("Tebakan koefisien a:", value=1, step=1, key="a_tebak")
        b_tebak = st.number_input("Tebakan koefisien b:", value=1, step=1, key="b_tebak")
        c_tebak = st.number_input("Tebakan konstanta c:", value=0, step=1, key="c_tebak")

        def fungsi_tebakan(x):
            return a_tebak * x**2 + b_tebak * x + c_tebak

        if st.button("🔍 Cek Kecocokan", key="cek_rumus"):
            cocok = all(np.isclose(fungsi_tebakan(x), fx, rtol=1e-9)
                        for x, fx in zip(st.session_state.x_list, st.session_state.fx_list))

            if cocok:
                st.success("✅ Tebakanmu benar! Selamat, kamu telah menemukan rumus f(x)!")
                st.session_state.langkah_3 = True
                st.session_state.cocok = True
            else:
                st.error("❌ Masih ada yang belum cocok. Coba perbaiki tebakanmu.")

### LANGKAH 3: Ubah ke Kuadrat Sempurna
if st.session_state.langkah_3 and st.session_state.cocok:
    with st.expander("🧠 Langkah 3: Bentuk Kuadrat Sempurna", expanded=True):
        a = a_tebak
        b = b_tebak
        c = c_tebak

        h = -b / (2 * a)
        k = fungsi_tebakan(h)

        st.markdown("Rumus yang kamu temukan:")
        st.latex(f"f(x) = {a}x^2 + {b}x + {c}")

        st.markdown("Kita ubah ke bentuk kuadrat sempurna:")
        st.latex(
            r"f(x) = a(x - h)^2 + k" + f" = {a}(x {h:+.2f})² + {k:.2f}"
        )
        st.success(f"Jadi: f(x) = {a}(x {h:+.2f})² + {k:.2f}")

        # Grafik akhir
        st.subheader("📊 Grafik Lengkap Fungsi")
        x_vals = np.linspace(h - 10, h + 10, 400)
        y_vals = fungsi_asli(x_vals)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_vals, y_vals, label="f(x)", color="blue")
        ax.axvline(h, color="red", linestyle="--", label="Sumbu Simetri")
        ax.plot(h, k, "ro", label="Titik Puncak")
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="green", label="Titik Data")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
