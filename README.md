# Interactive Stock Visualizer and Predictor

This project allows you to search for stock prices, visualize the prices as candlestick plot and perform predictions using Machine Learning techniques.

The web development framework used is [Django](https://www.djangoproject.com/) , the interface is in JavaScript and the [ChartJs](https://www.chartjs.org/) library.

![moneyshow_web_page](https://github.com/user-attachments/assets/711bfaa3-ae3d-4a39-94d4-b1d9fcb04d4b)

## Features
- 🔎 Search stock prices using [Alpha Vantage](https://www.alphavantage.co/) or [Yahoo Finance](https://finance.yahoo.com/)
- 📈 Interactive visualization of stock prices with [Chart.js](https://www.chartjs.org/) candlestick plot
- 🔮 Perform stock price predictions with Machine Learning algorithms, using [Scikit-learn](https://scikit-learn.org/) and [XGBoost](https://xgboost.readthedocs.io)
- 🌍 Easy-to-use web interface built with Django

## Getting Started

## The Docker way
Building and running a Docker container using the give `Dockerfile` file can be easily performed by using the available scripts:
```bash
chmod u+x docker_build.sh && chmod u+x docker_run.sh # give execution rights to the scripts for the current user
./docker_build.sh && ./docker_run.sh
```
The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000) .

## The Docker Compose way
A [Datadog](https://www.datadoghq.com/) Agent is already configured to analyze the application.
1. Place your precious API KEY in the `.env` file in the root directory of the project - example:
```
DD_API_KEY=__your_precious_beloved_datadog_api_key__
```

2. Starting the Docker Compose using the given `docker-compose.yaml` can be easily performed by using the available script:
```bash
chmod u+x dockercompose_up.sh # give execution rights to the script for the current user
./dockercompose_up.sh
```
The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000) .
The Datadog Agent traces will be available at [Datadog](https://app.datadoghq.eu).

## The manual way
### 0. Requirements
- 🐍 Python 3.10
- 🔑 Alpha Vantage API key (if using Alpha Vantage for stock prices), get one [here](https://www.alphavantage.co/support/#api-key)
- 📦 Required Python packages, listed in `requirements.txt`

### 1. Clone the Repository
```bash
git clone https://github.com/gabripo/moneyshow.git
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

If you're using Alpha Vantage, you'll need to configure your API key 🔑.
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

### 6. Start the Django Server
```bash
python manage.py runserver
```

## Usage

### 1. Search for a stock by symbol

Insert the symbol (ticker) of the stock, then click on "Visualize Stock" to fetch and visualize its data 📈.

You can zoom in the generated graph and reset the zoom with the "Reset Zoom" button above it.

### 2. Predict stock prices

Select a prediction method from the dropdown menu, then click on "Predict" 🔮.


## For the developers
Checkout the repo, open it with Visual Studio Code: debug configurations are there.
You know what to do.

## Future extensions
- Use [skforecast](https://skforecast.org) for time series prediction
- Real-time data fetching
