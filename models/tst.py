# import tensorflow as tf
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.preprocessing.text import Tokenizer
#
# import json
#
#
# class ModelTester:
#     def __init__(self):
#         # Tải mô hình đã lưu
#         self.model = tf.keras.models.load_model("D:/CODING/StockVietNam/.venv/models/Ruanmei.h5")
#
#         # Tải tokenizer nếu cần
#         self.tokenizer = self.load_tokenizer()
#
#     def load_tokenizer(self):
#         # Nếu bạn đã lưu tokenizer, tải nó ở đây
#         # Ví dụ: trả về một tokenizer đã lưu sẵn hoặc một cái mới nếu không có sẵn
#         # Đây là ví dụ và cần điều chỉnh theo cách bạn đã lưu tokenizer
#         return Tokenizer(num_words=10000)
#
#     def preprocess_input(self, text):
#         # Tiền xử lý văn bản đầu vào
#         sequence = self.tokenizer.texts_to_sequences([text])
#         padded_sequence = pad_sequences(sequence, maxlen=100)
#         return padded_sequence
#
#     def predict(self, text):
#         # Tiền xử lý dữ liệu đầu vào
#         processed_input = self.preprocess_input(text)
#
#         # Dự đoán
#         prediction = self.model.predict(processed_input)
#         return prediction
#
#     def test_model(self):
#         # Ví dụ văn bản đầu vào để kiểm tra mô hình
#         test_input = "What is the current price of AAPL?"
#         prediction = self.predict(test_input)
#
#         # Hiển thị kết quả dự đoán
#         print(f"Input: {test_input}")
#         print(f"Prediction: {prediction}")


import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


class ModelTester:
    def __init__(self):
        # Load the trained model
        self.model = tf.keras.models.load_model("D:/CODING/StockVietNam/.venv/models/Ruanmei.h5")
        # Initialize the tokenizer
        self.tokenizer = Tokenizer(num_words=10000)
        # Example class labels - replace with your actual labels
        self.class_labels = ["Class A", "Class B", "Class C"]  # Update according to your model

    def preprocess_input(self, input_text):
        sequences = self.tokenizer.texts_to_sequences([input_text])
        padded_sequences = pad_sequences(sequences, maxlen=100)
        return padded_sequences

    def predict(self, input_text):
        processed_input = self.preprocess_input(input_text)
        prediction = self.model.predict(processed_input)
        return prediction

    def interpret_prediction(self, prediction):
        # Assuming this is a classification model
        class_index = np.argmax(prediction, axis=-1)[0]
        return self.class_labels[class_index]


if __name__ == "__main__":
    tester = ModelTester()
    test_input = "hello"
    prediction = tester.predict(test_input)
    predicted_label = tester.interpret_prediction(prediction)

    print(f"Input: {test_input}")
    print(f"Prediction: {prediction}")
    print(f"Predicted Label: {predicted_label}")



