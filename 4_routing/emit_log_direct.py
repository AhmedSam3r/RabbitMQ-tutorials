import pika
import sys


def publish_msg():
    host_address = 'localhost'
    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    msg = ' '.join(sys.argv[2:]) or 'Hello World!'
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_address))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct', durable=True)

    channel.basic_publish(exchange='direct_logs',
                          routing_key=severity,
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE

                          ))
    print(f" [x] Sent '{msg}!'")


if __name__ == '__main__':
    # queue_name = input("Enter the name of the queue:\n")
    # msg = input("Enter msg to publish:\n")
    publish_msg()
