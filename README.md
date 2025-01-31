# Stock Assistant
This is a virtual assistant built with Python to query and predict stock prices using `vnstock3`. The assistant also supports natural language processing (NLP) to understand user commands.

## Features
- Query real-time stock prices
- Retrieve historical stock data
- Predict stock trends using machine learning models

## Installation
1. Clone this repository.
2. Install the dependencies:
```bash
pip install -r requirements.txt
```

# Example of Applying Linear Regression to Stock Data

Assume we have the closing prices of the VNM (Vinamilk) stock for the last 10 trading days:

| Day | Closing Price (thousand VND) |
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

## Step 1: Prepare Data

- X (independent variable): Sequential day numbers (1, 2, 3, ..., 10)
- y (dependent variable): Corresponding closing prices

## Step 2: Compute Necessary Values

1. Number of data points: n = 10
2. Sum of X: ΣX = 55
3. Sum of y: Σy = 719.6
4. Sum of X^2: ΣX^2 = 385
5. Sum of Xy: ΣXy = 4009.1

## Step 3: Apply Linear Regression Formula

Formula: y = β₀ + β₁x

Where:
- β₁ = (n * ΣXy - ΣX * Σy) / (n * ΣX^2 - (ΣX)^2)
- β₀ = (Σy - β₁ * ΣX) / n

Substituting values:

β₁ = (10 * 4009.1 - 55 * 719.6) / (10 * 385 - 55^2)
   = (40091 - 39578) / (3850 - 3025)
   = 513 / 825
   ≈ 0.3218

β₀ = (719.6 - 0.3218 * 55) / 10
   = (719.6 - 17.699) / 10
   ≈ 70.1901

Thus, the regression equation is:

y = 70.1901 + 0.3218x

## Step 4: Interpret Results

- β₀ (intercept) ≈ 70.1901: This is the predicted price when x = 0 (although in this case, x = 0 has no real-world meaning as days start from 1).
- β₁ (slope) ≈ 0.3218: This means that, on average, the stock price increases by approximately 321.8 VND per day.

## Step 5: Prediction

To predict the price for day 11:

y = 70.1901 + 0.3218 * 11 ≈ 73.7299

So, the predicted price for day 11 is approximately 73,730 VND.

## Step 6: Determine Trend

Since β₁ > 0 (0.3218 > 0), we conclude that the stock trend is upward.

## Notes

- This is a simplified model based solely on historical prices.
- In reality, many other factors influence stock prices (e.g., company news, macroeconomic conditions, market sentiment).
- This model assumes a linear relationship, which may not always hold in actual stock markets.
- Exercise caution when using any predictive model for stock investments.

---

## Detailed Explanation of `predict_trend` Function

The `predict_trend` function is designed to forecast the price trend of a given stock. Below is a breakdown of its working mechanism:

### Input:
- `stock_code`: The stock symbol to predict.

### Data Processing:
- Uses the `vnstock` library to fetch historical stock price data.
- Retrieves data from January 1, 2023, to the current date.
- Fetches data at a daily interval (`interval="1D"`).

### Preparing Data for the Model:
- `X`: An array of integers from 0 to the number of days in the dataset, representing time.
- `y`: An array of corresponding closing prices.

### Training the Model:
- Utilizes `LinearRegression` from `scikit-learn`.
- The model is trained with `X` as the independent variable and `y` as the dependent variable.

### Prediction:
- Generates an array `future_days` representing the next 5 days.
- Uses the trained model to predict prices for these 5 days.

### Output:
The function returns a dictionary containing:
- `code`: The stock symbol.
- `current_price`: The most recent closing price.
- `predicted_prices`: A list of predicted prices for the next 5 days.
- `trend`: The predicted trend ('up' if the last predicted price is higher than the current price, otherwise 'down').

### Exception Handling:
- If any error occurs during execution, the function returns a dictionary with an error message.

### Possible Enhancements:
- Utilize advanced models like ARIMA, LSTM.
- Incorporate technical indicators like RSI, MACD.
- Integrate sentiment analysis from news and social media.
- Apply cross-validation to assess model performance.
- Provide confidence intervals for predictions.

**Note:** Stock market forecasting is highly complex, and no model can predict prices with 100% accuracy.

