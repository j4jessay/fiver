# Module 1: Additional Exercises

## Overview

These exercises reinforce the concepts you learned in Module 1. Complete them to solidify your understanding of topics, partitions, and offsets.

**Difficulty Levels**:
- 🟢 **Beginner**: Follow instructions closely
- 🟡 **Intermediate**: Figure out some steps yourself
- 🔴 **Advanced**: Design and implement solutions

---

## Exercise Set 1: Topic Creation and Management

### Exercise 1.1: Create Multiple Topics 🟢

**Objective**: Practice creating topics with different configurations.

**Task**: Create the following topics:

| Topic Name | Partitions | Replication Factor |
|------------|------------|--------------------|
| `orders` | 5 | 1 |
| `user.events` | 10 | 1 |
| `logs.application` | 3 | 1 |
| `analytics.clickstream` | 12 | 1 |

**Verification**: List all topics and verify they exist.

<details>
<summary>Click for solution</summary>

```bash
# Create each topic
docker exec -it kafka kafka-topics --create --topic orders --partitions 5 --replication-factor 1 --bootstrap-server localhost:9092

docker exec -it kafka kafka-topics --create --topic user.events --partitions 10 --replication-factor 1 --bootstrap-server localhost:9092

docker exec -it kafka kafka-topics --create --topic logs.application --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

docker exec -it kafka kafka-topics --create --topic analytics.clickstream --partitions 12 --replication-factor 1 --bootstrap-server localhost:9092

# Verify
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# Describe each topic to confirm partition count
docker exec -it kafka kafka-topics --describe --topic orders --bootstrap-server localhost:9092
```
</details>

---

### Exercise 1.2: Configure Topic Retention 🟡

**Objective**: Learn to modify topic configurations.

**Task**:
1. Create a topic called `session.data` with 3 partitions
2. Set retention to 1 hour (3,600,000 milliseconds)
3. Set maximum message size to 512 KB (524,288 bytes)
4. Verify the configuration

<details>
<summary>Click for solution</summary>

```bash
# Create topic with configurations
docker exec -it kafka kafka-topics --create \
  --topic session.data \
  --partitions 3 \
  --replication-factor 1 \
  --config retention.ms=3600000 \
  --config max.message.bytes=524288 \
  --bootstrap-server localhost:9092

# Verify configuration
docker exec -it kafka kafka-configs --describe \
  --entity-type topics \
  --entity-name session.data \
  --bootstrap-server localhost:9092
```

**Expected Output**:
```
Dynamic configs for topic session.data are:
  retention.ms=3600000 sensitive=false
  max.message.bytes=524288 sensitive=false
```
</details>

---

### Exercise 1.3: Topic Cleanup 🟢

**Objective**: Practice deleting topics.

**Task**:
1. List all topics
2. Delete the following topics: `session.data`, `logs.application`
3. Verify they no longer exist

<details>
<summary>Click for solution</summary>

```bash
# List current topics
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# Delete topics
docker exec -it kafka kafka-topics --delete --topic session.data --bootstrap-server localhost:9092
docker exec -it kafka kafka-topics --delete --topic logs.application --bootstrap-server localhost:9092

# Verify deletion
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```
</details>

---

## Exercise Set 2: Message Production

### Exercise 2.1: Send Structured JSON Messages 🟢

**Objective**: Practice sending realistic data.

**Task**: Send 10 order messages to the `orders` topic in this format:
```json
{"order_id": "ORD001", "customer_id": "CUST123", "amount": 99.99, "status": "pending"}
```

<details>
<summary>Click for solution</summary>

