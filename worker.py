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
    time.sleep(body.count(b'.')) #以.作為停幾秒的依據，模擬出該工作忙碌
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    #加入ack，pass訊息給queue，不加的情況下完成的工作會重覆的派送

channel.basic_qos(prefetch_count=1) #代表每一個Consumer每次只會執行一個工作，在ack給Queue之後才會再將下一任務指派給閒置的Consumer
#告訴rabbitmq，用callback來接收訊息
channel.basic_consume(queue='task_queue', on_message_callback=callback)

#開始接收訊息，Queue中有訊息才會調用callback來處理
channel.start_consuming()