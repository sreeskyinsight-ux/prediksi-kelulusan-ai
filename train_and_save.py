import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

print("[INFO] Menyiapkan dataset yang lebih kaya...")
# Menambah variasi data latihan (Jam Belajar, Jam Tidur)
X = np.array([
    [1.0, 3.0], [1.5, 4.0], [2.0, 3.5], [2.5, 5.0],  # Pola kurang/gagal
    [3.0, 6.0], [3.5, 5.5], [4.0, 7.0], [4.5, 6.5],  # Pola batas
    [5.0, 7.0], [6.0, 8.0], [7.0, 7.5], [8.0, 8.0]   # Pola sukses
], dtype=float)

# Label Keputusan: 0 = Gagal, 1 = Lulus
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], dtype=float)

print("[INFO] Membangun arsitektur model...")
model = Sequential([
    Dense(units=8, activation='relu', input_shape=[2]), # Menambah neuron agar lebih kompleks
    Dense(units=4, activation='relu'),
    Dense(units=1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("[INFO] Melatih model dengan data baru...")
model.fit(X, y, epochs=300, verbose=0)

# Menyimpan ulang model yang sudah diperbarui
model.save("model_kelulusan.h5")
print("🎉 Model AI versi lanjutan berhasil dilatih dan disimpan ke 'model_kelulusan.h5'!")