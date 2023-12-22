import pika
import sys


def publish_msg():
    host_address='localhost'
    msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_address))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=False)

    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE

                          ))
    print(f" [x] Sent '{msg}!'")


if __name__ == '__main__':
    # queue_name = input("Enter the name of the queue:\n")
    # msg = input("Enter msg to publish:\n")
    publish_msg()
