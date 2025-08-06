import pika
import logging
import joblib
import pandas as pd
from services.crud.prediction import updateprediction
from database.database import get_session
from models.prediction import PredictionUpdate
import json
import numpy as np

# Загрузка модели (добавьте этот код в начало файла)
# Предполагается, что модель сохранена как 'xgboost_model.joblib'
try:
    model = joblib.load('modle.joblib')
    
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    raise

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

connection_params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username='rmuser',
        password='rmpassword'
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body):
    logger.info("1. Задача получена")
    try:
        # Парсим JSON из тела сообщения
        data = json.loads(body)
        prediction_id = properties.headers.get('id')
        
        # Порядок признаков ДОЛЖЕН совпадать с порядком при обучении модели!
        features_order = [
            'egkr', 'a1', 'a2', 'a3', 'ag', 
            'g1', 'g2', 'g3', 'gg', 
            'i1', 'i2', 'i3', 'ia', 'ig', 
            'f1', 'f2', 'f3', 'fa', 'fg', 
            'r1', 'r2', 'r3', 'ra', 'rg', 
            'pri', 'prm', 'prf', 'prr'
        ]
        
        # Создаем список значений в правильном порядке
        values = []
        for feature in features_order:
            try:
                # Пытаемся преобразовать в int, если не получается - используем 0
                val = int(float(data.get(feature, 0)))  # Двойное преобразование для случаев типа "5.0"
            except (ValueError, TypeError):
                val = 0
                logger.warning(f"Некорректное значение для {feature}: {data.get(feature)}")
            values.append(val)
        
        # Преобразуем в numpy array с явным указанием типа
        data_array = np.array([values], dtype=np.float32)  # XGBoost работает лучше с float32
        
        res = str(int(model.predict(data_array)[0]))
        
        # Логирование для отладки
        logger.debug(f"Данные для предсказания: {data_array}")
        logger.debug(f"Тип данных: {data_array.dtype}")
        logger.debug(f"Результат: {res}")
        
        # Сохранение результата
        session = next(get_session())
        prediction = PredictionUpdate(
            status='done',
            id=prediction_id,
            a1=values[features_order.index('a1')],
            a2=values[features_order.index('a2')],
            a3=values[features_order.index('a3')],
            ag=values[features_order.index('ag')],
            g1=values[features_order.index('g1')],
            g2=values[features_order.index('g2')],
            g3=values[features_order.index('g3')],
            gg=values[features_order.index('gg')],
            i1=values[features_order.index('i1')],
            i2=values[features_order.index('i2')],
            i3=values[features_order.index('i3')],
            ia=values[features_order.index('ia')],
            ig=values[features_order.index('ig')],
            f1=values[features_order.index('f1')],
            f2=values[features_order.index('f2')],
            f3=values[features_order.index('f3')],
            fa=values[features_order.index('fa')],
            fg=values[features_order.index('fg')],
            r1=values[features_order.index('r1')],
            r2=values[features_order.index('r2')],
            r3=values[features_order.index('r3')],
            ra=values[features_order.index('ra')],
            rg=values[features_order.index('rg')],
            pri=values[features_order.index('pri')],
            prm=values[features_order.index('prm')],
            prf=values[features_order.index('prf')],
            prr=values[features_order.index('prr')],
            egkr=values[features_order.index('egkr')],
            result=res
        )
        updateprediction(prediction, prediction_id, session)
        logger.info(f'7. Конец задачи {prediction_id}, результат: {res}')
    except Exception as e:
        logger.exception(f"Ошибка при обработке задачи {prediction_id}:")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()