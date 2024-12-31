#Import libraries

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pdfkit


app = Flask(__name__)

# 1 - User selections for portfolio stocks and weight percents

# List of S&P 500 symbols with company name and sector
stocks_info = [
    ("AAPL", "Apple Inc.", "Information Technology"), ("MSFT", "Microsoft Corporation", "Information Technology"), ("AMZN", "Amazon.com, Inc.", "Consumer Discretionary"),
    ("GOOGL", "Alphabet Inc. Class A", "Communication Services"), ("GOOG", "Alphabet Inc. Class C", "Communication Services"), ("META", "Meta Platforms, Inc.", "Communication Services"),
    ("BRKB", "Berkshire Hathaway Inc. Class B", "Financials"), ("TSLA", "Tesla Inc.", "Consumer Discretionary"), ("UNH", "UnitedHealth Group Inc.", "Health Care"),
    ("LLY", "Eli Lilly and Company", "Health Care"), ("JPM", "JPMorgan Chase & Co.", "Financials"), ("XOM", "Exxon Mobil Corporation", "Energy"),
    ("JNJ", "Johnson & Johnson", "Health Care"), ("V", "Visa Inc. Class A", "Financials"), ("PG", "Procter & Gamble", "Consumer Staples"),
    ("AVGO", "Broadcom Inc.", "Information Technology"), ("MA", "Mastercard Inc. Class A", "Financials"), ("HD", "Home Depot Inc.", "Consumer Discretionary"),
    ("CVX", "Chevron Corporation", "Energy"), ("MRK", "Merck & Co., Inc.", "Health Care"), ("ABBV", "AbbVie Inc.", "Health Care"),
    ("PEP", "PepsiCo Inc.", "Consumer Staples"), ("COST", "Costco Wholesale Corporation", "Consumer Staples"), ("ADBE", "Adobe Inc.", "Information Technology"),
    ("KO", "Coca-Cola", "Consumer Staples"), ("CSCO", "Cisco Systems, Inc.", "Information Technology"), ("WMT", "Walmart Inc.", "Consumer Staples"),
    ("TMO", "Thermo Fisher Scientific Inc.", "Health Care"), ("MCD", "McDonald's Corporation", "Consumer Discretionary"), ("PFE", "Pfizer Inc.", "Health Care"),
    ("CRM", "Salesforce, Inc.", "Information Technology"), ("BAC", "Bank of America Corporation", "Financials"), ("ACN", "Accenture Plc Class A", "Information Technology"),
    ("CMCSA", "Comcast Corporation Class A", "Communication Services"), ("LIN", "Linde Plc", "Materials"), ("NFLX", "Netflix, Inc.", "Communication Services"),
    ("ABT", "Abbott Laboratories", "Health Care"), ("ORCL", "Oracle Corporation", "Information Technology"), ("DHR", "Danaher Corporation", "Health Care"),
    ("AMD", "Advanced Micro Devices, Inc.", "Information Technology"), ("WFC", "Wells Fargo & Company", "Financials"), ("DIS", "The Walt Disney Company", "Communication Services"),
    ("TXN", "Texas Instruments Incorporated", "Information Technology"), ("PM", "Philip Morris International Inc.", "Consumer Staples"), ("VZ", "Verizon Communications Inc.", "Communication Services"),
    ("INTU", "Intuit Inc.", "Information Technology"), ("COP", "ConocoPhillips", "Energy"), ("CAT", "Caterpillar Inc.", "Industrials"),
    ("AMGN", "Amgen Inc.", "Health Care"), ("NEE", "NextEra Energy, Inc.", "Utilities"), ("INTC", "Intel Corporation", "Information Technology"),
    ("UNP", "Union Pacific Corporation", "Industrials"), ("LOW", "Lowe's Companies, Inc.", "Consumer Discretionary"), ("IBM", "International Business Machines Corporation", "Information Technology"),
    ("BMY", "Bristol-Myers Squibb Company", "Health Care"), ("SPGI", "S&P Global Inc.", "Financials"), ("RTX", "RTX Corporation", "Industrials"),
    ("HON", "Honeywell International Inc.", "Industrials"), ("BA", "The Boeing Company", "Industrials"), ("UPS", "United Parcel Service, Inc. Class B", "Industrials"),
    ("GE", "General Electric Company", "Industrials"), ("QCOM", "Qualcomm Incorporated", "Information Technology"), ("AMAT", "Applied Materials, Inc.", "Information Technology"),
    ("NKE", "NIKE, Inc. Class B", "Consumer Discretionary"), ("PLD", "Prologis, Inc. REIT", "Real Estate"), ("NOW", "ServiceNow, Inc.", "Information Technology"),
    ("BKNG", "Booking Holdings Inc.", "Consumer Discretionary"), ("SBUX", "Starbucks Corporation", "Consumer Discretionary"), ("MS", "Morgan Stanley", "Financials"),
    ("ELV", "Elevance Health, Inc.", "Health Care"), ("MDT", "Medtronic Plc", "Health Care"), ("GS", "The Goldman Sachs Group, Inc.", "Financials"),
    ("DE", "Deere & Company", "Industrials"), ("ADP", "Automatic Data Processing, Inc.", "Industrials"), ("LMT", "Lockheed Martin Corporation", "Industrials"),
    ("TJX", "The TJX Companies, Inc.", "Consumer Discretionary"), ("T", "AT&T Inc.", "Communication Services"), ("BLK", "BlackRock, Inc.", "Financials"),
    ("ISRG", "Intuitive Surgical, Inc.", "Health Care"), ("MDLZ", "Mondelez International, Inc. Class A", "Consumer Staples"), ("GILD", "Gilead Sciences, Inc.", "Health Care"),
    ("MMC", "Marsh & McLennan Companies, Inc.", "Financials"), ("AXP", "American Express Company", "Financials"), ("SYK", "Stryker Corporation", "Health Care"),
    ("REGN", "Regeneron Pharmaceuticals, Inc.", "Health Care"), ("VRTX", "Vertex Pharmaceuticals Incorporated", "Health Care"), ("ETN", "Eaton Corporation Plc", "Industrials"),
    ("LRCX", "Lam Research Corporation", "Information Technology"), ("ADI", "Analog Devices, Inc.", "Information Technology"), ("SCHW", "The Charles Schwab Corporation", "Financials"),
    ("CVS", "CVS Health Corporation", "Health Care"), ("ZTS", "Zoetis Inc. Class A", "Health Care"), ("CI", "Cigna Group", "Health Care"),
    ("CB", "Chubb Limited", "Financials"), ("AMT", "American Tower Corporation REIT", "Real Estate"), ("SLB", "Schlumberger N.V.", "Energy"),
    ("C", "Citigroup Inc.", "Financials"), ("BDX", "Becton, Dickinson and Company", "Health Care"), ("MO", "Altria Group, Inc.", "Consumer Staples"),
    ("PGR", "The Progressive Corporation", "Financials"), ("TMUS", "T-Mobile US, Inc.", "Communication Services"), ("FI", "Fiserv, Inc.", "Financials"),
    ("SO", "The Southern Company", "Utilities"), ("EOG", "EOG Resources, Inc.", "Energy"), ("BSX", "Boston Scientific Corporation", "Health Care"),
    ("CME", "CME Group Inc. Class A", "Financials"), ("EQIX", "Equinix, Inc. REIT", "Real Estate"), ("MU", "Micron Technology, Inc.", "Information Technology"),
    ("DUK", "Duke Energy Corporation", "Utilities"), ("PANW", "Palo Alto Networks, Inc.", "Information Technology"), ("PYPL", "PayPal Holdings, Inc.", "Financials"),
    ("AON", "Aon Plc Class A", "Financials"), ("SNPS", "Synopsys, Inc.", "Information Technology"), ("ITW", "Illinois Tool Works Inc.", "Industrials"),
    ("KLAC", "KLA Corporation", "Information Technology"), ("HUBB", "Hubbell Incorporated", "Industrials"), ("ICE", "Intercontinental Exchange, Inc.", "Financials"),
    ("APD", "Air Products and Chemicals, Inc.", "Materials"), ("SHW", "Sherwin-Williams Company", "Materials"), ("CDNS", "Cadence Design Systems, Inc.", "Information Technology"),
    ("CSX", "CSX Corporation", "Industrials"), ("NOC", "Northrop Grumman Corporation", "Industrials"), ("CL", "Colgate-Palmolive Company", "Consumer Staples"),
    ("MPC", "Marathon Petroleum Corporation", "Energy"), ("HUM", "Humana Inc.", "Health Care"), ("FDX", "FedEx Corporation", "Industrials"),
    ("WM", "Waste Management, Inc.", "Industrials"), ("MCK", "McKesson Corporation", "Health Care"), ("TGT", "Target Corporation", "Consumer Staples"),
    ("ORLY", "O'Reilly Automotive, Inc.", "Consumer Discretionary"), ("HCA", "HCA Healthcare, Inc.", "Health Care"), ("FCX", "Freeport-McMoRan Inc.", "Materials"),
    ("EMR", "Emerson Electric Co.", "Industrials"), ("PXD", "Pioneer Natural Resources Company", "Energy"), ("MMM", "3M Company", "Industrials"),
    ("MCO", "Moody's Corporation", "Financials"), ("ROP", "Roper Technologies, Inc.", "Information Technology"), ("CMG", "Chipotle Mexican Grill, Inc.", "Consumer Discretionary"),
    ("PSX", "Phillips 66", "Energy"), ("MAR", "Marriott International, Inc. Class A", "Consumer Discretionary"), ("PH", "Parker-Hannifin Corporation", "Industrials"),
    ("APH", "Amphenol Corporation Class A", "Information Technology"), ("GD", "General Dynamics Corporation", "Industrials"), ("USB", "U.S. Bancorp", "Financials"),
    ("NXPI", "NXP Semiconductors N.V.", "Information Technology"), ("AJG", "Arthur J. Gallagher & Co.", "Financials"), ("NSC", "Norfolk Southern Corporation", "Industrials"),
    ("PNC", "PNC Financial Services Group, Inc.", "Financials"), ("VLO", "Valero Energy Corporation", "Energy"), ("F", "Ford Motor Company", "Consumer Discretionary"),
    ("MSI", "Motorola Solutions, Inc.", "Information Technology"), ("GM", "General Motors Company", "Consumer Discretionary"), ("TT", "Trane Technologies plc", "Industrials"),
    ("EW", "Edwards Lifesciences Corporation", "Health Care"), ("CARR", "Carrier Global Corporation", "Industrials"), ("AZO", "AutoZone, Inc.", "Consumer Discretionary"),
    ("ADSK", "Autodesk, Inc.", "Information Technology"), ("TDG", "TransDigm Group Incorporated", "Industrials"), ("ANET", "Arista Networks, Inc.", "Information Technology"),
    ("SRE", "Sempra", "Utilities"), ("ECL", "Ecolab Inc.", "Materials"), ("OXY", "Occidental Petroleum Corporation", "Energy"),
    ("PCAR", "PACCAR Inc", "Industrials"), ("ADM", "Archer-Daniels-Midland Company", "Consumer Staples"), ("MNST", "Monster Beverage Corporation", "Consumer Staples"),
    ("KMB", "Kimberly-Clark Corporation", "Consumer Staples"), ("PSA", "Public Storage REIT", "Real Estate"), ("CCI", "Crown Castle Inc.", "Real Estate"),
    ("CHTR", "Charter Communications, Inc. Class A", "Communication Services"), ("MCHP", "Microchip Technology Incorporated", "Information Technology"), ("MSCI", "MSCI Inc.", "Financials"),
    ("CTAS", "Cintas Corporation", "Industrials"), ("WMB", "The Williams Companies, Inc.", "Energy"), ("AIG", "American International Group, Inc.", "Financials"),
    ("STZ", "Constellation Brands, Inc. Class A", "Consumer Staples"), ("HES", "Hess Corporation", "Energy"), ("NUE", "Nucor Corporation", "Materials"),
    ("ROST", "Ross Stores, Inc.", "Consumer Discretionary"), ("AFL", "Aflac Incorporated", "Financials"), ("KVUE", "Kenvue Inc.", "Consumer Staples"),
    ("AEP", "American Electric Power Company, Inc.", "Utilities"), ("IDXX", "IDEXX Laboratories, Inc.", "Health Care"), ("D", "Dominion Energy, Inc.", "Utilities"),
    ("TEL", "TE Connectivity Ltd.", "Information Technology"), ("JCI", "Johnson Controls International plc", "Industrials"), ("MET", "MetLife, Inc.", "Financials"),
    ("GIS", "General Mills, Inc.", "Consumer Staples"), ("IQV", "IQVIA Holdings Inc.", "Health Care"), ("EXC", "Exelon Corporation", "Utilities"),
    ("WELL", "Welltower Inc.", "Real Estate"), ("DXCM", "Dexcom, Inc.", "Health Care"), ("HLT", "Hilton Worldwide Holdings Inc.", "Consumer Discretionary"),
    ("ON", "ON Semiconductor Corporation", "Information Technology"), ("COF", "Capital One Financial Corporation", "Financials"), ("PAYX", "Paychex, Inc.", "Industrials"),
    ("TFC", "Truist Financial Corporation", "Financials"), ("BIIB", "Biogen Inc.", "Health Care"), ("O", "Realty Income Corporation REIT", "Real Estate"),
    ("FTNT", "Fortinet, Inc.", "Information Technology"), ("DOW", "Dow Inc.", "Materials"), ("TRV", "The Travelers Companies, Inc.", "Financials"),
    ("DLR", "Digital Realty Trust, Inc. REIT", "Real Estate"), ("MRNA", "Moderna, Inc.", "Health Care"), ("CPRT", "Copart, Inc.", "Industrials"),
    ("ODFL", "Old Dominion Freight Line, Inc.", "Industrials"), ("DHI", "D.R. Horton, Inc.", "Consumer Discretionary"), ("YUM", "Yum! Brands, Inc.", "Consumer Discretionary"),
    ("SPG", "Simon Property Group, Inc. REIT", "Real Estate"), ("CTSH", "Cognizant Technology Solutions Corporation", "Information Technology"), ("AME", "AMETEK, Inc.", "Industrials"),
    ("BKR", "Baker Hughes Company Class A", "Energy"), ("SYY", "Sysco Corporation", "Consumer Staples"), ("A", "Agilent Technologies, Inc.", "Health Care"),
    ("CTVA", "Corteva, Inc.", "Materials"), ("CNC", "Centene Corporation", "Health Care"), ("EL", "The Estée Lauder Companies Inc. Class A", "Consumer Staples"),
    ("AMP", "Ameriprise Financial, Inc.", "Financials"), ("CEG", "Constellation Energy Corporation", "Utilities"), ("HAL", "Halliburton Company", "Energy"),
    ("OTIS", "Otis Worldwide Corporation", "Industrials"), ("ROK", "Rockwell Automation, Inc.", "Industrials"), ("PRU", "Prudential Financial, Inc.", "Financials"),
    ("DD", "DuPont de Nemours, Inc.", "Materials"), ("KMI", "Kinder Morgan, Inc.", "Energy"), ("VRSK", "Verisk Analytics, Inc.", "Industrials"),
    ("LHX", "L3Harris Technologies, Inc.", "Industrials"), ("DG", "Dollar General Corporation", "Consumer Staples"), ("FIS", "Fidelity National Information Services, Inc.", "Financials"),
    ("CMI", "Cummins Inc.", "Industrials"), ("CSGP", "CoStar Group, Inc. REIT", "Real Estate"), ("FAST", "Fastenal Company", "Industrials"),
    ("PPG", "PPG Industries, Inc.", "Materials"), ("GPN", "Global Payments Inc.", "Financials"), ("GWW", "W.W. Grainger, Inc.", "Industrials"),
    ("HSY", "The Hershey Company", "Consumer Staples"), ("BK", "The Bank of New York Mellon Corporation", "Financials"), ("XEL", "Xcel Energy Inc.", "Utilities"),
    ("DVN", "Devon Energy Corporation", "Energy"), ("EA", "Electronic Arts Inc.", "Communication Services"), ("NEM", "Newmont Corporation", "Materials"),
    ("ED", "Consolidated Edison, Inc.", "Utilities"), ("URI", "United Rentals, Inc.", "Industrials"), ("VICI", "VICI Properties Inc. REIT", "Real Estate"),
    ("PEG", "Public Service Enterprise Group Incorporated", "Utilities"), ("KR", "The Kroger Co.", "Consumer Staples"), ("RSG", "Republic Services, Inc.", "Industrials"),
    ("LEN", "Lennar Corporation Class A", "Consumer Discretionary"), ("PWR", "Quanta Services, Inc.", "Industrials"), ("WST", "West Pharmaceutical Services, Inc.", "Health Care"),
    ("COR", "Cencora Inc.", "Health Care"), ("OKE", "ONEOK, Inc.", "Energy"), ("VMC", "Vulcan Materials Company", "Materials"),
    ("KDP", "Keurig Dr Pepper Inc.", "Consumer Staples"), ("WBD", "Warner Bros. Discovery, Inc. Series A", "Communication Services"), ("ACGL", "Arch Capital Group Ltd.", "Financials")
]