```bash
# Start producer
docker exec -it kafka kafka-console-producer \
  --topic orders \
  --bootstrap-server localhost:9092

# Type each message (one per line):
>{"order_id": "ORD001", "customer_id": "CUST123", "amount": 99.99, "status": "pending"}
>{"order_id": "ORD002", "customer_id": "CUST456", "amount": 149.50, "status": "pending"}
>{"order_id": "ORD003", "customer_id": "CUST123", "amount": 75.00, "status": "shipped"}
>{"order_id": "ORD004", "customer_id": "CUST789", "amount": 200.00, "status": "pending"}
>{"order_id": "ORD005", "customer_id": "CUST456", "amount": 50.25, "status": "delivered"}
>{"order_id": "ORD006", "customer_id": "CUST123", "amount": 120.00, "status": "pending"}
>{"order_id": "ORD007", "customer_id": "CUST999", "amount": 89.99, "status": "cancelled"}
>{"order_id": "ORD008", "customer_id": "CUST456", "amount": 175.00, "status": "shipped"}
>{"order_id": "ORD009", "customer_id": "CUST789", "amount": 99.00, "status": "pending"}
>{"order_id": "ORD010", "customer_id": "CUST123", "amount": 250.00, "status": "pending"}

# Verify
docker exec -it kafka kafka-console-consumer \
  --topic orders \
  --from-beginning \
  --max-messages 10 \
  --bootstrap-server localhost:9092
```
</details>

---

### Exercise 2.2: Keyed Messages for User Events 🟡

**Objective**: Practice using keys to maintain order for related events.

**Task**:
1. Send 20 user events to `user.events` topic
2. Use `customer_id` as the key (5 different customers)
3. Each customer should have 4 events
4. Verify all events for each customer went to the same partition

<details>
<summary>Click for solution</summary>

```bash
# Start producer with key parsing
docker exec -it kafka kafka-console-producer \
  --topic user.events \
  --property "parse.key=true" \
  --property "key.separator=:" \
  --bootstrap-server localhost:9092

# Send messages (format: key:value)
>CUST123:{"event": "login", "timestamp": "2025-11-11T10:00:00Z"}
>CUST456:{"event": "login", "timestamp": "2025-11-11T10:01:00Z"}
>CUST123:{"event": "view_product", "product_id": "PROD001", "timestamp": "2025-11-11T10:02:00Z"}
>CUST789:{"event": "login", "timestamp": "2025-11-11T10:03:00Z"}
>CUST456:{"event": "add_to_cart", "product_id": "PROD002", "timestamp": "2025-11-11T10:04:00Z"}
>CUST999:{"event": "login", "timestamp": "2025-11-11T10:05:00Z"}
>CUST123:{"event": "add_to_cart", "product_id": "PROD001", "timestamp": "2025-11-11T10:06:00Z"}
>CUST666:{"event": "login", "timestamp": "2025-11-11T10:07:00Z"}
>CUST456:{"event": "checkout", "total": 99.99, "timestamp": "2025-11-11T10:08:00Z"}
>CUST789:{"event": "view_product", "product_id": "PROD003", "timestamp": "2025-11-11T10:09:00Z"}
>CUST123:{"event": "checkout", "total": 149.99, "timestamp": "2025-11-11T10:10:00Z"}
>CUST999:{"event": "view_product", "product_id": "PROD004", "timestamp": "2025-11-11T10:11:00Z"}
>CUST456:{"event": "logout", "timestamp": "2025-11-11T10:12:00Z"}
>CUST666:{"event": "view_product", "product_id": "PROD005", "timestamp": "2025-11-11T10:13:00Z"}
>CUST789:{"event": "logout", "timestamp": "2025-11-11T10:14:00Z"}
>CUST123:{"event": "logout", "timestamp": "2025-11-11T10:15:00Z"}
>CUST999:{"event": "add_to_cart", "product_id": "PROD004", "timestamp": "2025-11-11T10:16:00Z"}
>CUST666:{"event": "add_to_cart", "product_id": "PROD005", "timestamp": "2025-11-11T10:17:00Z"}
>CUST999:{"event": "logout", "timestamp": "2025-11-11T10:18:00Z"}
>CUST666:{"event": "logout", "timestamp": "2025-11-11T10:19:00Z"}

# Verify partition assignment
docker exec -it kafka kafka-console-consumer \
  --topic user.events \
  --from-beginning \
  --property print.key=true \
  --property print.partition=true \
  --property key.separator=" => " \
  --bootstrap-server localhost:9092
```

