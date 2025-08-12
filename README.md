# 📈 Dummy Stock Market Simulator 💹

A realistic Indian stock market and mutual fund simulator built with Flask!

🔗 **Live Demo**: [stockmarket.com](http://stockmarket.pythonanywhere.com)
# Flask Stock Market Simulator - Detailed Code Explanation

## 1. Import Statements (Lines 1-8)

```python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import random
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
import statistics
```

**What's happening here:**

- **Flask imports**: Core Flask functionality for web development
  - `Flask`: Main application class
  - `render_template`: Renders HTML templates with data
  - `request`: Handles HTTP requests (GET, POST data)
  - `redirect`: Redirects users to different pages
  - `url_for`: Generates URLs for routes
  - `flash`: Shows temporary messages to users
  - `jsonify`: Converts Python data to JSON for API responses
  - `session`: Manages user login sessions
- **os**: Interacts with operating system (file operations)
- **random**: Generates random numbers for stock price simulation
- **json**: Handles JSON data storage and parsing
- **datetime**: Manages dates and times for transactions
- **pandas/numpy**: Data analysis libraries for stock price calculations
- **werkzeug.security**: Provides password hashing for security
- **statistics**: Mathematical calculations for user analytics

## 2. Flask App Initialization (Lines 10-11)

```python
app = Flask(__name__)
app.secret_key = 'stockmarketsimulatorsecretkey'
```

**What's happening:**

- Creates the main Flask application instance
- Sets a secret key needed for session management and security
- The secret key encrypts session data stored in cookies

## 3. Data Directory Setup (Lines 13-16)

```python
if not os.path.exists('data'):
    os.makedirs('data')
```

**What's happening:**

- Checks if a 'data' folder exists
- Creates the folder if it doesn't exist
- This folder will store all application data (users, transactions, etc.)

## 4. Stock Data Definition (Lines 18-35)

```python
STOCKS = {
    'RELIANCE': {'name': 'Reliance Industries', 'sector': 'Oil & Gas', 'price': 2755.35, 'volatile': False},
    'TCS': {'name': 'Tata Consultancy Services', 'sector': 'IT', 'price': 3684.80, 'volatile': False},
    # ... more stocks
}
```

**What's happening:**

- Defines a dictionary containing Indian stock market data
- Each stock has:
  - `name`: Full company name
  - `sector`: Industry category
  - `price`: Current stock price in INR
  - `volatile`: Whether the stock has high price fluctuations
- This serves as the master data for all available stocks

## 5. Mutual Funds Definition (Lines 37-44)

```python
MUTUAL_FUNDS = {
    'HDFC_TOP_100': {'name': 'HDFC Top 100 Fund', 'category': 'Large Cap', 'nav': 875.45, 'risk': 'Moderate'},
    # ... more funds
}
```

**What's happening:**

- Similar to stocks, but for mutual fund investments
- Each fund has NAV (Net Asset Value) instead of price
- Includes risk category for investment guidance

## 6. Admin Credentials (Lines 46-48)

```python
ADMIN_USERNAME = "Admin-Prajwal"
ADMIN_PASSWORD = "Admin0307"
```

**What's happening:**

- Hardcoded admin login credentials
- Used for accessing administrative features
- **Note**: In production, these should be environment variables

## 7. File Path Definitions (Lines 50-56)

```python
users_file = 'data/users.json'
stocks_data_file = 'data/stocks_data.json'
transactions_file = 'data/transactions.json'
portfolio_file = 'data/portfolio.json'
mutual_funds_file = 'data/mutual_funds.json'
```

**What's happening:**

- Defines file paths for data storage
- Each file serves a specific purpose:
  - `users.json`: User accounts and balances
  - `stocks_data.json`: Historical stock price data
  - `transactions.json`: All buy/sell transactions
  - `portfolio.json`: Current user holdings
  - `mutual_funds.json`: Mutual fund investments

## 8. File Initialization (Lines 58-74)

```python
if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        json.dump({}, f)
# ... similar for other files
```

**What's happening:**

- Checks if data files exist
- Creates empty JSON files if they don't exist
- Prevents errors when the app runs for the first time
- Each file starts as an empty dictionary `{}`

## 9. Stock Data Generation Function (Lines 76-126)

```python
def generate_stock_data():
    stock_data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    # ... complex stock simulation logic
```

**What's happening:**

- Creates realistic historical stock price data
- Generates 1 year of daily stock prices
- Uses mathematical models to simulate:
  - **Random walk**: Price changes based on probability
  - **Volatility**: Different stocks have different price movement ranges
  - **OHLC data**: Open, High, Low, Close prices for each day
- This makes charts and analysis look realistic

**Key concepts:**

- **Business days only**: `freq='B'` excludes weekends
- **Normal distribution**: `np.random.normal()` creates realistic price changes
- **Adjustment factor**: Ensures the final price matches current price

## 10. Helper Functions (Lines 136-158)

```python
def get_users():
    with open(users_file, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)
```

**What's happening:**

- Creates utility functions for data operations
- **Separation of concerns**: Data handling is separate from business logic
- Each data type (users, transactions, portfolio) has get/save functions
- Makes code cleaner and reduces repetition

## 11. Stock Price Update Function (Lines 160-177)

```python
def update_stock_prices():
    updated_stocks = {}
    for symbol, info in STOCKS.items():
        base_price = info['price']
        volatility = 0.01 if not info['volatile'] else 0.03
        change = random.uniform(-volatility, volatility)
        new_price = round(base_price * (1 + change), 2)
```

**What's happening:**

- Simulates real-time stock price changes
- **Volatility difference**:
  - Stable stocks: ±1% change
  - Volatile stocks: ±3% change
- Calculates percentage change for display
- Returns updated stock data with new prices

## 12. User Strategy Analysis Function (Lines 179-290)

```python
def analyze_user_strategy(email):
    # Complex analysis of user's investment behavior
    transactions_data = get_transactions()
    portfolio_data = get_portfolio()
    # ... detailed analysis logic
```

**What's happening:**

- **Advanced feature**: Analyzes how users invest
- Examines patterns like:
  - **Trading frequency**: How often they buy/sell
  - **Risk profile**: Do they prefer safe or risky investments?
  - **Sector preference**: Which industries they favor
  - **Holding period**: How long they keep investments
- **Business intelligence**: Helps understand user behavior
- **Investment classification**: Labels users as "Day Trader", "Long-term Investor", etc.

## 13. Market Insights Function (Lines 292-340)

```python
def get_market_insights():
    # Analyzes overall platform activity
    portfolio_data = get_portfolio()
    transactions_data = get_transactions()
    # ... market analysis
```

**What's happening:**

- **Platform analytics**: Overview of entire application usage
- Calculates:
  - Most popular stocks
  - Top performing users
  - Sector-wise investment volume
  - Average user performance
- **Admin dashboard data**: Helps admins understand platform health

## 14. Route Functions (Lines 342 onwards)

### Home Route (Lines 342-347)

```python
@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')
```

**What's happening:**

- **Entry point**: First page users see
- **Authentication check**: If user is logged in, redirect to dashboard
- **Route decorator**: `@app.route('/')` makes this function handle requests to the root URL

### Registration Route (Lines 355-383)

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # ... registration logic
```

**What's happening:**

- **Dual method route**: Handles both GET (show form) and POST (process form)
- **Form processing**: Extracts email and password from form
- **Duplicate check**: Ensures email isn't already registered
- **Password security**: Uses `generate_password_hash()` to encrypt passwords
- **Initial setup**: Gives new users ₹10,00,000 starting balance
- **Data initialization**: Creates empty portfolio and transaction history

### Login Route (Lines 385-404)

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... admin check
    if email == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    # ... user login logic
```

**What's happening:**

- **Dual authentication**: Supports both admin and regular user login
- **Admin bypass**: Hardcoded admin credentials (not ideal for production)
- **Session management**: Stores user email in session for authentication
- **Password verification**: Uses `check_password_hash()` for security
- **Redirect logic**: Different dashboards for admin vs users

### Dashboard Route (Lines 410-440)

```python
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    # ... calculate portfolio values
```

**What's happening:**

- **Authentication guard**: Redirects to login if not authenticated
- **Portfolio calculation**:
  - Cash balance from user account
  - Stock value from current holdings × current prices
  - Mutual fund value from units × NAV
- **Real-time updates**: Gets current stock prices
- **Summary display**: Shows total portfolio worth

### Trading Routes (Lines 496-605)

#### Buy Stock Route

```python
@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    # ... validation and purchase logic
    total_cost = stock_price * quantity
    if users[email]['balance'] < total_cost:
        flash('Insufficient funds!')
```

**What's happening:**

- **Form processing**: Gets stock symbol and quantity
- **Cost calculation**: Price × quantity
- **Balance check**: Ensures user has enough money
- **Database updates**:
  - Reduces user's cash balance
  - Increases stock holdings
  - Records transaction history
- **User feedback**: Flash messages for success/error

#### Sell Stock Route

```python
@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    # ... validation and sale logic
    if portfolio[email]['stocks'][symbol] < quantity:
        flash('You do not own enough shares to sell!')
```

**What's happening:**

- **Ownership validation**: Checks if user owns enough shares
- **Sale execution**:
  - Increases cash balance
  - Decreases stock holdings
  - Records sell transaction
- **Portfolio cleanup**: Removes stock if quantity becomes zero

### Admin Routes (Lines 700 onwards)

#### Admin Dashboard

```python
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session or not session['admin']:
        flash('Please login as admin!')
        return redirect(url_for('admin_login'))
```

**What's happening:**

- **Admin authentication**: Checks admin session
- **Platform overview**: Shows overall statistics
- **User insights**: Analyzes all user behavior
- **Market data**: Stock popularity and sector analysis

#### Admin User Management

```python
@app.route('/admin/users')
def admin_users():
    # ... calculate user statistics
    user_data.append({
        'email': email,
        'balance': cash_balance,
        'total_value': total_value,
        'strategy': strategy['strategy']
    })
```

**What's happening:**

- **User listing**: Shows all registered users
- **Performance metrics**: Calculates portfolio value for each user
- **Strategy analysis**: Uses the strategy analysis function
- **Ranking**: Sorts users by portfolio value

### API Routes (Lines 800 onwards)

```python
@app.route('/api/stock_price/<symbol>')
def api_stock_price(symbol):
    return jsonify({
        'symbol': symbol,
        'price': updated_stocks[symbol]['price'],
        'change': updated_stocks[symbol]['change']
    })
```

**What's happening:**

- **REST API**: Provides data in JSON format
- **Dynamic URLs**: `<symbol>` is a parameter
- **Real-time data**: Returns current stock prices
- **AJAX support**: Frontend JavaScript can fetch this data
- **Error handling**: Returns 404 for invalid stocks

## 15. Application Startup (Lines 850-851)

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**What's happening:**

- **Development server**: Only runs if script is executed directly
- **Debug mode**: Shows detailed error messages and auto-reloads
- **Network access**: `host='0.0.0.0'` allows external connections
- **Port specification**: Application runs on port 5000

## Key Programming Concepts Used

### 1. **MVC Architecture**

- **Model**: Data functions (get_users, save_transactions, etc.)
- **View**: HTML templates rendered with data
- **Controller**: Route functions handling requests

### 2. **Session Management**

- Tracks logged-in users across requests
- Stores user email and admin status
- Enables authentication without repeated login

### 3. **Data Persistence**

- JSON files for simple data storage
- File-based database alternative
- Automatic file creation and management

### 4. **Financial Calculations**

- Portfolio valuation (stocks + cash + mutual funds)
- Profit/loss tracking
- Real-time price updates with volatility simulation

### 5. **Security Features**

- Password hashing (never store plain passwords)
- Session-based authentication
- Input validation and error handling

### 6. **Business Logic**

- Investment strategy analysis
- Market insights and analytics
- User behavior classification

This application demonstrates a complete web-based trading simulator with user management, real-time data, and administrative features - perfect for learning financial applications and web development concepts!


### Installation

1. Clone this repository
```bash
git clone https://github.com/prajwal032004/dummy-stock-market.git
cd dummy-stock-market
```

2. Run the application
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`


## 🎓 Educational Purpose

This simulator is designed for educational purposes to:
- Learn about stock market investing without financial risk
- Understand portfolio diversification
- Practice investment strategies
- Get familiar with market terminology and concepts

## 🛠️ Future Improvements

- [ ] Add more Indian stocks and mutual funds
- [ ] Implement IPO investments
- [ ] Create different market scenarios (bull/bear markets)
- [ ] Add stock news that impacts prices
- [ ] Implement leaderboard for users

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Contributors

- Your Name - Prajwal

---

⭐ Star this repo if you find it useful! ⭐