selected_symbols = []  # User selected stock symbols
weights_dict = {}      # User selected weights for each stock
total_allocation = 100 # Total allocation percentage must sum to 100%
stock_data_dict = {}   # To store stock data



# 2 - Fetch current Fed interest rate data via API for MPT Score calculations

# Alpha Vantage API key
api_key = 'your-api-key'

# Function to fetch Federal Funds Rate
def fetch_federal_funds_rate():
    
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey={api_key}'  # Create the API URL
    
    # Make the API request
    response = requests.get(url) 
    
    if response.status_code == 200:
        # Try to parse the JSON data
        try:
            data = response.json().get('data', [])
            
            if data:
                # Convert to DataFrame and keep only the date and value columns
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'])
                df = df[['date', 'value']]
                df = df.sort_values(by='date', ascending=False)  # Sort by date to get the most recent rate
                
                # Get the most recent daily rate
                most_recent_rate = df.iloc[0]['value']  # Assuming daily rate is in percentage
                
                # Convert to daily risk-free rate for 252 trading days
                risk_free_rate = most_recent_rate / 100 / 252  # Convert from percentage to fraction and divide by 252 tradiing days
                
                return risk_free_rate
            else:
                print("No data available for Federal Funds Rate.")
                return None
        except ValueError:
            print("Error parsing JSON response.")
            return None
    else:
        print(f"API request failed with status code {response.status_code}.")
        return None


