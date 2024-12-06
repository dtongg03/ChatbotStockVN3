import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

# Đọc dữ liệu
data = pd.read_csv("dataset/dialogs_expanded.csv")

# Kiểm tra cột trong dữ liệu
print(data.columns)

# Tiền xử lý (ví dụ: token hóa, padding)
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(data['question'])  # Sử dụng cột 'question' để token hóa
question_sequences = tokenizer.texts_to_sequences(data['question'])
answer_sequences = tokenizer.texts_to_sequences(data['answer'])

# Padding cho dữ liệu
question_padded = pad_sequences(question_sequences, maxlen=100)
answer_padded = pad_sequences(answer_sequences, maxlen=100)

# Xây dựng mô hình (ví dụ: LSTM)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Huấn luyện mô hình
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Sử dụng cột nhãn 'answer_len'
model.fit(question_padded, data['answer_len'], epochs=10)  # Thay đổi cột nhãn nếu cần

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists('models'):
    os.makedirs('models')

# Lưu mô hình
model.save("models/Ruanmei.h5")
