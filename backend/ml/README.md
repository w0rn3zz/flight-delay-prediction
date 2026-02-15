# ML Models Technical Documentation

Техническая документация по работе с моделями машинного обучения.

## Обзор

Все модели решают задачу **бинарной классификации** — предсказание задержки авиарейса.

- **Классы:** `False` (без задержки), `True` (задержка)
- **Моделей:** 4 (CatBoost Default/Optimized, LightGBM Default/Optimized)

---

## Входные данные (Features)

| # | Название | Тип | Описание | Диапазон / Примеры |
|---|----------|-----|----------|-------------------|
| 0 | `Month` | int | Месяц вылета | 1-12 |
| 1 | `DayofMonth` | int | День месяца | 1-31 |
| 2 | `DayOfWeek` | int | День недели | 1-7 (1=Пн, 7=Вс) |
| 3 | `DepTime` | int | Время вылета в формате HHMM | 0-2359 (например, 1430 = 14:30) |
| 4 | `UniqueCarrier` | str/int | Код авиакомпании | "AA", "UA", "DL" или Label Encoded |
| 5 | `Origin` | str/int | Код аэропорта отправления | "LAX", "JFK" или Label Encoded |
| 6 | `Dest` | str/int | Код аэропорта назначения | "ORD", "ATL" или Label Encoded |
| 7 | `Distance` | int | Расстояние в милях | 0-5000+ |

**Порядок фичей критически важен!**

---

## CatBoost Models

### Загрузка

```python
import pickle

with open('ml/catboost_default_model.pkl', 'rb') as f:
    model = pickle.load(f)

# или optimized версия
with open('ml/catboost_optimized_model.pkl', 'rb') as f:
    model = pickle.load(f)
```

### Формат входных данных

CatBoost принимает **pandas DataFrame** с категориальными колонками как строки:

```python
import pandas as pd

data = pd.DataFrame([{
    'Month': 7,
    'DayofMonth': 15,
    'DayOfWeek': 3,
    'DepTime': 1430,
    'UniqueCarrier': 'AA',  # строка!
    'Origin': 'LAX',        # строка!
    'Dest': 'JFK',          # строка!
    'Distance': 2475
}])
```

### Предсказание

```python
# Класс (True/False)
prediction = model.predict(data)
# >>> array([False])

# Вероятности [P(no_delay), P(delay)]
probabilities = model.predict_proba(data)
# >>> array([[0.9377, 0.0623]])

# Вероятность задержки
delay_probability = probabilities[0][1]  # 0.0623 = 6.23%
```

### Выходные данные

| Метод | Возвращает | Shape | Пример |
|-------|-----------|-------|--------|
| `predict(X)` | numpy.ndarray[bool] | (n_samples,) | `[False, True, False]` |
| `predict_proba(X)` | numpy.ndarray[float] | (n_samples, 2) | `[[0.94, 0.06], [0.30, 0.70]]` |

### Дополнительные методы

```python
# Названия фичей
model.feature_names_
# >>> ['Month', 'DayofMonth', 'DayOfWeek', 'DepTime', 'UniqueCarrier', 'Origin', 'Dest', 'Distance']

# Индексы категориальных фичей
model.get_cat_feature_indices()
# >>> [0, 1, 2, 4, 5, 6]

# Feature importance
importance = model.get_feature_importance()
# >>> array([7.72, 6.66, 5.75, 40.63, 11.28, 9.93, 10.66, 7.38])

# Feature importance с именами
list(zip(model.feature_names_, importance))
# >>> [('Month', 7.72), ('DayofMonth', 6.66), ...]
```

---

## LightGBM Models

### Загрузка

```python
import joblib

model = joblib.load('ml/lightgbm_default_model.pkl')

# или optimized версия
model = joblib.load('ml/lightgbm_optimized_model.pkl')
```

### Формат входных данных

**ВАЖНО:** LightGBM требует **numpy array** с числовыми данными.
Категориальные признаки должны быть предварительно закодированы (Label Encoding).

```python
import numpy as np

# Категории закодированы как числа!
data = np.array([[
    7,      # Month
    15,     # DayofMonth
    3,      # DayOfWeek
    1430,   # DepTime
    5,      # UniqueCarrier (Label Encoded: AA=0, UA=1, DL=2, ...)
    100,    # Origin (Label Encoded: LAX=100, JFK=50, ...)
    200,    # Dest (Label Encoded)
    2475    # Distance
]])
```

### Предсказание

```python
# Класс (True/False)
prediction = model.predict(data)
# >>> array([False])

# Вероятности [P(no_delay), P(delay)]
probabilities = model.predict_proba(data)
# >>> array([[0.8732, 0.1268]])

# Вероятность задержки
delay_probability = probabilities[0][1]  # 0.1268 = 12.68%
```

### Batch предсказания

```python
# Несколько записей одновременно
batch_data = np.array([
    [7, 15, 3, 1430, 5, 100, 200, 2475],
    [12, 25, 1, 600, 2, 50, 150, 1000],
    [1, 1, 7, 2200, 0, 0, 0, 500],
])

predictions = model.predict(batch_data)
# >>> array([False, False, True])

probabilities = model.predict_proba(batch_data)
# >>> array([[0.888, 0.112],
#            [0.993, 0.007],
#            [0.377, 0.623]])
```

### Дополнительные методы

