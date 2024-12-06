import re
import random
import nltk
import json
import yaml
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
import pandas as pd

class EnhancedNLPProcessor:
    def __init__(self, config_file='D:/CODING/StockVietNam/.venv/NLP/nlp_config.yaml'):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()

        with open(config_file, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)

        self.supported_languages = self.config['languages']

    def detect_language(self, text):
        try:
            lang = detect(text)
            return lang if lang in self.supported_languages else 'english'
        except:
            return 'english'

    def preprocess_text(self, text, language):
        text = text.lower()
        tokens = word_tokenize(text)

        # Xử lý slang
        slang_dict = self.config['slang'].get(language, {})
        tokens = [slang_dict.get(token, token) for token in tokens]

        # Loại bỏ stop words và lemmatize
        if language == 'english':
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]

        return tokens

    def extract_stock_code(self, text):
        match = re.search(r'\b[A-Z]{2,5}\b', text)
        return match.group(0) if match else None

    def extract_date(self, text):
        date = re.search(r'\d{2}-\d{2}-\d{4}', text)
        return date.group(0) if date else None

    def analyze_sentiment(self, tokens, language):
        positive = set(self.config['sentiment_analysis']['positive'][language])
        negative = set(self.config['sentiment_analysis']['negative'][language])
        neutral = set(self.config['sentiment_analysis']['neutral'][language])

        sentiment_score = sum((1 if token in positive else -1 if token in negative else 0) for token in tokens)

        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        else:
            return 'neutral'

    def parse_user_input(self, user_input):
        # Xác định ngôn ngữ
        language = self.detect_language(user_input)

        # Tiền xử lý văn bản
        tokens = self.preprocess_text(user_input, language)
        sentiment = self.analyze_sentiment(tokens, language)

        # Trích xuất thông tin từ đầu vào
        stock_code = self.extract_stock_code(user_input)
        date = self.extract_date(user_input)

        # Ghi log đầu vào để kiểm tra
        print(f"User input: {user_input}")
        print(f"Tokens: {tokens}")
        print(f"Language: {language}")
        print(f"Sentiment: {sentiment}")
        print(f"Stock code: {stock_code}")
        print(f"Date: {date}")

        # Định nghĩa từ khóa và các lệnh
        keywords = self.config['keywords']

        # Xử lý các lệnh chào hỏi
        if any(word in tokens for word in keywords['greeting'][language]):
            return ("greeting", language, sentiment)

        # Xử lý các lệnh tạm biệt
        elif any(word in tokens for word in keywords['farewell'][language]):
            return ("farewell", language, sentiment)

        # Xử lý các lệnh liên quan đến thông tin chứng khoán
        elif any(word in tokens for word in keywords['stock_info'][language]):
            if "price" in tokens or "current" in tokens:
                return ("real_time_price", stock_code, date, language, sentiment)
            elif "history" in tokens:
                return ("historical_data", stock_code, language, sentiment)
            elif "trend" in tokens or "predict" in tokens:
                return ("predict_trend", stock_code, language, sentiment)
            elif "chart" in tokens or "graph" in tokens or "dmm" in tokens:
                return ("stock_chart", stock_code, language, sentiment)

        # Lệnh không xác định
        return ("unknown_command", language, sentiment)

    def generate_response(self, command, *args):
        language = args[-2] if len(args) >= 2 else 'english'
        sentiment = args[-1] if args else 'neutral'
        print(f"Command: {command}")
        if command in ['greeting', 'farewell', 'unknown']:
            responses = self.config['responses'][command][language]
            return random.choice(responses)
        try:
            data_dict = json.loads(args[0]) if isinstance(args[0], str) else args[0]
        except (json.JSONDecodeError, TypeError, IndexError):
            return self.config['responses']['unknown'][language][0]
        if command == "real_time_price":
            templates = self.config['templates']['real_time_price'][language]
            template = random.choice(templates)
            price = data_dict.get('price', 'N/A')
            change = data_dict.get('change', 'N/A')
            percent_change = data_dict.get('percent_change', 'N/A')
            code = data_dict.get('code', 'N/A')
            try:
                change_value = float(change.replace(' VND', '').replace(',', '')) if isinstance(change, str) else change
                percent_change_value = float(percent_change.replace('%', '').replace(',', '')) if isinstance(
                    percent_change, str) else percent_change
                trend = random.choice(self.config['trends']['up' if change_value > 0 else 'down'][language])
            except ValueError:
                change_value = 'N/A'
                percent_change_value = 'N/A'
                trend = random.choice(self.config['trends']['no_change'][language])
            response = template.format(code=code, price=price, change=change_value, percent_change=percent_change_value,
                                       trend=trend)

        elif command == "historical_data":
            templates = self.config['templates']['historical_data'][language]
            template = random.choice(templates)
            code = data_dict.get('code', 'N/A')
            start = data_dict.get('start', 'N/A')
            end = data_dict.get('end', 'N/A')
            count = data_dict.get('count', '0')
            if 'data_preview_format' not in self.config or language not in self.config['data_preview_format']:
                data_preview_format = "{date} | Open: {open}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}"
            else:
                data_preview_format = self.config['data_preview_format'][language][0]

            data_preview_list = data_dict.get('data_preview', [])

            data_preview = ""
            for data in data_preview_list:
                try:
                    date = data['time'].strftime('%Y-%m-%d') if isinstance(data['time'], pd.Timestamp) else 'N/A'
                    open_price = float(data['open']) if isinstance(data['open'], (float, int)) else 'N/A'
                    high_price = float(data['high']) if isinstance(data['high'], (float, int)) else 'N/A'
                    low_price = float(data['low']) if isinstance(data['low'], (float, int)) else 'N/A'
                    close_price = float(data['close']) if isinstance(data['close'], (float, int)) else 'N/A'
                    volume = int(data['volume']) if isinstance(data['volume'], (int, float)) else 'N/A'

                    data_preview += data_preview_format.format(
                        date=date,
                        open=open_price,
                        high=high_price,
                        low=low_price,
                        close=close_price,
                        volume=volume
                    ) + "\n"
                except (ValueError, KeyError):
                    continue

            response = template.format(
                code=code,
                start=start,
                end=end,
                count=count,
                data_preview=data_preview.strip()
            )

        elif command == "predict_trend":
            templates = self.config['templates']['predict_trend'][language]
            template = random.choice(templates)

            current_price = str(data_dict.get('current_price', 'N/A'))
            predicted_prices = data_dict.get('predicted_prices', [0])
            predicted_price = predicted_prices[-1] if predicted_prices else 0

            try:
                current_price_value = float(current_price.replace(',', '')) if isinstance(current_price,
                                                                                          str) else current_price
                trend = random.choice(
                    self.config['trends']['up' if predicted_price > current_price_value else 'down'][language])
            except ValueError:
                trend = random.choice(self.config['trends']['no_change'][language])

            response = template.format(code=data_dict.get('code', 'N/A'),
                                       trend=trend,
                                       current_price=current_price,
                                       predicted_price=predicted_price)
        elif command == "stock_chart":
            # Lấy templates từ config
            templates = self.config['templates']['stock_chart'][language]

            # Chọn template ngẫu nhiên
            template = random.choice(templates)

            # Lấy dữ liệu từ data_dict
            code = data_dict.get('code', 'N/A')
            start_date = data_dict.get('start', 'N/A')
            end_date = data_dict.get('end', 'N/A')

            # Format lại các biến và tạo phản hồi
            if code != 'N/A':
                print(f"Code: {code}, Start: {start_date}, End: {end_date}")

                try:
                    # Sử dụng template đã chọn để tạo phản hồi
                    response = template.format(code=code, start=start_date, end=end_date)
                    print(f"Response: {response}")  # Debug in ra phản hồi
                except KeyError as e:
                    print(f"Error formatting template: {e}")
                    return "Error in formatting template."
            else:
                response = "Invalid stock code provided."

            return response  # Trả về câu trả lời cuối cùng

        else:
            return self.config['responses']['unknown'][language][0]
        #emoji = random.choice(self.config['emojis'][sentiment])
        interjection = random.choice(self.config['interjections'][language])

        return f"{interjection} {response}"

    def find_similar_response(self, user_input, language):
        all_responses = [item for sublist in self.config['responses'].values() for item in sublist[language]]
        vectorized_responses = self.vectorizer.fit_transform(all_responses + [user_input])
        similarities = cosine_similarity(vectorized_responses[-1], vectorized_responses[:-1])
        most_similar_index = similarities.argmax()
        return all_responses[most_similar_index]

    def process_input(self, user_input):
        command = self.parse_user_input(user_input)
        if command[0] == "unknown_command":
            return self.find_similar_response(user_input, command[1])
        return self.generate_response(*command)