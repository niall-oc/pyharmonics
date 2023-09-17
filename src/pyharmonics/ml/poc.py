# IMPORTING IMPORTANT LIBRARIES
from pyharmonics.marketdata import BinanceCandleData
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM


def new_dataset(dataset, step_size):
    data_X, data_Y = [], []
    for i in range(len(dataset) - step_size - 1):
        a = dataset[i:(i + step_size), 0]
        data_X.append(a)
        data_Y.append(dataset[i + step_size, 0])
    return np.array(data_X), np.array(data_Y)

# FOR REPRODUCIBILITY
np.random.seed(756)

# IMPORTING DATASET
b = BinanceCandleData()
b.get_candles('BTCUSDT', b.HOUR_4, 5000)


# TAKING DIFFERENT INDICATORS FOR PREDICTION
OHLC_avg = b.df[b.CLOSE]

# PREPARATION OF TIME SERIES DATASE
OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg), 1))
scaler = MinMaxScaler(feature_range=(0, 1))
OHLC_avg = scaler.fit_transform(OHLC_avg)

# TRAIN-TEST SPLIT
train_OHLC = int(len(OHLC_avg) * 0.75)
test_OHLC = len(OHLC_avg) - train_OHLC
train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC, :], OHLC_avg[train_OHLC:len(OHLC_avg), :]

# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
trainX, trainY = new_dataset(train_OHLC, 1)
testX, testY = new_dataset(test_OHLC, 1)

# RESHAPING TRAIN AND TEST DATA
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
step_size = 1

# LSTM MODEL
model = Sequential()
model.add(LSTM(32, input_shape=(1, step_size), return_sequences=True))
model.add(LSTM(16))
model.add(Dense(1))
model.add(Activation('linear'))

# MODEL COMPILING AND TRAINING
model.compile(loss='mean_squared_error', optimizer='adagrad')  # Try SGD, adam, adagrad and compare!!!
model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

# PREDICTION
trainPredict = model.predict(trainX, use_multiprocessing=True)
testPredict = model.predict(testX, use_multiprocessing=True)

# DE-NORMALIZING FOR PLOTTING
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])


# TRAINING RMSE
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train RMSE: %.2f' % (trainScore))

# TEST RMSE
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test RMSE: %.2f' % (testScore))

# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
trainPredictPlot = np.empty_like(OHLC_avg)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[step_size:len(trainPredict) + step_size, :] = trainPredict

# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
testPredictPlot = np.empty_like(OHLC_avg)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict) + (step_size * 2) + 1:len(OHLC_avg) - 1, :] = testPredict

# DE-NORMALIZING MAIN DATASET
OHLC_avg = scaler.inverse_transform(OHLC_avg)
b.df['OHLC_avg'] = OHLC_avg
b.df['train'] = trainPredictPlot
b.df['test'] = testPredictPlot

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
        y=b.df['OHLC_avg'],
        mode="lines",
        line=dict(color='rgba(200, 200, 200, 0.85)', width=1)
    )
)
main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['train'],
        mode="lines",
        line=dict(color='rgba(80, 200, 80, 0.85)', width=1)
    )
)
main_plot.add_trace(
    go.Scatter(
        x=b.df.index,
        y=b.df['test'],
        mode="lines",
        line=dict(color='rgba(200, 200, 80, 0.85)', width=1)
    )
)

main_plot.show()
# PLOT OF MAIN OHLC VALUES, TRAIN PREDICTIONS AND TEST PREDICTIONS
# plt.plot(OHLC_avg, 'g', label = 'original dataset')
# plt.plot(trainPredictPlot, 'r', label = 'training set')
# plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
# plt.legend(loc = 'upper right')
# plt.xlabel('Time in Days')
# plt.ylabel('OHLC Value of Apple Stocks')
# plt.show()

# PREDICT FUTURE VALUES
last_val = testPredict[-1]
last_val_scaled = last_val / last_val
next_val = model.predict(np.reshape(last_val_scaled, (1, 1, 1)))
print("Last Day Value:", np.ndarray.item(last_val))
print("Next Day Value:", np.ndarray.item(last_val * next_val))
# print np.append(last_val, next_val)
