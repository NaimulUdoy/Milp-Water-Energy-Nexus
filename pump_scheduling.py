"""
Mixed-Integer Linear Programming (MILP) model for optimal water pump scheduling 
under variable electricity pricing.
"""
import cvxpy as cp
import numpy as np
from config import (
    HOURS, GRID_PRICE, WATER_DEMAND,
    TANK_CAPACITY, TANK_MIN_VOL, TANK_MAX_VOL, TANK_INITIAL,
    PUMP_CAPACITY, PUMP_POWER_KW
)

def solve_pump_scheduling():
    """
    Solves the optimal pump scheduling problem to minimize total energy cost.
    """
    # Decision Variables
    # Continuous variables
    pump_flow = cp.Variable(HOURS, name="pump_flow")       # Water pumped into tank (m^3/h)
    tank_volume = cp.Variable(HOURS + 1, name="tank_volume") # Tank water volume (m^3)
    power_consumed = cp.Variable(HOURS, name="power_consumed") # Electrical power (kW)
    
    # Binary variables (MILP component for pump on/off status)
    u_pump = cp.Variable(HOURS, boolean=True)

    constraints = []

    # Initial and boundary conditions for water tank storage
    constraints += [tank_volume[0] == TANK_INITIAL]
    constraints += [tank_volume[HOURS] >= TANK_INITIAL] # Ensure tank is refilled by end of day

    for t in range(HOURS):
        # 1. Tank Mass Balance Constraint
        # Volume[t+1] = Volume[t] + Inflow (Pumping) - Outflow (Community Demand)
        constraints += [
            tank_volume[t+1] == tank_volume[t] + pump_flow[t] - WATER_DEMAND[t]
        ]

        # 2. Tank Storage Operational Limits
        constraints += [tank_volume[t] >= TANK_MIN_VOL]
        constraints += [tank_volume[t] <= TANK_MAX_VOL]

        # 3. Pump Capacity and Commitment Constraints
        constraints += [pump_flow[t] >= 0]
        constraints += [pump_flow[t] <= PUMP_CAPACITY * u_pump[t]]

        # 4. Energy Consumption Coupling (Linear scaling with pump flow rate)
        # Assuming power scale factor is proportional to flow rate ratio
        power_scale = PUMP_POWER_KW / PUMP_CAPACITY
        constraints += [power_consumed[t] == power_scale * pump_flow[t]]

    # Objective Function: Minimize total electricity cost ($)
    total_energy_cost = cp.sum(cp.multiply(GRID_PRICE, power_consumed))
    objective = cp.Minimize(total_energy_cost)

    prob = cp.Problem(objective, constraints)
    
    # Solve using an MILP solver available in CVXPY (e.g., ECOS_BB, CBC, GLPK_MI)
    prob.solve(solver=cp.ECOS_BB, verbose=False)

    results = {
        "status": prob.status,
        "total_cost": prob.value,
        "pump_flow": pump_flow.value,
        "tank_volume": tank_volume.value[:-1],
        "power_consumed": power_consumed.value,
        "u_pump": u_pump.value
    }
    return results