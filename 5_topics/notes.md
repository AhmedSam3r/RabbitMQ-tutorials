**Topic Exchange**
- Messages sent to a topic exchange require a routing key in the form of a list of words delimited by dots (e.g., "stock.usd.nyse", "nyse.vmw", "quick.orange.rabbit").
- The routing key can contain as many words as needed, up to a limit of 255 bytes.
- The logic of a topic exchange is similar to a direct exchange: a message with a specific routing key is delivered to queues bound with a matching binding key.
- Special cases for binding keys in topic exchanges include:
  - `*` (star): Substitutes for exactly one word in the routing key.
  - `#` (hash): Substitutes for zero or more words in the routing key.
- For example, with a binding key like "stock.*.nyse," a message with a routing key like "stock.usd.nyse" would match and be delivered to the bound queue.
![Alt text](<Screenshot from 2023-12-06 22-08-49.png>)

***Important Note***
- Topic exchange is powerful and can behave like other exchanges.

- When a queue is bound with "#" (hash) binding key - it will receive all the messages, regardless of the routing key - 
  **like in fanout exchange**.

- When special characters "*" (star) and "#" (hash) aren't used in bindings, 
  the topic exchange will behave just **like in direct exchange**.

* So topic can behave like three different types of exhcange (including itself) depending on the case

- See how they act when publishing message in a certain pattern
![Alt text](<Screenshot from 2023-12-06 22-21-14.png>)


![Alt text](<Screenshot from 2023-12-06 22-23-53.png>)


![Alt text](<Screenshot from 2023-12-06 22-26-23.png>)