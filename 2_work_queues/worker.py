import pika
import os
import sys
import time
import threading


def receive_msg():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='mq')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done, TAG:", method.delivery_tag)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='task_queue',
                        on_message_callback=callback)

    channel.basic_qos(prefetch_count=2)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    # connection.close()


if __name__ == '__main__':
    try:
        
        receive_msg()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