**Look for**: All messages for `CUST123` should have the same partition number!
</details>

---

### Exercise 2.3: Batch Message Sending 🔴

**Objective**: Learn to send many messages quickly using scripts.

**Task**: Write a bash script to send 1000 messages to `analytics.clickstream` topic with random click data.

<details>
<summary>Click for solution</summary>

Create a file `send_clicks.sh`:

```bash
#!/bin/bash

# Array of page names
pages=("home" "products" "cart" "checkout" "about" "contact")
users=("user_1" "user_2" "user_3" "user_4" "user_5" "user_6" "user_7" "user_8" "user_9" "user_10")

# Send 1000 messages
for i in {1..1000}; do
  user=${users[$RANDOM % ${#users[@]}]}
  page=${pages[$RANDOM % ${#pages[@]}]}
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  echo "$user:{\"page\": \"$page\", \"timestamp\": \"$timestamp\", \"click_id\": $i}"
done | docker exec -i kafka kafka-console-producer \
  --topic analytics.clickstream \
  --property "parse.key=true" \
  --property "key.separator=:" \
  --bootstrap-server localhost:9092

echo "Sent 1000 click events!"
```

Make executable and run:
```bash
chmod +x send_clicks.sh
./send_clicks.sh
```

Verify:
```bash
# Count messages
docker exec -it kafka kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic analytics.clickstream
```
</details>

---

## Exercise Set 3: Message Consumption

### Exercise 3.1: Consume with Filtering (Manual) 🟢

**Objective**: Learn to consume and filter messages manually.

**Task**:
1. Consume messages from `orders` topic
2. Manually identify all orders with `status: "pending"`
3. Count how many there are

<details>
<summary>Click for solution</summary>

```bash
docker exec -it kafka kafka-console-consumer \
  --topic orders \
  --from-beginning \
  --bootstrap-server localhost:9092

# Manually look for "status": "pending" in the output
# Count them manually (should be 6 from Exercise 2.1)
```

**Better approach** (using grep):
```bash
docker exec -it kafka kafka-console-consumer \
  --topic orders \
  --from-beginning \
  --timeout-ms 5000 \
  --bootstrap-server localhost:9092 | grep '"status": "pending"' | wc -l
```
</details>

---

### Exercise 3.2: Offset-Based Reading 🟡

**Objective**: Learn to read from specific offsets.

**Task**:
1. Find out the total number of messages in each partition of `user.events`
2. Consume only messages from partition 0, starting at offset 5
3. Consume the last 10 messages from partition 0

<details>
<summary>Click for solution</summary>

```bash
# 1. Get partition offsets
docker exec -it kafka kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic user.events

# Output example:
# user.events:0:8
# user.events:1:6
# user.events:2:6
# (means partition 0 has offsets 0-7, partition 1 has 0-5, etc.)

# 2. Consume from partition 0, offset 5 onwards
docker exec -it kafka kafka-console-consumer \
  --topic user.events \
  --partition 0 \
  --offset 5 \
  --bootstrap-server localhost:9092

# 3. Consume last 10 messages (read all and take last 10)
docker exec -it kafka kafka-console-consumer \
  --topic user.events \
  --partition 0 \
  --from-beginning \
  --max-messages 100 \
  --bootstrap-server localhost:9092 | tail -n 10
```
</details>

---

### Exercise 3.3: Consumer Group Parallel Processing 🔴

**Objective**: Understand consumer group partitioning.

**Task**:
1. Create 3 terminal windows
2. Start 3 consumers in the same consumer group for `analytics.clickstream` (12 partitions)
3. Send 100 new messages
4. Observe how messages are distributed
5. Check consumer group status
6. Add a 4th consumer and observe rebalancing

