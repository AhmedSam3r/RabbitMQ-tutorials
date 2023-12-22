  **Exchanges**
- In RabbitMQ's messaging model, producers do not send messages directly to queues; instead, they send messages to exchanges.

- An exchange is a simple component that receives messages from producers on one side and pushes them to queues on the other side.

- The producer may not know which specific queue will receive the message; this is determined by the exchange.

- The rules for handling messages within an exchange, such as whether to append them to a specific queue or discard them, are defined by the exchange type.

- There are different exchange types available, including:
  -  direct
  -  topic
  -  headers
  -  fanout
* empty string denotes the default or nameless exchange: messages are routed to the queue with the name specified by routing_key, if it exists
![Alt text](<Screenshot from 2023-12-06 14-33-08.png>)

  **Temporary queues**
- The server will generate a random queue name since we provide an empty queue name in our broadcast case
  - At this point result.method.queue contains a random queue name. For example it may look like amq.gen-JzTY20BRgKO-HjmUJj0wLg
  - ```result = channel.queue_declare(queue='')```
- once the consumer connection is closed, the queue should be deleted. There's an exclusive flag 
  - ```result = channel.queue_declare(queue='', exclusive=True)```

  **Bindings**
- ![Alt text](<Screenshot from 2023-12-06 14-38-36.png>)
- tell the exchange to send messages to our queue is called a binding


**Summary**
![Alt text](<Screenshot from 2023-12-06 14-40-48.png>)