from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import pandas as pd
import numpy as np
import joblib

data = pd.read_csv(r'Obesity Predictor\dataset/ObesityDataSet.csv')

target_encoder = LabelEncoder()
data['NObeyesdad'] = target_encoder.fit_transform(data['NObeyesdad'])

encoders = {}

for col in data.drop('NObeyesdad', axis=1).select_dtypes(exclude='number').columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    encoders[col] = le


x = data.drop('NObeyesdad', axis=1)
y = data['NObeyesdad']
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)


model = Sequential([
    Dense(16, activation='relu',
          input_shape=(x_train.shape[1],)),
    Dense(8, activation='relu'),
    Dense(7, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])


model.fit(x_train_scaled,y_train,epochs=250,batch_size=32,validation_split=0.2,verbose=1)
y_pred_prob = model.predict(x_test_scaled)
y_pred = np.argmax(y_pred_prob, axis=1)

print("*" * 50)
print("MODEL EVALUATION")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("*" * 50)

model.save("obesity_ann_model.keras")
joblib.dump(scaler, "obesity_scaler.pkl")
joblib.dump(encoders, "feature_encoders.pkl")
joblib.dump( target_encoder,"target_encoder.pkl")

print("Model Saved Successfully")
print("Scaler Saved Successfully")
print("Feature Encoders Saved Successfully")
print("Target Encoder Saved Successfully")
print("*" * 50)