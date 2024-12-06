from NLP.nlp_processor import EnhancedNLPProcessor
from STOCK.stock_data import get_real_time_price, get_historical_data, predict_trend, plot_stock_prices
import sqlite3

nlp_processor = EnhancedNLPProcessor()

def process_query(user_input):
    command_info = nlp_processor.parse_user_input(user_input)
    print(f"Command info: {command_info}")  # In ra thông tin command_info để kiểm tra
    command = command_info[0]

    if command == "greeting" or command == "farewell":
        return nlp_processor.generate_response(command)

    elif command == "real_time_price":
        stock_code = command_info[1]
        date = command_info[2]
        if stock_code:
            real_time_data = get_real_time_price(stock_code, date)
            if real_time_data:
                return nlp_processor.generate_response(command, real_time_data)
            else:
                return "Unable to retrieve real-time price data."
        else:
            return "No valid stock code found."

    elif command == "historical_data":
        stock_code = command_info[1]  # Chỉ lấy stock_code
        if stock_code:
            historical_data = get_historical_data(stock_code)  # Gọi hàm với stock_code duy nhất
            if historical_data:
                return nlp_processor.generate_response(command, historical_data)
            else:
                return "Unable to retrieve historical data."
        else:
            return "Please provide a valid stock code."

    elif command == "predict_trend" or command == "predict_with_model":
        stock_code = command_info[1]
        if stock_code:
            trend_data = predict_trend(stock_code)
            if trend_data:
                return nlp_processor.generate_response(command, trend_data)
            else:
                return "Unable to predict trend."
        else:
            return "No valid stock code found."

    elif command == "stock_chart":
        stock_code = command_info[1]
        if stock_code:
            file_path = plot_stock_prices(stock_code)
            if file_path:
                return nlp_processor.generate_response(command, file_path)
            else:
                return "Complied."
        else:
            return "Complied."
    else:
        return "Invalid command."


def save_message_to_db(sender, message_content):
    conn = sqlite3.connect('D:\CODING\StockVietNam\.venv\database\chatbox.db')
    cursor = conn.cursor()

    # Lưu tin nhắn vào bảng messages
    cursor.execute('''
        INSERT INTO messages (sender, message_content)
        VALUES (?, ?)
    ''', (sender, message_content))

    # Commit thay đổi và đóng kết nối
    conn.commit()
    conn.close()

if __name__ == '__main__':
    while True:
        user_input = input("Your command: ")
        if "quit" in user_input:
            break
        response = process_query(user_input)
        print(f"Ruan mei: {response}")
        # Lưu tin nhắn của người dùng và phản hồi của chatbot vào cơ sở dữ liệu
        save_message_to_db("user", user_input)
        save_message_to_db("chatbot", response)