from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import random
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'stockmarketsimulatorsecretkey'

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Define Indian stock data
STOCKS = {
    'RELIANCE': {'name': 'Reliance Industries', 'sector': 'Oil & Gas', 'price': 2755.35, 'volatile': False},
    'TCS': {'name': 'Tata Consultancy Services', 'sector': 'IT', 'price': 3684.80, 'volatile': False},
    'HDFC': {'name': 'HDFC Bank', 'sector': 'Banking', 'price': 1687.25, 'volatile': False},
    'INFY': {'name': 'Infosys', 'sector': 'IT', 'price': 1558.65, 'volatile': False},
    'ICICI': {'name': 'ICICI Bank', 'sector': 'Banking', 'price': 945.70, 'volatile': False},
    'BAJAJ': {'name': 'Bajaj Finance', 'sector': 'Finance', 'price': 7245.30, 'volatile': False},
    'BHARTI': {'name': 'Bharti Airtel', 'sector': 'Telecom', 'price': 1034.55, 'volatile': False},
    'ITC': {'name': 'ITC Limited', 'sector': 'FMCG', 'price': 447.80, 'volatile': False},
    'LT': {'name': 'Larsen & Toubro', 'sector': 'Construction', 'price': 2975.15, 'volatile': False}, 
    'SBI': {'name': 'State Bank of India', 'sector': 'Banking', 'price': 725.60, 'volatile': False},
    'ZOMATO': {'name': 'Zomato Ltd', 'sector': 'Food Delivery', 'price': 162.45, 'volatile': True},
    'PAYTM': {'name': 'Paytm', 'sector': 'Fintech', 'price': 385.25, 'volatile': True},
    'YESBANK': {'name': 'Yes Bank', 'sector': 'Banking', 'price': 24.35, 'volatile': True},
    'IRCTC': {'name': 'Indian Railway Catering', 'sector': 'Travel', 'price': 854.70, 'volatile': True},
    'TATAMOTORS': {'name': 'Tata Motors', 'sector': 'Automobile', 'price': 759.80, 'volatile': True},
}

# Define mutual funds
MUTUAL_FUNDS = {
    'HDFC_TOP_100': {'name': 'HDFC Top 100 Fund', 'category': 'Large Cap', 'nav': 875.45, 'risk': 'Moderate'},
    'SBI_BLUECHIP': {'name': 'SBI Blue Chip Fund', 'category': 'Large Cap', 'nav': 56.78, 'risk': 'Moderate'},
    'AXIS_MIDCAP': {'name': 'Axis Midcap Fund', 'category': 'Mid Cap', 'nav': 72.35, 'risk': 'High'},
    'MIRAE_EMERGING': {'name': 'Mirae Asset Emerging Bluechip', 'category': 'Mid-Large Cap', 'nav': 104.25, 'risk': 'High'},
    'PARAG_FLEXI': {'name': 'Parag Parikh Flexi Cap Fund', 'category': 'Flexi Cap', 'nav': 58.90, 'risk': 'Moderate'},
}

# Global variables to store user and stock data
users_file = 'data/users.json'
stocks_data_file = 'data/stocks_data.json'
transactions_file = 'data/transactions.json'
portfolio_file = 'data/portfolio.json'
mutual_funds_file = 'data/mutual_funds.json'

# Initialize files if they don't exist
if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        json.dump({}, f)

if not os.path.exists(transactions_file):
    with open(transactions_file, 'w') as f:
        json.dump({}, f)

if not os.path.exists(portfolio_file):
    with open(portfolio_file, 'w') as f:
        json.dump({}, f)

if not os.path.exists(mutual_funds_file):
    with open(mutual_funds_file, 'w') as f:
        json.dump({}, f)

# Generate historical stock data
def generate_stock_data():
    stock_data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    dates = [date.strftime('%Y-%m-%d') for date in date_range]
    
    for symbol, info in STOCKS.items():
        base_price = info['price']
        volatility = 0.03 if not info['volatile'] else 0.08
        
        prices = []
        current_price = base_price * 0.8  # Start lower than current price
        
        for _ in dates:
            # Random walk with drift
            change_percent = np.random.normal(0.0003, volatility)
            current_price *= (1 + change_percent)
            prices.append(round(current_price, 2))
        
        # Ensure the last price is the current price
        adjustment_factor = base_price / prices[-1]
        prices = [round(price * adjustment_factor, 2) for price in prices]
        
        ohlc_data = []
        for i, date in enumerate(dates):
            if i > 0:
                open_price = prices[i-1]
                close_price = prices[i]
                high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.02))
                low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.02))
                
                ohlc_data.append({
                    'date': date,
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': int(random.uniform(100000, 5000000))
                })
        
        stock_data[symbol] = {
            'info': info,
            'ohlc': ohlc_data
        }
    
    with open(stocks_data_file, 'w') as f:
        json.dump(stock_data, f)
    
    return stock_data

