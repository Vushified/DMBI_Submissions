#!/usr/bin/env python3
"""Generate Star and Snowflake Schema SVG diagrams for Smart EV Charging Analytics."""
import os

ROW_H = 34
HDR_H = 36
COL_TYPE_W = 60
FONT = "Segoe UI, Arial, sans-serif"

def table_svg(x, y, name, rows, header_color="#E3F2FD", border_color="#1976D2"):
    key_w = 40
    name_col_w = max([len(r[1]) for r in rows] + [len(name)]) * 8 + 30
    w = COL_TYPE_W + name_col_w + key_w
    h = HDR_H + ROW_H * len(rows)
    out = ["<g>"]
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{HDR_H}" fill="{header_color}" stroke="{border_color}" stroke-width="1.5" rx="3"/>')
    out.append(f'<text x="{x+w/2}" y="{y+HDR_H/2+5}" text-anchor="middle" font-size="14px" font-weight="bold" fill="#0D47A1">{name}</text>')
    for i, (typ, col, key) in enumerate(rows):
        ry = y + HDR_H + i * ROW_H
        bg = "#FFFFFF" if i % 2 == 0 else "#F8FAFC"
        out.append(f'<rect x="{x}" y="{ry}" width="{w}" height="{ROW_H}" fill="{bg}" stroke="{border_color}" stroke-width="0.8"/>')
        out.append(f'<line x1="{x+COL_TYPE_W}" y1="{ry}" x2="{x+COL_TYPE_W}" y2="{ry+ROW_H}" stroke="{border_color}" stroke-width="0.8"/>')
        out.append(f'<line x1="{x+COL_TYPE_W+name_col_w}" y1="{ry}" x2="{x+COL_TYPE_W+name_col_w}" y2="{ry+ROW_H}" stroke="{border_color}" stroke-width="0.8"/>')
        out.append(f'<text x="{x+8}" y="{ry+ROW_H/2+4}" font-size="12px" fill="#546E7A">{typ}</text>')
        out.append(f'<text x="{x+COL_TYPE_W+8}" y="{ry+ROW_H/2+4}" font-size="12px" font-weight="500" fill="#263238">{col}</text>')
        key_color = "#C62828" if key == "PK" else ("#1565C0" if key == "FK" else "#90A4AE")
        out.append(f'<text x="{x+COL_TYPE_W+name_col_w+8}" y="{ry+ROW_H/2+4}" font-size="11px" font-weight="bold" fill="{key_color}">{key}</text>')
    out.append("</g>")
    return "\n".join(out), w, h

def draw_edge(x1, y1, x2, y2, label="", color="#37474F"):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    path = f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" stroke-width="1.5" stroke-dasharray="none"/>'
    text = f'<text x="{mx}" y="{my-5}" text-anchor="middle" font-size="11px" fill="{color}" font-style="italic">{label}</text>' if label else ""
    return path + "\n" + text

