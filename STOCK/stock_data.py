import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from vnstock3 import Vnstock
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


def get_real_time_price(stock_code, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')  # Sử dụng datetime.now()
    stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
    try:
        df = stock_obj.quote.history(start='2000-01-01', end=date, interval="1D")
        if df.empty:
            print(f"No data available for {stock_code}")
            return json.dumps({
                'code': stock_code,
                'price': 'N/A',
                'change': 'N/A',
                'percent_change': 'N/A'
            })

        # Kiểm tra cột 'close' có tồn tại không
        if 'close' not in df.columns:
            print(f"'close' column not found in data for {stock_code}")
            return json.dumps({
                'code': stock_code,
                'price': 'N/A',
                'change': 'N/A',
                'percent_change': 'N/A'
            })

        # Lấy dữ liệu phiên đóng cửa gần nhất
        latest_data = df.iloc[-1]
        price = latest_data['close']

        # Tính thay đổi giá nếu có dữ liệu nhiều hơn 1 ngày
        if len(df) > 1:
            previous_price = df['close'].iloc[-2]
            change = price - previous_price
            percent_change = (change / previous_price) * 100
        else:
            change = 'N/A'
            percent_change = 'N/A'

        return json.dumps({
            'code': stock_code,
            'price': str(price * 1000) + " VND",
            'change': round(change, 2) if change != 'N/A' else 'N/A',
            'percent_change': round(percent_change, 2) if percent_change != 'N/A' else 'N/A'
        })

    except Exception as e:
        print(f"Exception occurred: {e}")
        return json.dumps({'error': str(e)})

def get_historical_data(stock_code):
    """
    Lấy dữ liệu lịch sử chứng khoán trong 7 ngày gần nhất.
    """
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
        data = stock_obj.quote.history(start=start_date, end=end_date, interval="1D")
        return {
            'code': stock_code,
            'start': start_date,
            'end': end_date,
            'count': len(data),
            'data_preview': data.head().to_dict('records')  # Thêm một số dữ liệu mẫu để kiểm tra
        }
    except Exception as e:
        return {'error': str(e)}

def predict_trend(stock_code):
    try:
        enddate = datetime.now().strftime('%Y-%m-%d')
        stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
        data = stock_obj.quote.history(start='2023-01-01', end=enddate, interval="1D")
        print(data)
        X = np.arange(len(data)).reshape(-1, 1)
        y = data['close'].values
        model = LinearRegression()
        model.fit(X, y)
        future_days = np.arange(len(X), len(X) + 5).reshape(-1, 1)
        predicted_prices = model.predict(future_days)
        return {
            'code': stock_code,
            'current_price': y[-1],
            'predicted_prices': predicted_prices.tolist(),  # Chuyển đổi thành danh sách để dễ đọc
            'trend': 'up' if predicted_prices[-1] > y[-1] else 'down'
        }
    except Exception as e:
        return {'error': str(e)}


def train_model(stock_code):
    try:
        stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
        enddate = datetime.now().strftime('%Y-%m-%d')
        data = stock_obj.quote.history(start='2023-01-01', end=enddate, interval="1D")
        if len(data) < 100:
            raise ValueError("not enough data to train model")
        data = data.tail(100)
        X = np.arange(len(data) - 1).reshape(-1, 1)  # Các chỉ số ngày từ 0 đến 28
        y = data['close'].values[1:]  # Giá đóng cửa từ ngày thứ 2 đến ngày cuối
        X_train = X  # Tập huấn luyện là tất cả dữ liệu hiện có
        y_train = y  # Giá mục tiêu là giá đóng cửa ngày hôm sau

        model = LinearRegression()
        model.fit(X_train, y_train)
        return model
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None


def predict_trend_with_model(stock_code):
    """
    Dự đoán giá của phiên giao dịch tiếp theo dựa trên mô hình hồi quy tuyến tính đã huấn luyện với 30 ngày dữ liệu gần nhất.
    """
    model = train_model(stock_code)
    if model is None:
        return {'error': 'not enough data to train model.'}
    try:
        stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
        enddate = datetime.now().strftime('%Y-%m-%d')
        data = stock_obj.quote.history(start='2023-01-01', end=enddate, interval="1D")
        if len(data) < 100:
            return {'error': 'not enough data to train model.'}
        last_30_days = data.tail(100)
        current_price = last_30_days['close'].values[-1]
        X = np.arange(len(last_30_days)).reshape(-1, 1)
        latest_index = len(last_30_days)
        future_day = np.array([[latest_index]])  # Ngày tiếp theo để dự đoán
        predicted_price = model.predict(future_day)[0]
        return {
            'code': stock_code,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'trend': 'up' if predicted_price > current_price else 'down'
        }
    except Exception as e:
        return {'error': str(e)}


def plot_stock_prices(stock_code):
    try:
        # Lấy dữ liệu chứng khoán
        enddate = datetime.now().strftime('%Y-%m-%d')
        stock_obj = Vnstock().stock(symbol=stock_code.upper(), source="VCI")
        data = stock_obj.quote.history(start='2023-01-01', end=enddate, interval="1D")
        if data.empty:
            raise ValueError("Không có dữ liệu để vẽ biểu đồ.")
        # Tạo các chỉ số (MA20, MA50)
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA50'] = data['close'].rolling(window=50).mean()
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(14, 8))
        # Vẽ biểu đồ đường giá
        ax.plot(data.index, data['close'], label='Giá đóng cửa', color='blue', alpha=0.7)

        # Vẽ đường MA20 và MA50
        ax.plot(data.index, data['MA20'], label='MA20', color='orange', linestyle='--')
        ax.plot(data.index, data['MA50'], label='MA50', color='green', linestyle='--')

        # Thiết lập định dạng ngày
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Thêm các chú thích và các yếu tố khác
        ax.set_title(f'Biểu đồ giá chứng khoán {stock_code}')
        ax.set_xlabel('Ngày')
        ax.set_ylabel('Giá')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        # Tạo thư mục nếu chưa tồn tại
        output_dir = "D:/CODING/StockVietNam/.venv/stock_chart"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = os.path.join(output_dir, f"{stock_code}_stock_chart.png")
        plt.savefig(file_path)
        plt.show()
        #plt.close()  
        
        plt.show()
    except Exception as e:
        print(f"Error: {e}")





print(get_real_time_price('SHP'))  # Lấy giá của mã chứng khoán VIC vào ngày 3 tháng 9 năm 2024

print(get_historical_data('VIC'))

if __name__ == "__main__":
    stock_code = "SHP"  # Ví dụ mã chứng khoán
    result = predict_trend_with_model(stock_code)
    print(result)

predict_trend('SHP')