# 3 - Fetch current S&P500 data via API for MPT Score calculations

# Function to fetch S&P 500 Adjusted Close data; S&P 500 ETF SPY used as a proxy for S&P 500
def fetch_sp500_data():
                
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&outputsize=full&apikey={api_key}'  # Create the API URL
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('Time Series (Daily)', {})
        if data:
            df = pd.DataFrame.from_dict(data, orient='index')
            df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount', 'split_coefficient']
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df = df.sort_index()

            # Fill missing data by forward filling
            df = df.ffill()

            # Adjust prices using split coefficient
            for i in range(len(df)-1, -1, -1):  # Loop in reverse to apply splits retroactively
                split_coefficient = df['split_coefficient'].iloc[i]
                if split_coefficient != 1.0:  # If there's a split, adjust prior rows
                    df.iloc[:i+1, df.columns.get_loc('open')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('high')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('low')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('close')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('volume')] *= split_coefficient

            # Filter the DataFrame to keep only data from the last 10 years
            today = datetime.now()
            ten_years_ago = today - timedelta(days=10*365)  # 10 years ago from today
            df = df[df.index >= ten_years_ago]  # Filter the DataFrame

            return df
        else:
            print(f"No data for S&P 500.")
            return None
    else:
        print(f"API request failed for S&P 500 data with status code {response.status_code}.")
        return None

