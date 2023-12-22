1. **Round-robin dispatching**
- One of the advantages of using a Task Queue is the ability to easily parallelise work. If we are building up a backlog of work, we can just add more workers and that way, scale easily.
- By default, RabbitMQ will send each message to the next consumer, in sequence. On average every consumer will **get the same number of messages**, soIt distributes the tasks evenly

2. **Message acknowledgment**
* When a consumer starts a long task and terminates before completing it, the current code in RabbitMQ immediately marks the message for deletion, resulting in message loss.
* To avoid losing tasks, RabbitMQ supports message acknowledgments (ack).
* An acknowledgment is sent by the consumer to inform RabbitMQ that a message has been received, processed, and can be deleted.
* If a consumer dies without sending an acknowledgment (e.g., channel or connection closed), RabbitMQ re-queues the message, delivering it to another consumer if available.
* A default timeout of 30 minutes is enforced on consumer delivery acknowledgment to detect stuck consumers.
* Manual message acknowledgments are enabled by default, and in previous examples, auto_ack=True flag was used to disable them. It's recommended to remove this flag and send proper acknowledgments from the worker after completing a task.

3. **Message durability**
* Although this command is correct by itself, it won't work in our setup. That's because we've already defined a queue called hello which is not durable. **RabbitMQ doesn't allow you to redefine an existing queue with different parameters**
* To ensure messages survive even if RabbitMQ server stops, both the queue and messages need to be marked as durable.
* To make a queue durable, it must be declared as such during creation: channel.queue_declare(queue='task_queue', durable=True).
* It's essential to apply this queue_declare change to both producer and consumer code.
* By declaring the queue as durable, we ensure it survives a RabbitMQ node restart.
* Additionally, messages must be marked as persistent by supplying the delivery_mode property with the value ```pika.spec.PERSISTENT_DELIVERY_MODE``` when publishing them using channel.basic_publish. This guarantees that messages are not lost even in the event of a RabbitMQ restart or crash.
* 
***NOTE***

  - **Time Window for Saving:**
     - When a message is marked as persistent, RabbitMQ is instructed to save it to disk.
     - However, there is a short time window between the moment RabbitMQ accepts the message and when it actually gets saved to disk.
     - During this brief period, if RabbitMQ crashes or the server stops, there is a possibility that the message might not be written to disk, leading to potential loss.

  - **fsync(2) not Performed for Every Message:**
     - RabbitMQ doesn't perform `fsync(2)` for every message. `fsync(2)` is a system call that ensures data is physically stored on disk.
     - Instead, RabbitMQ may save the message to cache and not immediately write it to the disk.
     - In the event of a crash before the data is synced to disk, there could be some data loss.

4. Fair Dispatch
   - The current message dispatching in RabbitMQ may not meet specific workload distribution requirements, especially in scenarios with uneven task weights among workers.
   - RabbitMQ dispatches messages blindly as they enter the queue, without considering the workload or unacknowledged messages for consumers.
   - This can lead to uneven distribution of work among workers, where may even worker is consistently busy, and odd may be underutilized.
   - To address this, the `Channel#basic_qos` method with `prefetch_count=1` setting can be used. This employs the `basic.qos` protocol method to instruct RabbitMQ not to assign more than one message to a worker at a time.
   - In other words, a worker won't receive a new message until it has processed and acknowledged the previous one, ensuring a more balanced distribution of tasks among available workers.



this error occurs:
    pika.exceptions.ChannelClosedByBroker: (406, 'PRECONDITION_FAILED - unknown delivery tag 1')

when we set auto_ack is true:
        channel.basic_consume(queue='task_queue',
                        # auto_ack=True,
                        on_message_callback=callback)
then manually setting it in the callback function:
    ch.basic_ack(delivery_tag=method.delivery_tag)


the callback arguments
* CHANNEL 
```<BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x7fa613c57940> params=<ConnectionParameters host=localhost port=5672 virtual_host=/ ssl=False>>>>```
* METHOD 
```<Basic.Deliver(['consumer_tag=ctag1.0cd28aefc77340f1a255f96c86650394', 'delivery_tag=2', 'exchange=', 'redelivered=False', 'routing_key=task_queue'])>```
* properties
```<BasicProperties(['delivery_mode=2'])>```