# Mô hình Hồi quy Tuyến tính (LinearRegression)

## Định nghĩa
Hồi quy Tuyến tính là một phương pháp thống kê được sử dụng để mô hình hóa mối quan hệ tuyến tính giữa một biến phụ thuộc (y) và một hoặc nhiều biến độc lập (x). Trong trường hợp đơn giản nhất, nó tìm cách khớp một đường thẳng với dữ liệu.

## Công thức
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε

Trong đó:
- y là biến phụ thuộc
- x₁, x₂, ..., xₙ là các biến độc lập
- β₀ là hệ số chặn (intercept)
- β₁, β₂, ..., βₙ là các hệ số hồi quy
- ε là sai số ngẫu nhiên

## Cách phân tích dữ liệu

1. **Thu thập dữ liệu**: 
   Trong trường hợp của hàm `predict_trend`, dữ liệu là giá đóng cửa hàng ngày của cổ phiếu.

2. **Chuẩn bị dữ liệu**: 
   - X (biến độc lập): Là số thứ tự của ngày (0, 1, 2, ...)
   - y (biến phụ thuộc): Là giá đóng cửa tương ứng

3. **Huấn luyện mô hình**: 
   Mô hình tìm các giá trị tối ưu cho β₀ và β₁ bằng cách tối thiểu hóa tổng bình phương sai số giữa giá trị dự đoán và giá trị thực tế.

4. **Phương pháp Bình phương Tối thiểu (Least Squares Method)**:
   - Tính toán đường thẳng "phù hợp nhất" bằng cách tối thiểu hóa tổng bình phương của các sai số (residuals).
   - Sai số là khoảng cách theo chiều dọc từ mỗi điểm dữ liệu đến đường hồi quy.

## Cách đưa ra kết quả

1. **Dự đoán**: 
   Sau khi đã tìm được β₀ và β₁, mô hình có thể dự đoán giá y cho bất kỳ giá trị x nào bằng cách áp dụng công thức: y = β₀ + β₁x

2. **Đánh giá mô hình**:
   - R-squared (R²): Đo lường mức độ biến thiên trong y được giải thích bởi x.
   - Mean Squared Error (MSE): Trung bình bình phương sai số giữa giá trị dự đoán và giá trị thực tế.

3. **Diễn giải kết quả**:
   - Hệ số β₁ cho biết mức độ thay đổi trung bình của y khi x tăng 1 đơn vị.
   - Dấu của β₁ chỉ ra hướng của mối quan hệ (dương là tăng, âm là giảm).

## Ứng dụng trong dự đoán xu hướng cổ phiếu

1. Mô hình học mối quan hệ giữa thời gian (X) và giá cổ phiếu (y).
2. Nếu β₁ > 0, xu hướng được coi là tăng; nếu β₁ < 0, xu hướng được coi là giảm.
3. Mô hình dự đoán giá cho các ngày trong tương lai bằng cách ngoại suy đường hồi quy.

## Ưu điểm và Hạn chế

**Ưu điểm**:
- Đơn giản, dễ hiểu và triển khai
- Hiệu quả tính toán cao
- Cung cấp các hệ số có thể diễn giải được

**Hạn chế**:
- Giả định mối quan hệ tuyến tính, có thể không phù hợp với nhiều dữ liệu tài chính phức tạp
- Nhạy cảm với outliers
- Không nắm bắt được các mối quan hệ phi tuyến tính hoặc các yếu tố khác ảnh hưởng đến giá cổ phiếu

Lưu ý: Trong thực tế, giá cổ phiếu thường bị ảnh hưởng bởi nhiều yếu tố phức tạp hơn, và mô hình hồi quy tuyến tính đơn giản này có thể không đủ để dự đoán chính xác xu hướng thị trường.