<details>
<summary>Click for solution</summary>

**Terminal 1** (Consumer 1):
```bash
docker exec -it kafka kafka-console-consumer \
  --topic analytics.clickstream \
  --group click-processors \
  --property print.partition=true \
  --bootstrap-server localhost:9092
```

**Terminal 2** (Consumer 2):
```bash
docker exec -it kafka kafka-console-consumer \
  --topic analytics.clickstream \
  --group click-processors \
  --property print.partition=true \
  --bootstrap-server localhost:9092
```

**Terminal 3** (Consumer 3):
```bash
docker exec -it kafka kafka-console-consumer \
  --topic analytics.clickstream \
  --group click-processors \
  --property print.partition=true \
  --bootstrap-server localhost:9092
```

**Terminal 4** (Producer):
```bash
for i in {1..100}; do
  echo "user_$((RANDOM % 10)):click_$i"
done | docker exec -i kafka kafka-console-producer \
  --topic analytics.clickstream \
  --property "parse.key=true" \
  --property "key.separator=:" \
  --bootstrap-server localhost:9092
```

**Observe**:
- Each consumer should receive messages from 4 partitions (12 partitions / 3 consumers = 4)
- Messages from the same partition only go to one consumer

**Check status**:
```bash
docker exec -it kafka kafka-consumer-groups --describe \
  --group click-processors \
  --bootstrap-server localhost:9092
```

**Add 4th consumer** (Terminal 5):
```bash
docker exec -it kafka kafka-console-consumer \
  --topic analytics.clickstream \
  --group click-processors \
  --property print.partition=true \
  --bootstrap-server localhost:9092
```

**Observe rebalancing**:
- Partitions will be redistributed (12 / 4 = 3 partitions per consumer)
- Some consumers will lose partitions, others will gain
</details>

---

## Exercise Set 4: Advanced Scenarios

### Exercise 4.1: Simulate Late Consumer 🟡

**Objective**: Understand consumer lag.

**Task**:
1. Send 50 messages to `orders` topic
2. Start a consumer and process 25 messages
3. Stop the consumer
4. Send 25 more messages
5. Check consumer lag
6. Restart consumer and observe catch-up

<details>
<summary>Click for solution</summary>

```bash
# 1. Send 50 messages
for i in {1..50}; do
  echo "{\"order_id\": \"ORD$(printf %03d $i)\", \"amount\": $((RANDOM % 500))}"
done | docker exec -i kafka kafka-console-producer \
  --topic orders \
  --bootstrap-server localhost:9092

# 2. Start consumer (Terminal 1)
docker exec -it kafka kafka-console-consumer \
  --topic orders \
  --group late-consumer-test \
  --max-messages 25 \
  --bootstrap-server localhost:9092

# (Consumer will exit after 25 messages)

# 4. Send 25 more messages (Terminal 2)
for i in {51..75}; do
  echo "{\"order_id\": \"ORD$(printf %03d $i)\", \"amount\": $((RANDOM % 500))}"
done | docker exec -i kafka kafka-console-producer \
  --topic orders \
  --bootstrap-server localhost:9092

# 5. Check lag
docker exec -it kafka kafka-consumer-groups --describe \
  --group late-consumer-test \
  --bootstrap-server localhost:9092

# Expected: LAG should show ~25

# 6. Restart consumer
docker exec -it kafka kafka-console-consumer \
  --topic orders \
  --group late-consumer-test \
  --bootstrap-server localhost:9092

# Should immediately start consuming the lagged messages
```
</details>

---

### Exercise 4.2: Reset Consumer Offset 🔴

**Objective**: Learn to replay messages by resetting offsets.

**Task**:
1. Consume all messages from `user.events` with a consumer group
2. Reset the offset to the beginning
3. Consume again and verify all messages are re-processed

<details>
<summary>Click for solution</summary>

