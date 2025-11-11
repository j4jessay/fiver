# Module 1 Lab: Kafka Fundamentals - Hands-On

## Lab Overview

**Duration**: 40 minutes (hands-on)
**Prerequisites**: Completed theory reading (20 minutes)

In this lab, you'll:
1. ✅ Start your first Kafka cluster (Zookeeper + Kafka Broker)
2. ✅ Create topics manually
3. ✅ Send messages using command-line producer
4. ✅ Read messages using command-line consumer
5. ✅ Observe partitions and offsets in action
6. ✅ Experiment with keys and message distribution

---

## Lab Environment

### What You're Building

```
Your Laptop
┌────────────────────────────────────────────┐
│  Docker Containers:                        │
│                                            │
│  ┌──────────────┐                          │
│  │  ZooKeeper   │  Port 2181               │
│  └──────┬───────┘                          │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐                          │
│  │ Kafka Broker │  Ports 9092, 29092       │
│  │  (Broker 0)  │                          │
│  │              │                          │
│  │  Topics:     │                          │
│  │  Partitions: │                          │
│  │  Messages:   │                          │
│  └──────────────┘                          │
└────────────────────────────────────────────┘
```

### Ports You'll Use

| Port | Service | Purpose |
|------|---------|---------|
| 2181 | ZooKeeper | Cluster coordination |
| 9092 | Kafka | External connections (from your laptop) |
| 29092 | Kafka | Internal connections (between containers) |

---

## Step 1: Start Kafka Cluster

### 1.1 Navigate to Lab Directory

```bash
cd /path/to/kafka-tutorials/module-1-kafka-fundamentals/lab
```

**Verify you're in the right place**:
```bash
ls
# You should see: docker-compose.yml
```

### 1.2 Start Services

```bash
docker compose up -d
```

**Expected Output**:
```
[+] Running 3/3
 ✔ Network lab_kafka-network    Created
 ✔ Container zookeeper          Started
 ✔ Container kafka              Started
```

**What just happened?**
- Created a Docker network for Kafka and ZooKeeper to communicate
- Started ZooKeeper container (manages Kafka cluster)
- Started Kafka broker container (message broker)

### 1.3 Verify Services Are Running

**Check container status**:
```bash
docker ps
```

**Expected Output** (should see 2 containers):
```
CONTAINER ID   IMAGE                             STATUS         PORTS
abc123...      confluentinc/cp-kafka:7.5.0       Up 30 seconds  0.0.0.0:9092->9092/tcp
def456...      confluentinc/cp-zookeeper:7.5.0   Up 35 seconds  0.0.0.0:2181->2181/tcp
```

