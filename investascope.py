import pandas as pd
import datetime
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import sys
import argparse
import os
import io
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
key = config['Credentials']['key']


def get_mmddyyyy_format(day):
    formatted_date = day.strftime("%m%d%Y")
    formatted_date = formatted_date[:2] + '-' + formatted_date[2:4] + '-' + formatted_date[4:]
    return formatted_date

def check_csv_file(value):
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid file.")
    if not value.endswith('.csv'):
        raise argparse.ArgumentTypeError("Input file must be a CSV file.")
    return value

def preprocess_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Skip the first 5 lines
    cleaned_lines = lines[5:]

    # Find and exclude the problematic paragraph at the end
    end_paragraph_index = next((i for i, line in enumerate(cleaned_lines) if line.startswith('"The data')), len(cleaned_lines))
    cleaned_lines = cleaned_lines[:end_paragraph_index]

    # Join the cleaned lines into a single string
    cleaned_content = ''.join(cleaned_lines)

    return cleaned_content

parser = argparse.ArgumentParser(description="Process investment data from a CSV file.")
    
parser.add_argument("-f", "--csv_file", type=check_csv_file, help="Input CSV file containing investment data")
parser.add_argument("-c", "--investment_company", required=True, help="Name of the investment company")
parser.add_argument("-g", "--growth_type", choices=["money", "percentage"], required=True, help="Type of growth: money or percentage")
parser.add_argument("-d", "--include_dividend", action="store_true", help="Include dividends in calculations")

def main():

    args = parser.parse_args()

    file = args.csv_file

    api_key = key
    ts = TimeSeries(key=api_key, output_format='pandas')

    cleaned_content = preprocess_csv(file)

    # Now you can parse the cleaned content using Pandas
    df = pd.read_csv(io.StringIO(cleaned_content))
    print(df)
    df['date'] = pd.to_datetime(df['Settlement Date'])
    start_date = df['date'].min().date().strftime('%Y-%m-%d')
    start_date_formatted = get_mmddyyyy_format(df['date'].min().date())
    end_date = df['date'].max().date().strftime('%Y-%m-%d')


    unique_symbols = df['Symbol'].unique()
    unique_symbols = [symbol.strip() for symbol in unique_symbols if not symbol.strip().isdigit() and symbol.strip() != '']

    dfs = {s: None for s in unique_symbols}


    for symbol in unique_symbols:
        # Get historical price data for the symbol from AlphaVantage
        print(symbol)
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        
        # Only keep the 'close' column and reset the index to have 'date' as a column
        data = data['4. close'].reset_index()
        data.columns = ['date', 'Close']
        data['Symbol'] = symbol
        
        # Append the data for the current symbol to the stock_data DataFrame
        buy_data = df[df['Action'].str.contains('YOU BOUGHT')]

        buy_data = buy_data[buy_data['Symbol'].str.strip() == symbol]
        buy_data.sort_values(by='date', ascending=True, inplace=True)
        data.sort_values(by='date', ascending=True, inplace=True)

        
        # Step 1: Calculate the cumulative sum of 'Amount ($)'
        buy_data['Total Amount'] = -buy_data['Amount ($)'].cumsum()
        buy_data['Total Quantity'] = buy_data['Quantity'].cumsum()

        # Step 2: Merge the DataFrames on 'Date' column
        merged_df = pd.merge(data, buy_data, on=['date'], how='left')
        # Step 3: Fill NaN values in the 'Total Amount' column with the value of the previous day
        merged_df['Total Amount'].fillna(method='ffill', inplace=True)
        merged_df['Total Quantity'].fillna(method='ffill', inplace=True)

        print(merged_df)
    
        # Print the merged DataFrame
        
        filtered_df = merged_df[(merged_df['date'] >= start_date) & (merged_df['date'] <= end_date)]

        filtered_df['cost'] = filtered_df['Total Quantity'] * filtered_df['Close']
        #print(filtered_df.columns)
        dfs[symbol] = filtered_df[['date', 'Total Amount', 'Symbol_x', 'cost']]


    combined_df = pd.concat(dfs.values(), ignore_index=True)

    final_df = combined_df.groupby('date').agg({'Total Amount': 'sum', 'cost': 'sum'}).reset_index()

    final_df['ROI'] = (final_df['cost']/final_df['Total Amount'] - 1) * 100

    print(final_df)

    plt.figure(figsize=(12, 6))
    plt.plot(final_df['date'], final_df['ROI'])
    plt.xlabel('Date')
    plt.ylabel('Percent Change')
    plt.title(f'Portfolio Percent Change, {start_date_formatted} to {get_mmddyyyy_format(datetime.datetime.now())}')
    plt.grid()
    plt.savefig(f"inv_{get_mmddyyyy_format(datetime.datetime.now())}.png")

if __name__=="__main__":
    main()

