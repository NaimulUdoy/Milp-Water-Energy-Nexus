"""
Main execution script for the Water-Energy Nexus Pump Dispatch Optimizer.
"""
import numpy as np
from models.pump_scheduling import solve_pump_scheduling
from config import WATER_DEMAND, GRID_PRICE

def main():
    print("=== Running Water-Energy Nexus MILP Pump Optimization ===")
    res = solve_pump_scheduling()
    
    print(f"Optimization Status: {res['status']}")
    print(f"Total Daily Electricity Pumping Cost: ${res['total_cost']:.2f}\n")

    print(f"{'Hour':<5} | {'Price ($/kWh)':<14} | {'Demand (m^3)':<14} | {'Pump Flow':<12} | {'State':<8} | {'Tank Vol (m^3)':<14}")
    print("-" * 78)
    
    for h in range(len(WATER_DEMAND)):
        pump_state = "ON" if res['u_pump'][h] > 0.5 else "OFF"
        print(f"{h:<5} | {GRID_PRICE[h]:<14.2f} | {WATER_DEMAND[h]:<14.1f} | "
              f"{res['pump_flow'][h]:<12.1f} | {pump_state:<8} | {res['tank_volume'][h]:<14.1f}")

if __name__ == "__main__":
    main()