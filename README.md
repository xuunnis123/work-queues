# work-queues
RabbitMQ

# RabbitMQ - Work Queues

###### tags: `RabbitMQ`
1. 先安裝 RabbitMQ server，並啟動
`docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

2. 開發端需要安裝`pip install pika`
`new_task.py`
```python=
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()
```
`worker.py`
```python=
#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
```
3. 總共要執行三個shell，會以round-robin方式執行
shell 1:
`python worker.py`
shell 2:
`python worker.py`
shell 3:
`
python new_task.py First message.
python new_task.py Second message..
python new_task.py Third message...
python new_task.py Fourth message....
python new_task.py Fifth message.....
`

 
 


4. 結果：
 shell 1
 ```shell=
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received 'First message.'
 [x] Done
 [x] Received 'Third message...'
 [x] Done
 [x] Received 'Fifth message.....'
 [x] Done
 ```
 shell 2
```shell=
[*] Waiting for messages. To exit press CTRL+C
[x] Received 'Second message..'
[x] Done
[x] Received 'Fourth message....'
[x] Done
```
