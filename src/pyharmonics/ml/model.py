# IMPORTING IMPORTANT LIBRARIES
from pyharmonics.marketdata import BinanceCandleData
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from keras.metrics import mean_squared_error, mean_absolute_percentage_error
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout, LSTM
from copy import deepcopy


def new_dataset(dataset, step_size, predict_size):
    data_X, data_Y = [], []
    for begin in range(len(dataset) - step_size - predict_size - 1):
        end = begin + step_size
        data_X.append(dataset[begin:end])
        data_Y.append(dataset[end:end + predict_size])
    return np.array(data_X), np.array(data_Y)


def get_step_sizes(data, step_size=60, predict_size=2):
    """
    >>> ll = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> new_dataset(ll)
    (array([[1], [2], [3], [4], [5], [6], [7], [8]]), array([2, 3, 4, 5, 6, 7, 8, 9]))
    >>> new_dataset(ll, step_size=2)
    (array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]), array([3, 4, 5, 6, 7, 8, 9]))
    """
    array_steps, array_y = [], []
    for start in range(len(data) - step_size - 1):
        end = start + step_size
        a = data[start:end]
        array_steps.append(a)
        array_y.append(data[end])
    return np.array(array_steps), np.array(array_y)

def get_training_split(series_data, split=.8):
    """
    """
    split_idx = int(len(series_data) * split)
    return series_data[:split_idx], series_data[split_idx:]

def predict_next(model, last_step, scaler, num_steps=10):
    next_step = deepcopy(last_step)
    predict = []
    for i in range(num_steps):
        result = model.predict(next_step)
        predict.append(result[0][0])
        next_step = np.reshape(np.array(list(next_step[0][0])[1:] + [result[0][0]]), (1, 1, step_size))
    return np.array(predict)

def create_model():
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True))
    model.add(Dropout(.4))
    model.add(LSTM(100, activation='relu', return_sequences=False))
    model.add(Dropout(.4))
    model.add(Dense(1))

    # MODEL COMPILING AND TRAINING
    # Try SGD, adam, adagrad and compare!!!
    model.compile(optimizer='adam', loss='mse')
    return model
# FOR REPRODUCIBILITY
np.random.seed(756)

# IMPORTING DATASET
b = BinanceCandleData()
b.get_candles('BTCUSDT', b.DAY_1, 5000)

# Scale and transform data
series_data = b.df[b.CLOSE]
scaler_range = (0, 1)
scaler = MinMaxScaler(feature_range=scaler_range)
series_data = scaler.fit_transform(np.reshape(series_data.values, (len(series_data), 1)))

train_OHLC, test_OHLC = get_training_split(series_data)

# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
step_size = 60
trainX, trainY = new_dataset(train_OHLC, step_size)
testX, testY = new_dataset(test_OHLC, step_size)

# RESHAPING TRAIN AND TEST DATA
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# LSTM MODEL
try:
    model = load_model('BTC_DAY_1.keras')
except OSError as e:
    model = create_model()
    model.fit(trainX, trainY, epochs=5000, batch_size=100, verbose=2)
    model.save('BTC_DAY_1.keras')

# PREDICTION
trainPredict = model.predict(trainX, use_multiprocessing=True)
testPredict = model.predict(testX, use_multiprocessing=True)
last_step = np.reshape(trainY[-step_size:], (1, 1, step_size))
prediction = predict_next(model, last_step, scaler, num_steps=len(testY))


# DE-NORMALIZING FOR PLOTTING
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
prediction = scaler.inverse_transform([prediction])


# TRAINING RMSE
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train RMSE: %.2f' % (trainScore))

# TEST RMSE
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test RMSE: %.2f' % (testScore))

# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
trainPredictPlot = np.empty_like(series_data)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[step_size - 1:len(trainPredict) + step_size - 1, :] = trainPredict

# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
testPredictPlot = np.empty_like(series_data)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict) + (step_size * 2) - 1:len(series_data) - 1, :] = testPredict

freePredictPlot = np.empty_like(series_data)
freePredictPlot[:, :] = np.nan
freePredictPlot[len(trainPredict) + (step_size * 2) - 1: len(series_data) - 1, :] = np.array(prediction[0]).reshape(len(prediction[0]), 1)


b.df['train'] = trainPredictPlot
b.df['test'] = testPredictPlot
b.df['free'] = freePredictPlot

main_plot = make_subplots(
    rows=1, shared_xaxes=True,
    vertical_spacing=0.025,
    row_heights=[1]
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

main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['close'],
        mode="lines",
        line=dict(color='rgba(200, 200, 200, 0.85)', width=1)
    )  # , row=1, col=1
)
main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['train'],
        mode="lines",
        line=dict(color='rgba(80, 200, 80, 0.85)', width=1)
    )  # , row=2, col=1
)
main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['test'],
        mode="lines",
        line=dict(color='rgba(200, 200, 80, 0.85)', width=1)
    )  # , row=2, col=1
)
main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['free'],
        mode="lines",
        line=dict(color='rgba(200, 80, 80, 0.85)', width=1)
    )  # , row=2, col=1
)

main_plot.show()