def generate_star_charging(out_dir):
    W, H = 1200, 950
    fact_rows = [
        ("int", "session_id", "PK"),
        ("int", "driver_id", "FK"),
        ("int", "vehicle_id", "FK"),
        ("int", "station_id", "FK"),
        ("int", "tariff_id", "FK"),
        ("int", "date_id", "FK"),
        ("float", "energy_consumed_kwh", ""),
        ("int", "charging_duration_min", ""),
        ("float", "initial_soc_pct", ""),
        ("float", "final_soc_pct", ""),
        ("float", "charging_cost_inr", ""),
        ("float", "peak_power_kw", "")
    ]
    f_svg, fw, fh = table_svg(460, 360, "Fact_Charging_Sessions", fact_rows, "#E8F5E9", "#2E7D32")
    
    d1, w1, h1 = table_svg(470, 30, "Dim_Time_Date", [("int", "date_id", "PK"), ("date", "full_date", ""), ("int", "hour_of_day", ""), ("string", "day_of_week", ""), ("bool", "peak_hour_flag", "")], "#FFF3E0", "#EF6C00")
    d2, w2, h2 = table_svg(50, 100, "Dim_Driver", [("int", "driver_id", "PK"), ("string", "driver_name", ""), ("string", "driver_type", ""), ("string", "loyalty_tier", "")], "#EDE7F6", "#512DA8")
    d3, w3, h3 = table_svg(40, 500, "Dim_EV_Vehicle", [("int", "vehicle_id", "PK"), ("string", "oem_brand", ""), ("string", "model_name", ""), ("float", "battery_kwh", ""), ("string", "chemistry", "")], "#EDE7F6", "#512DA8")
    d4, w4, h4 = table_svg(850, 100, "Dim_Station", [("int", "station_id", "PK"), ("string", "station_name", ""), ("string", "charger_type", ""), ("string", "city", ""), ("int", "total_ports", "")], "#EDE7F6", "#512DA8")
    d5, w5, h5 = table_svg(850, 500, "Dim_Tariff_Plan", [("int", "tariff_id", "PK"), ("string", "plan_name", ""), ("string", "rate_type", ""), ("float", "rate_per_kwh", "")], "#EDE7F6", "#512DA8")
    
    edges = [
        draw_edge(470 + w1/2, 30 + h1, 460 + fw/2, 360, "occurs on"),
        draw_edge(50 + w2, 100 + h2/2, 460, 360 + 60, "initiated by"),
        draw_edge(40 + w3, 500 + h3/2, 460, 360 + 200, "charges"),
        draw_edge(850, 100 + h4/2, 460 + fw, 360 + 60, "plugged at"),
        draw_edge(850, 500 + h5/2, 460 + fw, 360 + 200, "billed under"),
    ]
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<rect width="{W}" height="{H}" fill="#FAFAFA"/>
<text x="{W/2}" y="26" text-anchor="middle" font-size="18px" font-weight="bold" fill="#1A237E">Star Schema: Smart EV Charging Operational Platform (Fact_Charging_Sessions)</text>
{"\n".join(edges)}
{f_svg}
{d1} {d2} {d3} {d4} {d5}
</svg>'''
    with open(os.path.join(out_dir, "STAR_Charging_Sessions.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def generate_star_battery(out_dir):
    W, H = 1150, 850
    fact_rows = [
        ("int", "telemetry_id", "PK"),
        ("int", "battery_pack_id", "FK"),
        ("int", "vehicle_id", "FK"),
        ("int", "date_id", "FK"),
        ("float", "soh_percentage", ""),
        ("int", "cycle_count", ""),
        ("float", "internal_res_mohm", ""),
        ("float", "max_cell_temp_c", ""),
        ("float", "cell_delta_mv", ""),
        ("bool", "thermal_warning_flag", "")
    ]
    f_svg, fw, fh = table_svg(440, 280, "Fact_Battery_Health", fact_rows, "#E0F2F1", "#00695C")
    
    d1, w1, h1 = table_svg(460, 30, "Dim_Time_Date", [("int", "date_id", "PK"), ("date", "full_date", ""), ("int", "month", ""), ("int", "year", "")], "#FFF3E0", "#EF6C00")
    d2, w2, h2 = table_svg(40, 280, "Dim_Battery_Pack", [("int", "battery_pack_id", "PK"), ("string", "serial_number", ""), ("string", "cell_format", ""), ("float", "nominal_voltage", ""), ("string", "cooling_type", "")], "#EDE7F6", "#512DA8")
    d3, w3, h3 = table_svg(820, 280, "Dim_EV_Vehicle", [("int", "vehicle_id", "PK"), ("string", "oem_brand", ""), ("string", "model_name", ""), ("float", "fleet_id", "")], "#EDE7F6", "#512DA8")
    
    edges = [
        draw_edge(460 + w1/2, 30 + h1, 440 + fw/2, 280, "measured at"),
        draw_edge(40 + w2, 280 + h2/2, 440, 280 + 100, "monitors"),
        draw_edge(820, 280 + h3/2, 440 + fw, 280 + 100, "installed on"),
    ]
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<rect width="{W}" height="{H}" fill="#FAFAFA"/>
<text x="{W/2}" y="26" text-anchor="middle" font-size="18px" font-weight="bold" fill="#004D40">Star Schema: EV Fleet Battery Health & Telemetry Analytics (Fact_Battery_Health)</text>
{"\n".join(edges)}
{f_svg}
{d1} {d2} {d3}
</svg>'''
    with open(os.path.join(out_dir, "STAR_Battery_Health.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def generate_snowflake(out_dir):
    W, H = 1380, 980
    fact_rows = [
        ("int", "session_id", "PK"),
        ("int", "station_id", "FK"),
        ("int", "vehicle_id", "FK"),
        ("int", "driver_id", "FK"),
        ("int", "date_id", "FK"),
        ("float", "energy_kwh", ""),
        ("int", "duration_min", ""),
        ("float", "cost_inr", "")
    ]
    f_svg, fw, fh = table_svg(520, 380, "Fact_Charging_Sessions", fact_rows, "#E8F5E9", "#2E7D32")
    
    # Normalized Station Hierarchy
    d_st, w_st, h_st = table_svg(880, 380, "Dim_Station", [("int", "station_id", "PK"), ("string", "name", ""), ("int", "city_id", "FK"), ("string", "charger_type", "")], "#EDE7F6", "#512DA8")
    d_city, w_city, h_city = table_svg(880, 180, "Dim_City", [("int", "city_id", "PK"), ("string", "city_name", ""), ("int", "state_id", "FK")], "#F3E5F5", "#7B1FA2")
    d_state, w_state, h_state = table_svg(880, 20, "Dim_State", [("int", "state_id", "PK"), ("string", "state_name", ""), ("string", "region_zone", "")], "#F3E5F5", "#7B1FA2")
    
    # Normalized Vehicle Hierarchy
    d_veh, w_veh, h_veh = table_svg(160, 380, "Dim_EV_Vehicle", [("int", "vehicle_id", "PK"), ("string", "model_name", ""), ("int", "oem_id", "FK"), ("float", "battery_kwh", "")], "#EDE7F6", "#512DA8")
    d_oem, w_oem, h_oem = table_svg(160, 180, "Dim_OEM_Brand", [("int", "oem_id", "PK"), ("string", "brand_name", ""), ("int", "category_id", "FK")], "#F3E5F5", "#7B1FA2")
    d_cat, w_cat, h_cat = table_svg(160, 20, "Dim_Vehicle_Category", [("int", "category_id", "PK"), ("string", "category_name", ""), ("string", "segment_class", "")], "#F3E5F5", "#7B1FA2")
    
    d_date, w_date, h_date = table_svg(520, 40, "Dim_Time_Date", [("int", "date_id", "PK"), ("date", "full_date", ""), ("int", "hour", ""), ("string", "day_of_week", "")], "#FFF3E0", "#EF6C00")
    d_driver, w_driver, h_driver = table_svg(520, 750, "Dim_Driver", [("int", "driver_id", "PK"), ("string", "name", ""), ("string", "loyalty_tier", "")], "#EDE7F6", "#512DA8")
    
    edges = [
        draw_edge(520 + fw, 380 + 80, 880, 380 + 40, "station_id"),
        draw_edge(880 + w_st/2, 380, 880 + w_city/2, 180 + h_city, "city_id"),
        draw_edge(880 + w_city/2, 180, 880 + w_state/2, 20 + h_state, "state_id"),
        
        draw_edge(520, 380 + 80, 160 + w_veh, 380 + 40, "vehicle_id"),
        draw_edge(160 + w_veh/2, 380, 160 + w_oem/2, 180 + h_oem, "oem_id"),
        draw_edge(160 + w_oem/2, 180, 160 + w_cat/2, 20 + h_cat, "category_id"),
        
        draw_edge(520 + fw/2, 40 + h_date, 520 + fw/2, 380, "date_id"),
        draw_edge(520 + fw/2, 380 + fh, 520 + fw/2, 750, "driver_id")
    ]
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<rect width="{W}" height="{H}" fill="#FAFAFA"/>
<text x="{W/2}" y="26" text-anchor="middle" font-size="18px" font-weight="bold" fill="#283593">Snowflake Schema: Normalized Hierarchies for EV Charging Analytics</text>
{"\n".join(edges)}
{f_svg}
{d_st} {d_city} {d_state}
{d_veh} {d_oem} {d_cat}
{d_date} {d_driver}
</svg>'''
    with open(os.path.join(out_dir, "SNOWFLAKE_EV_Platform.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == '__main__':
    target_dir = os.path.dirname(os.path.abspath(__file__))
    generate_star_charging(target_dir)
    generate_star_battery(target_dir)
    generate_snowflake(target_dir)
    print('All EV Schema diagrams generated successfully in', target_dir)