```bash
# 1. Consume all messages
docker exec -it kafka kafka-console-consumer \
  --topic user.events \
  --group replay-test \
  --from-beginning \
  --timeout-ms 10000 \
  --bootstrap-server localhost:9092

# 2. Reset offset to earliest
docker exec -it kafka kafka-consumer-groups --reset-offsets \
  --group replay-test \
  --topic user.events \
  --to-earliest \
  --execute \
  --bootstrap-server localhost:9092

# Expected output shows new offsets set to 0

# 3. Consume again
docker exec -it kafka kafka-console-consumer \
  --topic user.events \
  --group replay-test \
  --timeout-ms 10000 \
  --bootstrap-server localhost:9092

# Should see all messages again!
```

**Other reset options**:
```bash
# Reset to specific offset
--to-offset 100

# Reset to specific datetime
--to-datetime 2025-11-11T10:00:00.000

# Shift forward by N
--shift-by 50

# Shift backward by N
--shift-by -20
```
</details>

---

### Exercise 4.3: Multi-Topic Consumer 🔴

**Objective**: Consume from multiple topics simultaneously.

**Task**: Create a consumer that reads from both `orders` and `user.events` topics.

<details>
<summary>Click for solution</summary>

```bash
# Method 1: Whitelist multiple topics
docker exec -it kafka kafka-console-consumer \
  --whitelist "orders|user.events" \
  --from-beginning \
  --property print.topic=true \
  --bootstrap-server localhost:9092

# Method 2: Topic pattern (all topics starting with "user")
docker exec -it kafka kafka-console-consumer \
  --whitelist "user.*" \
  --from-beginning \
  --property print.topic=true \
  --bootstrap-server localhost:9092

# With consumer group
docker exec -it kafka kafka-console-consumer \
  --whitelist "orders|user.events" \
  --group multi-topic-group \
  --property print.topic=true \
  --bootstrap-server localhost:9092
```
</details>

---

## Challenge Projects

### Challenge 1: E-Commerce Order Pipeline 🔴

**Scenario**: Build a simple order processing simulation.

**Requirements**:
1. Create topic `ecommerce.orders` with 5 partitions
2. Send 100 orders with these fields:
   - `order_id`, `customer_id`, `product_id`, `quantity`, `price`, `status`
3. Use `customer_id` as message key
4. Create 3 consumer groups:
   - `inventory-service` (processes all orders)
   - `billing-service` (processes all orders)
   - `analytics-service` (processes all orders)
5. Verify each service received all orders independently

<details>
<summary>Click for hints</summary>

**Hints**:
- Each consumer group maintains independent offsets
- All groups can consume the same messages
- Use JSON format for orders
- Test with `--from-beginning` to ensure all messages are received
</details>

---

### Challenge 2: User Session Tracking 🔴

**Scenario**: Track user sessions using keyed messages.

**Requirements**:
1. Create topic `user.sessions` with 10 partitions
2. Simulate 20 users with 5-10 events each (login, click, purchase, logout)
3. Use `user_id` as key
4. Consume with 3 consumers in a group
5. Verify that all events for a specific user went to the same partition

<details>
<summary>Click for hints</summary>

**Hints**:
- Generate events with timestamps
- Include session_id in each event
- Use property `print.partition=true` to see partition assignment
- Group events by partition to verify user consistency
</details>

---

## Wrap-Up

**Congratulations!** 🎉

If you completed all exercises, you now have hands-on experience with:

✅ Creating and configuring topics
✅ Sending messages with and without keys
✅ Consuming messages from different offsets
✅ Using consumer groups for parallel processing
✅ Managing consumer offsets and lag
✅ Replaying messages

**Next Steps**:
- Review any concepts that were challenging
- Experiment with different configurations
- Proceed to **Module 2** to learn about Producers and Consumers in Python!

---

**Questions?** Review the [theory files](../theory/) or check the [main README](../../README.md).

**Ready for the next module?** → [Module 2: Producers & Consumers](../../module-2-producers-consumers/)
