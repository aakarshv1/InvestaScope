# InvestaScope
Envisioning Your Financial Journey!

## Tool Setup
1. Set up python virtual environment:
```sh
python(3) -m venv investascope_env
```   
2. Generate free API Key from [Alpha Vantage](https://www.alphavantage.co/)
3. Input API Key to `configtemplate.ini` and change file name to `config.ini`

## Usage
- **-f, --csv_file**: Specify the path to the CSV file containing transaction history 
- **-c, --investment_company**: Required. Provide the name of the investment company to correctly interpret the format of the transaction history.
- **-g, --growth_type**: Required. Choose the type of growth calculation ("money" or "percentage")
- **-d, --include_dividend**: Include this flag to factor in dividends when performing calculations.

Example:
```sh
python plot.py -f investment_data.csv -c Fidelity -g percentage
```
Example Result (Portfolio Percent Change):
![example](https://github.com/aakarshv1/InvestaScope/assets/23005664/e0e2ca07-df63-4bb7-af4c-5341027f4e92)


## Features Currently in Development
- support for more formats of transaction history from various brockerage platforms
- more types of metrics such as sector breakdown and dividend yield
   

