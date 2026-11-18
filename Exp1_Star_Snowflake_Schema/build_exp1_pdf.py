#!/usr/bin/env python3
"""Build comprehensive university-standard PDF report for Experiment 1."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Experiment 1: Star & Snowflake Schema Design (Smart EV Charging Analytics)")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(pdf_path, img_dir):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0D47A1'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#37474F'),
        spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1565C0'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2E7D32'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#212121'),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#212121'),
        leftIndent=15,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#212121')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0D47A1')
    )
    table_hdr = ParagraphStyle(
        'TableHdr',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Experiment 1 – Star and Snowflake Schema Design", title_style))
    story.append(Paragraph("<b>Domain:</b> Smart Electric Vehicle (EV) Charging & Fleet Battery Telemetry Analytics", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Name:</b> Vidushi Singh", table_cell),
            Paragraph("<b>Roll No:</b> 53", table_cell),
            Paragraph("<b>Class / Div:</b> D15A", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 150, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CFD8DC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Aim & Objectives
    story.append(Paragraph("Aim", h1_style))
    story.append(Paragraph("To conceptualize, model, and design two dimensional Star Schemas (Operational Charging Sessions and Battery Health Telemetry) and an enterprise Snowflake Schema for a nationwide Smart Electric Vehicle (EV) Charging Network (such as Ather Grid / Tata Power EZ Charge), identifying appropriate fact tables, dimension hierarchies, primary/foreign key relationships, and additive measures.", body_style))
    
    story.append(Paragraph("Objectives", h1_style))
    story.append(Paragraph("• Understand fundamental principles of multidimensional data warehouse design and OLAP architectures.", bullet_style))
    story.append(Paragraph("• Construct a central operational Star Schema (Fact_Charging_Sessions) for energy dispatch and billing analytics.", bullet_style))
    story.append(Paragraph("• Construct an asset health Star Schema (Fact_Battery_Health) for predictive battery degradation and thermal safety.", bullet_style))
    story.append(Paragraph("• Design a fully normalized Snowflake Schema decomposing station geography and vehicle manufacturer hierarchies.", bullet_style))
    story.append(Paragraph("• Benchmark analytical OLAP querying performance between denormalized Star and normalized Snowflake representations.", bullet_style))

    # Theory
    story.append(Paragraph("Theoretical Foundation", h1_style))
    story.append(Paragraph("A <b>Data Warehouse Schema</b> serves as the structural blueprint organizing business events into measurable numeric metrics (facts) and context-giving descriptive attributes (dimensions). In high-throughput IoT domains like EV charging networks, telemetry streams from smart EVSEs (Electric Vehicle Supply Equipment) and battery management systems (BMS) must support multi-grain slice-and-dice queries across temporal, geographical, vehicle, and tariff planes.", body_style))
    story.append(Paragraph("<b>Star Schema Architecture:</b> Employs a single central fact table directly referenced by non-normalized (denormalized) dimension tables. This provides minimal table join overhead, rapid OLAP roll-up/drill-down aggregation, and intuitive ad-hoc query formulations at the expense of controlled redundancy.", body_style))
    story.append(Paragraph("<b>Snowflake Schema Architecture:</b> Normalizes dimension tables into progressive third-normal-form (3NF) relational sub-dimensions (e.g., Station -&gt; City -&gt; State -&gt; Region). This eliminates attribute redundancy, minimizes storage footprint, and ensures strict master-data integrity, while introducing multi-table join overhead during analytical execution.", body_style))

    story.append(PageBreak())

    # Star Schema 1
    story.append(Paragraph("1. Star Schema 1: Smart EV Operational Charging Platform", h1_style))
    story.append(Paragraph("The central fact table <code>Fact_Charging_Sessions</code> logs each discreet EV charging event. It tracks energy delivered, session duration, state of charge (SoC) progression, peak power, and billing amount across dimensions.", body_style))
    
    img_star1 = os.path.join(img_dir, "STAR_Charging_Sessions.png")
    if os.path.exists(img_star1):
        story.append(Image(img_star1, width=500, height=350))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Data Dictionary: Fact_Charging_Sessions", h2_style))
    fact1_data = [
        [Paragraph("Field Name", table_hdr), Paragraph("Type", table_hdr), Paragraph("Key", table_hdr), Paragraph("Business Description", table_hdr)],
        [Paragraph("session_id", table_cell_bold), Paragraph("BIGINT", table_cell), Paragraph("PK", table_cell_bold), Paragraph("Unique charging transaction identifier", table_cell)],
        [Paragraph("driver_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Driver (Account & loyalty profile)", table_cell)],
        [Paragraph("vehicle_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_EV_Vehicle (OEM, model, battery pack)", table_cell)],
        [Paragraph("station_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Station (Charger type, location)", table_cell)],
        [Paragraph("tariff_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Tariff_Plan (Time-of-use pricing tier)", table_cell)],
        [Paragraph("date_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Time_Date (Timestamp, hour, peak flag)", table_cell)],
        [Paragraph("energy_consumed_kwh", table_cell), Paragraph("DECIMAL(8,2)", table_cell), Paragraph("-", table_cell), Paragraph("Total electric energy transferred into battery (kWh)", table_cell)],
        [Paragraph("charging_duration_min", table_cell), Paragraph("INT", table_cell), Paragraph("-", table_cell), Paragraph("Duration of connection in minutes", table_cell)],
        [Paragraph("initial_soc_pct", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("State of Charge percentage upon plug-in (0–100%)", table_cell)],
        [Paragraph("final_soc_pct", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("State of Charge percentage upon unplug (0–100%)", table_cell)],
        [Paragraph("charging_cost_inr", table_cell), Paragraph("DECIMAL(8,2)", table_cell), Paragraph("-", table_cell), Paragraph("Total revenue invoiced to subscriber in INR (₹)", table_cell)],
        [Paragraph("peak_power_kw", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("Maximum sustained charging rate observed (kW)", table_cell)]
    ]
    t1 = Table(fact1_data, colWidths=[110, 70, 40, 284])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B5E20')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F8E9')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)

    story.append(PageBreak())

    # Star Schema 2
    story.append(Paragraph("2. Star Schema 2: Fleet Battery Health & Predictive Maintenance", h1_style))
    story.append(Paragraph("The asset health fact table <code>Fact_Battery_Health</code> captures periodic telemetry streams from vehicle Battery Management Systems (BMS) to detect capacity loss, thermal stress, and internal cell degradation.", body_style))

    img_star2 = os.path.join(img_dir, "STAR_Battery_Health.png")
    if os.path.exists(img_star2):
        story.append(Image(img_star2, width=490, height=330))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Data Dictionary: Fact_Battery_Health", h2_style))
    fact2_data = [
        [Paragraph("Field Name", table_hdr), Paragraph("Type", table_hdr), Paragraph("Key", table_hdr), Paragraph("Business Description", table_hdr)],
        [Paragraph("telemetry_id", table_cell_bold), Paragraph("BIGINT", table_cell), Paragraph("PK", table_cell_bold), Paragraph("Unique telemetry sample record identifier", table_cell)],
        [Paragraph("battery_pack_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Battery_Pack (Chemistry, cooling type)", table_cell)],
        [Paragraph("vehicle_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_EV_Vehicle (Fleet vehicle identifier)", table_cell)],
        [Paragraph("date_id", table_cell_bold), Paragraph("INT", table_cell), Paragraph("FK", table_cell_bold), Paragraph("References Dim_Time_Date (Reading timestamp)", table_cell)],
        [Paragraph("soh_percentage", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("Current State of Health (SOH) relative to nominal capacity", table_cell)],
        [Paragraph("cycle_count", table_cell), Paragraph("INT", table_cell), Paragraph("-", table_cell), Paragraph("Cumulative full equivalent charge/discharge cycles", table_cell)],
        [Paragraph("internal_res_mohm", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("Equivalent series internal resistance (milli-ohms)", table_cell)],
        [Paragraph("max_cell_temp_c", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("Peak individual cell temperature during cycle (°C)", table_cell)],
        [Paragraph("cell_delta_mv", table_cell), Paragraph("FLOAT", table_cell), Paragraph("-", table_cell), Paragraph("Maximum voltage deviation between weakest/strongest cells", table_cell)],
        [Paragraph("thermal_warning_flag", table_cell), Paragraph("BOOLEAN", table_cell), Paragraph("-", table_cell), Paragraph("Binary trigger when cell temp exceeds 45°C threshold", table_cell)]
    ]
    t2 = Table(fact2_data, colWidths=[110, 70, 40, 284])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#004D40')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#E0F2F1')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # Snowflake Schema
    story.append(Paragraph("3. Snowflake Schema: Enterprise Multi-Level Dimensional Hierarchy", h1_style))
    story.append(Paragraph("In the enterprise Snowflake Schema, high-cardinality dimensions are normalized into distinct sub-tables. Station locations decompose into <code>Dim_Station -&gt; Dim_City -&gt; Dim_State</code>, while vehicles normalize into <code>Dim_EV_Vehicle -&gt; Dim_OEM_Brand -&gt; Dim_Vehicle_Category</code>.", body_style))

    img_snow = os.path.join(img_dir, "SNOWFLAKE_EV_Platform.png")
    if os.path.exists(img_snow):
        story.append(Image(img_snow, width=500, height=330))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Comparative Architectural Analysis: Star vs Snowflake Schema", h1_style))
    comp_data = [
        [Paragraph("Evaluation Parameter", table_hdr), Paragraph("Star Schema", table_hdr), Paragraph("Snowflake Schema", table_hdr)],
        [Paragraph("Normalisation Level", table_cell_bold), Paragraph("Denormalised (Dimensions in 2NF / 1NF)", table_cell), Paragraph("Fully Normalised (Dimensions split into 3NF)", table_cell)],
        [Paragraph("Query Complexity", table_cell_bold), Paragraph("Simple single-level JOINs; straightforward SQL", table_cell), Paragraph("Complex multi-level hierarchical JOIN paths", table_cell)],
        [Paragraph("Query Response Speed", table_cell_bold), Paragraph("Significantly faster for OLAP roll-up / drill-down", table_cell), Paragraph("Slower due to relational foreign key traversal", table_cell)],
        [Paragraph("Storage & Redundancy", table_cell_bold), Paragraph("Controlled redundancy across dimension text values", table_cell), Paragraph("Minimal storage footprint; zero duplicate values", table_cell)],
        [Paragraph("Data Maintenance & ETL", table_cell_bold), Paragraph("Potential anomalies during manual attribute updates", table_cell), Paragraph("High integrity; single-point dimension updates", table_cell)],
        [Paragraph("Target Use Case", table_cell_bold), Paragraph("Real-time executive dashboards & business KPI BI", table_cell), Paragraph("Enterprise data warehouses with vast master taxonomies", table_cell)]
    ]
    t3 = Table(comp_data, colWidths=[120, 192, 192])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#283593')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#EDE7F6')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t3)
    story.append(Spacer(1, 10))

    # Conclusion
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("In this experiment, two comprehensive Star Schemas and an enterprise Snowflake Schema were successfully designed and implemented for a Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics platform. The operational Star Schema (<code>Fact_Charging_Sessions</code>) optimizes energy delivery and revenue analytics across drivers, vehicles, stations, and tariffs. The asset-health Star Schema (<code>Fact_Battery_Health</code>) enables real-time detection of battery degradation, cell imbalance, and thermal stress. Finally, the Snowflake Schema establishes normalized geographic and vehicle hierarchies, illustrating the trade-off between normalized data integrity and denormalized query throughput.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == '__main__':
    base_dir = r'.\DMBI-Lab-Vidushi\Exp1_Star_Snowflake_Schema'
    out_pdf = os.path.join(base_dir, "EXP-1_DMBI_53_EV_Charging_Platform.pdf")
    build_pdf(out_pdf, base_dir)

