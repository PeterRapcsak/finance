import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import requests
from datetime import datetime, timedelta
import numpy as np

# Function to fetch initial data
def fetch_initial_data():
    # Fetch S&P 500 data
    sp500_data = fetch_stock_data("^GSPC")
    
    # Fetch NASDAQ data
    nasdaq_data = fetch_stock_data("^IXIC")
    
    # Fetch HUF-EUR conversion rates for the last 5 days
    huf_eur_rates = fetch_historical_currency_rates()
    
    return sp500_data, nasdaq_data, huf_eur_rates

# Function to fetch live stock data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    # Fetch data for the last 7 days to ensure we have enough data points
    hist = stock.history(period="71d", interval="1m")
    # Filter out weekends
    hist = hist[hist.index.dayofweek < 5]  # Keep only weekdays
    # Filter out non-trading hours
    hist = hist.between_time('09:30', '16:00')
    return hist

# Function to fetch HUF-EUR conversion rate for the last 5 days
def fetch_currency_rate():
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    data = response.json()
    return data['rates']['HUF']

# Function to fetch historical HUF-EUR conversion rates for the last 5 days
def fetch_historical_currency_rates():
    rates = []
    for i in range(5):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"https://api.exchangerate-api.com/v4/historical/EUR/{date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates.append(data['rates']['HUF'])
    return rates

# Function to update the GUI
def update_data():
    # Fetch S&P 500 data
    sp500_ax.clear()
    sp500_ax.plot(sp500_data.index, sp500_data['Close'], label="S&P 500", color='cyan')
    sp500_ax.set_title("S&P 500 Last 5 Days", color='white')
    sp500_ax.legend()
    sp500_ax.set_facecolor('#2E2E2E')  # Dark background for the plot
    sp500_ax.tick_params(axis='x', colors='white')
    sp500_ax.tick_params(axis='y', colors='white')
    sp500_ax.spines['bottom'].set_color('white')
    sp500_ax.spines['top'].set_color('white')
    sp500_ax.spines['left'].set_color('white')
    sp500_ax.spines['right'].set_color('white')

    # Fetch NASDAQ data
    nasdaq_ax.clear()
    nasdaq_ax.plot(nasdaq_data.index, nasdaq_data['Close'], label="NASDAQ", color='magenta')
    nasdaq_ax.set_title("NASDAQ Last 5 Days", color='white')
    nasdaq_ax.legend()
    nasdaq_ax.set_facecolor('#2E2E2E')  # Dark background for the plot
    nasdaq_ax.tick_params(axis='x', colors='white')
    nasdaq_ax.tick_params(axis='y', colors='white')
    nasdaq_ax.spines['bottom'].set_color('white')
    nasdaq_ax.spines['top'].set_color('white')
    nasdaq_ax.spines['left'].set_color('white')
    nasdaq_ax.spines['right'].set_color('white')

    # Fetch HUF-EUR conversion rate and update the graph
    huf_eur_ax.clear()
    huf_eur_ax.plot(huf_eur_rates, label="HUF-EUR", color='yellow')
    huf_eur_ax.set_title("HUF-EUR Conversion Last 5 Days", color='white')
    huf_eur_ax.legend()
    huf_eur_ax.set_facecolor('#2E2E2E')  # Dark background for the plot
    huf_eur_ax.tick_params(axis='x', colors='white')
    huf_eur_ax.tick_params(axis='y', colors='white')
    huf_eur_ax.spines['bottom'].set_color('white')
    huf_eur_ax.spines['top'].set_color('white')
    huf_eur_ax.spines['left'].set_color('white')
    huf_eur_ax.spines['right'].set_color('white')

    # Redraw the canvas
    canvas.draw()

    # Schedule the next update
    root.after(60000, update_data)  # Update every 60 seconds

# Fetch initial data before starting the application
sp500_data, nasdaq_data, huf_eur_rates = fetch_initial_data()

# Create the main window
root = tk.Tk()
root.title("Finance Tracker")
root.geometry("800x800")
root.configure(bg='#2E2E2E')  # Dark background for the app

# Create frames for the graphs
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create matplotlib figures and axes
fig, (sp500_ax, nasdaq_ax, huf_eur_ax) = plt.subplots(3, 1, figsize=(8, 8))
fig.tight_layout(pad=3.0)
fig.patch.set_facecolor('#2E2E2E')  # Dark background for the figure

# Embed the matplotlib figures in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initial data update
update_data()

# Run the application
root.mainloop()