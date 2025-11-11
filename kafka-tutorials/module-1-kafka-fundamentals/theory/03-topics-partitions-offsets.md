# Topics, Partitions, and Offsets - Deep Dive

## Introduction

You've learned the basics of Kafka architecture. Now let's dive deep into the most important concepts: **topics**, **partitions**, and **offsets**. Understanding these is crucial for building effective Kafka applications.

**Reading Time**: 8-10 minutes

---

## Topics: The Foundation

### Creating Topics

Topics can be created in two ways:

**1. Explicit Creation (Recommended)**
```bash
kafka-topics --create \
  --topic vehicle.telemetry \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server kafka:9092
```

**2. Auto-Creation (When Producer Writes)**
```python
# If topic doesn't exist, Kafka creates it automatically
producer.send("new-topic", value="hello")
# Topic created with default settings (usually 1 partition)
```

**Best Practice**: Explicitly create topics in production to control partition count and replication factor.

### Topic Configuration

Topics have many configuration parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retention.ms` | 168 hours (7 days) | How long to keep messages |
| `retention.bytes` | -1 (unlimited) | Max bytes per partition |
| `segment.ms` | 168 hours | Log segment file rollover time |
| `compression.type` | producer | Compression codec (gzip, snappy, lz4) |
| `max.message.bytes` | 1 MB | Max message size |
| `min.insync.replicas` | 1 | Min replicas for writes |

**Example: Change retention to 30 days**
```bash
kafka-configs --alter \
  --topic vehicle.telemetry \
  --add-config retention.ms=2592000000 \
  --bootstrap-server kafka:9092
```

### Topic Naming Best Practices

**Good Names**:
```
vehicle.telemetry          # namespace.entity
user.clicks                # clear purpose
payment.transactions       # readable
order.fulfillment.events   # hierarchical
```

**Bad Names**:
```
data                      # too generic
topic1                    # meaningless
myTopic                   # inconsistent casing
VEHICLE_TELEMETRY         # use lowercase and dots
```

**Conventions**:
- Use **lowercase** letters
- Use **dots** (`.`) for namespacing
- Be **descriptive** and specific
- Use **nouns** (things, not actions)
- Avoid special characters

---

## Partitions: Parallelism and Ordering

### Why Partitions Exist

Without partitions:
```
Single Log:
[msg1, msg2, msg3, msg4, msg5, ...]
  ↓
Limited to 1 producer, 1 consumer
Bottleneck!
```

With partitions:
```
Partition 0: [msg1, msg4, msg7, ...]  → Consumer 1
Partition 1: [msg2, msg5, msg8, ...]  → Consumer 2
Partition 2: [msg3, msg6, msg9, ...]  → Consumer 3

3x parallelism!
```

### How Many Partitions?

**Too Few**:
- Limited parallelism
- Scalability bottleneck
- Underutilized consumers

**Too Many**:
- More memory/file handles per broker
- Longer leader election times
- More overhead

**Rule of Thumb**:
```
Number of Partitions = max(
  Desired Throughput / Consumer Throughput,
  Desired Throughput / Producer Throughput
)
```

**Example Calculation**:
```
Desired: 1,000 MB/sec total throughput
Consumer throughput: 50 MB/sec
Producer throughput: 100 MB/sec

Partitions needed:
  For consumers: 1000 / 50 = 20 partitions
  For producers: 1000 / 100 = 10 partitions

Choose max(20, 10) = 20 partitions
```

**Practical Recommendations**:
- **Low volume** (< 10 MB/sec): 3-5 partitions
- **Medium volume** (10-100 MB/sec): 10-20 partitions
- **High volume** (> 100 MB/sec): 30-50+ partitions
- **Our lab** (20 msg/sec): 3 partitions (plenty!)

### Partition Distribution Across Brokers

With multiple brokers, partitions are distributed:

```
Topic: vehicle.telemetry (6 partitions, 3 brokers)

Broker 1:        Broker 2:        Broker 3:
- Partition 0    - Partition 1    - Partition 2
- Partition 3    - Partition 4    - Partition 5

