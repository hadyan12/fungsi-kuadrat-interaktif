import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Temukan Rumus Fungsi Kuadrat", page_icon="📀")
st.title("\ud83d\udcc0 Temukan Sendiri Rumus Fungsi Kuadrat!")

# Fungsi asli yang disembunyikan dari siswa (boleh diubah a,b,c-nya)
def fungsi_asli(x):
    return 2 * x**2 + 3 * x + 1

# Inisialisasi session state
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.langkah_2 = False
    st.session_state.langkah_3 = False
    st.session_state.langkah_4 = False
    st.session_state.langkah_5 = False
    st.session_state.salah_tebakan = 0
    st.session_state.tebakan_benar = False

# ---------- LANGKAH 1: EKSPERIMEN NILAI X ----------
with st.expander("🔍 Langkah 1: Eksperimen Nilai x", expanded=not st.session_state.langkah_2):
    st.markdown("Masukkan beberapa nilai \( x \), lalu amati hasil \( f(x) \) dan bentuk grafiknya.")
    x = st.number_input("Masukkan nilai x:", value=0, step=1, key="x_input")
    if st.button("Tambah ke tabel", key="tambah_x"):
        if x not in st.session_state.x_list:
            st.session_state.x_list.append(x)
            st.session_state.fx_list.append(fungsi_asli(x))
        else:
            st.warning("Nilai x ini sudah pernah dimasukkan.")

    if st.session_state.x_list:
        st.markdown("### Tabel Data Percobaan")
        st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

        # Grafik
        x_min = min(st.session_state.x_list) - 2
        x_max = max(st.session_state.x_list) + 2
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = fungsi_asli(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="f(x)", color="lightgray")
        ax.scatter(st.session_state.x_list, st.session_state.fx_list, color='blue', label='Titik Data')
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        if len(st.session_state.x_list) >= 3:
            if st.button("Lanjut ke Langkah 2"):
                st.session_state.langkah_2 = True
                st.rerun()

# ---------- LANGKAH 2: TEBAK TITIK PUNCAK ----------
if st.session_state.langkah_2 and not st.session_state.langkah_3:
    with st.expander("🏛️ Langkah 2: Tebak Titik Puncak", expanded=True):
        st.markdown("""
        Amati grafik parabola. Coba tebak kira-kira di mana titik puncaknya:
        """)
        x_tebak = st.number_input("Tebakan nilai x titik puncak:", value=0, key="x_puncak")
        fx_tebak = st.number_input("Tebakan nilai f(x) di titik puncak:", value=0, key="fx_puncak")

        x_asli = -3 / (2 * 2)  # -b/(2a) dari fungsi_asli
        fx_asli = fungsi_asli(x_asli)

        if st.button("Cek Tebakan Titik Puncak"):
            if abs(x_tebak - x_asli) < 0.5 and abs(fx_tebak - fx_asli) < 1:
                st.success("Tebakanmu mendekati titik puncak yang benar!")
                st.session_state.langkah_3 = True
            else:
                st.info("Belum tepat. Coba amati kembali grafiknya, dan ingat bahwa parabola simetris!")

# ---------- LANGKAH 3: TEBAK RUMUS F(X) ----------
if st.session_state.langkah_3 and not st.session_state.langkah_4:
    with st.expander("✍️ Langkah 3: Tebak Rumus f(x)", expanded=True):
        st.latex("f(x) = ax^2 + bx + c")
        a_tebak = st.number_input("Tebakan koefisien a:", value=1, key="a_tebak")
        b_tebak = st.number_input("Tebakan koefisien b:", value=1, key="b_tebak")
        c_tebak = st.number_input("Tebakan konstanta c:", value=0, key="c_tebak")

        def f_tebakan(x):
            return a_tebak * x**2 + b_tebak * x + c_tebak

        if st.button("Cek Kecocokan Rumus"):
            cocok = True
            for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
                if f_tebakan(x) != fx:
                    cocok = False
                    break

            if cocok:
                st.success("Tebakanmu benar! Selamat, kamu menemukan rumus f(x).")
                st.session_state.tebakan_benar = True
                st.session_state.langkah_4 = True
            else:
                st.error("Masih belum cocok dengan semua titik. Coba perbaiki tebakanmu.")
                st.session_state.salah_tebakan += 1

                if st.session_state.salah_tebakan >= 3:
                    st.info("Ingin petunjuk?")
                    with st.expander("🕵️ Petunjuk!"):
                        st.markdown("""
                        - Lihat bentuk grafik: apakah membuka ke atas atau ke bawah? Itu memberi tahu tanda dari \( a \)
                        - Tebak koefisien berdasarkan seberapa cepat parabola naik/turun
                        - Kamu bisa pakai 3 titik dan susun persamaan untuk mendapatkan a, b, dan c secara sistematis (eliminasi atau substitusi)
                        """)

# ---------- LANGKAH 4: UBah ke Bentuk Kuadrat Sempurna ----------
if st.session_state.langkah_4 and st.session_state.tebakan_benar:
    with st.expander("🧠 Langkah 4: Ubah ke Bentuk Kuadrat Sempurna", expanded=True):
        a = a_tebak
        b = b_tebak
        c = c_tebak
        h = -b / (2 * a)
        k = fungsi_asli(h)

        st.markdown("Dari rumus:")
        st.latex(f"f(x) = {a}x^2 + {b}x + {c}")

        st.markdown("Kita ubah ke bentuk kuadrat sempurna:")
        st.latex(f"f(x) = {a}(x {(-h):+})^2 + {k:.2f}")

        st.success(f"Titik puncak parabola: (x, f(x)) = ({h:.2f}, {k:.2f})")

        # Grafik Akhir
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
        st.success("Selamat! Kamu berhasil menemukan rumus fungsi kuadrat dan titik puncaknya!")
