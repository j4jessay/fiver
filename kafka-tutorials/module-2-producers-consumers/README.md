# Module 2: Producers & Consumers

## Module Overview

**Duration**: 75 minutes (25 min theory + 50 min hands-on)

In this module, you'll learn how to build applications that interact with Kafka using Python. You'll progress from simple "Hello World" producers to a full vehicle telemetry simulator.

---

## Learning Objectives

By the end of this module, you will be able to:

✅ Build Kafka producers in Python from scratch
✅ Understand producer configurations and delivery guarantees
✅ Implement error handling and retries
✅ Build Kafka consumers with proper offset management
✅ Work with consumer groups
✅ Serialize/deserialize JSON messages

---

## Prerequisites

- ✅ Completed Module 1 (Kafka Fundamentals)
- ✅ Python 3.8+ installed
- ✅ Basic Python knowledge (functions, loops, dictionaries)
- ✅ Kafka cluster running (from Module 1)

---

## Module Structure

### Theory (25 minutes)

1. **[Producer Architecture](theory/01-producer-architecture.md)** (12 min)
   - How producers work internally
   - Delivery guarantees (at-most-once, at-least-once, exactly-once)
   - Batching and compression
   - Error handling strategies

2. **[Consumer Groups](theory/02-consumer-groups.md)** (13 min)
   - Consumer group fundamentals
   - Partition assignment strategies
   - Offset management (auto vs manual commit)
   - Rebalancing

### Lab (50 minutes)

**[Hands-On Lab →](lab/README.md)**

You'll build:
1. **Simple Producer** - Hello World example
2. **Vehicle Telemetry Simulator** - Real IoT data generator
3. **Simple Consumer** - Message processor
4. **Consumer Group** - Parallel processing

**Files you'll create**:
- `producer-simple.py` - Basic producer
- `producer-vehicle.py` - Full vehicle simulator
- `consumer-simple.py` - Basic consumer
- `consumer-group.py` - Consumer group example

---

## What You'll Build

### Vehicle Telemetry Simulator

```python
# Simulates 10 vehicles sending telemetry every 2 seconds
{
  "vehicle_id": "vehicle_001",
  "timestamp_utc": "2025-11-11T10:30:00Z",
  "location": {"lat": 37.7749, "lon": -122.4194},
  "speed_kmph": 85,
  "fuel_percent": 67,
  "engine_temp_celsius": 92,
  "status": "active"  # or "speeding", "low_fuel", "overheating"
}
```

**Features**:
- Realistic vehicle movement simulation
- Random variations in speed, fuel, temperature
- Status detection (speeding, low fuel, overheating)
- Proper error handling with retries
- Delivery callbacks for monitoring

---

## Key Concepts

### Producer

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send message
producer.send('vehicle.telemetry', value={"vehicle_id": "v001"})
producer.flush()
```

### Consumer

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'vehicle.telemetry',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='my-group'
)

for message in consumer:
    print(message.value)
```

---

## Quick Start

1. **Read the theory** (25 minutes)
   ```bash
   cd module-2-producers-consumers/theory
   cat 01-producer-architecture.md
   cat 02-consumer-groups.md
   ```

2. **Start the lab** (50 minutes)
   ```bash
   cd ../lab
   cat README.md
   ```

3. **Complete exercises**
   - Build simple producer
   - Build vehicle simulator
   - Build consumer
   - Test with consumer groups

---

## Troubleshooting

**ModuleNotFoundError: No module named 'kafka'**
```bash
pip install kafka-python
```

**Connection refused to localhost:9092**
```bash
# Make sure Kafka is running from Module 1
cd ../module-1-kafka-fundamentals/lab
docker compose up -d
```

**Messages not appearing in consumer**
- Check topic name (typo?)
- Verify producer sent messages successfully
- Use `--from-beginning` flag on consumer

---

## Next Steps

After completing this module:

👉 **[Module 3: Stream Processing with ksqlDB →](../module-3-stream-processing/)**

You'll learn to:
- Process streams in real-time using SQL
- Filter and transform data
- Create aggregations
- Join streams

---

**Ready to start?** → [Begin with Theory](theory/01-producer-architecture.md) or jump straight to [Lab](lab/README.md)
