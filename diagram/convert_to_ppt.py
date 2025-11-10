#!/usr/bin/env python3
"""
Convert Architecture Presentation Markdown to PowerPoint
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import re

# Color scheme
DATABRICKS_GREEN = RGBColor(0, 154, 94)
AWS_BLUE = RGBColor(27, 102, 201)
ORANGE_ACCENT = RGBColor(255, 153, 0)
DARK_GREY = RGBColor(35, 47, 62)
LIGHT_GREY = RGBColor(245, 245, 245)

def create_presentation():
    """Create PowerPoint presentation from architecture content"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Slide
    slide = add_title_slide(prs,
        "Databricks Data Lakehouse Architecture on AWS",
        "Modern Cloud Data Platform for Analytics & AI")

    # Slide 2: Executive Summary
    slide = add_content_slide(prs, "Executive Summary")
    add_section(slide, "What We Built",
        "A modern, cloud-native data lakehouse that unifies data engineering, analytics, and AI/ML workloads on a single platform")
    add_bullets(slide, [
        "Unified Platform: Single platform for all data workloads",
        "Scalable & Cost-Effective: Auto-scaling with pay-per-use pricing",
        "Data Quality: Progressive refinement (Bronze → Silver → Gold)",
        "Security-First: Multi-layered security with encryption and audit logging",
        "Real-Time Insights: Supports both batch and streaming analytics"
    ], top=2.5)
    add_section(slide, "Business Impact", "", top=5.0)
    add_bullets(slide, [
        "Faster time-to-insight for business users",
        "40-60% infrastructure cost reduction",
        "Self-service analytics without IT bottlenecks",
        "Foundation for AI/ML initiatives"
    ], top=5.5)

    # Slide 3: What is a Data Lakehouse
    slide = add_content_slide(prs, "Understanding the Data Lakehouse")
    add_text_box(slide, "The Evolution of Data Platforms",
        left=0.5, top=1.5, width=9, height=0.6, bold=True, font_size=18)
    add_text_box(slide, "Data Lakehouse = Best of Both Worlds\n\nCombines the flexibility and cost-effectiveness of data lakes with the reliability and performance of data warehouses",
        left=1, top=4.5, width=8, height=2, font_size=16)

    # Slide 4: Architecture Overview
    slide = add_content_slide(prs, "High-Level Architecture Overview")
    add_text_box(slide, "[INSERT ARCHITECTURE DIAGRAM HERE]\n\ndatabricks-lakehouse-final-v2.drawio",
        left=1, top=2, width=8, height=4.5, font_size=14, align='center')

    # Slide 5: Medallion Architecture
    slide = add_content_slide(prs, "Data Quality Progression: Bronze → Silver → Gold")
    zones = [
        ("🥉 Bronze Zone - Raw Data Layer", [
            "Landing zone for all raw, unprocessed data",
            "Exact copy of source data",
            "Append-only, time-stamped, preserves original format"
        ]),
        ("🥈 Silver Zone - Validated Data Layer", [
            "Cleaned and validated data",
            "Schema enforcement, deduplication, data quality checks",
            "Standardized formats, ready for business logic"
        ]),
        ("🥇 Gold Zone - Curated Data Layer", [
            "Business-ready, analytics-optimized data",
            "Aggregations, business logic, feature engineering",
            "Optimized for queries, serving layer for BI"
        ])
    ]
    top = 1.8
    for zone_title, zone_bullets in zones:
        add_section(slide, zone_title, "", top=top, font_size=14)
        add_bullets(slide, zone_bullets, top=top+0.4, font_size=12, left=1.5)
        top += 1.8

    # Slide 6: Data Sources & Ingestion
    slide = add_content_slide(prs, "How Data Enters the Platform")
    add_section(slide, "Data Sources", "", top=1.8)
    add_bullets(slide, [
        "On-Premises Oracle Database - Legacy enterprise databases",
        "REST APIs - Real-time data from external services",
        "CSV Files - Flat files from business systems",
        "External S3 - Partner data or external storage",
        "Streaming Data - IoT devices, clickstreams, logs"
    ], top=2.3, font_size=13)
    add_section(slide, "AWS Ingestion Services", "", top=4.2)
    add_bullets(slide, [
        "AWS DMS - Database migration (Oracle → Bronze Zone)",
        "API Gateway - API management (REST APIs → Lambda → Bronze)",
        "Lambda - Serverless compute for data transformation",
        "Transfer Family - Secure file transfer (CSV/Files → Bronze)",
        "Kinesis - Stream processing (Real-time events → Bronze)"
    ], top=4.7, font_size=13)

    # Slide 7: What is Databricks
    slide = add_content_slide(prs, "Databricks - The Heart of Our Architecture")
    add_section(slide, "Databricks = Unified Analytics Platform", "", top=1.8, font_size=18)
    add_bullets(slide, [
        "🔧 Data Engineering: ETL/ELT pipelines, Auto Loader, Delta Lake",
        "🔬 Data Science & ML: Notebooks, distributed training, MLflow",
        "📊 Business Analytics: Databricks SQL, dashboards, BI integration",
        "🎯 Real-Time Streaming: Structured Streaming, sub-second latency"
    ], top=2.5, font_size=14)

    # Slide 8: Databricks Components
    slide = add_content_slide(prs, "Inside Databricks - Key Components")
    components = [
        ("Unity Catalog", "Centralized metadata and governance layer"),
        ("Delta Lake Engine", "ACID transaction layer for data lakes"),
        ("Databricks SQL", "SQL-based analytics interface"),
        ("Workflows", "Job orchestration and scheduling"),
        ("Notebooks", "Interactive development environment"),
        ("MLflow", "ML lifecycle management")
    ]
    top = 2.0
    for comp_name, comp_desc in components:
        add_text_box(slide, f"• {comp_name}: {comp_desc}",
            left=1, top=top, width=8, height=0.5, font_size=13)
        top += 0.7

    # Slide 9: Data Processing Flow
    slide = add_content_slide(prs, "Bronze → Silver → Gold Transformation")
    add_section(slide, "Step 1: Bronze → Silver", "", top=1.8)
    add_bullets(slide, [
        "Data validation and quality checks",
        "Schema enforcement and standardization",
        "Duplicate removal and basic cleansing"
    ], top=2.3, font_size=13)
    add_section(slide, "Step 2: Silver → Gold", "", top=3.8)
    add_bullets(slide, [
        "Business logic application",
        "Data aggregations and summarizations",
        "Feature engineering for ML"
    ], top=4.3, font_size=13)
    add_text_box(slide, "Orchestration: AWS Step Functions + Lambda + EventBridge",
        left=1, top=5.8, width=8, height=0.5, font_size=12, italic=True)

    # Slide 10: Analytics & Consumption
    slide = add_content_slide(prs, "How Business Users Access Data")
    add_section(slide, "Analytics Tools Connected to Gold Zone", "", top=1.8)
    add_bullets(slide, [
        "🤖 AI-Powered: ThoughtSpot (NLP search), AWS Bedrock (GenAI)",
        "🧪 Machine Learning: Amazon SageMaker, Databricks MLflow",
        "📊 Business Intelligence: QuickSight, Tableau, Power BI, Athena",
        "🏢 Data Warehouse: Amazon Redshift"
    ], top=2.4, font_size=13)
    add_section(slide, "End User Access Patterns", "", top=4.5)
    add_bullets(slide, [
        "Business Users: Self-service analytics via BI tools",
        "Data Scientists: Model training in SageMaker/Notebooks",
        "Data Analysts: Ad-hoc SQL queries",
        "Applications: REST APIs for predictions"
    ], top=5.0, font_size=13)

    # Slide 11: Security & Governance
    slide = add_content_slide(prs, "Multi-Layered Security Approach")
    add_bullets(slide, [
        "🔐 Identity & Access: IAM, Unity Catalog, Secrets Manager",
        "🔒 Data Encryption: KMS (at rest), TLS/HTTPS (in transit)",
        "📋 Governance & Compliance: Unity Catalog, Lake Formation, Config",
        "📝 Audit & Monitoring: CloudTrail, Unity Catalog Audit Logs"
    ], top=2.0, font_size=15)
    add_text_box(slide, "Security is built into every layer - from data ingestion to consumption",
        left=1, top=5.5, width=8, height=0.8, font_size=14, italic=True, align='center')

    # Slide 12: Monitoring & Operations
    slide = add_content_slide(prs, "Observability & Operational Excellence")
    add_bullets(slide, [
        "📊 Metrics & Logging: CloudWatch (centralized logging and metrics)",
        "🔍 Distributed Tracing: X-Ray (end-to-end request tracing)",
        "🔔 Alerting: SNS (email/SMS/Slack), EventBridge (automation)",
        "⚙️ Infrastructure: Systems Manager (configuration and patching)"
    ], top=2.0, font_size=15)

    # Slide 13: Complete Data Flow
    slide = add_content_slide(prs, "End-to-End Data Flow")
    add_bullets(slide, [
        "1️⃣ Data Ingestion: Sources → AWS Services → Bronze Zone",
        "2️⃣ Data Validation: Bronze → Databricks → Silver Zone",
        "3️⃣ Data Curation: Silver → Databricks → Gold Zone",
        "4️⃣ Analytics: Gold → BI Tools/ML Platforms → Insights",
        "5️⃣ Governance: Unity Catalog + Lake Formation",
        "6️⃣ Monitoring: CloudWatch + X-Ray"
    ], top=2.0, font_size=15)
    add_text_box(slide, "Timeline: Raw data → Analytics-ready in hours (batch) or seconds (streaming)",
        left=1, top=6, width=8, height=0.5, font_size=13, italic=True, align='center')

    # Slide 14: Use Cases
    slide = add_content_slide(prs, "Real-World Use Cases")
    use_cases = [
        ("Real-Time Analytics", "Monitor customer behavior with live dashboards"),
        ("Machine Learning & AI", "Predict customer churn proactively"),
        ("Data Warehouse Modernization", "60% cost reduction, 10x faster queries"),
        ("Self-Service Analytics", "Empower users without IT bottlenecks"),
        ("Regulatory Compliance", "Complete audit trail for GDPR/SOC2/HIPAA")
    ]
    top = 2.0
    for uc_title, uc_desc in use_cases:
        add_text_box(slide, f"• {uc_title}: {uc_desc}",
            left=1, top=top, width=8, height=0.5, font_size=13)
        top += 0.9

    # Slide 15: Architecture Benefits
    slide = add_content_slide(prs, "Why This Architecture?")
    add_section(slide, "Technical Benefits", "", top=1.8)
    add_bullets(slide, [
        "⚡ Performance: 10-100x faster queries with Delta Lake",
        "📈 Scalability: Auto-scaling to petabyte-scale",
        "💰 Cost: 40-60% savings vs traditional data warehouses",
        "🔄 Flexibility: All data formats, multiple languages"
    ], top=2.3, font_size=13)
    add_section(slide, "Business Benefits", "", top=4.3)
    add_bullets(slide, [
        "📊 Unified Analytics: Single platform eliminates silos",
        "🚀 Faster Insights: Self-service without IT bottlenecks",
        "🤝 Collaboration: Shared notebooks and workflows",
        "🎯 AI/ML Ready: Foundation for AI initiatives"
    ], top=4.8, font_size=13)

    # Slide 16: Technology Stack
    slide = add_content_slide(prs, "Complete Technology Stack")
    add_bullets(slide, [
        "AWS Infrastructure: Lambda, S3, IAM, KMS, CloudWatch, Step Functions",
        "Databricks Platform: Spark, Delta Lake, Unity Catalog, MLflow",
        "Analytics & BI: SageMaker, Bedrock, QuickSight, Athena, Redshift",
        "Integration: DMS, Kinesis, API Gateway, Transfer Family, EventBridge"
    ], top=2.0, font_size=14)
    add_text_box(slide, "Best-of-breed technologies integrated into a cohesive platform",
        left=1, top=5.5, width=8, height=0.5, font_size=14, italic=True, align='center')

    # Slide 17: Key Takeaways
    slide = add_content_slide(prs, "Key Takeaways")
    add_bullets(slide, [
        "1️⃣ Unified Platform: Single platform for data engineering, data science, and analytics",
        "2️⃣ Progressive Quality: Bronze → Silver → Gold ensures data reliability",
        "3️⃣ Cloud-Native: Auto-scaling infrastructure, pay-per-use pricing",
        "4️⃣ Security-First: Multi-layered security with complete audit trail",
        "5️⃣ Business Enablement: Self-service analytics and AI/ML foundation"
    ], top=2.0, font_size=15)
    add_text_box(slide, "The lakehouse is a journey, not a destination.\nPlan for continuous improvement.",
        left=1, top=5.8, width=8, height=1, font_size=14, italic=True, align='center')

    # Slide 18: Questions & Next Steps
    slide = add_title_slide(prs, "Questions & Discussion", "")
    add_section(slide, "📚 Additional Resources", "", top=3)
    add_bullets(slide, [
        "Architecture Documentation: ARCHITECTURE_DOCUMENTATION.md",
        "Architecture Diagram: databricks-lakehouse-final-v2.drawio",
        "Databricks Docs: https://docs.databricks.com/",
        "AWS Lakehouse: https://aws.amazon.com/big-data/"
    ], top=3.6, font_size=13)
    add_section(slide, "🚀 Next Steps", "", top=5.2)
    add_bullets(slide, [
        "Review architecture with stakeholders",
        "Identify pilot use case",
        "Assemble implementation team"
    ], top=5.8, font_size=13)

    return prs