```python
# Названия фичей
model.feature_name_
# >>> ['Month', 'DayofMonth', 'DayOfWeek', 'DepTime', 'UniqueCarrier', 'Origin', 'Dest', 'Distance']

# Количество фичей
model.n_features_in_
# >>> 8

# Классы
model.classes_
# >>> array([False, True])

# Feature importance (количество splits)
model.feature_importances_
# >>> array([109, 556, 56, 353, 114, 821, 862, 129])
```

---

## Сравнение использования

| Аспект | CatBoost | LightGBM |
|--------|----------|----------|
| Загрузка | `pickle.load()` | `joblib.load()` |
| Формат входа | pandas DataFrame | numpy array |
| Категории | Строки (автообработка) | Label Encoded (числа) |
| Выход predict | `np.ndarray[bool]` | `np.ndarray[bool]` |
| Выход predict_proba | `np.ndarray[float]` shape (n, 2) | `np.ndarray[float]` shape (n, 2) |

---

## Примеры для API

### Pydantic схема запроса

```python
from pydantic import BaseModel, Field

class FlightPredictionRequest(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Месяц (1-12)")
    day_of_month: int = Field(..., ge=1, le=31, description="День месяца")
    day_of_week: int = Field(..., ge=1, le=7, description="День недели")
    dep_time: int = Field(..., ge=0, le=2359, description="Время вылета HHMM")
    carrier: str = Field(..., min_length=2, max_length=3, description="Код авиакомпании")
    origin: str = Field(..., min_length=3, max_length=4, description="Аэропорт отправления")
    dest: str = Field(..., min_length=3, max_length=4, description="Аэропорт назначения")
    distance: int = Field(..., ge=0, description="Расстояние в милях")
```

### Pydantic схема ответа

```python
class FlightPredictionResponse(BaseModel):
    delayed: bool
    delay_probability: float = Field(..., ge=0, le=1)
    no_delay_probability: float = Field(..., ge=0, le=1)
    model_used: str
    prediction_id: str
```

### Сервис предсказания

```python
import pandas as pd
import numpy as np
from uuid import uuid4

class PredictionService:
    def __init__(self, catboost_model, lightgbm_model, label_encoders: dict):
        self.catboost = catboost_model
        self.lightgbm = lightgbm_model
        self.encoders = label_encoders  # {'UniqueCarrier': encoder, 'Origin': encoder, 'Dest': encoder}
    
    def predict_catboost(self, request: FlightPredictionRequest) -> FlightPredictionResponse:
        df = pd.DataFrame([{
            'Month': request.month,
            'DayofMonth': request.day_of_month,
            'DayOfWeek': request.day_of_week,
            'DepTime': request.dep_time,
            'UniqueCarrier': request.carrier,
            'Origin': request.origin,
            'Dest': request.dest,
            'Distance': request.distance
        }])
        
        proba = self.catboost.predict_proba(df)[0]
        
        return FlightPredictionResponse(
            delayed=bool(proba[1] > 0.5),
            delay_probability=float(proba[1]),
            no_delay_probability=float(proba[0]),
            model_used='catboost',
            prediction_id=str(uuid4())
        )
    
    def predict_lightgbm(self, request: FlightPredictionRequest) -> FlightPredictionResponse:
        # Encode categorical features
        carrier_encoded = self.encoders['UniqueCarrier'].transform([request.carrier])[0]
        origin_encoded = self.encoders['Origin'].transform([request.origin])[0]
        dest_encoded = self.encoders['Dest'].transform([request.dest])[0]
        
        data = np.array([[
            request.month,
            request.day_of_month,
            request.day_of_week,
            request.dep_time,
            carrier_encoded,
            origin_encoded,
            dest_encoded,
            request.distance
        ]])
        
        proba = self.lightgbm.predict_proba(data)[0]
        
        return FlightPredictionResponse(
            delayed=bool(proba[1] > 0.5),
            delay_probability=float(proba[1]),
            no_delay_probability=float(proba[0]),
            model_used='lightgbm',
            prediction_id=str(uuid4())
        )
```

---

## Данные для сохранения в БД

### Таблица predictions

```sql
CREATE TABLE predictions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Input data
    month INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    dep_time INT NOT NULL,
    carrier VARCHAR(3) NOT NULL,
    origin VARCHAR(4) NOT NULL,
    dest VARCHAR(4) NOT NULL,
    distance INT NOT NULL,
    
    -- Output data
    model_name VARCHAR(50) NOT NULL,
    predicted_delayed BOOLEAN NOT NULL,
    delay_probability FLOAT NOT NULL,
    
    -- Metadata
    latency_ms INT,
    client_ip VARCHAR(45),
    user_agent TEXT
);
```

### Таблица feedback (для мониторинга качества)

```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY,
    prediction_id UUID REFERENCES predictions(id),
    actual_delayed BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Важные замечания

1. **Label Encoders для LightGBM:** При обучении LightGBM использовались Label Encoders для категориальных признаков. Необходимо сохранить эти encoders или создать mapping вручную.

2. **Unknown categories:** Если на вход придёт неизвестная авиакомпания или аэропорт:
   - CatBoost: обработает автоматически
   - LightGBM: выбросит ошибку или даст некорректный результат

3. **Валидация DepTime:** Формат HHMM означает, что валидные значения: 0-59 для минут, 0-23 для часов. Например, 1465 — невалидное время.

4. **Threshold:** По умолчанию threshold = 0.5. Можно настроить для баланса precision/recall.