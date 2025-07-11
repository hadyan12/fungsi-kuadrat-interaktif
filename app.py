import streamlit as st
import matplotlib.pyplot as plt

def f(x):
    return x**2 + 2*x + 1

st.set_page_config(page_title="Belajar Fungsi Kuadrat", page_icon="🎓")
st.title("🎓 Interaktif Belajar Fungsi Kuadrat: f(x) = x² + 2x + 1")

# Inisialisasi session_state
for key in ["step1_done", "step2_done"]:
    if key not in st.session_state:
        st.session_state[key] = False

# STEP 1
with st.expander("📘 Langkah 1: Eksplorasi Fungsi", expanded=not st.session_state["step1_done"]):
    st.markdown("Masukkan nilai x (1–10) dan lihat cara kerja fungsi.")
    x = st.number_input("Nilai x:", min_value=1, max_value=10, step=1)

    if st.button("Lihat Langkah-langkah"):
        st.markdown(f"""
        - x² = {x}² = {x**2}  
        - 2x = 2 × {x} = {2*x}  
        - Jumlah: {x**2} + {2*x} + 1 = {f(x)}  
        ✅ Maka f({x}) = **{f(x)}**
        """)
        st.session_state["step1_done"] = True

# STEP 2
if st.session_state["step1_done"]:
    with st.expander("📗 Langkah 2: Uji Pemahaman", expanded=not st.session_state["step2_done"]):
        x2 = st.number_input("Masukkan nilai x baru:", min_value=1, max_value=10, step=1, key="x2")
        jawaban = st.number_input(f"Hitung sendiri dulu: f({x2}) = {x2}² + 2×{x2} + 1 = ... ?", step=1, key="jawaban")

        if st.button("Cek Jawaban"):
            if jawaban == f(x2):
                st.success("✅ Jawabanmu benar!")
            else:
                st.error(f"❌ Belum tepat. Jawaban yang benar adalah {f(x2)}.")
            st.session_state["step2_done"] = True

# STEP 3
if st.session_state["step2_done"]:
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
