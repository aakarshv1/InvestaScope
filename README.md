# InvestaScope
Envision your financial journey with InvestaScope, a simple Python command-line tool that can yield valuable portfolio performance metrics from a simple csv file of your investment history!

## Tool Setup
1. Set up python virtual environment and activate:
```sh
python(3) -m venv investascope_env
source investascope_env/bin/activate
```
2. Install necessary packages by running the following command:
```sh
pip install -r requirements.txt
```
4. Generate free API Key from [Alpha Vantage](https://www.alphavantage.co/)
5. Input API Key to `configtemplate.ini` and change file name to `config.ini`
6. Generate a CSV file of your activities and orders history from your brokerage platform.

## Usage
- **-f, --csv_file**: Specify the path to the CSV file containing activity/orders history. 
- **-c, --investment_company**: Required. Provide the name of the brokerage platform to correctly interpret the format of the activity/orders history. Currently, only Fidelity Investments is supported.
- **-g, --growth_type**: Required. Choose the type of growth calculation ("money" or "percentage").
- **-d, --include_dividend**: Include this flag to factor in dividends when performing calculations.

Example:
```sh
python plot.py -f investment_data.csv -c Fidelity -g percentage
```
Example Result (Portfolio Percent Change):
![example](https://github.com/aakarshv1/InvestaScope/assets/23005664/e0e2ca07-df63-4bb7-af4c-5341027f4e92)


## Features in Development
- support for more formats of transaction history from various brockerage platforms
- more types of metrics such as sector breakdown and dividend yield
- Docker container for easier setup
   

