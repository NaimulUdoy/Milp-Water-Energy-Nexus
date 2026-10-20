"""
Configuration parameters for the Water-Energy Nexus Pump Scheduling model.
"""
import numpy as np

# Operational Horizon (24 hours)
HOURS = 24

# Time-of-Use (TOU) Electricity Grid Prices ($/kWh)
GRID_PRICE = np.array([
    0.06, 0.05, 0.05, 0.06, 0.08, 0.12,  # Hours 0-5 (Night/Morning transition)
    0.18, 0.24, 0.22, 0.15, 0.12, 0.10,  # Hours 6-11 (Peak morning hours)
    0.10, 0.11, 0.13, 0.16, 0.26, 0.28,  # Hours 12-17 (Peak evening hours)
    0.20, 0.14, 0.10, 0.08, 0.07, 0.06   # Hours 18-23 (Night)
])

# Community Water Demand Profile (cubic meters per hour, m^3/h)
WATER_DEMAND = np.array([
    120, 90, 80, 85, 110, 180,
    250, 310, 290, 240, 220, 210,
    205, 215, 230, 260, 340, 380,
    350, 280, 220, 180, 150, 130
])

# Water Storage Tank Parameters
TANK_CAPACITY = 2000.0  # Maximum tank volume (m^3)
TANK_MIN_VOL = 400.0    # Minimum reserve volume (m^3)
TANK_MAX_VOL = 1900.0   # Maximum operational volume (m^3)
TANK_INITIAL = 1000.0   # Starting volume at hour 0 (m^3)

# Pump Station Parameters (Multiple pumps or a scalable pump unit)
PUMP_CAPACITY = 350.0   # Maximum water pumping rate (m^3/h)
PUMP_POWER_KW = 110.0   # Power consumption rate at full capacity (kW)