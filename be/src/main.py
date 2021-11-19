import sys
sys.path.append('../lib')       # I usually use venvs instead of target lib folder

from flask import Flask, make_response, request
from flask_cors import CORS
import traceback
import pandas as pd
from utils import SUPPORTED_MONTHS, SUPPORTED_TYPES, init_log
import data

app = Flask(__name__)
CORS(app)

logger = init_log()

@app.route('/data', methods=['GET'])
def get_data():
  try:
    request_args = request.args

    months = request_args.get('months')
    type = request_args.get('type')
    steps = 1     # forecast 1 day = tomorrow

    logger.debug(f"months: {months}")
    logger.debug(f"type: {type}")

    if not all([months, type]):
      return make_response({"error": "Missing required parameters"}, 400)

    months_string = SUPPORTED_MONTHS.get(months)

    if type not in SUPPORTED_TYPES or not months_string:
      return make_response({"error": "Unsupported value(s) for argument(s)"}, 400)

    data_df = data.get_data(months_string, type)    
    forecast_df = data.get_multiple_prediction(data_df, steps)

    logger.debug(forecast_df)
    
    return make_response(
      {
        "history": data_df.to_json(orient="split"),
        "forecast": forecast_df.to_json(orient="split")
      },
      200)

  except Exception:
    traceback.print_exc()
    return make_response({"error": "Internal server error"}, 500)


@app.route('/backtest', methods=['GET'])
def get_backtest_data():
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

    data_df = data.get_data(months_string, type)    
    forecast_df = data.get_multiple_prediction(data_df, -len(data_df))

    logger.debug(forecast_df)

    forecast_df.columns = [f"{column}_forecast" for column in data_df.columns]
    data_df = pd.concat([data_df, forecast_df], axis=1)
    
    return make_response(
      {
        "history": data_df.to_json(orient="split"),
        "forecast": forecast_df.to_json(orient="split")
      },
      200)

  except Exception:
    traceback.print_exc()
    return make_response({"error": "Internal server error"}, 500)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)