Load balanced automatically!
```

**Benefits**:
- Even distribution of data
- Even distribution of traffic
- No single broker hotspot

### You Cannot Reduce Partitions!

**Important Limitation**:
```
✅ Can increase: 3 partitions → 6 partitions (OK)
❌ Cannot decrease: 6 partitions → 3 partitions (NOT POSSIBLE)
```

**Why?**: Kafka can't determine which data to delete from which partition.

**Recommendation**: Start with fewer partitions, increase if needed.

---

## Message Keys and Partition Assignment

### Messages Without Keys (Round-Robin)

```python
# No key specified
producer.send("vehicle.telemetry", value={"speed": 80})
producer.send("vehicle.telemetry", value={"speed": 85})
producer.send("vehicle.telemetry", value={"speed": 90})

# Kafka distributes evenly:
Partition 0: message 1
Partition 1: message 2
Partition 2: message 3
Partition 0: message 4
Partition 1: message 5
...
```

**Result**: Even distribution, but **no ordering guarantee** for related messages.

### Messages With Keys (Hash-Based)

```python
# With vehicle_id as key
producer.send("vehicle.telemetry", key="vehicle_123", value={"speed": 80})
producer.send("vehicle.telemetry", key="vehicle_456", value={"speed": 85})
producer.send("vehicle.telemetry", key="vehicle_123", value={"speed": 90})

# Kafka uses hash(key) % num_partitions:
vehicle_123 → hash("vehicle_123") % 3 = 1 → Partition 1
vehicle_456 → hash("vehicle_456") % 3 = 0 → Partition 0
vehicle_123 → hash("vehicle_123") % 3 = 1 → Partition 1 (same!)

Result:
Partition 0: [vehicle_456 msg]
Partition 1: [vehicle_123 msg1, vehicle_123 msg2]  ← Ordered!
Partition 2: []
```

**Key Guarantees**:
✅ Same key → always same partition
✅ Messages for same key are ordered
✅ Enables stateful processing (e.g., per-user aggregations)

**Warning**: If you change partition count, keys may be reassigned to different partitions!

### Choosing Keys

**Good Keys**:
```python
# User-specific data
key = user_id

# Device-specific data
key = device_id

# Order processing
key = order_id

# Our project: vehicle telemetry
key = vehicle_id
```

**Bad Keys**:
```python
# Random values (defeats purpose)
key = random.randint(1, 1000)

# Timestamp (poor distribution)
key = str(time.time())

# Constant value (all to one partition!)
key = "constant"
```

**When NOT to use keys**:
- Don't need ordering for related events
- Want even distribution
- Messages are independent

---

## Offsets: The Position Tracker

### Offset Basics

```
Partition 0:
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│ speed  │ speed  │ speed  │ speed  │ speed  │ speed  │ speed  │
│  70    │  75    │  80    │  85    │  90    │  95    │  100   │
└────────┴────────┴────────┴────────┴────────┴────────┴────────┘
Offset:   0        1        2        3        4        5        6
          ↑                                              ↑
      Earliest                                      Latest (LEO)

LEO = Log End Offset (next offset to be written)
```

**Key Facts**:
- Offsets are **integers** starting at 0
- Offsets are **per-partition** (not global)
- Offsets are **immutable** (never change for a message)
- Offsets are **sequential** (no gaps under normal operation)

### Types of Offsets

**1. Current Offset**
```
The next offset that will be read by a consumer
Consumer at offset 3 → will read message at offset 3 next
```

**2. Committed Offset**
```
The last offset that was successfully processed
Consumer commits offset 5 → "I've processed up to offset 4"
If consumer crashes, it resumes from offset 5
```

**3. Log End Offset (LEO)**
```
The offset of the next message to be written
LEO = 100 → next message will have offset 100
```

**4. High Water Mark (HWM)**
```
The offset of the last message replicated to all in-sync replicas
Only messages up to HWM are visible to consumers
Ensures consistency even if leader fails
```

### Offset Management

**Consumer Offset Commits**:
```python
# Manual commit (more control)
consumer = KafkaConsumer(
    'vehicle.telemetry',
    enable_auto_commit=False
)
for message in consumer:
    process(message)
    consumer.commit()  # Commit after processing

