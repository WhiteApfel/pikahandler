Как пользоваться
================

Это обычный декоратор, который не нарушает существующий код. Однако стоит обратить внимание, что лямбда-функция фильтра принимает не четыре аргумента, а один - словарь. Аргументы аналогичны исходным в pika.

::

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
   def helloworld(ch, method, properties, body):
       print(body)

   @ph.handler("main", lambda r: r["body"] == "HelloPython")
   def hellopython(ch, method, properties, body):
       print(body)

   ph.start()
