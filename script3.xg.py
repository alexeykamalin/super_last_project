import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

# === Загрузка данных ===
df = pd.read_csv("super_new_dataset.csv", sep=";")

# === Предобработка ===
df = df.drop(columns=["hash"])            # идентификатор не нужен

X = df.drop(columns=["ball"])
y = df["ball"]

# === Разделение ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Обучение модели XGBoost ===
model = XGBRegressor(subsample=0.6, 
                      n_estimators= 300, 
                      max_depth= 4, 
                      learning_rate= 0.01, 
                      gamma= 0.3, 
                      colsample_bytree= 0.6,
                      random_state=42)
model.fit(X_train, y_train)

# === Предсказание ===
y_pred = model.predict(X_test)

# === Метрики ===
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)


print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R^2: {r2:.2f}")