# Generate stock data if it doesn't exist
if not os.path.exists(stocks_data_file):
    stock_data = generate_stock_data()
else:
    with open(stocks_data_file, 'r') as f:
        stock_data = json.load(f)

# Helper functions
def get_users():
    with open(users_file, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

def get_transactions():
    with open(transactions_file, 'r') as f:
        return json.load(f)

def save_transactions(transactions):
    with open(transactions_file, 'w') as f:
        json.dump(transactions, f)

def get_portfolio():
    with open(portfolio_file, 'r') as f:
        return json.load(f)

def save_portfolio(portfolio):
    with open(portfolio_file, 'w') as f:
        json.dump(portfolio, f)

def get_mutual_funds():
    with open(mutual_funds_file, 'r') as f:
        return json.load(f)

def save_mutual_funds(mutual_funds):
    with open(mutual_funds_file, 'w') as f:
        json.dump(mutual_funds, f)

def update_stock_prices():
    """Update stock prices with random movements"""
    updated_stocks = {}
    for symbol, info in STOCKS.items():
        base_price = info['price']
        volatility = 0.01 if not info['volatile'] else 0.03
        change = random.uniform(-volatility, volatility)
        new_price = round(base_price * (1 + change), 2)
        
        # Create a copy of the info dictionary
        updated_stocks[symbol] = info.copy()
        updated_stocks[symbol]['price'] = new_price
        updated_stocks[symbol]['change'] = round(change * 100, 2)
    
    return updated_stocks

# Routes
@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        users = get_users()
        
        if email in users:
            flash('Email already exists!')
            return redirect(url_for('register'))
        
        users[email] = {
            'password': generate_password_hash(password),
            'balance': 1000000.0,  # Starting with 10 lakhs
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        save_users(users)
        
        # Initialize empty portfolio and transactions for the user
        portfolio = get_portfolio()
        portfolio[email] = {'stocks': {}, 'mutual_funds': {}}
        save_portfolio(portfolio)
        
        transactions = get_transactions()
        transactions[email] = []
        save_transactions(transactions)
        
        mutual_funds = get_mutual_funds()
        mutual_funds[email] = {}
        save_mutual_funds(mutual_funds)
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        users = get_users()
        
        if email in users and check_password_hash(users[email]['password'], password):
            session['email'] = email
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    users = get_users()
    portfolio = get_portfolio()
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    # Calculate portfolio value
    portfolio_value = users[email]['balance']
    stock_value = 0
    
    if email in portfolio and 'stocks' in portfolio[email]:
        for symbol, quantity in portfolio[email]['stocks'].items():
            if symbol in updated_stocks:
                stock_value += updated_stocks[symbol]['price'] * quantity
    
    mutual_fund_value = 0
    if email in portfolio and 'mutual_funds' in portfolio[email]:
        for fund_id, units in portfolio[email]['mutual_funds'].items():
            if fund_id in MUTUAL_FUNDS:
                mutual_fund_value += MUTUAL_FUNDS[fund_id]['nav'] * units
    
    total_value = portfolio_value + stock_value + mutual_fund_value
    
    return render_template('dashboard.html', 
                          cash_balance=users[email]['balance'], 
                          stock_value=stock_value,
                          mutual_fund_value=mutual_fund_value,
                          total_value=total_value,
                          stocks=updated_stocks)

@app.route('/market')
def market():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    return render_template('market.html', stocks=updated_stocks)

@app.route('/stock/<symbol>')
def stock_detail(symbol):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if symbol not in stock_data:
        flash('Stock not found!')
        return redirect(url_for('market'))
    
    updated_stocks = update_stock_prices()
    stock_info = updated_stocks[symbol]
    
    # Get historical data
    hist_data = stock_data[symbol]['ohlc']
    
    return render_template('stock_detail.html', 
                          symbol=symbol, 
                          stock=stock_info, 
                          historical_data=json.dumps(hist_data))

@app.route('/portfolio')
def portfolio_view():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    portfolio_data = get_portfolio()
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    # Get user's stocks
    user_stocks = []
    total_value = 0
    
    if email in portfolio_data and 'stocks' in portfolio_data[email]:
        for symbol, quantity in portfolio_data[email]['stocks'].items():
            if symbol in updated_stocks:
                stock_price = updated_stocks[symbol]['price']
                investment_value = stock_price * quantity
                total_value += investment_value
                
                user_stocks.append({
                    'symbol': symbol,
                    'name': updated_stocks[symbol]['name'],
                    'quantity': quantity,
                    'price': stock_price,
                    'value': investment_value
                })
    
    # Get user's mutual funds
    user_funds = []
    fund_total = 0
    
    if email in portfolio_data and 'mutual_funds' in portfolio_data[email]:
        for fund_id, units in portfolio_data[email]['mutual_funds'].items():
            if fund_id in MUTUAL_FUNDS:
                nav = MUTUAL_FUNDS[fund_id]['nav']
                investment_value = nav * units
                fund_total += investment_value
                
                user_funds.append({
                    'id': fund_id,
                    'name': MUTUAL_FUNDS[fund_id]['name'],
                    'units': units,
                    'nav': nav,
                    'value': investment_value
                })
    
    return render_template('portfolio.html', 
                          stocks=user_stocks, 
                          mutual_funds=user_funds,
                          stock_total=total_value,
                          fund_total=fund_total)

@app.route('/mutual_funds')
def mutual_funds():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    return render_template('mutual_funds.html', funds=MUTUAL_FUNDS)

@app.route('/transactions')
def transactions():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    transactions_data = get_transactions()
    
    user_transactions = []
    if email in transactions_data:
        user_transactions = transactions_data[email]
    
    return render_template('transactions.html', transactions=user_transactions)

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    if symbol not in updated_stocks:
        flash('Stock not found!')
        return redirect(url_for('market'))
    
    stock_price = updated_stocks[symbol]['price']
    total_cost = stock_price * quantity
    
    users = get_users()
    
    if users[email]['balance'] < total_cost:
        flash('Insufficient funds!')
        return redirect(url_for('stock_detail', symbol=symbol))
    
    # Update user balance
    users[email]['balance'] -= total_cost
    save_users(users)
    
    # Update portfolio
    portfolio = get_portfolio()
    
    if email not in portfolio:
        portfolio[email] = {'stocks': {}, 'mutual_funds': {}}
    
    if 'stocks' not in portfolio[email]:
        portfolio[email]['stocks'] = {}
    
    if symbol in portfolio[email]['stocks']:
        portfolio[email]['stocks'][symbol] += quantity
    else:
        portfolio[email]['stocks'][symbol] = quantity
    
    save_portfolio(portfolio)
    
    # Record transaction
    transactions = get_transactions()
    
    if email not in transactions:
        transactions[email] = []
    
    transactions[email].append({
        'type': 'BUY',
        'asset_type': 'STOCK',
        'asset_id': symbol,
        'quantity': quantity,
        'price': stock_price,
        'total': total_cost,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    save_transactions(transactions)
    
    flash(f'Successfully bought {quantity} shares of {symbol}!')
    return redirect(url_for('portfolio_view'))

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    if symbol not in updated_stocks:
        flash('Stock not found!')
        return redirect(url_for('portfolio_view'))
    
    portfolio = get_portfolio()
    
    if (email not in portfolio or 
        'stocks' not in portfolio[email] or 
        symbol not in portfolio[email]['stocks'] or 
        portfolio[email]['stocks'][symbol] < quantity):
        flash('You do not own enough shares to sell!')
        return redirect(url_for('portfolio_view'))
    
    stock_price = updated_stocks[symbol]['price']
    total_value = stock_price * quantity
    
    # Update user balance
    users = get_users()
    users[email]['balance'] += total_value
    save_users(users)
    
    # Update portfolio
    portfolio[email]['stocks'][symbol] -= quantity
    
    if portfolio[email]['stocks'][symbol] == 0:
        del portfolio[email]['stocks'][symbol]
    
    save_portfolio(portfolio)
    
    # Record transaction
    transactions = get_transactions()
    
    if email not in transactions:
        transactions[email] = []
    
    transactions[email].append({
        'type': 'SELL',
        'asset_type': 'STOCK',
        'asset_id': symbol,
        'quantity': quantity,
        'price': stock_price,
        'total': total_value,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    save_transactions(transactions)
    
    flash(f'Successfully sold {quantity} shares of {symbol}!')
    return redirect(url_for('portfolio_view'))

@app.route('/buy_mutual_fund', methods=['POST'])
def buy_mutual_fund():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    fund_id = request.form['fund_id']
    amount = float(request.form['amount'])
    
    if fund_id not in MUTUAL_FUNDS:
        flash('Mutual Fund not found!')
        return redirect(url_for('mutual_funds'))
    
    nav = MUTUAL_FUNDS[fund_id]['nav']
    units = amount / nav
    
    users = get_users()
    
    if users[email]['balance'] < amount:
        flash('Insufficient funds!')
        return redirect(url_for('mutual_funds'))
    
    # Update user balance
    users[email]['balance'] -= amount
    save_users(users)
    
    # Update portfolio
    portfolio = get_portfolio()
    
    if email not in portfolio:
        portfolio[email] = {'stocks': {}, 'mutual_funds': {}}
    
    if 'mutual_funds' not in portfolio[email]:
        portfolio[email]['mutual_funds'] = {}
    
    if fund_id in portfolio[email]['mutual_funds']:
        portfolio[email]['mutual_funds'][fund_id] += units
    else:
        portfolio[email]['mutual_funds'][fund_id] = units
    
    save_portfolio(portfolio)
    
    # Record transaction
    transactions = get_transactions()
    
    if email not in transactions:
        transactions[email] = []
    
    transactions[email].append({
        'type': 'BUY',
        'asset_type': 'MUTUAL_FUND',
        'asset_id': fund_id,
        'units': round(units, 3),
        'nav': nav,
        'total': amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    save_transactions(transactions)
    
    flash(f'Successfully invested ₹{amount} in {MUTUAL_FUNDS[fund_id]["name"]}!')
    return redirect(url_for('portfolio_view'))

@app.route('/sell_mutual_fund', methods=['POST'])
def sell_mutual_fund():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    fund_id = request.form['fund_id']
    units = float(request.form['units'])
    
    if fund_id not in MUTUAL_FUNDS:
        flash('Mutual Fund not found!')
        return redirect(url_for('portfolio_view'))
    
    portfolio = get_portfolio()
    
    if (email not in portfolio or 
        'mutual_funds' not in portfolio[email] or 
        fund_id not in portfolio[email]['mutual_funds'] or 
        portfolio[email]['mutual_funds'][fund_id] < units):
        flash('You do not own enough units to sell!')
        return redirect(url_for('portfolio_view'))
    
    nav = MUTUAL_FUNDS[fund_id]['nav']
    amount = units * nav
    
    # Update user balance
    users = get_users()
    users[email]['balance'] += amount
    save_users(users)
    
    # Update portfolio
    portfolio[email]['mutual_funds'][fund_id] -= units
    
    if portfolio[email]['mutual_funds'][fund_id] < 0.001:
        del portfolio[email]['mutual_funds'][fund_id]
    
    save_portfolio(portfolio)
    
    # Record transaction
    transactions = get_transactions()
    
    if email not in transactions:
        transactions[email] = []
    
    transactions[email].append({
        'type': 'SELL',
        'asset_type': 'MUTUAL_FUND',
        'asset_id': fund_id,
        'units': round(units, 3),
        'nav': nav,
        'total': amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    save_transactions(transactions)
    
    flash(f'Successfully redeemed {units} units of {MUTUAL_FUNDS[fund_id]["name"]}!')
    return redirect(url_for('portfolio_view'))

@app.route('/add_funds', methods=['GET', 'POST'])
def add_funds():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = session['email']
        amount = float(request.form['amount'])
        
        if amount <= 0:
            flash('Please enter a valid amount!')
            return redirect(url_for('add_funds'))
        
        users = get_users()
        users[email]['balance'] += amount
        save_users(users)
        
        # Record transaction
        transactions = get_transactions()
        
        if email not in transactions:
            transactions[email] = []
        
        transactions[email].append({
            'type': 'DEPOSIT',
            'asset_type': 'CASH',
            'asset_id': 'INR',
            'quantity': 1,
            'price': amount,
            'total': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        save_transactions(transactions)
        
        flash(f'Successfully added ₹{amount} to your account!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_funds.html')

@app.route('/api/stock_price/<symbol>')
def api_stock_price(symbol):
    if symbol not in STOCKS:
        return jsonify({'error': 'Stock not found'}), 404
    
    # Update stock prices
    updated_stocks = update_stock_prices()
    
    return jsonify({
        'symbol': symbol,
        'price': updated_stocks[symbol]['price'],
        'change': updated_stocks[symbol]['change']
    })

@app.route('/api/stock_history/<symbol>')
def api_stock_history(symbol):
    if symbol not in stock_data:
        return jsonify({'error': 'Stock not found'}), 404
    
    return jsonify(stock_data[symbol]['ohlc'])

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)