# Fetch the S&P 500 data and store it in the dictionary
stock_data_dict['sp500_data'] = fetch_sp500_data()



# 4 - Fetch stock data via API for user selected stocks

# Fetch OHLCV stock data along with dividend and split coefficient via Alpha Vantage API
def fetch_stock_data(symbol):    
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={api_key}'  # Create the API URL
    
    response = requests.get(url)  # Make the API request
    if response.status_code == 200:
        data = response.json().get('Time Series (Daily)', {})
        if data:  # Convert to DataFrame if data is returned
            df = pd.DataFrame.from_dict(data, orient='index')
            df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount', 'split_coefficient']
            df.index = pd.to_datetime(df.index)
            df = df.astype(float).sort_index().ffill()  # Fill missing data by forward filling with last value in dataset

             # Adjust prices using split coefficient
            for i in range(len(df)-1, -1, -1):  # Loop in reverse to apply splits retroactively
                split_coefficient = df['split_coefficient'].iloc[i]
                if split_coefficient != 1.0:  # If there's a split, adjust prior rows
                    df.iloc[:i+1, df.columns.get_loc('open')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('high')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('low')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('close')] /= split_coefficient
                    df.iloc[:i+1, df.columns.get_loc('volume')] *= split_coefficient

            # Keep only data from the last 10 years
            ten_years_ago = datetime.now() - timedelta(days=10*365)
            df = df[df.index >= ten_years_ago]
            
            return df
    print(f"Failed to fetch data for {symbol}")
    return None

