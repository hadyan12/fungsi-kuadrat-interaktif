import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="📐 Temukan Fungsi Kuadrat!", page_icon="📐")

# --- Header Awal ---
st.title("📐 Temukan Sendiri Fungsi Kuadrat!")

st.markdown("""
### Pertemuan 1: Eksplorasi Awal Fungsi Kuadrat

#### 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum fungsi kuadrat melalui pengamatan data.
- Menentukan akar-akar fungsi kuadrat dari bentuk umum.
- Menumbuhkan keterampilan berpikir kritis dan eksploratif.

#### 🧭 Profil Pelajar Pancasila
- Bernalar kritis 🧠
- Mandiri 💪
- Kreatif 🎨
- Beriman dan bertakwa kepada Tuhan YME 🙏

---

💬 *Yuk kita mulai belajar fungsi kuadrat bukan dengan menghafal rumus, tapi dengan eksplorasi seperti ilmuwan matematika!*
""")

# --- Fungsi Rahasia (dengan titik puncak bulat) ---
def fungsi_rahasia(x):
    return 1 * (x - 2)**2 - 3  # Titik puncak di (2, -3)

# --- Inisialisasi Session State ---
if "x_list" not in st.session_state:
    st.session_state.x_list = []
    st.session_state.fx_list = []
    st.session_state.tebakan_a = None
    st.session_state.tebakan_b = None
    st.session_state.tebakan_c = None
    st.session_state.jumlah_salah = 0
    st.session_state.lanjut_tebakan = False
    st.session_state.lanjut_akar = False

# --- Langkah 1: Eksperimen Nilai x ---
st.header("🔍 Langkah 1: Eksperimen Nilai x")

with st.form(key="form_x"):
    col1, col2 = st.columns([3, 1])
    with col1:
        x_input = st.number_input("Masukkan nilai x:", step=1)
    with col2:
        submit = st.form_submit_button("➕ Tambahkan")

if submit and x_input not in st.session_state.x_list:
    st.session_state.x_list.append(x_input)
    st.session_state.fx_list.append(fungsi_rahasia(x_input))

if st.session_state.x_list:
    st.write("📊 Data (x, f(x)) yang sudah kamu uji:")
    st.table({"x": st.session_state.x_list, "f(x)": st.session_state.fx_list})

    fig, ax = plt.subplots()
    ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="blue")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Grafik Titik (x, f(x))")
    ax.grid(True)
    ax.set_xlim(min(st.session_state.x_list) - 2, max(st.session_state.x_list) + 2)
    st.pyplot(fig)

    if len(st.session_state.x_list) >= 3:
        if st.button("➡ Lanjut ke Langkah 2: Menebak Rumus"):
            st.session_state.lanjut_tebakan = True

# --- Langkah 2: Menebak Rumus Kuadrat ---
if st.session_state.lanjut_tebakan:
    st.header("✏ Langkah 2: Menebak Bentuk Umum Fungsi Kuadrat")

    st.latex(r"f(x) = ax^2 + bx + c")

    col1, col2, col3 = st.columns(3)
    a = col1.number_input("Tebak a:", key="a_tebak", step=1, value=1)
    b = col2.number_input("Tebak b:", key="b_tebak", step=1, value=0)
    c = col3.number_input("Tebak c:", key="c_tebak", step=1, value=0)

    def fungsi_tebakan(x): return a * x**2 + b * x + c

    if st.button("🔍 Cek Tebakan"):
        benar = True
        for x, fx in zip(st.session_state.x_list, st.session_state.fx_list):
            if fungsi_tebakan(x) != fx:
                benar = False
                break

        if benar:
            st.success("✅ Hebat! Kamu berhasil menemukan rumusnya!")
            st.session_state.lanjut_akar = True
            st.session_state.tebakan_a = a
            st.session_state.tebakan_b = b
            st.session_state.tebakan_c = c
        else:
            st.session_state.jumlah_salah += 1
            st.error("❌ Masih belum tepat. Coba lagi yuk!")

        if st.session_state.jumlah_salah >= 3:
            st.warning("📌 Kamu sudah mencoba 3 kali. Yuk ikuti bantuan langkah-langkah:")
            st.markdown("""
            #### 💡 Petunjuk Menemukan Koefisien
            1. Perhatikan perubahan nilai \( f(x) \) saat \( x \) naik 1 satuan.
            2. Hitung selisih kedua antar \( f(x) \) — jika konstan, itu menandakan bentuk kuadrat.
            3. Gunakan titik puncak (minimum atau maksimum) untuk membantu menebak nilai \( a \) dan \( b \).
            4. Ingat bahwa bentuk kuadrat umum berasal dari bentuk kuadrat sempurna:
               \[
               f(x) = a(x - h)^2 + k \rightarrow ax^2 + bx + c
               \]
            5. Jika tahu titik puncak \((h, k)\), coba ubah ke bentuk umum!

            🌟 *Coba kembali dengan pendekatan yang lebih sistematis.*
            """)

# --- Langkah 3: Menentukan Akar Persamaan Kuadrat ---
if st.session_state.lanjut_akar:
    st.header("🧠 Langkah 3: Menentukan Akar Persamaan")

    a = st.session_state.tebakan_a
    b = st.session_state.tebakan_b
    c = st.session_state.tebakan_c

    st.latex(f"f(x) = {a}x^2 + {b}x + {c}")

    D = b**2 - 4*a*c
    st.latex(r"\text{Diskriminan: } D = b^2 - 4ac = " + str(D))

    if D > 0:
        akar1 = (-b + D**0.5) / (2*a)
        akar2 = (-b - D**0.5) / (2*a)
        st.success(f"Akar-akarnya adalah: x₁ = {akar1:.2f}, x₂ = {akar2:.2f}")
    elif D == 0:
        akar = -b / (2*a)
        st.success(f"Akar kembar: x = {akar:.2f}")
    else:
        st.info("Fungsi ini tidak memiliki akar real karena D < 0.")

    # Grafik akhir
    st.subheader("📈 Grafik Lengkap Fungsi")
    x_vals = np.linspace(min(st.session_state.x_list) - 2, max(st.session_state.x_list) + 2, 400)
    y_vals = [fungsi_rahasia(x) for x in x_vals]

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.scatter(st.session_state.x_list, st.session_state.fx_list, color="green", label="Data Kamu")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
