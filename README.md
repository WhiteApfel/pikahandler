# PikaHandler

Класс-хендлер для удобной работы с обработкой сообщений из RabbitMQ 

### Установка

```shell script
python -m pip install pikahandler
```

### Использование

```python
from pikahandler import PikaHandler

server = '192.168.0.73'
port = 8472
host = "/"
user = "eugene"
password = "spell-thickness-macarena-belie-gawk-fiske-puffy"

# Без авторизации
ph = PikaHandler(server, port, host)

# С авторизацией
ph = PikaHandler(server, port, host, user, password)

# Через connection
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(server, port, host))
ph = PikaHandler(connection=connection)

@ph.handler("main", lambda r: r["body"] == "HelloWorld")
def helloworld(ch, method, poperties, body):
    print(body)

@ph.handler("main", lambda r: r["body"] == "HelloPython")
def hellopython(ch, method, poperties, body):
    print(body)

ph.start()
```