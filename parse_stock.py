import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Функция для закрытия всплывающих окон
def close_popups(driver):
    try:
        # Ищем и закрываем окно с политикой cookies
        cookies_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler'))
        )
        cookies_popup.click()
    except Exception as e:
        print(f"No cookies popup found or failed to close: {e}")

# Функция для парсинга страницы с помощью Selenium
def parse_page_selenium(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    companies = []
    rows = soup.select('.nasdaq-screener__table-body .nasdaq-screener__row')
    for row in rows:
        company_name = row.select_one('.nasdaq-screener__cell a').text.strip()
        companies.append(company_name)
    return companies

# Основная функция для парсинга всех страниц
def parse_all_pages(base_url, total_pages):
    companies = []
    driver = webdriver.Chrome()  # Убедитесь, что драйвер установлен и настроен
    driver.get(base_url)

    # Закрываем всплывающие окна, если они есть
    close_popups(driver)

    try:
        for page in range(1, total_pages + 1):
            print(f"Parsing page: {page}")
            companies.extend(parse_page_selenium(driver))

            # Переход на следующую страницу с использованием JavaScript
            next_button = driver.find_element(By.CSS_SELECTOR, 'button.pagination__next')
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)  # Добавляем паузу, чтобы страница успела обновиться и данные загрузились
            else:
                break

    finally:
        driver.quit()

    return companies

# URL для первой страницы
base_url = "https://www.nasdaq.com/market-activity/stocks/screener"

# Общее количество страниц
total_pages = 5

# Получаем данные
all_companies = parse_all_pages(base_url, total_pages)

# Сохраняем данные в файл
with open('nasdaq_companies.txt', 'w') as f:
    for company in all_companies:
        f.write(f"{company}\n")

print(f"Парсинг завершен. Найдено {len(all_companies)} компаний.")
