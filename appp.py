import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

# ---------------------------- SETUP AWAL ----------------------------
st.set_page_config(page_title="📐 Eksplorasi Fungsi Kuadrat", page_icon="📐")
st.title("📐 Eksplorasi Mandiri Fungsi Kuadrat")

st.markdown("""
Selamat datang di eksplorasi fungsi kuadrat! 🎓
Kamu akan belajar lewat percobaan, analisis data, dan berpikir kritis. Bukan sekadar rumus, tapi *proses menemukan*.
---
## 🎯 Tujuan Pembelajaran
- Menuliskan bentuk umum fungsi kuadrat dari data
- Menentukan akar-akar dengan metode faktorisasi
---
## 🇮🇩 Profil Pelajar Pancasila
- Bernalar kritis dan mandiri
- Kreatif dalam menemukan pola
- Bertanggung jawab atas proses belajar
---
""")

# ---------------------------- INISIALISASI ----------------------------
# Perbaikan fungsi_rahasia dan Fungsi 1 agar konsisten dengan faktorisasi (x-2)(x-4)
def fungsi_rahasia(x):
    return (x - 2)*(x - 4) # y = x^2 - 6x + 8

fungsi_pilihan = {
    "Fungsi 1": (lambda x: x**2 - 6*x + 8), # Sesuaikan agar faktorisasi (x-2)(x-4) valid
    "Fungsi 2": (lambda x: x**2 - 5*x + 6),
    "Fungsi 3": (lambda x: x**2 - 4*x + 3)
}
fungsi_latex = {
    "Fungsi 1": "y = x^{2} - 6x + 8", # Sesuaikan agar faktorisasi (x-2)(x-4) valid
    "Fungsi 2": "y = x^{2} - 5x + 6",
    "Fungsi 3": "y = x^{2} - 4x + 3"
}
faktorisasi_dict = {
    "Fungsi 1": ["(x - 2)(x - 4)", 2, 4],
    "Fungsi 2": ["(x - 2)(x - 3)", 2, 3],
    "Fungsi 3": ["(x - 1)(x - 3)", 1, 3]
}

if "data_titik" not in st.session_state:
    st.session_state.data_titik = []
    st.session_state.input_manual = []
    st.session_state.langkah = 1
    st.session_state.tebakan_abc = {"a": "", "b": "", "c": ""}
    st.session_state.salah_tebakan_abc = 0
    st.session_state.salah_faktorisasi = 0
    st.session_state.sudah_eliminasi = False
    st.session_state.tebakan_fungsi = ""
    st.session_state.fungsi_tersisa = []
    st.session_state.salah_input_x1x2 = 0
    st.session_state.tiga_titik = []
    st.session_state.grafik_benar_muncul = False
    st.session_state.x_benar_ditebak = set()
    st.session_state.show_pembahasan_langkah5 = False

# ---------------------------- LANGKAH 1 ----------------------------
st.header("🟩 Langkah 1: Masukkan Titik-titik")
st.markdown("Masukkan nilai x antara -2 sampai 7 untuk melihat nilai y")

x_input = st.number_input("Nilai x:", min_value=-2, max_value=7, step=1, key="x_input")
if st.button("Tambah Titik"):
    if x_input not in [x for x, _ in st.session_state.data_titik]:
        y_val = fungsi_rahasia(x_input)
        st.session_state.data_titik.append((x_input, y_val))