# Auto commit (easier, less control)
consumer = KafkaConsumer(
    'vehicle.telemetry',
    enable_auto_commit=True,
    auto_commit_interval_ms=5000  # Commit every 5 seconds
)
```

**Where Are Offsets Stored?**
```
Old Kafka (< 0.9): ZooKeeper
New Kafka (> 0.9): Internal topic __consumer_offsets

Topic __consumer_offsets:
  key: (group_id, topic, partition)
  value: offset

Example:
  ("analytics-group", "vehicle.telemetry", 0) → 12345
  ("alerts-group", "vehicle.telemetry", 0) → 200
```

**Different consumer groups** have independent offsets!

---

## Partition Internals

### Segment Files

Partitions are stored as **segment files** on disk:

```
Partition Directory:
/var/lib/kafka/data/vehicle.telemetry-0/
  ├── 00000000000000000000.log    # Segment 1 (offsets 0-999)
  ├── 00000000000000001000.log    # Segment 2 (offsets 1000-1999)
  ├── 00000000000000002000.log    # Segment 3 (offsets 2000-2999)
  ├── 00000000000000000000.index  # Index for segment 1
  ├── 00000000000000001000.index  # Index for segment 2
  └── 00000000000000002000.index  # Index for segment 3
```

**Why Segments?**
- Easier to delete old data (delete old segments)
- Faster reads (index files for quick lookup)
- Easier compaction (clean old segments)

### Log File Format

```
.log file (simplified):
┌────────────────────────────────────────────────────┐
│ Offset | Timestamp | Key Size | Value Size | Key | Value |
├────────────────────────────────────────────────────┤
│   0    | 1699... | 11       | 50         | vehicle_123 | {...} │
│   1    | 1699... | 11       | 52         | vehicle_456 | {...} │
│   2    | 1699... | 11       | 48         | vehicle_789 | {...} │
└────────────────────────────────────────────────────┘
```

**Index File** (for fast lookups):
```
.index file:
Offset → Position in .log file

Example:
Offset 1000 → Byte 524288
Offset 2000 → Byte 1048576
```

### Compaction (Optional Topic)

**Log Compaction** keeps only the latest value for each key:

```
Before Compaction:
Offset: 0      1      2      3      4      5
Key:    user1  user2  user1  user2  user1  user3
Value:  v1     v1     v2     v2     v3     v1

After Compaction:
Offset: 4      3      5
Key:    user1  user2  user3
Value:  v3     v2     v1

Only latest value per key is kept!
```

**Use Cases**:
- User profiles (keep latest state)
- Product catalog (current inventory)
- Configuration updates

**Our Project**: We won't use compaction (time-based retention is fine for telemetry).

---

## Practical Examples

### Example 1: Vehicle Telemetry (Our Project)

```
Topic: vehicle.telemetry
Partitions: 3
Key: vehicle_id
```

**Why this works well**:
✅ All events for one vehicle go to same partition (ordered!)
✅ 10 vehicles distributed across 3 partitions (balanced)
✅ Can add more consumers for parallel processing

**Message Flow**:
```python
# Vehicle 1 sends data
{"vehicle_id": "v001", "speed": 80, "fuel": 75}  → Partition 1

# Vehicle 1 sends more data (same partition!)
{"vehicle_id": "v001", "speed": 85, "fuel": 74}  → Partition 1

# Vehicle 2 sends data (different partition)
{"vehicle_id": "v002", "speed": 60, "fuel": 90}  → Partition 0
```

**Consumer Reads**:
```
Consumer Group "analytics":
  Consumer 1 reads Partition 0 (vehicles v002, v005, v008)
  Consumer 2 reads Partition 1 (vehicles v001, v004, v007, v010)
  Consumer 3 reads Partition 2 (vehicles v003, v006, v009)
```

### Example 2: User Clickstream

```
Topic: user.clicks
Partitions: 12
Key: user_id
```

**Scenario**: Track user activity on a website

```python
# User 123 clicks button
{"user_id": "123", "action": "click", "page": "home"}  → Partition 5

# Same user views product (same partition!)
{"user_id": "123", "action": "view", "product_id": "p456"}  → Partition 5