# Home route to render the search UI
@app.route('/')
def home():
    return render_template('index.html', stocks=stocks_info)

# Clear only user-selected stocks from the dictionaries, preserving sp500_data
def clear_user_selected_data():
    global stock_data_dict, stock_metrics_dict
    
    # Remove user-selected stock data from stock_data_dict, but keep sp500_data
    symbols_to_remove = [symbol for symbol in stock_data_dict if symbol != 'sp500_data']
    for symbol in symbols_to_remove:
        del stock_data_dict[symbol]
    
    # Remove user-selected stock metrics from stock_metrics_dict, but keep sp500_data
    symbols_to_remove = [symbol for symbol in stock_metrics_dict if symbol != 'sp500_data']
    for symbol in symbols_to_remove:
        del stock_metrics_dict[symbol]

# Handle form submission and fetch stock data, then return it for the chart & other calculated metrics, download button
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    global selected_symbols, weights_dict

    # Clear previously selected stock data and metrics
    clear_user_selected_data()

    selected_symbols = data.get('selected_symbols', [])
    weights_dict = data.get('weights_dict', {})

    # Validate if weights sum to 100
    total_weight = sum([float(weight) for weight in weights_dict.values()])
    if round(total_weight, 2) != 100.00:
        return jsonify({'error': f'Total weight allocation is {total_weight:.2f}%. Please adjust to 100%.'}), 400

    # Fetch stock data for each selected symbol
    stock_data_response = {}
    for symbol in selected_symbols:
        stock_data = fetch_stock_data(symbol)
        if stock_data is not None:
            stock_data_dict[symbol] = stock_data
            # Add stock data to the response
            stock_data_response[symbol] = {
                'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
                'open': stock_data['open'].tolist(),
                'high': stock_data['high'].tolist(),
                'low': stock_data['low'].tolist(),
                'close': stock_data['close'].tolist()
            }

    # Fetch Federal Funds Rate and S&P500 Data
    risk_free_rate = fetch_federal_funds_rate()
    sp500_data = fetch_sp500_data()

    # Include them in the response if necessary
    additional_data = {
        'risk_free_rate': risk_free_rate,
        'sp500_data': sp500_data['adjusted_close'].tolist() if sp500_data is not None else []
    }

    # Calculate stock metrics
    for symbol, df in stock_data_dict.items():
        calculate_stock_metrics(symbol, df)

    # Calculate portfolio-level metrics
    portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(weights_dict)
    mpt_score = calculate_mpt_score(sharpe_ratio, portfolio_return, portfolio_volatility)

    # Send stock metrics along with stock data and portfolio metrics
    if stock_data_response:
        return jsonify({
            'message': 'Stock data fetched successfully!',
            'stock_data': stock_data_response,
            'stock_metrics': stock_metrics_dict,  # Include the stock metrics
            'additional_data': additional_data,  # Include the extra data
            'portfolio_metrics': {
                'portfolio_return': portfolio_return,
                'portfolio_volatility': portfolio_volatility,
                'sharpe_ratio': sharpe_ratio,
                'mpt_score': mpt_score
            }
        })
    else:
        return jsonify({'error': 'Failed to fetch stock data.'}), 500