if st.session_state.data_titik:
    df = pd.DataFrame(st.session_state.data_titik, columns=["x", "y"])
    st.write("### Tabel Titik")
    st.dataframe(df)

    fig, ax = plt.subplots()
    x_vals, y_vals = zip(*st.session_state.data_titik)
    ax.scatter(x_vals, y_vals, color="green")
    for x, y in st.session_state.data_titik:
        ax.axvline(x, ymax=(y+2)/(max(y_vals)+3), linestyle="dotted", color="gray")
        ax.axhline(y, xmax=(x+2)/10, linestyle="dotted", color="gray")
        ax.text(x, y, f"({x},{y})", fontsize=8, ha='right')
    ax.set_title("Titik-titik (x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(range(-2, 8))
    ax.set_yticks(range(min(y_vals)-2, max(y_vals)+3))
    
    # Remove grid and set plain background
    ax.grid(False)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    st.pyplot(fig)

    if len(st.session_state.data_titik) >= 5:
        if st.button("➡ Lanjut ke Langkah 2"):
            st.session_state.langkah = 2
            st.rerun()

# ---------------------------- LANGKAH 2 ----------------------------
if st.session_state.langkah >= 2:
    st.header("🟦 Langkah 2: Tebak y dari Nilai x")
    st.markdown("Masukkan **nilai x dan y** yang kamu tebak. Sistem akan mencocokkan dengan fungsi yang tersembunyi.")
    col1, col2 = st.columns(2)
    with col1:
        x_manual = st.number_input("Tebak nilai x:", min_value=-2, max_value=7, step=1, key="manual_x")
    with col2:
        y_manual = st.text_input("Tebak nilai y:", key="manual_y")

    if st.button("Cek Tebakan"):
        if x_manual in st.session_state.x_benar_ditebak:
            st.warning(f"Anda sudah menebak dengan benar untuk x = {x_manual}. Silakan coba nilai x yang lain.")
        else:
            try:
                y_manual_val = int(y_manual)
                y_benar = fungsi_rahasia(x_manual)
                if y_manual_val == y_benar:
                    st.success("✅ Benar")
                    st.session_state.input_manual.append((x_manual, y_manual_val, "✅ Benar"))
                    st.session_state.x_benar_ditebak.add(x_manual)
                else:
                    st.error("❌ Salah")
                    st.session_state.input_manual.append((x_manual, y_manual_val, "❌ Salah"))
            except ValueError:
                st.session_state.input_manual.append((x_manual, y_manual, "⚠ Input tidak valid"))
                st.error("Masukkan harus berupa bilangan bulat untuk y.")

    if st.session_state.input_manual:
        st.write("### Tabel Hasil Tebakanmu")
        df2 = pd.DataFrame(st.session_state.input_manual, columns=["x", "y Tebakan", "Status"])
        df2.index = df2.index + 1
        st.dataframe(df2)

        unique_correct_x = set(row[0] for row in st.session_state.input_manual if row[2] == "✅ Benar")
        if len(unique_correct_x) >= 3:
            if st.button("➡ Lanjut ke Langkah 3"):
                st.session_state.langkah = 3
                valid_three_points = []
                for x_val in list(unique_correct_x)[:3]:
                    for item in st.session_state.input_manual:
                        if item[0] == x_val and item[2] == "✅ Benar":
                            valid_three_points.append(item)
                            break
                st.session_state.tiga_titik = valid_three_points
                st.rerun()

# ---------------------------- LANGKAH 3 ----------------------------
if st.session_state.langkah >= 3:
    st.header("🟨 Langkah 3: Substitusi dan Eliminasi")
    st.markdown("Gunakan 3 titik dari tebakan benar untuk membentuk sistem persamaan kuadrat.")
    titik = st.session_state.tiga_titik
    for x, y, *_ in titik:
        st.latex(f"({x}, {y})")

    st.markdown("### Substitusi ke $y = ax^2 + bx + c$:")
    for x, y, *_ in titik:
        st.latex(f"{y} = a({x})^2 + b({x}) + c")

    if not st.session_state.sudah_eliminasi:
        if st.button("✍️ Saya sudah eliminasi"):
            st.session_state.sudah_eliminasi = True
            st.rerun()
    else:
        a = st.text_input("a =", value=st.session_state.tebakan_abc["a"])
        b = st.text_input("b =", value=st.session_state.tebakan_abc["b"])
        c = st.text_input("c =", value=st.session_state.tebakan_abc["c"])

        if st.button("Cek Jawaban Bentuk Umum"):
            st.session_state.tebakan_abc = {"a": a, "b": b, "c": c}
            try:
                # Perbaikan: Sesuaikan nilai a, b, c dengan fungsi_rahasia yang baru (x^2 - 6x + 8)
                if int(a) == 1 and int(b) == -6 and int(c) == 8:
                    st.success("✅ Jawaban benar!")
                    st.session_state.grafik_benar_muncul = True
                else:
                    st.session_state.salah_tebakan_abc += 1
                    st.error("❌ Jawaban belum tepat")
                    if st.session_state.salah_tebakan_abc >= 3:
                        st.info("Hint: coba eliminasi ulang satu pasang persamaan saja terlebih dahulu.")
            except ValueError:
                st.error("Masukkan a, b, dan c harus berupa bilangan bulat.")
    
    if st.session_state.grafik_benar_muncul:
        st.subheader("🎉 Fungsi Kuadrat yang Ditemukan!")
        st.latex(fungsi_latex["Fungsi 1"])
        
        # Rentang X yang lebih luas
        x_plot = np.linspace(-5, 10, 400) # Diperlebar dari -2, 7 menjadi -5, 10
        y_plot = fungsi_pilihan["Fungsi 1"](x_plot)

        fig_quad, ax_quad = plt.subplots(figsize=(10, 6)) # Perbesar ukuran figur
        ax_quad.plot(x_plot, y_plot, color='blue', label=f'${fungsi_latex["Fungsi 1"].split("=")[1]}$')
        ax_quad.scatter([x for x,y,s in st.session_state.tiga_titik], [y for x,y,s in st.session_state.tiga_titik], color='red', s=100, zorder=5, label='Titik yang Digunakan') # Perbesar ukuran titik
        
        # Atur batas sumbu Y secara dinamis atau lebih lebar
        min_y_val = min(y_plot) if len(y_plot) > 0 else -10
        max_y_val = max(y_plot) if len(y_plot) > 0 else 20
        ax_quad.set_ylim(min_y_val - 5, max_y_val + 5) # Tambahkan margin pada Y

        ax_quad.set_title("Grafik Fungsi Kuadrat")
        ax_quad.set_xlabel("x")
        ax_quad.set_ylabel("y")
        ax_quad.grid(True)
        ax_quad.axhline(0, color='black',linewidth=0.5)
        ax_quad.axvline(0, color='black',linewidth=0.5)
        ax_quad.legend()
        st.pyplot(fig_quad)

        if st.button("➡ Lanjut ke Langkah 4"):
            st.session_state.langkah = 4
            st.rerun()

# ---------------------------- LANGKAH 4 ----------------------------
if st.session_state.langkah >= 4:
    st.header("🟧 Langkah 4: Pilih Fungsi")
    st.markdown("Pilih salah satu fungsi kuadrat berikut untuk kamu faktorkan:")
    for k, rumus in fungsi_latex.items():
        st.latex(f"{k}: {rumus}")
    st.session_state.tebakan_fungsi = st.radio("Pilih salah satu:", list(fungsi_latex.keys()))
    if st.button("Cek Pilihan Fungsi"):
        st.session_state.fungsi_tersisa = [f for f in fungsi_latex if f != st.session_state.tebakan_fungsi]
        st.session_state.langkah = 5
        st.session_state.show_pembahasan_langkah5 = False 
        st.rerun()

# ---------------------------- LANGKAH 5 ----------------------------
if st.session_state.langkah >= 5:
    st.header("🟪 Langkah 5: Faktorisasi Fungsi Pilihan")
    kode = st.session_state.tebakan_fungsi
    st.latex(fungsi_latex[kode])
    st.markdown("Apa faktorisasi dari fungsi ini?")
    
    opsi_faktorisasi = [
        faktorisasi_dict[kode][0],
        "(x + 1)(x - 7)",
        "(x - 5)(x - 2)",
        "(x + 3)(x - 1)",
        "(x - 2)^2"
    ]
    random.shuffle(opsi_faktorisasi)

    pilihan = st.radio("Pilih faktorisasi yang benar:", opsi_faktorisasi)
    if st.button("Cek Faktorisasi"):
        if pilihan == faktorisasi_dict[kode][0]:
            st.success("✅ Benar!")
            st.session_state.show_pembahasan_langkah5 = True
        else:
            st.session_state.salah_faktorisasi += 1
            st.error("❌ Masih salah")
            st.session_state.show_pembahasan_langkah5 = False
            if st.session_state.salah_faktorisasi >= 3:
                st.info("Hint: Perhatikan koefisien tengah dan konstanta. Ingat, $(x-p)(x-q) = x^2 - (p+q)x + pq$.")

    if st.session_state.show_pembahasan_langkah5:
        st.subheader("💡 Pembahasan Lengkap Metode Faktorisasi:")
        st.markdown(f"""
        Untuk memfaktorkan fungsi kuadrat dalam bentuk umum $ax^2 + bx + c$, terutama ketika $a=1$ (seperti fungsi ini), kita mencari dua bilangan ($p$ dan $q$) yang memenuhi dua kondisi penting:
        1.  **Hasil Kali (Produk) $p \times q = c$**: Kedua bilangan tersebut jika dikalikan harus menghasilkan nilai **konstanta** ($c$).
        2.  **Hasil Jumlah (Sum) $p + q = b$**: Kedua bilangan tersebut jika dijumlahkan harus menghasilkan nilai **koefisien dari $x$** ($b$).

        Setelah menemukan $p$ dan $q$, bentuk faktorisasinya akan menjadi $(x - p)(x - q)$.

        Mari kita terapkan pada **Fungsi {kode}** yaitu $y = {fungsi_latex[kode].split('=')[1]}$:
        """)

        # Tentukan nilai b dan c berdasarkan fungsi yang dipilih
        if kode == "Fungsi 1": # y = x^2 - 6x + 8
            b_val = -6
            c_val = 8
            p_val = 2
            q_val = 4
        elif kode == "Fungsi 2": # y = x^2 - 5x + 6
            b_val = -5
            c_val = 6
            p_val = 2
            q_val = 3
        elif kode == "Fungsi 3": # y = x^2 - 4x + 3
            b_val = -4
            c_val = 3
            p_val = 1
            q_val = 3
        
        st.markdown(f"""
        Fungsi yang kita faktorkan adalah: ${fungsi_latex[kode].split('=')[1]}$
        Di sini, nilai koefisien $x$ adalah $b = {b_val}$, dan nilai konstanta adalah $c = {c_val}$.

        **Langkah 1: Cari pasangan bilangan yang hasil kalinya $c$ ($c = {c_val}$)**
        """)
        
        if kode == "Fungsi 1":
            st.markdown(f"""
            Kita cari dua bilangan yang jika dikalikan menghasilkan $8$. Beberapa kemungkinannya adalah:
            * $1 \times 8 = 8$
            * $-1 \times -8 = 8$
            * $2 \times 4 = 8$
            * $-2 \times -4 = 8$
            """)
        elif kode == "Fungsi 2":
            st.markdown(f"""
            Kita cari dua bilangan yang jika dikalikan menghasilkan $6$. Beberapa kemungkinannya adalah:
            * $1 \times 6 = 6$
            * $-1 \times -6 = 6$
            * $2 \times 3 = 6$
            * $-2 \times -3 = 6$
            """)
        elif kode == "Fungsi 3":
            st.markdown(f"""
            Kita cari dua bilangan yang jika dikalikan menghasilkan $3$. Beberapa kemungkinannya adalah:
            * $1 \times 3 = 3$
            * $-1 \times -3 = 3$
            """)

        st.markdown(f"""
        **Langkah 2: Dari pasangan tersebut, cari yang hasil jumlahnya $b$ ($b = {b_val}$)**
        """)

        if kode == "Fungsi 1":
            st.markdown(f"""
            Sekarang, mari kita jumlahkan pasangan-pasangan di atas untuk melihat mana yang hasilnya $-6$:
            * $1 + 8 = 9$ (bukan)
            * $-1 + (-8) = -9$ (bukan)
            * $2 + 4 = 6$ (bukan)
            * $\\boxed{-2 + (-4) = -6}$ (cocok!)

            Kita menemukan bilangan tersebut adalah **-2 dan -4**.
            """)
        elif kode == "Fungsi 2":
            st.markdown(f"""
            Sekarang, mari kita jumlahkan pasangan-pasangan di atas untuk melihat mana yang hasilnya $-5$:
            * $1 + 6 = 7$ (bukan)
            * $-1 + (-6) = -7$ (bukan)
            * $\\boxed{-2 + (-3) = -5}$ (cocok!)

            Kita menemukan bilangan tersebut adalah **-2 dan -3**.
            """)
        elif kode == "Fungsi 3":
            st.markdown(f"""
            Sekarang, mari kita jumlahkan pasangan-pasangan di atas untuk melihat mana yang hasilnya $-4$:
            * $1 + 3 = 4$ (bukan)
            * $\\boxed{-1 + (-3) = -4}$ (cocok!)

            Kita menemukan bilangan tersebut adalah **-1 dan -3**.
            """)

        st.markdown(f"""
        **Langkah 3: Tuliskan dalam bentuk faktorisasi $(x - p)(x - q)$**
        Karena bilangan yang kita temukan adalah ${-p_val}$ dan ${-q_val}$, maka faktorisasinya adalah:
        $y = (x - {p_val})(x - {q_val})$
        Yang jika disederhanakan menjadi **$y = {faktorisasi_dict[kode][0]}$**
        """)
        
        if st.button("➡ Lanjut ke Langkah 6"):
            st.session_state.langkah = 6
            st.rerun()


# ---------------------------- LANGKAH 6 ----------------------------
if st.session_state.langkah >= 6:
    st.header("🟥 Langkah 6: Akar dari Dua Fungsi Lainnya")
    st.markdown("Masukkan akar-akar dari dua fungsi kuadrat yang belum kamu pilih.")
    for fungsi_sisa in st.session_state.fungsi_tersisa:
        st.latex(fungsi_latex[fungsi_sisa])
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input(f"x₁ untuk {fungsi_sisa}", key=f"x1_{fungsi_sisa}", step=1)
        with col2:
            x2 = st.number_input(f"x₂ untuk {fungsi_sisa}", key=f"x2_{fungsi_sisa}", step=1)

        if st.button(f"Cek Akar {fungsi_sisa}"):
            benar_x1 = faktorisasi_dict[fungsi_sisa][1]
            benar_x2 = faktorisasi_dict[fungsi_sisa][2]
            if sorted([x1, x2]) == sorted([benar_x1, benar_x2]):
                st.success(f"✅ Akar-akarnya benar untuk {fungsi_sisa}!")
            else:
                st.session_state.salah_input_x1x2 += 1
                st.error("❌ Salah")
                if st.session_state.salah_input_x1x2 >= 3:
                    st.info(f"Hint: Gunakan $ {faktorisasi_dict[fungsi_sisa][0]} = 0 $, lalu cari nilai x.")
