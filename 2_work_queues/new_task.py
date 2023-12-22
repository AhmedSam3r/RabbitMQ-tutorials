import pika
import sys


def publish_msg():
    args = sys.argv
    msg = ' '.join(args[2:]) or "Hello World!"
    queue_name = args[1] or "task_queue"
    print("queue_name = ", queue_name)
    host_address='localhost'
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_address))
    channel = connection.channel()
    # channel.queue_declare(queue='mq')
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE

                          ))
    print(f" [x] Sent '{msg}!'")


if __name__ == '__main__':
    # queue_name = input("Enter the name of the queue:\n")
    # msg = input("Enter msg to publish:\n")
    publish_msg()
