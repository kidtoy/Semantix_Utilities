import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

df = pd.read_csv("~/Downloads/measurements_per_sensor_train.csv")
df1 = df.drop(labels="vendor", axis=1)
df2 = df1.drop(labels="id_campaign", axis=1)
df3 = df2.drop(labels="ssid", axis=1)
df4 = df3.drop(labels="Unnamed: 0", axis=1)
df5 = df4.drop(labels="mac_address", axis=1)
df6 = df5.drop(labels="date_time", axis=1)
# df7 = df6.drop(labels="total.all.sensors", axis=1)
# df8 = df7.drop(labels="closest.sensor.x", axis=1)
# df9 = df8.drop(labels="second.closest.sensor.x", axis=1)
# df10 = df9.drop(labels="closest.sensor.y", axis=1)
# df11 = df10.drop(labels="second.closest.sensor.y", axis=1)
# df12 = df11.drop(labels="closest.sensor.z", axis=1)
# df13 = df12.drop(labels="second.closest.sensor.z", axis=1)
df14 = df6.drop(labels="closest.sensor.id", axis=1)
df15 = df14.drop(labels="second.closest.sensor.id", axis=1)
df16 = df15.replace(to_replace=100, value=-100)

dfB = pd.read_csv("~/Downloads/challenge_test_set2.csv") # Conjunto de testes
# result = pd.read_csv("~/Downloads/results.csv")

dfB1 = dfB.drop(labels="vendor", axis=1)
dfB2 = dfB1.drop(labels="id_campaign", axis=1)
dfB3 = dfB2.drop(labels="ssid", axis=1)
dfB5 = dfB3.drop(labels="mac_address", axis=1)
dfB6 = dfB5.drop(labels="date_time", axis=1)
# dfB7 = dfB6.drop(labels="total.all.sensors", axis=1)
# dfB8 = dfB7.drop(labels="closest.sensor.x", axis=1)
# dfB9 = dfB8.drop(labels="second.closest.sensor.x", axis=1)
# dfB10 = dfB9.drop(labels="closest.sensor.y", axis=1)
# dfB11 = dfB10.drop(labels="second.closest.sensor.y", axis=1)
# dfB12 = dfB11.drop(labels="closest.sensor.z", axis=1)
# dfB13 = dfB12.drop(labels="second.closest.sensor.z", axis=1)
dfB14 = dfB6.drop(labels="closest.sensor.id", axis=1)
dfB15 = dfB14.drop(labels="second.closest.sensor.id", axis=1)
dfTesting = dfB15.replace(to_replace=100, value=-100)
#
print(dfTesting.shape)

X = df16.drop('pos',axis=1)
y = df16['pos']

X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()

scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(224,36),max_iter=10000)
mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))

# print(predictions)

predictions = mlp.predict(dfTesting)

print(predictions)
# print(confusion_matrix(result,predictions))
# print(classification_report(result,predictions))