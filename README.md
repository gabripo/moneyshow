# Interactive Stock Visualizer and Predictor

This project allows you to search for stock prices using Alpha Vantage (API required) or Yahoo Finance, visualize the prices using Graph.js (candlestick plot), and perform predictions using Machine Learning techniques.

The web development framework used is Django.

## Features
- Search stock prices using Alpha Vantage or Yahoo Finance
- Visualize stock prices with Graph.js candlestick plot
- Perform stock price predictions with Machine Learning algorithms
- Easy-to-use web interface built with Django

## Requirements
- Python 3.x
- Alpha Vantage API key (if using Alpha Vantage for stock prices)
- Required Python packages (listed in `requirements.txt`)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/stock-price-visualizer.git
cd stock-price-visualizer
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage your dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using the requirements.txt file.

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

If you're using Alpha Vantage, you'll need to configure your API key.
- Create a folder named `proj_secrets` in the project root directory.
- Create a `__init__.py` file in the created folder.
- Add your Alpha Vantage API key into the `__init__.py` file:
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

### 7. Search for a stock by symbol

Insert the symbol (ticker) of the stock, then click on "Visualize Stock" to fetch its data.

### 8. (Optional) Predict stock prices

Select a prediction method from the dropdown menu, then click on "Predict".

Open your browser and navigate to http://127.0.0.1:8000 to access the application.
