python3 -m venv venv
source venv/bin/activate

to spin up a rabbitmq broker, write in a terminal & keep it open
```docker run --name rabbibtmq -p 5672:5672 rabbitmq```

then open a terminal and write
```python3 receive.py```
open another terminal and write to send your messages
```python3 send.py```


*** To establish a connection ***
* Create a TCP connection using your host address
* Connect with the channel
* Intiate the your message queue with a specific name
* Publish the message you want through specifiying the exchange type, the routing key (queue name) and the message
* autoack=True is a flag that informs the mq that the message is received and being processed
