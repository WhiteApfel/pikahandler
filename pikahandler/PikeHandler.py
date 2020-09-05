import pika
import signal
import sys


class PikaHandler:
	"""
	Класс, который будет отвечать за расределение запросов к вашим функциям. Важная вещь, не надо его обижать.
	Вызывать в начале кода и потом использовать для декорирования.

	Передавать либо `server, port, host, user (optional), password (optional)`, либо `connection=connection`,
	где значение connection - `pika.BlockingConnection(pika.ConnectionParameters(<..>))`

	**Агрументы и атрибуты**

	:param server: домен или IP сервера, по умолчанию 'localhost'
	:type server: ``str``, optional
	:param port: порт сервера, по умолчанию '5672'
	:type port: ``int``, optional
	:param host: адрес очережи, по умолчанию - `/`
	:type host: ``str``, optional
	:param user: пользователь
	:type user: ``str``, optional
	:param password: пароль
	:type password: ``str``, optional
	:param connection: объект соединения
	:type connection: ``pika.BlockingConnection``, optional
	"""
	def __init__(self, server="localhost", port=5672, host="/", user=None, password=None, connection=None):
		if not connection:
			args = [server, port, host]
			if user and password:
				args.append(pika.PlainCredentials(user, password))
			self.connection = pika.BlockingConnection(pika.ConnectionParameters(*args))
			self.channel = self.connection.channel()
		else:
			self.connection = connection
			self.channel = self.connection.channel()
		self.handlers = dict()

		signal.signal(signal.SIGINT, self._close_connection)

	def _close_connection(self, **kwargs):
		print(' [*] You pressed Ctrl+C or killed me with -2')
		self.connection.close()
		print(' [*] Connection closed. By!')
		# .... Put your logic here .....
		sys.exit(0)

	def handler(self, queue: str, func=None):
		"""
		Декоратор для сохранения функции в список обрабатываемых

		**Аргументы**

		:param queue: название очереди
		:type queue: ``str``
		:param func: лямбда-функция или обычная функция, принимающая в себя один аргумент - класс с ключами ``ch``, ``method``, ``properties``, ``body``.
		"""
		def decorator(handler):
			print(f' [*] Function "{handler.__name__}" added to handler for "{queue}" queue')
			if func:
				if queue in self.handlers:
					self.handlers[queue].append({"handler": handler, "filter": func})
				else:
					self.channel.queue_declare(queue=queue)
					self.handlers[queue] = [{"handler": handler, "filter": func}]
				return handler
			else:
				raise ValueError("filter-function 'func' must be function with one argument or lambda")
		return decorator

	def _parse(self, ch, method, properties, body):
		for handler in self.handlers[method.routing_key]:
			if handler["filter"]({"ch": ch, "method": method, "properties": properties, "body": body}):
				handler["handler"](ch, method, properties, body)

	def start(self):
		"""
		Запускает приём и обработку сообщений из очереди.
		"""
		for queue in self.handlers.keys():
			self.channel.basic_consume(queue=queue, on_message_callback=self._parse, auto_ack=True)
		print(' [*] Waiting for messages. To exit press CTRL+C')
		self.channel.start_consuming()