**Check logs** (optional, to see what's happening):
```bash
# ZooKeeper logs
docker logs zookeeper

# Kafka broker logs
docker logs kafka
```

**Healthy logs should show**:
```
[2025-11-11 10:30:00] INFO Server started (org.apache.zookeeper.server.ZooKeeperServer)
[2025-11-11 10:30:05] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
```

### 1.4 Wait for Kafka to Be Ready

Kafka takes 30-60 seconds to fully start. Let's verify:

```bash
docker exec -it kafka \
  kafka-broker-api-versions --bootstrap-server localhost:9092
```

**Expected Output** (list of supported API versions):
```
localhost:9092 (id: 0 rack: null) -> (
  ApiVersion(apiKey=PRODUCE, minVersion=0, maxVersion=9),
  ApiVersion(apiKey=FETCH, minVersion=0, maxVersion=13),
  ...
)
```

✅ **If you see this, Kafka is ready!**

❌ **If you see "Connection refused"**: Wait 30 more seconds and try again.

---

## Step 2: Create Your First Topic

### 2.1 Create a Topic

Let's create a topic called `test.topic` with 3 partitions:

```bash
docker exec -it kafka \
  kafka-topics --create \
    --topic test.topic \
    --partitions 3 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
Created topic test.topic.
```

**What you just did**:
- `--topic test.topic`: Named the topic
- `--partitions 3`: Created 3 partitions for parallelism
- `--replication-factor 1`: No replication (only 1 broker)
- `--bootstrap-server localhost:9092`: Connected to Kafka broker

### 2.2 List All Topics

```bash
docker exec -it kafka \
  kafka-topics --list \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
test.topic
```

You might also see internal topics like `__consumer_offsets` (used by Kafka internally).

### 2.3 Describe the Topic

Get detailed information about your topic:

```bash
docker exec -it kafka \
  kafka-topics --describe \
    --topic test.topic \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
Topic: test.topic       TopicId: abc123...      PartitionCount: 3       ReplicationFactor: 1    Configs:
        Topic: test.topic       Partition: 0    Leader: 0       Replicas: 0     Isr: 0
        Topic: test.topic       Partition: 1    Leader: 0       Replicas: 0     Isr: 0
        Topic: test.topic       Partition: 2    Leader: 0       Replicas: 0     Isr: 0
```

**What this means**:
- **Partition: 0, 1, 2**: Three partitions created
- **Leader: 0**: Broker 0 is the leader for all partitions (we only have one broker)
- **Replicas: 0**: Data is stored on broker 0
- **Isr: 0**: Broker 0 is in-sync (no followers since RF=1)

---

## Step 3: Send Messages (Producer)

### 3.1 Start Console Producer

Open a console producer to send messages interactively:

```bash
docker exec -it kafka \
  kafka-console-producer \
    --topic test.topic \
    --bootstrap-server localhost:9092
```

**You'll see**:
```
>
```

The `>` prompt means you can now type messages!

### 3.2 Send Some Messages

Type each message and press **Enter**:

```
>Hello Kafka!
>This is my first message
>Kafka is awesome
>Learning about partitions
>Offset tracking is cool
```

**What's happening?**:
- Each line you type becomes one message
- Messages are sent to `test.topic`
- Kafka distributes them across 3 partitions (round-robin, since no keys)
- Each message gets a unique offset within its partition

### 3.3 Stop the Producer

Press **Ctrl+C** to exit the producer.

---

## Step 4: Read Messages (Consumer)

### 4.1 Start Console Consumer

In a **new terminal window** (or after exiting producer), start a consumer:

```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --from-beginning \
    --bootstrap-server localhost:9092
```

**Expected Output** (messages in any order):
```
Hello Kafka!
This is my first message
Kafka is awesome
Learning about partitions
Offset tracking is cool
```

**Important**: Messages may appear in different order than you sent them!

**Why?** Because they were distributed across 3 partitions, and consumer reads from all partitions in parallel.

### 4.2 Consumer with Offsets and Partitions

Let's see more details about each message:

**Stop previous consumer** (Ctrl+C), then run:

```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --from-beginning \
    --property print.partition=true \
    --property print.offset=true \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
Partition:0 Offset:0  Hello Kafka!
Partition:1 Offset:0  This is my first message
Partition:0 Offset:1  Kafka is awesome
Partition:2 Offset:0  Learning about partitions
Partition:1 Offset:1  Offset tracking is cool
```

**What this shows**:
- Messages are distributed across partitions 0, 1, and 2
- Offsets start at 0 within each partition
- Each partition has its own offset sequence

---

## Step 5: Working with Message Keys

### 5.1 Send Messages with Keys

Keys ensure related messages go to the same partition.

**Start producer with key parsing enabled**:

```bash
docker exec -it kafka \
  kafka-console-producer \
    --topic test.topic \
    --property "parse.key=true" \
    --property "key.separator=:" \
    --bootstrap-server localhost:9092
```

Now format messages as `key:value`:

```
>vehicle_001:Speed is 60 km/h
>vehicle_002:Speed is 70 km/h
>vehicle_001:Speed is 65 km/h
>vehicle_003:Speed is 80 km/h
>vehicle_001:Speed is 70 km/h
```

**What's different?**:
- `vehicle_001:` is the key
- `Speed is 60 km/h` is the value
- All messages with the same key go to the same partition!

**Exit producer** (Ctrl+C)

### 5.2 Consume with Keys

```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --from-beginning \
    --property print.key=true \
    --property print.partition=true \
    --property print.offset=true \
    --property key.separator=" => " \
    --bootstrap-server localhost:9092
```

**Expected Output** (notice key grouping):
```
Partition:0 Offset:2  null => Hello Kafka!
Partition:1 Offset:2  vehicle_001 => Speed is 60 km/h
Partition:1 Offset:3  vehicle_001 => Speed is 65 km/h
Partition:1 Offset:4  vehicle_001 => Speed is 70 km/h
Partition:2 Offset:1  vehicle_002 => Speed is 70 km/h
Partition:0 Offset:3  vehicle_003 => Speed is 80 km/h
```

**Observations**:
- All `vehicle_001` messages → Partition 1 (same partition!)
- Messages with same key are ordered within their partition
- Old messages (without keys) show `null` as key

---

## Step 6: Explore Topic Management

### 6.1 Create Another Topic

```bash
docker exec -it kafka \
  kafka-topics --create \
    --topic vehicle.telemetry \
    --partitions 5 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092
```

### 6.2 List All Topics

```bash
docker exec -it kafka \
  kafka-topics --list \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
test.topic
vehicle.telemetry
```

### 6.3 Alter Topic Configuration

Change retention time to 2 hours (instead of default 7 days):

```bash
docker exec -it kafka \
  kafka-configs --alter \
    --entity-type topics \
    --entity-name test.topic \
    --add-config retention.ms=7200000 \
    --bootstrap-server localhost:9092
```

**Verify**:
```bash
docker exec -it kafka \
  kafka-configs --describe \
    --entity-type topics \
    --entity-name test.topic \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
Dynamic configs for topic test.topic are:
  retention.ms=7200000 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:retention.ms=7200000}
```

### 6.4 Delete a Topic

```bash
docker exec -it kafka \
  kafka-topics --delete \
    --topic vehicle.telemetry \
    --bootstrap-server localhost:9092
```

**Warning**: Deleting a topic deletes ALL messages permanently!

---

## Step 7: Consumer Groups

### 7.1 Create a Consumer Group

Consumer groups allow multiple consumers to share the workload.

**Terminal 1** (Consumer 1):
```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --group my-first-group \
    --bootstrap-server localhost:9092
```

**Terminal 2** (Consumer 2):
```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --group my-first-group \
    --bootstrap-server localhost:9092
```

**Terminal 3** (Producer):
```bash
docker exec -it kafka \
  kafka-console-producer \
    --topic test.topic \
    --bootstrap-server localhost:9092
```

**Send messages**:
```
>Message 1
>Message 2
>Message 3
>Message 4
>Message 5
```

**Observe**: Messages are distributed between Consumer 1 and Consumer 2!
- Consumer 1 might get: Message 1, Message 3, Message 5
- Consumer 2 might get: Message 2, Message 4

### 7.2 Check Consumer Group Status

```bash
docker exec -it kafka \
  kafka-consumer-groups --describe \
    --group my-first-group \
    --bootstrap-server localhost:9092
```

**Expected Output**:
```
GROUP           TOPIC       PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
my-first-group  test.topic  0          5               5               0
my-first-group  test.topic  1          4               4               0
my-first-group  test.topic  2          6               6               0
```

**What this means**:
- **CURRENT-OFFSET**: Last offset consumed
- **LOG-END-OFFSET**: Latest offset in partition
- **LAG**: How far behind (0 = caught up)

---

## Step 8: Clean Up (Optional)

### Stop All Consumers and Producers

Press **Ctrl+C** in all terminals.

### Stop Kafka Services

```bash
docker compose down
```

**Expected Output**:
```
[+] Running 2/2
 ✔ Container kafka      Removed
 ✔ Container zookeeper  Removed
```

### Delete All Data (Optional)

```bash
docker compose down -v
```

The `-v` flag deletes volumes (all topics and messages).

---

## Lab Exercises

Now that you've completed the guided walkthrough, try these challenges!

### Exercise 1: Create a Custom Topic

**Task**: Create a topic called `user.clicks` with 10 partitions.

<details>
<summary>Click to reveal solution</summary>

```bash
docker exec -it kafka \
  kafka-topics --create \
    --topic user.clicks \
    --partitions 10 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092
```
</details>

### Exercise 2: Send Keyed Messages

**Task**: Send 20 messages to `user.clicks` with 5 different user keys (`user_001` through `user_005`).

<details>
<summary>Click to reveal solution</summary>

```bash
docker exec -it kafka \
  kafka-console-producer \
    --topic user.clicks \
    --property "parse.key=true" \
    --property "key.separator=:" \
    --bootstrap-server localhost:9092
```

Then type:
```
>user_001:Clicked homepage
>user_002:Clicked product page
>user_001:Clicked checkout
>user_003:Clicked about page
>user_001:Clicked login
... (15 more messages)
```
</details>

### Exercise 3: Verify Partition Distribution

**Task**: Consume messages from `user.clicks` and verify that all messages with the same key went to the same partition.

<details>
<summary>Click to reveal solution</summary>

```bash
docker exec -it kafka \
  kafka-console-consumer \
    --topic user.clicks \
    --from-beginning \
    --property print.key=true \
    --property print.partition=true \
    --bootstrap-server localhost:9092
```

**Look for**: All `user_001` messages should have the same partition number!
</details>

### Exercise 4: Monitor Consumer Lag

**Task**:
1. Start a consumer group
2. Send 100 messages
3. Stop the consumer
4. Send 50 more messages
5. Check the lag

<details>
<summary>Click to reveal solution</summary>

```bash
# 1. Start consumer (Terminal 1)
docker exec -it kafka \
  kafka-console-consumer \
    --topic test.topic \
    --group test-group \
    --bootstrap-server localhost:9092

# 2. Send 100 messages (Terminal 2)
for i in {1..100}; do
  echo "Message $i" | docker exec -i kafka \
    kafka-console-producer \
      --topic test.topic \
      --bootstrap-server localhost:9092
done

# 3. Stop consumer (Ctrl+C in Terminal 1)

# 4. Send 50 more messages
for i in {101..150}; do
  echo "Message $i" | docker exec -i kafka \
    kafka-console-producer \
      --topic test.topic \
      --bootstrap-server localhost:9092
done

# 5. Check lag
docker exec -it kafka \
  kafka-consumer-groups --describe \
    --group test-group \
    --bootstrap-server localhost:9092
```

**Expected**: LAG column should show ~50 (messages not yet consumed)
</details>

### Exercise 5: Experiment with Retention

**Task**:
1. Create a topic with 10-second retention
2. Send messages
3. Wait 15 seconds
4. Try to consume from beginning

<details>
<summary>Click to reveal solution</summary>

```bash
# 1. Create topic with 10-second retention
docker exec -it kafka \
  kafka-topics --create \
    --topic short-lived \
    --partitions 1 \
    --replication-factor 1 \
    --config retention.ms=10000 \
    --bootstrap-server localhost:9092

# 2. Send messages
echo -e "Message 1\nMessage 2\nMessage 3" | \
  docker exec -i kafka \
    kafka-console-producer \
      --topic short-lived \
      --bootstrap-server localhost:9092

# 3. Consume immediately (should see all messages)
docker exec -it kafka \
  kafka-console-consumer \
    --topic short-lived \
    --from-beginning \
    --bootstrap-server localhost:9092

# 4. Wait 15 seconds
sleep 15

# 5. Consume again (messages might be gone!)
docker exec -it kafka \
  kafka-console-consumer \
    --topic short-lived \
    --from-beginning \
    --timeout-ms 5000 \
    --bootstrap-server localhost:9092
```

**Observation**: Older messages may have been deleted!
</details>

---

## Troubleshooting

### Issue: "Connection refused" when running commands

**Cause**: Kafka not fully started yet.

**Solution**: Wait 30-60 seconds after `docker compose up`, then try again.

### Issue: Can't see containers with `docker ps`

**Cause**: Services didn't start or crashed.

**Solution**: Check logs:
```bash
docker compose logs
```

Look for error messages.

### Issue: Messages not appearing in consumer

**Possible Causes**:
1. Wrong topic name (typo)
2. Consumer started without `--from-beginning` (only sees new messages)
3. Producer and consumer using different topics

**Solution**:
```bash
# List all topics
docker exec -it kafka \
  kafka-topics --list --bootstrap-server localhost:9092

# Verify topic has messages
docker exec -it kafka \
  kafka-topics --describe --topic test.topic --bootstrap-server localhost:9092
```

### Issue: "Topic already exists" error

**Cause**: Trying to create a topic that already exists.

**Solution**:
- Use a different topic name, OR
- Delete the existing topic first:
```bash
docker exec -it kafka \
  kafka-topics --delete --topic test.topic --bootstrap-server localhost:9092
```

---

## Key Takeaways

✅ You've successfully run a Kafka cluster locally!

✅ You created topics with different partition counts

✅ You sent messages with and without keys

✅ You consumed messages and observed offsets

✅ You used consumer groups for parallel processing

✅ You experimented with topic configurations

---

## What's Next?

Congratulations on completing Module 1!

**Next Module**: [Module 2 - Producers & Consumers →](../../module-2-producers-consumers/)

In Module 2, you'll:
- Build a Python producer from scratch
- Create the vehicle telemetry simulator
- Understand producer configurations
- Learn about delivery guarantees and error handling

**Before moving on**, make sure you:
- ✅ Understand what topics, partitions, and offsets are
- ✅ Can create topics and send messages
- ✅ Can read messages using consumers
- ✅ Understand how keys affect partition assignment

---

## Quick Command Reference

```bash
# Start services
docker compose up -d

# Check logs
docker compose logs -f

# Create topic
docker exec -it kafka kafka-topics --create --topic <name> --partitions <num> --bootstrap-server localhost:9092

# List topics
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# Produce messages
docker exec -it kafka kafka-console-producer --topic <name> --bootstrap-server localhost:9092

# Consume messages
docker exec -it kafka kafka-console-consumer --topic <name> --from-beginning --bootstrap-server localhost:9092

# Describe consumer group
docker exec -it kafka kafka-consumer-groups --describe --group <name> --bootstrap-server localhost:9092

# Stop services
docker compose down

# Stop and delete data
docker compose down -v
```

---

**Happy Streaming!** 🚀

Questions? Check the [main README](../../README.md) or review the [theory materials](../theory/).
