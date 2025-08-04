from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor
import numpy as np
import pandas as pd

# Параметры для подбора
param_dist = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [3, 4, 5, 6, 8],
    "learning_rate": [0.01, 0.05, 0.1, 0.2],
    "subsample": [0.6, 0.8, 1.0],
    "colsample_bytree": [0.6, 0.8, 1.0],
    "gamma": [0, 0.1, 0.3, 1]
}

# Модель
xgb = XGBRegressor(random_state=42)

# RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=30,  # число комбинаций
    scoring="neg_mean_absolute_error",  # можно также "r2"
    cv=5,
    verbose=1,
    random_state=42,
    n_jobs=-1  # использовать все ядра
)
df = pd.read_csv("super_new_dataset.csv", sep=";")
df = df.drop(columns=["hash"])            # идентификатор не нужен

X = df.drop(columns=["ball"])
y = df["ball"]

# Обучение
random_search.fit(X, y)

# Лучшие параметры
print("Лучшие параметры:")
print(random_search.best_params_)

# Лучшая модель
best_model = random_search.best_estimator_

# Оценка на кросс-валидации
from sklearn.model_selection import cross_val_score
r2 = cross_val_score(best_model, X, y, cv=5, scoring="r2")
print(f"Среднее R²: {r2.mean():.3f}")
