import sys
sys.path.append('../lib')

from flask import Flask, make_response, request
from flask_cors import CORS
from utils import SUPPORTED_MONTHS, SUPPORTED_TYPES, init_log
import traceback
import yfinance as yf

app = Flask(__name__)
CORS(app)

logger = init_log()

@app.route('/getdata', methods=['GET', 'POST'])
def get_data():
  try:
    request_args = request.args

    months = request_args.get('months')
    type = request_args.get('type')

    logger.debug(f"months: {months}")
    logger.debug(f"type: {type}")

    if not all([months, type]):
      return make_response({"error": "Missing required parameters"}, 400)

    months_string = SUPPORTED_MONTHS.get(months)

    if type not in SUPPORTED_TYPES or not months_string:
      return make_response({"error": "Unsupported value(s) for argument(s)"}, 400)


    data_df = yf.download(
        # tickers list or string as well
        tickers = "CORN UGA NDAQ",

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = months_string,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

    # remove unused columns
    remove_columns = [column for column in data_df.columns if column[1] != type]    
    data_df = data_df.drop(remove_columns, axis=1)

    data_df.columns = ["_".join(column) for column in data_df.columns]
    # return make_response({"data": data_df.to_json()}, 200)
    return data_df.to_html()

  except Exception:
    traceback.print_exc()
    return make_response({"error": "Internal server error"}, 500)


if __name__ == "__main__":
  app.run(port=5000, debug=True)