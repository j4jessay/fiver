# Apache Kafka Tutorial - 6-Hour Hands-On Curriculum

## 🎯 Course Overview

This comprehensive 6-hour curriculum teaches Apache Kafka and stream processing through hands-on exercises. You'll build a **real-time IoT vehicle monitoring pipeline** from scratch, learning each component step-by-step.

### What You'll Build

A complete **Real-Time Vehicle Fleet Monitoring System** that:
- Streams telemetry from 10 vehicles every 2 seconds (GPS, speed, fuel, temperature)
- Processes data in real-time to detect alerts (speeding, low fuel, overheating)
- Exports data to Azure Blob Storage for analytics and dashboards
- Monitors the entire pipeline using Confluent Control Center

### Learning Approach

**70% Hands-On + 30% Theory**
- Build components yourself (not just copy-paste)
- Understand the "why" behind each decision
- Troubleshoot real issues
- Adapt the pipeline for your own use cases

---

## 📚 Course Modules

### Module 1: Kafka Fundamentals (60 minutes)
**Theory: 20 min | Hands-On: 40 min**

Learn the core concepts of Apache Kafka and event streaming.

**What You'll Learn:**
- What is event streaming and why it matters
- Kafka architecture (brokers, topics, partitions, offsets)
- Difference between Kafka and traditional databases
- When to use Kafka vs other messaging systems

**What You'll Build:**
- Set up Kafka with Docker (Zookeeper + Kafka Broker only)
- Create topics manually
- Send and receive messages using console tools
- Understand partitions and replication

**[Start Module 1 →](module-1-kafka-fundamentals/)**

---

### Module 2: Producers & Consumers (75 minutes)
**Theory: 25 min | Hands-On: 50 min**

Build applications that write to and read from Kafka.

**What You'll Learn:**
- Producer architecture and message delivery guarantees
- Consumer groups and offset management
- Serialization formats (JSON, Avro)
- Error handling and retries

**What You'll Build:**
- Simple "Hello World" producer from scratch
- Full vehicle telemetry simulator (step-by-step)
- Consumer to read and process messages
- Modify producer to add new vehicle data fields

**[Start Module 2 →](module-2-producers-consumers/)**

---

### Module 3: Stream Processing with ksqlDB (90 minutes)
**Theory: 30 min | Hands-On: 60 min**

Process streaming data in real-time using SQL.

**What You'll Learn:**
- Why stream processing (vs batch processing)
- ksqlDB fundamentals (streams vs tables)
- Filtering, transformations, and aggregations
- Windowing and time-based operations

**What You'll Build:**
- Speeding alert detection (speed > 80 km/h)
- Low fuel warnings (fuel < 15%)
- Overheating alerts (temperature > 100°C)
- 1-minute aggregated statistics per vehicle
- Custom queries for your own scenarios

**[Start Module 3 →](module-3-stream-processing/)**

---

### Module 4: Kafka Connect & Data Integration (60 minutes)
**Theory: 20 min | Hands-On: 40 min**

Export Kafka data to external systems without writing code.

**What You'll Learn:**
- Kafka Connect architecture
- Source vs Sink connectors
- Configuration and deployment
- Time-based partitioning strategies

**What You'll Build:**
- Azure Blob Storage sink connector
- Time-based partitioning (hourly folders)
- Automatic data export pipeline
- Modify flush settings and observe changes

**[Start Module 4 →](module-4-kafka-connect/)**

---

### Module 5: Monitoring & Operations (45 minutes)
**Theory: 15 min | Hands-On: 30 min**

Monitor, troubleshoot, and operate Kafka in production.

**What You'll Learn:**
- Key metrics to monitor (throughput, lag, errors)
- Common failure scenarios
- Debugging techniques
- Production best practices

**What You'll Do:**
- Navigate Confluent Control Center UI
- Diagnose producer/consumer lag issues
- Fix connector failures
- Intentionally break and repair the pipeline
- Read and understand Kafka logs

**[Start Module 5 →](module-5-monitoring-operations/)**

---

### Module 6: End-to-End Production Pipeline (60 minutes)
**Theory: 15 min | Hands-On: 45 min**

Deploy the complete pipeline and understand production considerations.