def add_title_slide(prs, title, subtitle):
    """Add title slide"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add colored background
    background = slide.shapes.add_shape(
        1,  # Rectangle
        0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = LIGHT_GREY
    background.line.fill.background()

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(2.5), Inches(8), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = DATABRICKS_GREEN
    title_para.alignment = PP_ALIGN.CENTER

    # Add subtitle if provided
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(
            Inches(1), Inches(4), Inches(8), Inches(1)
        )
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = subtitle
        subtitle_para = subtitle_frame.paragraphs[0]
        subtitle_para.font.size = Pt(24)
        subtitle_para.font.color.rgb = DARK_GREY
        subtitle_para.alignment = PP_ALIGN.CENTER

    return slide

def add_content_slide(prs, title):
    """Add content slide with title"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add white background
    background = slide.shapes.add_shape(
        1,  # Rectangle
        0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(255, 255, 255)
    background.line.fill.background()

    # Add header bar
    header = slide.shapes.add_shape(
        1,  # Rectangle
        0, 0, prs.slide_width, Inches(1)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = DATABRICKS_GREEN
    header.line.fill.background()

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.2), Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(28)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(255, 255, 255)

    return slide

def add_section(slide, title, text="", top=2.0, font_size=16):
    """Add section with title"""
    text_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(top), Inches(9), Inches(0.5)
    )
    text_frame = text_box.text_frame
    text_frame.text = title
    para = text_frame.paragraphs[0]
    para.font.size = Pt(font_size)
    para.font.bold = True
    para.font.color.rgb = AWS_BLUE

