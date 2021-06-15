#!/usr/bin/env python
import pika
import sys

# 連接 RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

# 創建頻道
channel = connection.channel()
# 宣告以及創建Queue
channel.queue_declare(queue='task_queue', durable=True) 
#durable:一但RabbitMQ異常中斷，所有的訊息也都會跟著消失，為了確保所有的訊息的保存，我們必需在建立Queue的時候加入參數

message = ' '.join(sys.argv[1:]) or "Hello World!" #設置參數接收外部傳入的字串
'''
不希望透過exchange的話就設為空字串
routing_key則為Queue名稱
'''
channel.basic_publish(
    exchange='', #簡單模式
    routing_key='task_queue', #指定Queue
    body=message, #傳送內容
    properties=pika.BasicProperties(
        delivery_mode=2,  # 1.非永久 ,2.永久 將訊息存在硬碟中，broker重啟後還是會存在
    ))
print(" [x] Sent %r" % message)
connection.close()