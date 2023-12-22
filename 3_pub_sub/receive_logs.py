import pika
import os
import sys
import time
import threading


def receive_msg():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Exclusive=True --> once the consumer connection is closed, the queue should be deleted
    channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=False)
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print("QUEUE NAME = ", queue_name)
    channel.queue_bind(exchange='logs', queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done, TAG:", method.delivery_tag)
        print("method = ", method.exchange)
        # ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        receive_msg()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
