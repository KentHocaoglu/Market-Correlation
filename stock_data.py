import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import seaborn as sns
import os


STARTTIME, ENDTIME = "2020-01-01", "2025-01-01"

def getStock(tickers:str) -> None:
# Take a stock id (ex. aapl) and pull stock information for the past 3 years 
# from yahoo finance
    stock_list = tickers.upper().split()
    data = yf.download(stock_list, STARTTIME, ENDTIME)
    returns = data['Close'].pct_change().dropna()

    os.makedirs("Plots", exist_ok=True)
    for ticker in stock_list:
        stock_returns = returns[ticker]
        mean = stock_returns.mean()
        std = stock_returns.std()

        print(f"\n{ticker.upper()} stats:")
        print(f"Mean daily return: {mean:.5f}")
        print(f"Standard deviation: {std:.5f}")
        plotStock(ticker, stock_returns, mean, std)

    evaluate_correlation(returns)

    
def evaluate_correlation(returns):
    # Evaluates the correlation between the given stock returns and plots it
    correlation_matrix = returns.corr()
    print("Correlation Matrix:\n")
    print(correlation_matrix)
    plotCorrelation(correlation_matrix)

def plotCorrelation(correlation_matrix):
    # Plots the correlation between the given stocks on a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='flare', fmt=".2f")
    plt.title("Correlation of Daily Returns")
    plt.tight_layout()
    plt.savefig("Plots/correlation_heatmap.png")
    plt.close()

def plotStock(ticker, stock_returns, mean, std):
    # Plots a normal distribution of the ticker given it's returns, mean, and std 
    # on a histogram and saves it to a png in a Plots folder
    plt.figure(figsize=(8, 5))
    plt.hist(stock_returns, bins=50, density=True, alpha=0.6, color='g', label='Stock Returns Histogram')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean, std)
    plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution Fit')

    plt.title(f'Normal Distribution of Daily Returns for {ticker}')
    plt.xlabel('Daily Return')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    filename = f"Plots/{ticker}_returns_distribution.png"
    plt.savefig(filename)
    plt.close()

def run() -> None:
    print("Which stocks' information would you like?")
    getStock(input())


if __name__ == '__main__':
    run()