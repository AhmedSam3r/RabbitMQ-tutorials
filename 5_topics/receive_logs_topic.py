import pika
import os
import sys
import time


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def receive_msg():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Exclusive=True --> once the consumer connection is closed, the queue should be deleted
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic', durable=True)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key] ex: facility.severity\n" % sys.argv[0])
        sys.exit(1)

    for severity in binding_keys:
        channel.queue_bind(exchange='topic_logs',
                           queue=queue_name,
                           routing_key=severity)

    channel.basic_consume(queue=queue_name,
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