# Route to search stocks dynamically
@app.route('/search', methods=['POST'])
def search():
    search_query = request.json.get('query', '').upper()
    matching_stocks = [stock for stock in stocks_info if search_query in stock[0]]
    return jsonify(matching_stocks)



# 5 - Display graphs for user selected stocks

# Route to render the chart page
@app.route('/chart')
def chart_page():
    return render_template('chart.html')

# Route to get available stock symbols for the dropdown
@app.route('/get_symbols', methods=['GET'])
def get_symbols():
    if stock_data_dict:  # Ensure there are stocks in the dictionary
        return jsonify(list(stock_data_dict.keys()))  # Send back available stock symbols
    else:
        return jsonify({'error': 'No stock data available yet'}), 400

# Route to get stock data for the selected symbol
@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    symbol = request.json.get('symbol')
    df = stock_data_dict.get(symbol)

    if df is not None:
        # Prepare the data for Plotly
        data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'open': df['open'].tolist(),
            'high': df['high'].tolist(),
            'low': df['low'].tolist(),
            'close': df['close'].tolist()
        }
        return jsonify(data)
    else:
        return jsonify({'error': f'No data available for {symbol}'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



    # 6 - Stock Statistical Summary Metrics for user-selected stocks

# Dictionary to store metrics for each stock
stock_metrics_dict = {}
risk_free_rate = None  # Define a global risk-free rate

# Function to calculate metrics for each stock
def calculate_stock_metrics(symbol, df):
    global risk_free_rate  # Declare risk_free_rate as global
    if df is not None:
        # Calculate daily returns
        df['daily_return'] = df['close'].pct_change()

        # Expected return (mean of daily returns)
        expected_return = df['daily_return'].mean()/100   #Jupyter code imports as decimal but here as a percentage so result is 100x. Temporary solution to divide by 100 here.

        # Volatility (standard deviation of daily returns)
        volatility = df['daily_return'].std()/100         #Jupyter code imports as decimal but here as a percentage so result is 100x. Temporary solution to divide by 100 here.

        # Risk-free rate (using fetched daily Fed rate)
        if risk_free_rate is None:  # Fetch risk-free rate only once
            risk_free_rate = fetch_federal_funds_rate()

        # Beta calculation (requires benchmark data S&P 500 data)
        if 'sp500_data' in stock_data_dict:
            sp500_data = stock_data_dict['sp500_data']
            sp500_returns = sp500_data['adjusted_close'].pct_change()

            # Ensure both stock and benchmark have matching dates
            merged_data = pd.merge(df[['daily_return']], sp500_data[['adjusted_close']], left_index=True, right_index=True, how='inner')
            merged_data['sp500_return'] = merged_data['adjusted_close'].pct_change()

            # Calculate covariance between stock and market benchmark S&P 500
            covariance = np.cov(merged_data['daily_return'][1:], merged_data['sp500_return'][1:])[0][1]
            market_variance = merged_data['sp500_return'][1:].var()

            # Beta = Covariance / Market Variance
            beta = covariance / market_variance
        else:
            beta = np.nan

        # Alpha calculation
        if beta is not np.nan:
            market_return = merged_data['sp500_return'].mean()
            alpha = expected_return - (risk_free_rate + beta * (market_return - risk_free_rate))
        else:
            alpha = np.nan

        # Correlation with other selected stocks
        correlations = {}
        for other_symbol, other_df in stock_data_dict.items():
            if symbol != other_symbol and other_df is not None:
                other_df['daily_return'] = other_df['close'].pct_change()
                correlations[other_symbol] = df['daily_return'].corr(other_df['daily_return'])

        # Store all calculated metrics in the dictionary
        stock_metrics_dict[symbol] = {
            'expected_return': expected_return,
            'volatility': volatility,
            'beta': beta,
            'alpha': alpha,
            'correlations': correlations
        }

# Iterate over the fetched stock data and calculate metrics for each
for symbol, df in stock_data_dict.items():
    calculate_stock_metrics(symbol, df)

# Display the calculated metrics for each stock
for symbol, metrics in stock_metrics_dict.items():
    print(f"Metrics for {symbol}:")
    print(f"  Expected Daily Return: {metrics['expected_return']}")
    print(f"  Volatility: {metrics['volatility']}")
    print(f"  Beta: {metrics['beta']}")
    print(f"  Alpha: {metrics['alpha']}")
    print(f"  Correlations: {metrics['correlations']}")

# Portfolio metrics calculations
def calculate_portfolio_metrics(weights):
    symbols_in_portfolio = [symbol for symbol in stock_data_dict.keys() if symbol in weights_dict]
    weights_in_portfolio = [weights_dict[symbol] for symbol in symbols_in_portfolio]

    portfolio_return = sum(weights_in_portfolio[i] * stock_metrics_dict[symbol]['expected_return']  # Calculated portfolio expected return
                           for i, symbol in enumerate(symbols_in_portfolio))
    
    portfolio_volatility = np.sqrt(sum(     # Calculated portfolio volatility
        weights_in_portfolio[i] * weights_in_portfolio[j] * stock_metrics_dict[symbol]['volatility'] 
        * stock_metrics_dict[other_symbol]['volatility'] 
        * stock_metrics_dict[symbol]['correlations'].get(other_symbol, 0)
        for i, symbol in enumerate(symbols_in_portfolio)
        for j, other_symbol in enumerate(symbols_in_portfolio)
    ))

    # Handle division by zero in Sharpe ratio calculation
    if portfolio_volatility == 0:
        sharpe_ratio = float('nan')  # Assign NaN if volatility is zero
    else:
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility  # Sharpe ratio calculation
    return portfolio_return, portfolio_volatility, sharpe_ratio

# Portfolio weights are sourced from user defined weights_dict
weights = [weights_dict[symbol] for symbol in stock_data_dict.keys() if symbol in weights_dict]
portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(weights)

# Print portfolio metrics
print(f"User Selected Portfolio Expected Daily Return: {portfolio_return}")
print(f"User Selected Portfolio Volatility: {portfolio_volatility}")
print(f"User Selected Portfolio Sharpe Ratio: {sharpe_ratio}")

# Scoring MPT (0-100) based on portfolio metrics
def calculate_mpt_score(sharpe_ratio, portfolio_return, portfolio_volatility):
    sharpe_score = np.clip((sharpe_ratio / 2) * 100, 0, 100)                    # Setting the threshold of 2 as a good Sharpe ratio
    return_score = np.clip(portfolio_return * 100, 0, 100)                      # Return * 100 capped at 100%
    volatility_score = np.clip(100 - (portfolio_volatility * 100), 0, 100)      # Volatility * 100 capped at 100
    
    return (sharpe_score + return_score + volatility_score) / 3

# Calculate and print the MPT Score of the user selected portfolio 
mpt_score = calculate_mpt_score(sharpe_ratio, portfolio_return, portfolio_volatility)
print(f"User Selected Portfolio MPT Score: {mpt_score}")



# 7 - Heatmap for user-defined portfolio

@app.route('/calculate_correlation', methods=['POST'])
def calculate_correlation():
    # Create a DataFrame to store correlations between stocks
    correlation_matrix = pd.DataFrame()

    # Iterate over the fetched stock data and fill the correlation matrix
    for symbol, metrics in stock_metrics_dict.items():
        correlation_matrix[symbol] = [metrics['correlations'].get(other_symbol, np.nan) for other_symbol in stock_metrics_dict.keys()]

    # Set the index to the stock symbols for proper labeling
    correlation_matrix.index = stock_metrics_dict.keys()

    # Convert the correlation matrix to JSON format to send to the frontend
    correlation_json = correlation_matrix.to_json(orient='split')

    return jsonify({
        'message': 'Correlation matrix calculated successfully!',
        'correlation_matrix': correlation_json
    })


@app.route('/download_report', methods=['GET'])
def download_report():
    # Calculate portfolio metrics (make sure the weights are passed correctly)
    portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(weights_dict)
    mpt_score = calculate_mpt_score(sharpe_ratio, portfolio_return, portfolio_volatility)  # Make sure MPT score is calculated

    # Render the report content as HTML
    rendered_html = render_template(
        'report_template.html',
        selected_symbols=selected_symbols,
        stock_metrics_dict=stock_metrics_dict,
        portfolio_metrics=(portfolio_return, portfolio_volatility, sharpe_ratio),  # Pass all the metrics
        mpt_score=mpt_score  # Pass the MPT score
    )

    # Convert the HTML content to PDF using pdfkit
    pdfkit.from_string(rendered_html, 'report.pdf')

    # Serve the generated PDF file
    return send_file('report.pdf', as_attachment=True, download_name='portfolio_report.pdf')



