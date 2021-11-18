from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
import pandas as pd
import utils

logger = utils.init_log()

def get_data(months, type):
  data_df = yf.download(
    # tickers list or string as well
    tickers = "CORN UGA NDAQ",

    # use "period" instead of start/end
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # (optional, default is '1mo')
    period = months,

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

  # remove unused columns (according to specified type arg)
  remove_columns = [column for column in data_df.columns if column[1] != type]    
  data_df = data_df.drop(remove_columns, axis=1)

  # rename and sort columns
  data_df.columns = [column[0] for column in data_df.columns]
  data_df = data_df.reindex(sorted(data_df.columns), axis=1)

  return data_df


def get_prediction(df, steps):
  # Model generation and fit
  model = ARIMA(df, order=(1,1,1))            # naive manual parameters estimation based on used time-series data
  fit_model = model.fit()
  logger.debug(fit_model.summary())

  # Backtest based on last n samples of seen data if n < 0 else forecasting out of sample
  forecast= fit_model.get_prediction(start=steps) if steps < 0 else fit_model.get_forecast(steps=steps)

  # Forecast mean
  mean_forecast = forecast.predicted_mean     # Predicted mean is a pandas series
  logger.debug("Predicted mean:")
  logger.debug(mean_forecast)
  logger.debug("\n\n")

  # Get confidence intervals of forecasts
  confidence_intervals = forecast.conf_int()  # Condence interval method returns pandas DataFrame
  logger.debug("Confidence intervals:")
  logger.debug(confidence_intervals)
  logger.debug("\n\n")

  return mean_forecast


def get_multiple_prediction(data_df, steps):
  frames = []

  for col in data_df.columns:
    forecast_series = get_prediction(data_df[col], steps)
    frames.append(forecast_series.to_frame(name=col))

  return pd.concat(frames, axis=1)
