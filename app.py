import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ===================== SETUP =====================
st.set_page_config(page_title="📐 Temukan Rumus Fungsi Kuadrat", page_icon="📐")
st.title("📐 Temukan Sendiri Rumus Fungsi Kuadrat!")

st.markdown("""
Hai, selamat datang di *ruang eksplorasi fungsi kuadrat!*

Hari ini kamu *bukan cuma belajar* seperti biasa.  
Kamu akan *menjadi peneliti matematika*: mencoba beberapa nilai, mengamati hasilnya, dan...  
🤔 *menebak sendiri rumus* fungsi yang tersembunyi di balik angka-angka itu.
""")

# ===================== INISIALISASI =====================
def fungsi_asli(x):
    return 2 * x**2 + 3 * x + 1

if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.langkah_4 = False
    st.session_state.salah_tebakan_puncak = 0
    st.session_state.puncak_ditebak = False
    st.session_state.tebakan_puncak_x = None
    st.session_state.tebakan_puncak_fx = None

# ===================== LANGKAH 1 =====================
st.header("🔍 Langkah 1: Eksperimen Nilai x")
st.markdown("Masukkan beberapa nilai \(x\) untuk melihat hasil \(f(x)\). Amati polanya!")

x_input = st.number_input("Masukkan nilai x:", step=1, key="input_x")
if st.button("➕ Tambahkan", key="btn_add_x"):
    if x_input not in st.session_state.x_list:
        st.session_state.x_list.append(x_input)
        st.session_state.fx_list.append(fungsi_asli(x_input))
    else:
        st.warning("Nilai x ini sudah dicoba sebelumnya.")

if st.session_state.x_list:
    st.subheader("📋 Data Percobaan")
    st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

    fig, ax = plt.subplots()
    ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue')
    ax.set_title("Plot Titik (x, f(x))")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    margin = 5
    min_x, max_x = min(st.session_state.x_list), max(st.session_state.x_list)
    ax.set_xlim(min_x - margin, max_x + margin)
    st.pyplot(fig)

    if len(st.session_state.x_list) >= 3:
        st.success("Kamu sudah mencoba cukup titik. Yuk ke langkah berikutnya!")
        if st.button("➡ Lanjut ke Langkah 2"):
            st.session_state.langkah_2 = True

# ===================== LANGKAH 2 =====================
if st.session_state.langkah_2:
    st.header("📍 Langkah 2: Tebak Titik Puncak")
    st.markdown("""
    Dari bentuk grafik, coba tebak nilai \(x\) yang merupakan titik puncak (sumbu simetri).  
    Lalu, tebak juga nilai \(f(x)\) di titik tersebut.
    """)

    tebakan_x = st.number_input("Tebak nilai x titik puncak:", step=1, key="tebak_x")
    tebakan_fx = st.number_input("Tebak nilai f(x) titik puncak:", step=1, key="tebak_fx")

    if st.button("🔍 Cek Tebakan Puncak"):
        x_puncak_benar = -3 / (2 * 2)  # -b/2a
        fx_puncak_benar = fungsi_asli(x_puncak_benar)

        benar = abs(tebakan_x - x_puncak_benar) < 0.1 and abs(tebakan_fx - fx_puncak_benar) < 0.5

        if benar:
            st.success("✅ Tebakanmu tepat! Titik puncaknya sudah benar.")
            st.session_state.puncak_ditebak = True
            st.session_state.tebakan_puncak_x = tebakan_x
            st.session_state.tebakan_puncak_fx = tebakan_fx
            st.session_state.langkah_3 = True
        else:
            st.session_state.salah_tebakan_puncak += 1
            st.error("❌ Belum tepat. Coba lagi ya!")

        if st.session_state.salah_tebakan_puncak >= 3:
            st.info("💡 *Petunjuk:* Grafik fungsi kuadrat selalu simetris. Carilah nilai x yang berada di tengah-tengah dua titik dengan f(x) yang sama.")

# ===================== LANGKAH 3 =====================
if st.session_state.langkah_3:
    st.header("✏️ Langkah 3: Tebak Rumus Umum")
    st.markdown("Sekarang coba tebak rumus \(f(x) = ax^2 + bx + c\)")

    a_tebak = st.number_input("Tebak nilai a:", value=1.0, step=0.5, key="a_tebak")
    b_tebak = st.number_input("Tebak nilai b:", value=1.0, step=0.5, key="b_tebak")
    c_tebak = st.number_input("Tebak nilai c:", value=0.0, step=0.5, key="c_tebak")

    def f_tebakan(x): return a_tebak * x**2 + b_tebak * x + c_tebak

    if st.button("✅ Cek Rumus"):
        semua_cocok = True
        for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
            if abs(f_tebakan(x) - fx) > 0.01:
                semua_cocok = False
                break
        if semua_cocok:
            st.success("🎉 Hebat! Rumusmu cocok dengan semua titik!")
            st.session_state.langkah_4 = True
        else:
            st.error("😕 Masih ada titik yang tidak cocok. Coba lagi ya!")

# ===================== LANGKAH 4 =====================
if st.session_state.langkah_4:
    st.header("🧠 Langkah 4: Bentuk Kuadrat Sempurna")
    a = a_tebak
    b = b_tebak
    c = c_tebak
    h = -b / (2 * a)
    k = c - (b**2) / (4 * a)

    st.markdown("Rumus umum kamu adalah:")
    st.latex(f"f(x) = {a}x^2 + {b}x + {c}")

    st.markdown("Kita ubah ke bentuk kuadrat sempurna:")
    st.latex(rf"f(x) = {a}(x {(-h):+})^2 + {k:.2f}")

    st.success(f"Jadi bentuk kuadrat sempurna: f(x) = {a}(x {(-h):+})² + {k:.2f}")

    st.subheader("📈 Grafik Lengkap")
    x_vals = np.linspace(h - 10, h + 10, 400)
    y_vals = fungsi_asli(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")
    ax.axvline(h, color="red", linestyle="--", label="Sumbu Simetri")
    ax.plot(h, k, "ro", label="Titik Puncak")
    ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="green", label="Titik Data")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.balloons()
