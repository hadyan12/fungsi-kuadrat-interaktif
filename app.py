import streamlit as st
import matplotlib.pyplot as plt

def f(x):
    return x**2 + 2*x + 1

st.set_page_config(page_title="Belajar Fungsi Kuadrat", page_icon="🎓")
st.title("🎓 Interaktif Belajar Fungsi Kuadrat: f(x) = x² + 2x + 1")

# Header edukatif
st.markdown("""
Selamat datang di **modul belajar fungsi matematika interaktif**!  
Di sini kamu akan belajar bagaimana sebuah **fungsi mengubah input menjadi output**, dengan cara yang menyenangkan dan praktis.

---

## 🔍 Apa yang akan kamu lakukan?

✅ Menjelajahi fungsi kuadrat: `f(x) = x² + 2x + 1`  
✅ Memasukkan nilai **x**, lalu melihat bagaimana fungsi bekerja langkah demi langkah  
✅ **Menguji pemahamanmu** dengan menghitung sendiri dan mencocokkan hasilnya  
✅ Melihat **grafik fungsi** untuk memahami bentuk visual dari f(x)

---

## 🎯 Tujuan Pembelajaran

- Memahami konsep **fungsi kuadrat sederhana**
- Menjelaskan proses evaluasi fungsi untuk berbagai nilai x
- Meningkatkan keterampilan berpikir logis dan mandiri
""")

# Inisialisasi session state
if "percobaan" not in st.session_state:
    st.session_state.percobaan = 0
    st.session_state.riwayat_x = []
    st.session_state.lanjut = True
    st.session_state.step1_done = False
    st.session_state.step2_done = False
    st.session_state.jumlah_salah = 0
    st.session_state.x2_benar = False

# Langkah 1 - Eksplorasi
if not st.session_state.step1_done:
    with st.expander("\U0001F4D8 Langkah 1: Eksplorasi Fungsi", expanded=True):
        st.write("Masukkan nilai x dan tekan tombol **Lihat hasil** untuk melihat bagaimana fungsi bekerja.")

        current_try = st.session_state.percobaan
        key_prefix = f"percobaan_{current_try}"

        if f"{key_prefix}_show_result" not in st.session_state:
            st.session_state[f"{key_prefix}_show_result"] = False
        if f"{key_prefix}_x_final" not in st.session_state:
            st.session_state[f"{key_prefix}_x_final"] = None

        if not st.session_state[f"{key_prefix}_show_result"]:
            x = st.number_input(
                f"Percobaan ke-{current_try + 1}: Masukkan nilai x (1–10):",
                min_value=1, max_value=10, step=1,
                key=f"{key_prefix}_x"
            )

            if st.button("\U0001F4E5 Lihat hasil", key=f"{key_prefix}_lihat"):
                st.session_state[f"{key_prefix}_x_final"] = x
                st.session_state[f"{key_prefix}_show_result"] = True

        if st.session_state[f"{key_prefix}_show_result"]:
            x = st.session_state[f"{key_prefix}_x_final"]
            st.info(f"Percobaan ke-{current_try + 1}, nilai x = {x}")
            st.markdown(f"""
            - x² = {x}² = {x**2}  
            - 2x = 2 × {x} = {2*x}  
            - Jumlah: {x**2} + {2*x} + 1 = {f(x)}  
            ✅ Maka f({x}) = **{f(x)}**
            """)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁 Coba nilai lain", key=f"{key_prefix}_lanjut"):
                    if x not in st.session_state.riwayat_x:
                        st.session_state.riwayat_x.append(x)
                    st.session_state.percobaan += 1
                    st.rerun()

            with col2:
                if st.button("❌ Selesai", key=f"{key_prefix}_selesai"):
                    if x not in st.session_state.riwayat_x:
                        st.session_state.riwayat_x.append(x)
                    st.session_state.step1_done = True
                    st.rerun()

            st.write("📌 Riwayat nilai x:", st.session_state.riwayat_x)

        if st.session_state.percobaan >= 3:
            st.info("⚠️ Sudah 3 kali mencoba.")
            st.session_state.step1_done = True
            st.rerun()

# Langkah 2 - Uji Pemahaman
if st.session_state.step1_done and not st.session_state.step2_done:
    with st.expander("📗 Langkah 2: Uji Pemahaman", expanded=True):
        st.write("Sekarang coba hitung **sendiri**, pakai nilai x yang **belum dipakai sebelumnya**.")

        x2_input = st.number_input("Masukkan nilai x baru:", min_value=1, max_value=10, step=1, key="x2_input")
        if x2_input in st.session_state.riwayat_x:
            st.warning("⚠️ Nilai ini sudah digunakan. Coba nilai lain.")
        else:
            jawaban = st.number_input(f"Hitung: f({x2_input}) = {x2_input}² + 2×{x2_input} + 1 = ... ?", step=1, key="jawaban_input")

            if st.button("Cek Jawaban", key="cekjawaban"):
                if jawaban == f(x2_input):
                    st.success("✅ Jawabanmu benar! Kamu hebat.")
                    st.session_state.step2_done = True
                    st.session_state.x2_benar = True
                else:
                    st.session_state.jumlah_salah += 1
                    sisa = 3 - st.session_state.jumlah_salah
                    if sisa > 0:
                        st.error(f"❌ Masih belum tepat. Coba lagi ya. ({sisa} kesempatan lagi)")
                    else:
                        st.warning("🧠 Sudah 3 kali salah. Yuk kita bantu bareng, kamu tetap yang hitung:")
                        kuadrat = st.number_input(f"Langkah 1: Hitung {x2_input}² =", step=1, key="kuadrat_bantu")
                        kali_dua = st.number_input(f"Langkah 2: Hitung 2 × {x2_input} =", step=1, key="kali2_bantu")
                        total = st.number_input(f"Langkah 3: Hitung {kuadrat} + {kali_dua} + 1 =", step=1, key="total_bantu")

                        if kuadrat == x2_input**2 and kali_dua == 2 * x2_input and total == f(x2_input):
                            st.success(f"✅ Betul! Maka f({x2_input}) = {total}")
                            st.session_state.step2_done = True
                            st.session_state.x2_benar = True
                        else:
                            st.info("🔁 Cek kembali perhitunganmu ya!")

# Langkah 3 - Visualisasi
if st.session_state.step2_done and st.session_state.x2_benar:
    with st.expander("📊 Langkah 3: Visualisasi Grafik"):
        x_vals = list(range(1, 11))
        y_vals = [f(x) for x in x_vals]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_vals, y_vals, marker='o', color='blue')
        ax.set_title("Grafik Fungsi f(x) = x² + 2x + 1")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)

        st.pyplot(fig)
