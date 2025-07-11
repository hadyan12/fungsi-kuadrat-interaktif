st.set_page_config(page_title="Temukan Rumus Fungsi Kuadrat", page_icon="📐")
st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")

st.markdown("""
Hai, selamat datang di *ruang eksplorasi fungsi kuadrat!*

Hari ini kamu *bukan cuma belajar* seperti biasa.  
Kamu akan *menjadi peneliti matematika*: mencoba beberapa nilai, mengamati hasilnya, dan...  
🤔 *menebak sendiri rumus* fungsi yang tersembunyi di balik angka-angka itu.

---

## 🧩 Apa yang akan kamu lakukan?

🔍 Melakukan *percobaan nilai x* dan melihat bagaimana hasil f(x) terbentuk  
📊 Mencatat data dalam bentuk tabel dan grafik  
🧠 Mencoba *menebak bentuk rumus* kuadrat dari pola data  
🧪 Menguji tebakanmu — apakah cocok dengan semua titik?  
🏁 Lalu akhirnya... mengubah rumus itu ke *bentuk kuadrat sempurna*

---

## 🎯 Tujuan Pembelajaran

- Melatih kemampuan *menganalisis pola* dari data
- Memahami *struktur fungsi kuadrat*
- Meningkatkan *logika berpikir mandiri*, bukan hanya hafalan rumus
- Membentuk *pemahaman yang lebih dalam* melalui eksplorasi

---

💡 *Tips dari Pembimbing:*
> Jangan takut salah! Justru dari kesalahan kamu akan lebih cepat paham.  
> Coba minimal 3–5 nilai x, amati hasilnya, lalu buat dugaan yang masuk akal.  
> Kita belajar *dengan cara yang dilakukan para ilmuwan!*

Selamat bereksperimen dan semangat menemukan sendiri! 🎓
""")

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def fungsi_asli(x):
    # INI RAHASIA (bisa diganti a, b, c sesukamu)
    return 2 * x**2 + 3 * x + 1

st.set_page_config(page_title="Menemukan Rumus Fungsi Kuadrat", page_icon="📐")
st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat")

st.markdown("""
Modul ini dirancang untuk mengajakmu *menemukan sendiri* bentuk fungsi kuadrat melalui percobaan nilai.

---

## 🎯 Tujuan Pembelajaran

- Mengamati pola dari data input-output
- Menemukan rumus fungsi kuadrat berdasarkan data
- Menguji dugaan rumus terhadap titik-titik baru
- Mengubah ke bentuk kuadrat sempurna *setelah menemukan sendiri bentuk umum*

""")

# Session state
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.tebakan_siswa = ""
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.cocok = False

### LANGKAH 1 - EKSPERIMEN NILAI x
with st.expander("🔍 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    st.write("Masukkan nilai x (boleh negatif atau positif), lalu lihat hasil f(x).")
    x = st.number_input("Masukkan nilai x:", value=1, step=1, key="x_input")
    if st.button("➕ Tambahkan ke tabel", key="add_x"):
        if x not in st.session_state.x_list:
            st.session_state.x_list.append(x)
            st.session_state.fx_list.append(fungsi_asli(x))
        else:
            st.warning("Nilai x ini sudah pernah dicoba.")

    if st.session_state.x_list:
        st.write("📋 Data percobaan kamu:")
        data = {
            "x": st.session_state.x_list,
            "f(x)": st.session_state.fx_list
        }
        st.table(data)

        # Grafik titik-titik
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

### LANGKAH 2 - TEBAK RUMUS
if st.session_state.langkah_2 and not st.session_state.langkah_3:
    with st.expander("✏ Langkah 2: Tebak Rumus", expanded=True):
        st.markdown("""
        Dari data percobaanmu, coba tebak rumus fungsi kuadrat dalam bentuk:
        \[
        f(x) = ax^2 + bx + c
        \]
        Masukkan nilai dugaanmu untuk a, b, dan c:
        """)
        a_tebak = st.number_input("Tebakan koefisien a:", value=1, step=1, key="a_tebak")
        b_tebak = st.number_input("Tebakan koefisien b:", value=1, step=1, key="b_tebak")
        c_tebak = st.number_input("Tebakan konstanta c:", value=0, step=1, key="c_tebak")

        def fungsi_tebakan(x): return a_tebak * x**2 + b_tebak * x + c_tebak

        if st.button("🔍 Cek Kecocokan", key="cek_rumus"):
            cocok = True
            for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
                if fungsi_tebakan(x) != fx:
                    cocok = False
                    break
            if cocok:
                st.success("✅ Tebakanmu benar! Selamat, kamu telah menemukan rumus f(x)!")
                st.session_state.langkah_3 = True
                st.session_state.cocok = True
            else:
                st.error("❌ Masih ada yang belum cocok. Coba perbaiki tebakanmu.")

### LANGKAH 3 - KUADRAT SEMPURNA
if st.session_state.langkah_3 and st.session_state.cocok:
    with st.expander("🧠 Langkah 3: Bentuk Kuadrat Sempurna", expanded=True):
        a = a_tebak
        b = b_tebak
        c = c_tebak

        h = -b / (2 * a)
        k = c - (b**2) / (4 * a)

        st.markdown("""
        Dari rumus umum yang kamu temukan:
        """)
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
