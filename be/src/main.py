import sys
sys.path.append('../lib')       # I usually use venvs instead of target lib folder

from flask import Flask, make_response, request
from flask_cors import CORS
from utils import SUPPORTED_MONTHS, SUPPORTED_TYPES, init_log
import traceback
import data

app = Flask(__name__)
CORS(app)

logger = init_log()

@app.route('/getdata', methods=['GET'])
def get_data():
  try:
    request_args = request.args

    months = request_args.get('months')
    type = request_args.get('type')
    steps = request_args.get('steps', 1)    # optional request arg 'steps' for larger forecast - default 1 = tomorrow

    logger.debug(f"months: {months}")
    logger.debug(f"type: {type}")

    if not all([months, type]):
      return make_response({"error": "Missing required parameters"}, 400)

    months_string = SUPPORTED_MONTHS.get(months)

    if type not in SUPPORTED_TYPES or not months_string:
      return make_response({"error": "Unsupported value(s) for argument(s)"}, 400)

    data_df = data.get_data(months_string, type)    
    forecast_series = data.get_multiple_prediction(data_df, steps)
    
    return make_response(data_df.to_json(orient="split"), 200)

  except Exception:
    traceback.print_exc()
    return make_response({"error": "Internal server error"}, 500)


if __name__ == "__main__":
  app.run(port=5000, debug=True)