# Different user
{"user_id": "456", "action": "click", "page": "cart"}  → Partition 2
```

**Why keys matter here**: To build user sessions, you need all events for a user in order!

### Example 3: Logs (No Keys)

```
Topic: application.logs
Partitions: 6
Key: None (no keys)
```

**Scenario**: Collect logs from 100 servers

```python
# Server 1 sends log
{"level": "INFO", "message": "Request processed", "server": "s1"}  → Partition 3

# Server 2 sends log
{"level": "ERROR", "message": "Database timeout", "server": "s2"}  → Partition 1

# Random distribution, no ordering needed
```

**Why no keys**: Logs are independent, just need even distribution.

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Too Few Partitions

```
Problem:
  Topic with 1 partition, 10 consumers
  → Only 1 consumer can read (others idle)

Solution:
  Use at least as many partitions as max consumers
```

### Mistake 2: Changing Partitions After Production

```
Problem:
  Start with 3 partitions, keyed by user_id
  Increase to 6 partitions later
  → Keys may be reassigned to different partitions!
  → Breaks ordering guarantees

Solution:
  Plan partitions upfront
  Over-provision if unsure
```

### Mistake 3: Using Bad Keys

```
Problem:
  key = timestamp (poor distribution, all recent data in one partition)

Solution:
  key = entity_id (user_id, device_id, etc.)
```

### Mistake 4: Not Committing Offsets

```
Problem:
  Consumer crashes without committing offset
  → Re-processes messages (duplicates)

Solution:
  Commit offsets after processing
  Use idempotent processing (handle duplicates gracefully)
```

---

## Key Takeaways

✅ **Topics** organize messages by category (choose good names!)

✅ **Partitions** enable parallelism (start with 3-5, increase if needed)

✅ **Keys** control which partition (use for ordering related messages)

✅ **Offsets** track position (sequential integers, per-partition)

✅ **Message keys** ensure ordering (same key → same partition → ordered)

✅ **Cannot reduce** partition count (only increase)

✅ **Offsets are committed** to __consumer_offsets topic

✅ **Different consumer groups** have independent offsets

---

## Hands-On Time!

You now have a solid theoretical understanding of topics, partitions, and offsets.

**Next Step**: Go to the lab and **actually use** these concepts!

👉 **[Start Lab: Module 1 Hands-On →](../lab/README.md)**

In the lab, you'll:
1. Create topics with different partition counts
2. Send messages with and without keys
3. Observe how messages are distributed
4. Read messages and track offsets
5. Experiment with multiple consumers

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────┐
│ TOPICS, PARTITIONS & OFFSETS CHEAT SHEET            │
├──────────────────────────────────────────────────────┤
│                                                      │
│ CREATE TOPIC:                                        │
│   kafka-topics --create --topic my-topic \          │
│     --partitions 3 --replication-factor 1           │
│                                                      │
│ LIST TOPICS:                                         │
│   kafka-topics --list --bootstrap-server kafka:9092 │
│                                                      │
│ DESCRIBE TOPIC:                                      │
│   kafka-topics --describe --topic my-topic          │
│                                                      │
│ SEND MESSAGE (with key):                            │
│   echo "key:value" | kafka-console-producer \       │
│     --topic my-topic --property "parse.key=true"    │
│                                                      │
│ CONSUME (from beginning):                           │
│   kafka-console-consumer --topic my-topic \         │
│     --from-beginning --bootstrap-server kafka:9092  │
│                                                      │
│ CONSUME (with keys and offsets):                    │
│   kafka-console-consumer --topic my-topic \         │
│     --property print.key=true \                     │
│     --property print.offset=true \                  │
│     --from-beginning                                │
│                                                      │
│ CHECK CONSUMER OFFSET:                              │
│   kafka-consumer-groups --describe \                │
│     --group my-group                                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Further Reading (Optional)

- [Kafka Topics Deep Dive](https://kafka.apache.org/documentation/#topicconfigs)
- [Partition Assignment Strategy](https://kafka.apache.org/documentation/#consumerconfigs_partition.assignment.strategy)
- [Log Compaction](https://kafka.apache.org/documentation/#compaction)

---

**Ready to get hands-on?** → [Go to Lab](../lab/README.md)
