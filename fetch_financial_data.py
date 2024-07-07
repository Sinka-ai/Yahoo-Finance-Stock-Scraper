import yfinance as yf
import pandas as pd
import requests


# Функция для получения логотипа компании
def get_company_logo(ticker):
    url = f"https://logo.clearbit.com/{ticker.lower()}.com"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        return None


# Функция для получения данных по компании
def get_company_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    dividends = stock.dividends
    next_dividend_date = info.get('exDividendDate', None)
    current_price = info.get('currentPrice', None)
    lot_size = info.get('regularMarketVolume', None)
    dividend_yield = info.get('dividendYield', None)

    # Рассчитываем дивидендную доходность
    if current_price and dividend_yield:
        dividend_to_price_ratio = dividend_yield * 100
    else:
        dividend_to_price_ratio = None

    # Собираем данные
    data = {
        'Логотип': get_company_logo(ticker),
        'Наименование компании': info.get('longName', None),
        'Тикер': ticker,
        'Экс-дивидендная дата': next_dividend_date,
        'Цена акции': current_price,
        'Размер лота': lot_size,
        'Сумма дивидендов на акцию': dividends.iloc[-1] if not dividends.empty else None,
        'Доходность дивидендов (%)': dividend_to_price_ratio
    }
    return data


# Чтение списка компаний из файла
with open('nasdaq_companies.txt', 'r') as f:
    companies = [line.strip() for line in f]

# Список для хранения данных
data_list = []

# Получение данных по каждой компании
for company in companies:
    try:
        print(f"Получение данных по {company}...")
        data = get_company_data(company)
        data_list.append(data)
    except Exception as e:
        print(f"Не удалось получить данные по {company}: {e}")

# Создание DataFrame из списка данных
df = pd.DataFrame(data_list)

# Сохранение данных в Excel файл
df.to_excel('nasdaq_companies_data.xlsx', index=False)

print("Получение данных завершено.")