**What You'll Learn:**
- Scaling Kafka (partitions, replication, brokers)
- Production deployment patterns
- Security and authentication
- Real-world use cases and industry applications

**What You'll Build:**
- Full 7-service Kafka stack (all components together)
- Complete vehicle monitoring pipeline
- Verification and testing procedures
- Custom adaptation: Modify for a different IoT use case

**[Start Module 6 →](module-6-end-to-end-pipeline/)**

---

## 🛠️ Prerequisites

### Required Knowledge
- ✅ Python basics (variables, functions, loops, dictionaries)
- ✅ Command line familiarity (cd, ls, running commands)
- ✅ Basic understanding of APIs and JSON format

### Not Required (We'll Teach You)
- ❌ Kafka experience
- ❌ Docker expertise (we cover the basics)
- ❌ Stream processing knowledge

### Software Requirements

**Must Have:**
- **Docker Desktop** (version 20.10+) - [Download](https://www.docker.com/products/docker-desktop/)
- **Docker Compose** (version 2.0+) - Usually included with Docker Desktop
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Text editor** (VS Code recommended) - [Download](https://code.visualstudio.com/)
- **Git** - For cloning the repository

**System Resources:**
- **8GB RAM minimum** (16GB recommended for smooth operation)
- **20GB free disk space**
- **Internet connection** (for downloading Docker images)

**Cloud Account (Module 4 onwards):**
- **Azure Account** (free tier works) - [Sign Up](https://azure.microsoft.com/free/)
  - Needed for blob storage integration
  - $200 free credit available

### System Check

Run these commands to verify your setup:

```bash
# Check Docker
docker --version          # Should show 20.10 or higher
docker compose version    # Should show 2.0 or higher

# Check Python
python3 --version         # Should show 3.8 or higher

# Test Docker is running
docker ps                 # Should list running containers (may be empty)
```

---

## 📖 How to Use This Course

### For Instructor-Led Training

1. **Before Class**:
   - Students install Docker and Python
   - Clone the repository
   - Run system checks

2. **During Class**:
   - Instructor explains theory using markdown files as reference
   - Students follow lab README step-by-step
   - Pause for exercises and Q&A after each module
   - Instructor demonstrates troubleshooting

3. **After Class**:
   - Students complete additional exercises
   - Work on capstone customization project

### For Self-Paced Learning

1. **Read theory files** in each module's `theory/` folder (20-30 minutes)
2. **Follow lab instructions** in each module's `lab/README.md` carefully
3. **Complete hands-on exercises** to reinforce learning
4. **Experiment and break things** to learn troubleshooting
5. **Check solutions** only after attempting exercises yourself

### For Video Course Creation

Each module includes:
- **Theory markdown files** (talking points and explanations)
- **Lab step-by-step guides** (screen recording instructions)
- **Command sequences** (exactly what to type)
- **Expected outputs** (what viewers should see)
- **Exercise challenges** (for practice sections)

Recommended video structure:
1. **Theory section**: Screen share markdown files with voice explanation
2. **Lab demonstration**: Record terminal and browser side-by-side
3. **Exercise walkthrough**: Show solution with explanation
4. **Summary**: Key takeaways (2-3 minutes)

---

## 📋 Learning Path Options

### Fast Track (3-4 hours)
**For experienced developers who want essentials:**
- Module 1: Skip theory, just run lab (20 min)
- Module 2: Skim theory, focus on producer code (40 min)
- Module 3: Focus on ksqlDB queries (50 min)
- Module 4: Configure connector quickly (30 min)
- Module 5: Skim, use reference later (15 min)
- Module 6: Full end-to-end deployment (60 min)

### Standard Path (6 hours)
**Recommended for most learners:**
- Follow all modules sequentially
- Complete theory + lab for each
- Do core exercises (marked "essential")
- Quick breaks between modules

### Deep Dive (8-10 hours)
**For beginners or comprehensive training:**
- All modules with full theory reading
- Complete all exercises including bonus challenges
- Additional reading from reference materials
- Build custom capstone project from scratch
- Experiment with different configurations

### Workshop Format (1 full day)
**For in-person training sessions:**
- **Morning Session (9 AM - 12 PM)**: Modules 1-3
  - Coffee break after Module 1
  - Q&A session after Module 3
- **Lunch Break (12 PM - 1 PM)**
- **Afternoon Session (1 PM - 4 PM)**: Modules 4-6
  - Coffee break after Module 5
  - Group capstone project discussion
  - Wrap-up and next steps

---

## 🎓 Learning Objectives

By the end of this course, you will be able to:

### Knowledge (Understand)
- ✅ Explain Kafka architecture (brokers, topics, partitions, offsets)
- ✅ Describe use cases for event streaming vs batch processing
- ✅ Understand stream processing concepts (filtering, aggregation, joins)
- ✅ Compare Kafka to message queues (RabbitMQ) and databases
- ✅ Recognize when Kafka is the right tool for a problem

### Skills (Apply)
- ✅ Build producers and consumers in Python from scratch
- ✅ Write ksqlDB queries for filtering and aggregation
- ✅ Configure and deploy Kafka Connect connectors
- ✅ Monitor Kafka using Control Center and CLI tools
- ✅ Troubleshoot common Kafka issues (lag, connection errors, data loss)
- ✅ Set up complete Kafka pipelines with Docker Compose

### Practice (Create)
- ✅ Design event-driven architectures for real-world problems
- ✅ Adapt the vehicle pipeline for other IoT use cases
- ✅ Build end-to-end streaming data pipelines
- ✅ Make production readiness decisions (partitions, replication, scaling)
- ✅ Implement data integration patterns with external systems

---

## 🏗️ Project Architecture

### Complete Pipeline Overview

```
┌─────────────────────────┐
│   Python Producer       │  Simulates 10 vehicles
│   (producer.py)         │  20 messages/sec total
│                         │  (GPS, speed, fuel, temp)
└───────────┬─────────────┘
            │
            │ JSON messages
            ▼
┌─────────────────────────┐
│   Apache Kafka Broker   │  Topic: vehicle.telemetry
│   (Confluent Platform)  │  Partitions: 3
│                         │  Replication: 1
└───────────┬─────────────┘
            │
            │ Stream of telemetry
            ▼
┌─────────────────────────┐
│   ksqlDB Server         │  Real-time SQL queries
│   (Stream Processing)   │  - Filter speeding (>80 km/h)
│                         │  - Detect low fuel (<15%)
│                         │  - Alert overheating (>100°C)
│                         │  - 1-min aggregations
└───────────┬─────────────┘
            │
            │ Processed streams
            ▼
┌─────────────────────────┐
│   Kafka Connect         │  Azure Blob Sink Connector
│   (Data Integration)    │  Time partitioning: hourly
│                         │  Format: JSON files
└───────────┬─────────────┘
            │
            │ Export to cloud
            ▼
┌─────────────────────────┐
│   Azure Blob Storage    │  Folder structure:
│   (Data Lake)           │  /alerts/year=2025/
│                         │         month=11/day=11/
│                         │         hour=15/*.json
└───────────┬─────────────┘
            │
            │ Analytics queries
            ▼
┌─────────────────────────┐
│   Power BI / Analytics  │  Dashboards:
│   (Visualization)       │  - Vehicle locations map
│                         │  - Alert trends
│                         │  - Speed/fuel charts
└─────────────────────────┘

        Monitored By
┌─────────────────────────┐
│  Confluent Control      │  Web UI: localhost:9021
│  Center                 │  - Topic metrics
│  (Monitoring)           │  - Consumer lag
│                         │  - Connector status
└─────────────────────────┘
```

### Progressive Build Approach

Each module adds components incrementally, so you understand each piece:

| Module | Components Added | What's Running | Complexity |
|--------|------------------|----------------|------------|
| **1** | Zookeeper, Kafka Broker | Basic Kafka cluster | ⭐ Simple |
| **2** | + Python Producer | Data generation | ⭐⭐ Medium |
| **3** | + ksqlDB Server, CLI | Stream processing | ⭐⭐⭐ Advanced |
| **4** | + Kafka Connect, Schema Registry | Data export | ⭐⭐⭐ Advanced |
| **5** | + Control Center | Full monitoring | ⭐⭐⭐⭐ Complex |
| **6** | All 7 services together | Production-like | ⭐⭐⭐⭐ Complete |

---

## 📊 Real-World Context

### Industry Use Cases

This exact architecture pattern is used by major companies:

#### Ride-Sharing (Uber, Lyft, Grab)
- **Real-time driver location tracking** (exactly like our vehicle telemetry!)
- **Surge pricing calculations** (detecting high-demand areas)
- **Trip matching** (pairing riders with nearby drivers)
- **Fraud detection** (unusual trip patterns)

#### E-Commerce (Amazon, Shopify, Alibaba)
- **Inventory updates** (real-time stock levels across warehouses)
- **Order processing** (order placement → payment → fulfillment)
- **Fraud detection** (suspicious purchase patterns)
- **Recommendation engines** (clickstream → product suggestions)

#### Financial Services (PayPal, Stripe, Square)
- **Transaction monitoring** (millions of payments per second)
- **Fraud alerts** (real-time risk scoring)
- **Real-time analytics** (dashboard for merchants)
- **Compliance logging** (audit trails for regulations)

#### IoT & Smart Cities (Tesla, Waymo, Smart Cities)
- **Vehicle telemetry** (exactly what you'll build!)
- **Sensor data aggregation** (thousands of sensors per city)
- **Predictive maintenance** (detecting issues before failure)
- **Energy grid management** (balancing supply/demand)

#### Social Media (LinkedIn, Twitter/X, Meta)
- **Activity feeds** (likes, comments, shares in real-time)
- **Notification systems** (instant push notifications)
- **Analytics pipelines** (user behavior tracking)
- **Content moderation** (flagging inappropriate content)

### Skills and Career Paths

**Job Roles Using Kafka:**
- **Data Engineer** (most common role)
- **Platform Engineer** (infrastructure focus)
- **Streaming Data Engineer** (specialized)
- **Backend Engineer** (microservices communication)
- **DevOps/SRE Engineer** (operating Kafka clusters)

**Average Salaries (US, 2025):**
- Entry-level Data Engineer: $90K-$120K
- Mid-level Streaming Engineer: $120K-$160K
- Senior Platform Engineer: $160K-$220K
- Staff/Principal Engineer: $220K-$350K

**Certifications:**
- [Confluent Certified Developer for Apache Kafka (CCDAK)](https://www.confluent.io/certification/)
- [Confluent Certified Administrator for Apache Kafka (CCAAK)](https://www.confluent.io/certification/)
- Both available online, ~$150 exam fee

**Companies Hiring Kafka Skills:**
LinkedIn, Uber, Netflix, Airbnb, Spotify, Microsoft, Amazon, Apple, Goldman Sachs, JPMorgan, and thousands more

---

## 🚀 Getting Started

### Quick Start (5 minutes)

```bash
# 1. Navigate to the kafka-tutorials directory
cd /path/to/kafka-tutorials

# 2. Start with Module 1
cd module-1-kafka-fundamentals

# 3. Read the theory (3-5 minutes)
cat theory/01-what-is-kafka.md

# 4. Start the lab
cd lab
cat README.md

# 5. Follow the step-by-step instructions!
```

### Recommended Schedule

#### Option 1: Full Day Workshop (6 hours + breaks)
```
9:00 AM  - 9:10 AM   Welcome & Setup Verification
9:10 AM  - 10:10 AM  Module 1: Kafka Fundamentals
10:10 AM - 10:25 AM  ☕ Coffee Break

10:25 AM - 11:40 AM  Module 2: Producers & Consumers
11:40 AM - 12:50 PM  Module 3: Stream Processing
12:50 PM - 1:50 PM   🍕 Lunch Break

1:50 PM  - 2:50 PM   Module 4: Kafka Connect
2:50 PM  - 3:35 PM   Module 5: Monitoring & Operations
3:35 PM  - 3:45 PM   ☕ Coffee Break

3:45 PM  - 4:45 PM   Module 6: End-to-End Pipeline
4:45 PM  - 5:00 PM   Wrap-Up, Q&A, Next Steps
```

#### Option 2: Two Half-Days (3 hours each)
**Day 1: Foundation**
- Module 1: Kafka Fundamentals
- Module 2: Producers & Consumers
- Module 3: Stream Processing

**Day 2: Integration & Production**
- Module 4: Kafka Connect
- Module 5: Monitoring & Operations
- Module 6: End-to-End Pipeline

#### Option 3: Six 1-Hour Sessions (Weekly Learning)
- Week 1: Module 1 (build foundation)
- Week 2: Module 2 (add producer)
- Week 3: Module 3 (add stream processing)
- Week 4: Module 4 (add data integration)
- Week 5: Module 5 (add monitoring)
- Week 6: Module 6 (complete pipeline + capstone)

---

## 📁 Repository Structure

```
kafka-tutorials/
│
├── README.md (this file - start here!)
│
├── module-1-kafka-fundamentals/
│   ├── theory/
│   │   ├── 01-what-is-kafka.md
│   │   ├── 02-architecture-overview.md
│   │   └── 03-topics-partitions-offsets.md
│   └── lab/
│       ├── README.md (step-by-step lab guide)
│       ├── docker-compose.yml (minimal: Zookeeper + Kafka)
│       └── exercises.md (hands-on practice)
│
├── module-2-producers-consumers/
│   ├── theory/
│   │   ├── 01-producer-architecture.md
│   │   └── 02-consumer-groups.md
│   └── lab/
│       ├── README.md
│       ├── producer-simple.py (basic example)
│       ├── producer-vehicle.py (full simulator)
│       ├── Dockerfile.producer
│       ├── requirements.txt
│       └── exercises.md
│
├── module-3-stream-processing/
│   ├── theory/
│   │   ├── 01-why-stream-processing.md
│   │   ├── 02-ksqldb-overview.md
│   │   └── 03-streams-vs-tables.md
│   └── lab/
│       ├── README.md
│       ├── docker-compose.yml (adds ksqlDB to stack)
│       ├── queries/
│       │   ├── 01-create-stream.sql
│       │   ├── 02-filtering.sql
│       │   └── 03-aggregations.sql
│       └── exercises.md
│
├── module-4-kafka-connect/
│   ├── theory/
│   │   ├── 01-what-is-kafka-connect.md
│   │   ├── 02-source-vs-sink.md
│   │   └── 03-connector-architecture.md
│   └── lab/
│       ├── README.md
│       ├── docker-compose.yml (adds Connect)
│       ├── config/
│       │   ├── azure-blob-sink.json
│       │   └── azure-credentials.env
│       ├── scripts/
│       │   ├── deploy_connector.sh
│       │   └── verify_connector.sh
│       └── exercises.md
│
├── module-5-monitoring-operations/
│   ├── theory/
│   │   ├── 01-kafka-monitoring.md
│   │   └── 02-troubleshooting-guide.md
│   └── lab/
│       ├── README.md
│       ├── common-issues.md
│       └── exercises.md
│
├── module-6-end-to-end-pipeline/
│   ├── theory/
│   │   ├── 01-production-considerations.md
│   │   ├── 02-scaling-kafka.md
│   │   └── 03-real-world-use-cases.md
│   └── lab/
│       ├── README.md
│       ├── docker-compose.yml (full stack - all 7 services)
│       ├── IMPLEMENTATION_GUIDE.md
│       ├── verify_setup.sh
│       └── capstone-challenge.md
│
└── reference/
    ├── quick-commands.md (cheat sheet)
    ├── troubleshooting.md (common issues & solutions)
    ├── docker-tips.md (Docker basics)
    ├── resources.md (books, courses, docs)
    └── next-steps.md (certifications, advanced topics)
```

---

## 🔧 Troubleshooting

### Common Setup Issues

**Docker not starting?**
```bash
# Check if Docker daemon is running
docker ps

# If error: "Cannot connect to Docker daemon"
# → Start Docker Desktop application
# → Wait 30 seconds for it to fully start
```

**Port conflicts (9092, 2181, etc.)?**
```bash
# Check what's using the port
lsof -i :9092    # macOS/Linux
netstat -ano | findstr :9092  # Windows

# Solution 1: Kill the process
kill -9 <PID>

# Solution 2: Change port in docker-compose.yml
# Edit the file and use different ports
```

**Out of memory errors?**
```bash
# Docker Desktop Settings:
# 1. Click Docker icon → Preferences/Settings
# 2. Resources → Memory
# 3. Increase to at least 8GB
# 4. Click "Apply & Restart"
```

**Azure connector fails on Mac M1/M2/M3?**
- This is a known ARM64 architecture issue
- Solution: Use GitHub Codespaces (instructions in Module 4)
- Alternative: Skip Azure integration, use local file sink

**Cannot access Control Center at localhost:9021?**
```bash
# Wait 2-3 minutes for all services to start
# Check if container is running:
docker ps | grep control-center

# Check logs:
docker logs <container-id>

# Restart if needed:
docker compose restart control-center
```

### Getting Help

- **During course**: Ask your instructor or check `reference/troubleshooting.md`
- **Self-paced**: Read the specific module's troubleshooting section
- **Community Support**:
  - [Confluent Community Slack](https://confluentcommunity.slack.com/)
  - [Apache Kafka Users Mailing List](https://kafka.apache.org/contact)
  - [Stack Overflow](https://stackoverflow.com/questions/tagged/apache-kafka) (tag: `apache-kafka`)

---

## 📚 Additional Resources

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) - Official Kafka docs
- [Confluent Platform Docs](https://docs.confluent.io/) - Comprehensive guides
- [ksqlDB Documentation](https://docs.ksqldb.io/) - Stream processing with SQL

### Books (Recommended Reading)
1. **"Kafka: The Definitive Guide"** by Neha Narkhede, Gwen Shapira, Todd Palino
   - Comprehensive Kafka bible (500+ pages)
   - Covers architecture, operations, and use cases

2. **"Designing Event-Driven Systems"** by Ben Stopford
   - Free PDF from Confluent
   - Architectural patterns and best practices

3. **"Streaming Systems"** by Tyler Akidau
   - Advanced stream processing concepts
   - Theory and practice of streaming

### Online Courses (Free & Paid)
- [Confluent Developer Courses](https://developer.confluent.io/learn-kafka/) - Free official courses
- [Apache Kafka for Beginners](https://www.udemy.com/topic/apache-kafka/) - Udemy courses ($10-$50)
- [LinkedIn Learning: Apache Kafka](https://www.linkedin.com/learning/) - Video tutorials

### Practice Environments
- [Confluent Cloud](https://www.confluent.io/confluent-cloud/) - Free trial ($400 credit)
- [AWS MSK](https://aws.amazon.com/msk/) - Managed Kafka on AWS
- [Azure Event Hubs](https://azure.microsoft.com/en-us/services/event-hubs/) - Kafka-compatible service

### Community
- [Confluent Community Forum](https://forum.confluent.io/)
- [Kafka Subreddit](https://www.reddit.com/r/apachekafka/)
- [Kafka Improvement Proposals (KIPs)](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals)

---

## 🎉 Ready to Begin?

You're all set to start your Kafka journey!

### Next Steps:

1. **Verify your system meets prerequisites** (Docker, Python, 8GB RAM)
2. **Navigate to Module 1**: `cd module-1-kafka-fundamentals`
3. **Read the theory folder**: Start with `theory/01-what-is-kafka.md`
4. **Follow the lab**: Open `lab/README.md` and build your first Kafka cluster!

👉 **[Go to Module 1: Kafka Fundamentals →](module-1-kafka-fundamentals/)**

---

## 📝 Course Feedback

This curriculum is continuously improved based on student feedback!

After completing the course, please share:
- ⭐ What worked well?
- ❓ What was confusing?
- ➕ What should be added?
- ⏱️ How long did each module actually take you?
- 💡 What real-world project did you build after this course?

Your feedback helps make this better for future learners!

---

## ⚖️ License & Credits

**Apache Kafka**: Apache License 2.0 (open source)
**Confluent Platform**: Community license (free for development)
**Course Materials**: Free to use for educational purposes

**Credits:**
- Based on the Apache Kafka project
- Uses Confluent Platform components
- Vehicle IoT scenario adapted from real-world fleet management systems

---

## 🙏 Acknowledgments

This curriculum was designed for hands-on data engineering education, emphasizing:
- **Learning by doing** (not just reading)
- **Real-world relevance** (industry-standard tools)
- **Progressive complexity** (beginners to advanced)
- **Practical skills** (job-ready knowledge)

Special thanks to the Apache Kafka community and Confluent for their excellent documentation and tools.

---

**Happy Streaming! 🚀**

Questions? Stuck on something? Check the `reference/` folder or start with Module 1 - everything will become clear as you build!

**Let's get started!** → [Module 1: Kafka Fundamentals](module-1-kafka-fundamentals/)
