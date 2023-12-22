import pika
import os
import sys



def receive_msg():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='mq')

    def callback(ch, method, properties, body):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("CHANNEL = ", ch)
        print("METHOD = ", method)
        print("properties = ", properties)
        print(f" [x] Received {body}")
        # another way of acknolwedging 
        # channel.basic_ack(1)
        # print("ACK DONE!")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    channel.basic_consume(queue='mq',
                        auto_ack=True,
                        on_message_callback=callback)

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
    
