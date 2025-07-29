import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, max_error
from sklearn.ensemble import GradientBoostingRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR

from sklearn.model_selection import GridSearchCV



# Улучшенный пайплайн моделирования
def build_advanced_models():
    # 1. Ансамбль моделей
    base_models = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('xgb', XGBRegressor(random_state=42)),

        ('svr', SVR(kernel='rbf'))
    ]
    
    stacking_model = StackingRegressor(
        estimators=base_models,
        final_estimator=LinearRegression()
    )
    
    # 2. Пайплайн с предобработкой
    models = {
        "Polynomial Regression": Pipeline([
            ('poly', PolynomialFeatures(degree=2)),
            ('scaler', StandardScaler()),
            ('lr', LinearRegression())
        ]),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200, learning_rate=0.05, random_state=42
        ),
        "Stacking Ensemble": stacking_model,
        "XGBoost": XGBRegressor(
            n_estimators=300, max_depth=5, learning_rate=0.1, random_state=42
        )
    }
    
    return models


def postprocess_predictions(y_pred, y_train):
    # 1. Округление до ближайшего реального значения из train
    unique_values = np.sort(y_train.unique())
    y_pred_rounded = np.array([unique_values[np.argmin(np.abs(unique_values - val))] for val in y_pred])
    
    # 2. Калибровка предсказаний
    q_train = np.percentile(y_train, np.linspace(0, 100, 101))
    q_pred = np.percentile(y_pred, np.linspace(0, 100, 101))
    y_pred_calibrated = np.interp(y_pred, q_pred, q_train)
    
    # 3. Ограничение диапазона
    y_pred_final = np.clip(y_pred_calibrated, y_train.min(), y_train.max())
    
    return y_pred_final

def advanced_model_analysis(models, X_train, X_test, y_train, y_test):
    results = []
    
    for name, model in models.items():
        # Обучение модели
        model.fit(X_train, y_train)
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.05, 0.1]
        }

        xgb = XGBRegressor(random_state=42)
        grid_search = GridSearchCV(xgb, param_grid, cv=5, scoring='neg_mean_absolute_error')
        grid_search.fit(X_train, y_train)
        best_xgb = grid_search.best_estimator_
        print(name, best_xgb)
        
        # Предсказания
        y_pred = model.predict(X_test)
        
        # Постобработка
        y_pred_processed = postprocess_predictions(y_pred, y_train)
        
        # Метрики
        metrics = {
            'Model': name,
            'R2': r2_score(y_test, y_pred_processed),
            'MAE': mean_absolute_error(y_test, y_pred_processed),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_processed)),
            'Max Error': max_error(y_test, y_pred_processed)
        }
        results.append(metrics)
    
    # Сравнительная таблица метрик
    results_df = pd.DataFrame(results)
    print("\nСравнение моделей:")
    print(results_df.sort_values('MAE', ascending=False))
    
    return results_df

# Основной пайплайн
df = pd.read_csv("super_new_dataset.csv", sep=';')

# Разделение данных
X = df.drop(columns=["hash", "ball"])
y = df["ball"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Построение и оценка моделей
models = build_advanced_models()
results = advanced_model_analysis(models, X_train, X_test, y_train, y_test)

# Анализ остатков лучшей модели
best_model_name = results.iloc[results['MAE'].idxmax()]['Model']
best_model = models[best_model_name]
y_pred = postprocess_predictions(best_model.predict(X_test), y_train)
residuals = y_test - y_pred