def add_bullets(slide, bullets, top=2.5, left=0.8, font_size=14):
    """Add bullet points"""
    text_box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(8.5), Inches(4)
    )
    text_frame = text_box.text_frame
    text_frame.word_wrap = True

    for bullet_text in bullets:
        p = text_frame.add_paragraph()
        p.text = bullet_text
        p.level = 0
        p.font.size = Pt(font_size)
        p.font.color.rgb = DARK_GREY
        p.space_after = Pt(8)

def add_text_box(slide, text, left, top, width, height, font_size=14,
                 bold=False, italic=False, align='left'):
    """Add text box"""
    text_box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    text_frame = text_box.text_frame
    text_frame.text = text
    text_frame.word_wrap = True

    para = text_frame.paragraphs[0]
    para.font.size = Pt(font_size)
    if bold:
        para.font.bold = True
    if italic:
        para.font.italic = True
    para.font.color.rgb = DARK_GREY

    if align == 'center':
        para.alignment = PP_ALIGN.CENTER
    elif align == 'right':
        para.alignment = PP_ALIGN.RIGHT

if __name__ == "__main__":
    print("Creating PowerPoint presentation...")
    prs = create_presentation()

    output_file = "Databricks_Architecture_Presentation.pptx"
    prs.save(output_file)
    print(f"✅ PowerPoint presentation created: {output_file}")
    print(f"\nNext steps:")
    print("1. Open the .pptx file in PowerPoint")
    print("2. Add the architecture diagram image to Slide 4")
    print("3. Apply your corporate template if needed")
    print("4. Review and adjust formatting as needed")
