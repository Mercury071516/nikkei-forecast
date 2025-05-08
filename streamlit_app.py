import os

os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/config.toml", "w") as f:
    f.write("""
[server]
port = $PORT
enableCORS = false
""")
import streamlit as st
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_cme_change_rate():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.investing.com/indices/japan-225-futures")
        time.sleep(5)
        price = driver.find_element(By.XPATH, '//*[@data-test="instrument-price-last"]').text
        change = driver.find_element(By.XPATH, '//*[@data-test="instrument-price-change"]').text
        current = float(price.replace(",", ""))
        delta = float(change.replace(",", "").replace("+", "").replace("−", "-"))
        previous = current - delta
        return (delta / previous) * 100
    except Exception as e:
        return f"取得失敗: {e}"
    finally:
        driver.quit()

def calc_last_change(ticker):
    df = ticker.history(period="7d")
    closes = df["Close"].dropna()
    if len(closes) >= 2:
        yest, today = closes.iloc[-2], closes.iloc[-1]
        return (today - yest) / yest * 100, yest
    return 0.0, 0.0

st.title("日経平均 終値予測アプリ")

if st.button("予測を実行"):
    nikkei = yf.Ticker("^N225")
    dow = yf.Ticker("^DJI")
    usd_jpy = yf.Ticker("JPY=X")

    nikkei_chg, nikkei_prev = calc_last_change(nikkei)
    dow_chg, _ = calc_last_change(dow)
    usd_chg, _ = calc_last_change(usd_jpy)
    cme_chg = get_cme_change_rate()

    weights = {"nikkei": 0.4, "cme": 0.3, "dow": 0.2, "usd_jpy": 0.1}
    avg_chg = (
        nikkei_chg * weights["nikkei"] +
        cme_chg * weights["cme"] +
        dow_chg * weights["dow"] +
        usd_chg * weights["usd_jpy"]
    )

    pred = nikkei_prev * (1 + avg_chg / 100)

    st.markdown("### 結果")
    st.write(f"日経平均変化率：{nikkei_chg:.2f}%")
    st.write(f"CME先物変化率：{cme_chg:.2f}%")
    st.write(f"NYダウ変化率：{dow_chg:.2f}%")
    st.write(f"ドル円変化率：{usd_chg:.2f}%")
    st.write(f"加重平均変化率：{avg_chg:.2f}%")
    st.success(f"予測終値：{pred:.2f} 円")
