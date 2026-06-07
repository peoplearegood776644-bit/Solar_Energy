import streamlit as tf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 0. CONFIGURATION & NAVIGATION SETUP
# ==========================================
tf.set_page_config(
    page_title="Solar Energy Analytics Hub",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Navigation Title
tf.sidebar.title("☀️ Solar Analytics Hub")
tf.sidebar.markdown("---")

# Main Navigation via Sidebar Selectbox
page = tf.sidebar.radio(
    "Navigate Dashboards",
    [
        "📊 Panel Efficiency Analyzer", 
        "💰 Homeowner Cost Calculator", 
        "🌐 Global Adoption Trends"
    ]
)

tf.sidebar.markdown("---")
tf.sidebar.info("💡 Tip: Adjust parameters real-time to watch predictive modeling change live.")

# ==========================================
# PAGE 1: 📊 SOLAR PANEL EFFICIENCY ANALYZER
# ==========================================
if page == "📊 Panel Efficiency Analyzer":
    tf.title("📊 Solar Panel Efficiency Analyzer")
    tf.markdown("Evaluate technical photovoltaic (PV) generation capacity under shifting thermal, environmental, and age degradation stressors.")
    
    # Page Layout Columns
    col_input, col_display = tf.columns(2, gap="large")
    
    with col_input:
        tf.subheader("⚙️ Technical Stressors")
        
        # User input parameters
        ambient_temp = tf.slider("Ambient Temperature (°C)", min_value=-10, max_value=50, value=25, step=1)
        irradiance = tf.slider("Solar Irradiance (W/m²)", min_value=200, max_value=1200, value=800, step=50)
        deg_years = tf.slider("System Operational Age (Years)", min_value=0, max_value=25, value=5, step=1)
        
        cell_type = tf.selectbox(
            "Photovoltaic Cell Architecture",
            ["Monocrystalline Silicon", "Polycrystalline Silicon", "Thin-Film (CdTe/CIGS)"]
        )
        
    # Cell Specs Constants Mapping
    cell_specs = {
        "Monocrystalline Silicon": {"base_eff": 0.22, "temp_coeff": -0.0035},
        "Polycrystalline Silicon": {"base_eff": 0.17, "temp_coeff": -0.0040},
        "Thin-Film (CdTe/CIGS)":   {"base_eff": 0.12, "temp_coeff": -0.0020}
    }
    
    selected_spec = cell_specs[cell_type]
    base_eta = selected_spec["base_eff"]
    t_coeff = selected_spec["temp_coeff"]
    panel_area = 1.7 # Standard panel area in m²
    
    # Core Mathematical Formulations
    t_cell = ambient_temp + (irradiance * 0.03) # Thermal rise formula
    
    # Thermal Deficit Loss Calculation
    if t_cell > 25.0:
        thermal_loss_factor = 1.0 + (t_coeff * (t_cell - 25.0))
        thermal_loss_factor = max(0.0, thermal_loss_factor)
    else:
        thermal_loss_factor = 1.0 # No thermal penalties below Standard Test Conditions (STC)
        
    # Compounding Age Degradation calculation (0.5% per annum)
    age_loss_factor = (1.0 - 0.005) ** deg_years
    
    # Final Efficiencies & Wattage Deliverables
    effective_efficiency = base_eta * thermal_loss_factor * age_loss_factor
    current_power_output = irradiance * panel_area * effective_efficiency
    
    # Ideal Output under STC (25°C cell, 1000 W/m², no age wear)
    ideal_stc_power = 1000 * panel_area * base_eta
    power_lost_heat_age = (irradiance * panel_area * base_eta) - current_power_output
    power_lost_heat_age = max(0.0, power_lost_heat_age)
    
    with col_display:
        tf.subheader("📈 Real-Time Output Analytics")
        
        # Metric Layout Block
        m1, m2, m3 = tf.columns(3)
        m1.metric("Effective Efficiency", f"{effective_efficiency * 100:.2f}%", f"Base: {base_eta*100:.0f}%", delta_color="off")
        m2.metric("Current Power per Panel", f"{current_power_output:.1f} W", f"STC Peak: {ideal_stc_power:.0f}W", delta_color="off")
        m3.metric("Heat & Age Energy Loss", f"{power_lost_heat_age:.1f} W", delta=None)
        
        tf.markdown("---")
        
        # Generate Irradiance Performance Curve Data
        irradiance_range = np.linspace(200, 1200, 50)
        curve_data = []
        
        for irr in irradiance_range:
            tc = ambient_temp + (irr * 0.03)
            tlf = max(0.0, 1.0 + (t_coeff * (tc - 25.0))) if tc > 25.0 else 1.0
            eff = base_eta * tlf * age_loss_factor
            power = irr * panel_area * eff
            ideal_p = irr * panel_area * base_eta
            
            curve_data.append({"Irradiance": irr, "Real Output (W)": power, "Ideal Baseline (W)": ideal_p})
            
        df_curve = pd.DataFrame(curve_data)
        
        # Interactive Plotly Curve Generation
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(x=df_curve["Irradiance"], y=df_curve["Real Output (W)"], name="De-rated Operating Output", line=dict(color="#FF4B4B", width=3)))
        fig_curve.add_trace(go.Scatter(x=df_curve["Irradiance"], y=df_curve["Ideal Baseline (W)"], name="Ideal STC Architecture", line=dict(color="#29B5E8", dash='dash')))
        
        fig_curve.update_layout(
            title=f"Power Curve Analysis: {cell_type}",
            xaxis_title="Solar Irradiance Over Plane of Array (W/m²)",
            yaxis_title="Power Output per Module (Watts)",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        tf.plotly_chart(fig_curve, use_container_width=True)

# ==========================================
# PAGE 2: 💰 HOMEOWNER COST SAVINGS CALCULATOR
# ==========================================
elif page == "💰 Homeowner Cost Calculator":
    tf.title("💰 Residential Solar Cost Savings & ROI Calculator")
    tf.markdown("Model financial return structures, break-even milestones, and localized micro-grid capital expenditure depreciation forecasts.")
    
    c_in, c_out = tf.columns(2, gap="large")
    
    with c_in:
        tf.subheader("💵 Financial Inputs")
        monthly_bill = tf.number_input("Average Monthly Electric Bill ($)", min_value=10, max_value=2000, value=250, step=10)
        grid_rate = tf.number_input("Utility Grid Tariff ($/kWh)", min_value=0.05, max_value=0.80, value=0.22, step=0.01)
        system_size = tf.slider("Target Solar Array Size (kW)", min_value=2.0, max_value=15.0, value=6.5, step=0.5)
        install_cost = tf.number_input("Gross Installation Cost ($)", min_value=1000, max_value=100000, value=18500, step=500)
        buyback_rate = tf.number_input("Net Metering Buyback Rate ($/kWh)", min_value=0.00, max_value=0.50, value=0.08, step=0.01)
        
    # Financial Analytics Math
    monthly_consumption_kwh = monthly_bill / grid_rate
    daily_consumption_kwh = monthly_consumption_kwh / 30.0
    
    # Yield output calculation using standard 4.5 peak sun hours rule
    daily_solar_production_kwh = system_size * 4.5 
    monthly_solar_production_kwh = daily_solar_production_kwh * 30.0
    
    # Financial Offset Engine
    if monthly_solar_production_kwh >= monthly_consumption_kwh:
        excess_kwh = monthly_solar_production_kwh - monthly_consumption_kwh
        monthly_savings = monthly_bill + (excess_kwh * buyback_rate)
    else:
        offset_savings = monthly_solar_production_kwh * grid_rate
        monthly_savings = offset_savings
        
    annual_savings = monthly_savings * 12.0
    payback_period = install_cost / annual_savings if annual_savings > 0 else float('inf')
    
    # 20-Year Capital Cash Flow Simulation with Net Present Value (Discount Rate = 5%)
    discount_rate = 0.05
    cumulative_cash_flow = -install_cost
    npv = -install_cost
    
    cash_flows_chart_data = [{"Year": 0, "Cumulative Balance ($)": cumulative_cash_flow, "Status": "Negative Balance"}]
    
    for year in range(1, 21):
        degraded_annual_savings = annual_savings * ((1.0 - 0.005) ** year)
        cumulative_cash_flow += degraded_annual_savings
        npv += degraded_annual_savings / ((1.0 + discount_rate) ** year)
        status = "Investment Recovered" if cumulative_cash_flow >= 0 else "Negative Balance"
        
        cash_flows_chart_data.append({
            "Year": year, 
            "Cumulative Balance ($)": cumulative_cash_flow, 
            "Status": status
        })
        
    df_finance = pd.DataFrame(cash_flows_chart_data)
    
    with c_out:
        tf.subheader("📈 Financial Returns Overview")
        
        f1, f2, f3 = tf.columns(3)
        f1.metric("Annual Savings Offset", f"${annual_savings:.2f}")
        f2.metric("Estimated Payback Period", f"{payback_period:.1f} Years" if payback_period != float('inf') else "N/A")
        f3.metric("Net Present Value (NPV)", f"${npv:.2f}")
        
        tf.markdown("---")
        
        # Interactive Cash Flow Chart
        fig_finance = px.bar(
            df_finance, 
            x="Year", 
            y="Cumulative Balance ($)", 
            color="Status",
            color_discrete_map={"Negative Balance": "#FF4B4B", "Investment Recovered": "#00D488"},
            title="20-Year Long-Term Cumulative Cash Recovery Projection"
        )
        fig_finance.add_hline(y=0, line_dash="dash", line_color="white", alpha=0.5)
        tf.plotly_chart(fig_finance, use_container_width=True)

# ==========================================
# PAGE 3: 🌐 GLOBAL ADOPTION TRENDS
# ==========================================
elif page == "🌐 Global Adoption Trends":
    tf.title("🌐 Global Solar Adoption Trends")
    tf.markdown("Analyze global historical data demonstrating photovoltaic grid integration growth across major industrial nations.")
    
    # Global dataset for visualization engine
    global_data = {
        "Year": sorted(list(range(2018, 2026)) * 4),
        "Country": ["China", "United States", "Germany", "India"] * 8,
        "Capacity (GW)": [
            175, 62, 45, 28,  # 2018
            205, 76, 49, 35,  # 2019
            253, 97, 54, 41,  # 2020
            306, 123, 59, 49, # 2021
