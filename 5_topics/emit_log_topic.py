import pika
import sys


def publish_msg():
    host_address = 'localhost'
    binding_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    msg = ' '.join(sys.argv[2:]) or 'Hello World!'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host_address))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic', durable=True)

    channel.basic_publish(exchange='topic_logs',
                          routing_key=binding_key,
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE

                          ))
    print(f" [x] Sent '{msg}!'")


if __name__ == '__main__':
    # queue_name = input("Enter the name of the queue:\n")
    # msg = input("Enter msg to publish:\n")
    publish_msg()
