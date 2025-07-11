def f(x):
    return x**2 + 2*x + 1

print("📘 SELAMAT DATANG DI KALKULATOR FUNGSI INTERAKTIF!\n")
print("Bagian 1: Mencoba nilai x sebanyak 3 kali\n")

percobaan = 0
nilai_x_sebelumnya = []

while percobaan < 3:
    try:
        x = int(input("Masukkan nilai x (1–10): "))
        if x < 1 or x > 10:
            print("❌ Nilai x harus antara 1 hingga 10.\n")
            continue
    except ValueError:
        print("❌ Input harus berupa angka antara 1 sampai 10. Coba lagi.\n")
        continue

    print(f"\n📘 Langkah-langkah mencari f(x) = x² + 2x + 1")
    print(f"Langkah 1: Hitung x² = {x}² = {x**2}")
    print(f"Langkah 2: Hitung 2x = 2 × {x} = {2*x}")
    print(f"Langkah 3: Tambahkan semuanya: {x**2} + {2*x} + 1 = {f(x)}")
    print(f"✅ Maka f({x}) = {f(x)}\n")

    nilai_x_sebelumnya.append(x)
    percobaan += 1

    if percobaan < 3:
        while True:
            lanjut = input("🔁 Ingin mencoba nilai x lain? (ya/tidak): ").lower()
            if lanjut == "ya":
                break
            elif lanjut == "tidak":
                percobaan = 3
                break
            else:
                print("⚠️ Jawaban hanya boleh 'ya' atau 'tidak'. Coba lagi.")
    else:
        print("⚠️ Maaf, cuma bisa 3 kali saja 😊\n")




print("📗 Bagian 2: Coba hitung sendiri, pakai nilai x yang belum pernah!\n")

kesempatan = 0

while True:
    try:
        x2 = int(input("Sekarang masukkan nilai x baru (1–10), tidak boleh sama seperti sebelumnya: "))
        if x2 < 1 or x2 > 10:
            print("❌ Nilai x harus antara 1 hingga 10.\n")
            continue
        if x2 in nilai_x_sebelumnya:
            print("⚠️ Nilai x ini sudah digunakan sebelumnya. Coba nilai x lain ya.\n")
            continue
    except ValueError:
        print("❌ Input harus berupa angka. Coba lagi.\n")
        continue
    break  # valid


while kesempatan < 3:
    try:
        jawaban_siswa = int(input(f"Coba hitung sendiri dulu, berapa hasil f({x2}) = {x2}² + 2×{x2} + 1 ? "))
        if jawaban_siswa == f(x2):
            print("✅ Jawabanmu benar! Kamu luar biasa.\n")
            break
        else:
            kesempatan += 1
            sisa = 3 - kesempatan
            if sisa > 0:
                print(f"❌ Masih belum tepat. Coba lagi ya. ({sisa} kesempatan lagi)\n")
    except ValueError:
        print("❌ Jawaban harus berupa angka. Coba lagi ya.\n")

if kesempatan == 3:
    print("\n🔍 Yuk kita coba bareng, tapi kamu yang hitung ya:")

    while True:
        try:
            kuadrat = int(input(f"Langkah 1: Berapa {x2}² = "))
            if kuadrat != x2**2:
                print("❌ Coba cek lagi kuadratnya.")
                continue
            break
        except ValueError:
            print("❌ Harus angka. Coba lagi.")

    while True:
        try:
            kali_dua = int(input(f"Langkah 2: Berapa 2 × {x2} = "))
            if kali_dua != 2 * x2:
                print("❌ Masih belum tepat. Coba lagi.")
                continue
            break
        except ValueError:
            print("❌ Harus angka. Coba lagi.")

    while True:
        try:
            total = int(input(f"Langkah 3: Berapa {kuadrat} + {kali_dua} + 1 = "))
            if total == f(x2):
                print(f"✅ Betul! Maka f({x2}) = {total}\n")
                break
            else:
                print("❌ Belum pas. Hitung lagi ya.")
        except ValueError:
            print("❌ Harus angka. Coba lagi.")

print("📊 Bagian 3: Visualisasi Grafik f(x) = x² + 2x + 1\n")

import matplotlib.pyplot as plt

x_vals = list(range(1, 11))
y_vals = [f(x) for x in x_vals]

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, marker='o', color='blue', linewidth=2)
plt.title('Grafik Fungsi f(x) = x² + 2x + 1')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.ylim(0, max(y_vals) + 5)
plt.grid(True)
plt.tight_layout()
plt.show()
