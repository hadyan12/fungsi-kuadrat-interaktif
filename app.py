import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Eksplorasi Fungsi Kuadrat", page_icon="🧮")
st.title("🧮 Eksplorasi Interaktif Fungsi Kuadrat")

st.markdown("""
Selamat datang di modul eksplorasi fungsi kuadrat!  
Kamu akan:
- 🔍 Melakukan eksperimen nilai `x` dan melihat hasil `f(x)`
- 🧠 Menebak rumus fungsi kuadrat berdasarkan data
- 🧮 Menentukan akar-akar dari fungsi tersebut

> Tujuanmu hari ini: Menemukan bentuk umum fungsi kuadrat dan menentukan akarnya!
---
""")

# Fungsi asli yang akan ditebak siswa
def fungsi_kuadrat(x):
    return 1 * x**2 - 4 * x + 3  # Titik puncak (2, -1), akar 1 dan 3

# Session State
if "x_vals" not in st.session_state:
    st.session_state.x_vals = []
    st.session_state.y_vals = []
    st.session_state.tebakan_salah = 0
    st.session_state.langkah_2 = False
    st.session_state.benar = False

# Langkah 1: Eksplorasi Nilai
with st.expander("📊 Langkah 1: Eksplorasi Nilai f(x) = ax² + bx + c", expanded=not st.session_state.langkah_2):
    st.write("Masukkan nilai `x`, lalu klik tambahkan:")
    x_input = st.number_input("Nilai x", step=1, value=0)
    if st.button("➕ Tambahkan Nilai"):
        if x_input not in st.session_state.x_vals:
            st.session_state.x_vals.append(x_input)
            st.session_state.y_vals.append(fungsi_kuadrat(x_input))
        else:
            st.warning("Nilai x sudah dicoba.")

    if st.session_state.x_vals:
        st.subheader("📋 Tabel Nilai")
        st.table({
            "x": st.session_state.x_vals,
            "f(x)": st.session_state.y_vals
        })

        # Grafik
        x_range = np.linspace(min(st.session_state.x_vals)-2, max(st.session_state.x_vals)+2, 200)
        y_range = fungsi_kuadrat(x_range)

        fig, ax = plt.subplots()
        ax.plot(x_range, y_range, label="f(x)", color="blue")
        ax.scatter(st.session_state.x_vals, st.session_state.y_vals, color="red", label="Titik Percobaan")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        if len(st.session_state.x_vals) >= 3:
            if st.button("➡ Lanjut ke Tebak Rumus"):
                st.session_state.langkah_2 = True
                st.rerun()

# Langkah 2: Tebak Rumus
if st.session_state.langkah_2 and not st.session_state.benar:
    with st.expander("✏️ Langkah 2: Tebak Bentuk Umum f(x)", expanded=True):
        st.latex(r"f(x) = ax^2 + bx + c")
        a = st.number_input("Tebakan a", value=1, step=1)
        b = st.number_input("Tebakan b", value=0, step=1)
        c = st.number_input("Tebakan c", value=0, step=1)

        def fungsi_tebakan(x):
            return a * x**2 + b * x + c

        if st.button("✅ Cek Tebakan"):
            cocok = True
            for x_val, y_val in zip(st.session_state.x_vals, st.session_state.y_vals):
                if fungsi_tebakan(x_val) != y_val:
                    cocok = False
                    break

            if cocok:
                st.success("🎉 Hebat! Tebakanmu benar!")
                st.session_state.benar = True
            else:
                st.session_state.tebakan_salah += 1
                st.error(f"Tebakan belum tepat. Coba lagi! ({st.session_state.tebakan_salah}/3)")

        if st.session_state.tebakan_salah >= 3:
            st.warning("⚠️ Sudah 3 kali salah. Yuk coba analisis data dengan cara ini:")
            st.markdown("""
            ### 💡 Langkah Bantuan:
            1. Perhatikan perubahan nilai `f(x)` saat `x` bertambah satu-satu  
            2. Hitung selisih antar nilai `f(x)` → apakah selisihnya tetap?
            3. Jika tidak tetap, coba cek selisih kedua (second difference)  
            4. Jika selisih kedua tetap, maka fungsi itu kuadrat!
            5. Gunakan sistem persamaan dari 3 titik untuk menebak `a`, `b`, dan `c`
            """)

# Langkah 3: Menentukan Akar
if st.session_state.benar:
    with st.expander("🧮 Langkah 3: Menentukan Akar Persamaan", expanded=True):
        st.markdown("Setelah kamu mengetahui rumusnya:")
        st.latex(f"f(x) = {a}x^2 + {b}x + {c}")

        D = b**2 - 4*a*c
        st.markdown(f"Diskriminan (D) = {b}² - 4({a})({c}) = {D}")

        if D < 0:
            st.error("Tidak ada akar real karena D < 0.")
        else:
            akar1 = (-b + D**0.5) / (2*a)
            akar2 = (-b - D**0.5) / (2*a)
            st.success(f"Akar-akarnya adalah: x₁ = {akar1:.2f}, x₂ = {akar2:.2f}")
            st.latex(r"x = \frac{-b \pm \sqrt{D}}{2a}")
