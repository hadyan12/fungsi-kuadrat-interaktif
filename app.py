import streamlit as st
import matplotlib.pyplot as plt

# Fungsi kuadrat
def f(x):
    return x**2 + 2*x + 1

st.set_page_config(page_title="Belajar Fungsi Kuadrat", page_icon="🎓")
st.title("🎓 Interaktif Belajar Fungsi Kuadrat: f(x) = x² + 2x + 1")

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

> 🧠 Belajar fungsi bukan sekadar mencari hasil — tapi memahami **proses di baliknya**. Ayo kita mulai eksplorasinya!
""")

st.header("📘 Bagian 1: Eksplorasi Fungsi")
percobaan = st.slider("Berapa kali kamu ingin mencoba nilai x?", 1, 3, 3)

nilai_x_sebelumnya = []

for i in range(percobaan):
    x = st.number_input(f"Masukkan nilai x ke-{i+1} (1–10):", min_value=1, max_value=10, key=f"x_{i}")
    if x in nilai_x_sebelumnya:
        st.warning("⚠️ Nilai ini sudah digunakan. Coba yang lain.")
        continue
    st.markdown(f"""
**Langkah-langkah mencari f(x) = x² + 2x + 1**  
- x² = {x}² = {x**2}  
- 2x = 2 × {x} = {2*x}  
- Jumlah: {x**2} + {2*x} + 1 = {f(x)}  
✅ Maka f({x}) = **{f(x)}**
""")
    nilai_x_sebelumnya.append(x)

st.header("📗 Bagian 2: Uji Pemahaman")
x2 = st.number_input("Coba masukkan nilai x baru (1–10), **berbeda dari sebelumnya**:", min_value=1, max_value=10, key="x2")

if x2 in nilai_x_sebelumnya:
    st.error("⚠️ Nilai x ini sudah digunakan sebelumnya. Coba yang lain.")
else:
    jawaban = st.number_input(f"Coba hitung sendiri: f({x2}) = {x2}² + 2×{x2} + 1 = ... ?", step=1, key="jawaban")

    if st.button("Cek Jawaban"):
        if jawaban == f(x2):
            st.success("✅ Jawabanmu benar! Kamu luar biasa.")
        else:
            st.error(f"❌ Jawabanmu belum tepat. Jawaban yang benar adalah {f(x2)}.")

    with st.expander("❓ Perlu bantuan langkah demi langkah? Klik di sini"):
        kuadrat = st.number_input(f"Langkah 1: Berapa {x2}² =", step=1, key="kuadrat")
        kali_dua = st.number_input(f"Langkah 2: Berapa 2 × {x2} =", step=1, key="kali_dua")
        total = st.number_input(f"Langkah 3: Berapa {kuadrat} + {kali_dua} + 1 =", step=1, key="total")

        if kuadrat == x2**2 and kali_dua == 2*x2 and total == f(x2):
            st.success(f"✅ Betul! Maka f({x2}) = {total}")
        else:
            st.info("📝 Pastikan setiap langkah sudah tepat ya!")

st.header("📊 Bagian 3: Grafik Fungsi")

x_vals = list(range(1, 11))
y_vals = [f(x) for x in x_vals]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_vals, y_vals, marker='o', color='blue', linewidth=2)
ax.set_title('Grafik Fungsi f(x) = x² + 2x + 1')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_ylim(0, max(y_vals) + 5)
ax.grid(True)
st.pyplot(fig)
