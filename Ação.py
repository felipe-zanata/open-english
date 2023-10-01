import yfinance as yf

# Defina o ticker da ação que você deseja obter o preço
ticker = "VIIA3.SA"  # Exemplo: Microsoft (MSFT)

# Use a função 'download' para obter os dados da ação
data = yf.download(tickers=ticker, period="1d")

# O preço da ação estará disponível na coluna 'Close' do DataFrame 'data'
preco_atual = data["Close"].iloc[-1]

print(f"Preço atual da ação {ticker}: R$ {preco_atual:.2f}")
