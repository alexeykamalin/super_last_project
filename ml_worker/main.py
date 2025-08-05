import pika
import logging
from services.crud.prediction import updateprediction
from database.database import get_session
from models.prediction import PredictionUpdate

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
# Настройка логирования 

connection_params = pika.ConnectionParameters(
    host='rabbitmq',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='rmuser',  # Имя пользователя по умолчанию
        password='rmpassword'   # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)

# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    logger.info("1. Задача получена")
    res = 123
    try:
        session = next(get_session())
        prediction = PredictionUpdate(
            status='done',
            id=properties.headers.get('id'),
            a1=properties.headers.get('a1'),
            a2=properties.headers.get('a2'),
            a3=properties.headers.get('a3'),
            g1=properties.headers.get('g1'),
            g2=properties.headers.get('g2'),
            g3=properties.headers.get('g3'),
            i1=properties.headers.get('i1'),
            i2=properties.headers.get('i2'),
            i3=properties.headers.get('i3'),
            ia=properties.headers.get('ia'),
            ig=properties.headers.get('ig'),
            f1=properties.headers.get('f1'),
            f2=properties.headers.get('f2'),
            f3=properties.headers.get('f3'),
            fa=properties.headers.get('fa'),
            fg=properties.headers.get('fg'),
            r1=properties.headers.get('r1'),
            r2=properties.headers.get('r2'),
            r3=properties.headers.get('r3'),
            ra=properties.headers.get('ra'),
            rg=properties.headers.get('rg'),
            pri=properties.headers.get('pri'),
            prm=properties.headers.get('prm'),
            prf=properties.headers.get('prf'),
            prr=properties.headers.get('prr'),
            egkr=properties.headers.get('egkr'),
            result=res
        )
        updateprediction(prediction, properties.headers.get('id'), session)
        logger.info('7. Конец задачи %s',properties.headers.get('id'))
    except Exception as e:
        logger.exception(e)

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True  # Автоматическое подтверждение обработки сообщений
)

channel.start_consuming()