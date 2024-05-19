from gurobipy import Model, GRB

from gurobipy import *

def solve_knapsack(values, constraint_values):
    """
    This function solves a knapsack problem to maximize the total value of items,
    considering multiple constraint limits.

    Args:
        values: A list representing the value of each item.
        constraint_values: A dictionary where each key represents a constraint type
                           and each value is a dictionary with 'values' representing
                           the constraint values for each item and 'max' representing
                           the maximum limit for that constraint.

    Returns:
        A tuple containing:
            - A list of indices representing the selected items to put in the knapsack.
            - The total value of the selected items.
            - The time taken by Gurobi to solve the model (in seconds).
    """
    # Create a Gurobi model instance named "knapsack"
    m = Model("knapsack")

    # Define the number of items based on the length of the values list
    item_count = len(values)

    # Define decision variables (x) as binary variables (0 or 1)
    #   - x[i] = 1 if item i is selected, 0 otherwise
    x = m.addVars(item_count, vtype=GRB.BINARY, name="x")

    # Define the objective function to maximize the total value of selected items
    m.setObjective(sum(values[i] * x[i] for i in range(item_count)), GRB.MAXIMIZE)

    # Define constraints based on the constraint values
    for constraint_type, constraint_data in constraint_values.items():
        # Extract constraint values and maximum limit
        constraint_vals = constraint_data['values']
        constraint_max = constraint_data['max']
        
        # Add constraint: Total value of selected items for each constraint <= constraint maximum
        m.addConstr(sum(constraint_vals[i] * x[i] for i in range(item_count)) <= constraint_max, f"Constraint_{constraint_type}")

    # Solve the model using Gurobi optimizer
    m.optimize()
    
    # Check if the solution is optimal (GRB.OPTIMAL status code)
    if m.status == GRB.OPTIMAL:
        # Extract indices of selected items (where x[i] is greater than 0.5 to account for rounding errors)
        selected_items = [i for i in range(item_count) if x[i].X > 0.5]
        # Return selected items, total value, and solution time
        return selected_items, m.objVal, m.Runtime
    else:
        # If not optimal, return empty list and 0 for all values
        return [], 0

from gurobipy import *


def solve_production(products, constraints):
    """
    Solves a production planning problem focusing on maximizing profit with multiple constraints.

    Parameters:
        - products (list of dicts): Information about each product, including profit and any other relevant data.
            - 'name' (str): Name of the product.
            - 'profit' (float): Profit per unit of the product.
            # (Optional) Additional data relevant to the problem (e.g., resource consumption).
        - constraints (dict): Dictionary containing constraint information. Each constraint is represented
                               by a key-value pair, where the key is the constraint name and the value is a dictionary
                               containing 'values' (list of constraint values for each product) and 'max' (maximum constraint value).

    Returns:
        - A dictionary with production levels and the total profit, or None if infeasible.
    """

    m = Model("Generic Production Planning")

    # Decision variables for production levels (consider using GRB.CONTINUOUS if applicable)
    x = {p['name']: m.addVar(vtype=GRB.CONTINUOUS, name=f"{p['name']}") for p in products}

    # Objective: Maximize profit
    m.setObjective(quicksum(p['profit'] * x[p['name']] for p in products), GRB.MAXIMIZE)

    # Add constraints for each constraint type
    for constraint_name, constraint_data in constraints.items():
        constraint_values = constraint_data['values']
        constraint_max = constraint_data['max']

        # Use a single constraint for each type
        constraint_expr = quicksum(constraint_values[i] * x[products[i]['name']] for i in range(len(products)))
        m.addConstr(constraint_expr <= constraint_max, f"{constraint_name}")

    # Solve model
    m.optimize()

    # Extract solution
    if m.status == GRB.OPTIMAL:
        production_levels = {v.varName: v.x for v in m.getVars()}
        total_profit = m.getObjective().getValue()
        return {
            'Production Levels': production_levels,
            'Total Profit': total_profit
        }
    else:
        return None


products = [
    {"name": "Product A", "profit": 10},
    {"name": "Product B", "profit": 15},
]

constraints = {
    "material": {
        "values": [2, 1],  # Material per unit (product A, B)
        "max": 119.5,  # Slightly modified material availability
    },
    "processing_time": {
        "values": [3, 2],  # Processing time per unit (product A, B)
        "max": 165,  # Total processing time available
    },
}

print(solve_production(products=products, constraints=constraints))

