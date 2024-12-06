# Ví dụ áp dụng Hồi quy Tuyến tính cho dữ liệu chứng khoán

Giả sử chúng ta có dữ liệu giá đóng cửa của mã chứng khoán VNM (Vinamilk) trong 10 ngày giao dịch gần đây nhất:

| Ngày | Giá đóng cửa (nghìn đồng) |
|------|---------------------------|
| 1    | 70.5                      |
| 2    | 71.2                      |
| 3    | 70.8                      |
| 4    | 71.5                      |
| 5    | 72.0                      |
| 6    | 71.8                      |
| 7    | 72.5                      |
| 8    | 73.0                      |
| 9    | 72.8                      |
| 10   | 73.5                      |

## Bước 1: Chuẩn bị dữ liệu

- X (biến độc lập): Số thứ tự ngày (1, 2, 3, ..., 10)
- y (biến phụ thuộc): Giá đóng cửa tương ứng

## Bước 2: Tính toán các giá trị cần thiết

1. Số lượng dữ liệu: n = 10
2. Tổng X: ΣX = 55
3. Tổng y: Σy = 719.6
4. Tổng X^2: ΣX^2 = 385
5. Tổng Xy: ΣXy = 4009.1

## Bước 3: Áp dụng công thức hồi quy tuyến tính

Công thức: y = β₀ + β₁x

Trong đó:
- β₁ = (n * ΣXy - ΣX * Σy) / (n * ΣX^2 - (ΣX)^2)
- β₀ = (Σy - β₁ * ΣX) / n

Thay số:

β₁ = (10 * 4009.1 - 55 * 719.6) / (10 * 385 - 55^2)
   = (40091 - 39578) / (3850 - 3025)
   = 513 / 825
   ≈ 0.3218

β₀ = (719.6 - 0.3218 * 55) / 10
   = (719.6 - 17.699) / 10
   ≈ 70.1901

Vậy, phương trình hồi quy tuyến tính của chúng ta là:

y = 70.1901 + 0.3218x

## Bước 4: Diễn giải kết quả

- β₀ (hệ số chặn) ≈ 70.1901: Đây là giá dự đoán khi x = 0 (tuy nhiên, trong trường hợp này, x = 0 không có ý nghĩa thực tế vì ngày bắt đầu từ 1).
- β₁ (độ dốc) ≈ 0.3218: Điều này có nghĩa là, trung bình, giá cổ phiếu tăng khoảng 321.8 đồng mỗi ngày.

## Bước 5: Dự đoán

Giả sử chúng ta muốn dự đoán giá cho ngày thứ 11:

y = 70.1901 + 0.3218 * 11 ≈ 73.7299

Vậy, giá dự đoán cho ngày thứ 11 là khoảng 73,730 đồng.

## Bước 6: Xác định xu hướng

Vì β₁ > 0 (0.3218 > 0), chúng ta có thể kết luận rằng xu hướng của cổ phiếu là đi lên.

## Lưu ý

- Đây là một mô hình đơn giản hóa và chỉ dựa trên dữ liệu lịch sử giá.
- Trong thực tế, nhiều yếu tố khác cũng ảnh hưởng đến giá cổ phiếu (ví dụ: tin tức công ty, tình hình kinh tế vĩ mô, tâm lý thị trường).
- Mô hình này giả định một mối quan hệ tuyến tính, điều này có thể không luôn đúng trong thị trường chứng khoán thực tế.
- Luôn cần thận trọng khi sử dụng bất kỳ mô hình dự đoán nào trong đầu tư chứng khoán.
