stock_price = {
    "AAPL": 227.50,   # Apple
    "MSFT": 528.32,   # Microsoft
    "GOOGL": 312.45,  # Alphabet (Google)
    "AMZN": 245.80,   # Amazon
    "TSLA": 378.60,   # Tesla
    "META": 845.20,   # Meta
    "NVDA": 212.75,   # NVIDIA
    "NFLX": 1320.40   # Netflix
}

holdings = {}   # symbol -> number of shares

print("Available stocks:", ", ".join(stock_price))

while True:
    symbol = input("Enter stock symbol (or 'done' to finish): ").upper().strip()

    if symbol == "DONE":
        break

    if symbol not in stock_price:
        print(f"Sorry, {symbol} is not in the price list.")
        continue

    try:
        quantity = int(input("How many shares? "))
    except ValueError:
        print("Please enter a whole number.")
        continue

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        continue

    holdings[symbol] = holdings.get(symbol, 0) + quantity

print("\n--- Portfolio Summary ---")
total = 0
for symbol, shares in holdings.items():
    price = stock_price[symbol]
    value = price * shares
    total += value
    print(f"{symbol}: {shares} x ${price:.2f} = ${value:.2f}")

print(f"Total investment value: ${total:.2f}")