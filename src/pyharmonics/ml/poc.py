# IMPORTING IMPORTANT LIBRARIES
from pyharmonics.marketdata import BinanceCandleData
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, RepeatVector, TimeDistributed


def new_dataset(dataset, step_size, predict_size):
    data_X, data_Y = [], []
    for begin in range(len(dataset) - step_size - predict_size - 1):
        end = begin + step_size
        data_X.append(dataset[begin:end])
        data_Y.append(dataset[end:end + predict_size])
    return np.array(data_X), np.array(data_Y)

# FOR REPRODUCIBILITY
np.random.seed(756)

# IMPORTING DATASET
b = BinanceCandleData()
b.get_candles('BTCUSDT', b.HOUR_4, 5000)


# TAKING DIFFERENT INDICATORS FOR PREDICTION
columns = [b.OPEN, b.HIGH, b.LOW, b.CLOSE, b.VOLUME]
candles = b.df[columns]

scaler_range = (0, 1)
scaler = MinMaxScaler(feature_range=scaler_range)

# PREPARATION OF TIME SERIES DATASE
OHLCV = np.reshape(candles.values, (len(candles), len(columns)))

# TRAIN-TEST SPLIT
train_OHLC = int(len(OHLCV) * 0.75)
test_OHLC = len(OHLCV) - train_OHLC
train_OHLC, test_OHLC = OHLCV[0:train_OHLC, :], OHLCV[train_OHLC:len(OHLCV), :]

# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
num_steps = 30
num_features = len(columns)
num_predicts = 2
num_neurons = num_features + num_predicts
trainX, trainY = new_dataset(train_OHLC, num_steps, num_predicts)
testX, testY = new_dataset(test_OHLC, num_steps, num_predicts)

trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], num_features))
testX = testX.reshape((testX.shape[0], testX.shape[1], num_features))

# LSTM MODEL
def create_model(num_features, num_steps, num_predicts):
    num_neurons = num_features + num_predicts
    model = Sequential()
    model.add(LSTM(num_neurons, activation='relu', input_shape=(num_steps, num_features)))
    model.add(RepeatVector(num_predicts))
    model.add(LSTM(num_neurons, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(num_features)))
    model.compile(optimizer='adam', loss='mse')
    return model

try:
    model = load_model('BTC_DAY_1.keras')
except OSError as e:
    model = create_model(num_features, num_steps, num_predicts)
    model.fit(trainX, trainY, epochs=500, batch_size=100, verbose=2)
    model.save('BTC_DAY_1.keras')

# PREDICTION
trainPredict = model.predict(trainX, use_multiprocessing=True)
testPredict = model.predict(testX, use_multiprocessing=True)


# TRAINING RMSE
trainmScore = [mean_squared_error(trainY[i], trainPredict[i], squared=False) for i in range(len(trainY))]
print('Train RMSE: %.2f' % (trainmScore[-1]))

# TEST RMSE
testmScore = [mean_squared_error(testY[i], testPredict[i], squared=False) for i in range(len(testY))]
print('Test RMSE: %.2f' % (testmScore[-1]))

# TRAINING RMSE
trainpScore = [mean_absolute_percentage_error(trainY[i], trainPredict[i]) for i in range(len(trainY))]
print('Train RMAPE: %.2f' % (trainpScore[-1]))

# TEST RMSE
testpScore = [mean_absolute_percentage_error(testY[i], testPredict[i]) for i in range(len(testY))]
print('Test RMAPE: %.2f' % (testpScore[-1]))

# Next n predictions
print("next train", trainPredict[-1])
print("Next test", testPredict[-1])


main_plot = make_subplots(
    rows=3, shared_xaxes=True,
    vertical_spacing=0.025,
    row_heights=[.4, .3, .3]
)
fonts = dict(
    font=dict(
        family="Courier New, monospace, bold",
        size=15
    ),
    title_font_size=38
)
main_plot.update_layout(
    xaxis_rangeslider_visible=False,
    template='plotly_dark',
    showlegend=False,
    title={
        'text': 'learn',
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    **fonts
)
train_df = b.df[:len(trainmScore)].copy()
main_plot.add_trace(
    go.Candlestick(
        x=list(range(len(trainmScore))),
        open=train_df[b.OPEN],
        high=train_df[b.HIGH],
        close=train_df[b.CLOSE],
        low=train_df[b.LOW],
    ),
    row=1, col=1
)

main_plot.add_trace(
    go.Scatter(
        x=list(range(len(trainmScore))),
        y=trainmScore,
        mode="lines",
        line=dict(color='rgba(200, 200, 80, 0.85)', width=1)
    ),
    row=2, col=1
)
main_plot.add_trace(
    go.Scatter(
        x=list(range(len(trainpScore))),
        y=trainpScore,
        mode="lines",
        line=dict(color='rgba(250, 100, 80, 0.85)', width=1)
    ), row=3, col=1
)
main_plot.show()
