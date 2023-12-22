import pika
import sys


def publish_msg():
    args = sys.argv
    msg = args[1] or "Hello World!"
    queue_name = args[2] or "mq"
    ip_address='localhost'
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip_address))
    channel = connection.channel()
    # channel.queue_declare(queue='mq')
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=msg)
    print(f" [x] Sent '{msg}!'")
    


if __name__ == '__main__':
    # queue_name = input("Enter the name of the queue:\n")
    # msg = input("Enter msg to publish:\n")
    publish_msg()
