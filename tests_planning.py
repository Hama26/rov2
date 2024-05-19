from gurobipy import Model, GRB, quicksum
import pandas as pd
from tabulate import tabulate

def solve_production(products, constraints):
    """
    Solves a production planning problem focusing on maximizing profit with multiple constraints.

    Parameters:
        - products (list of dicts): Information about each product, including profit and any other relevant data.
            - 'name' (str): Name of the product.
            - 'profit' (float): Profit per unit of the product.
        - constraints (dict): Dictionary containing constraint information. Each constraint is represented
                               by a key-value pair, where the key is the constraint name and the value is a dictionary
                               containing 'values' (list of constraint values for each product) and 'max' (maximum constraint value).

    Returns:
        - A dictionary with production levels, the total profit, and the runtime.
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
            'Total Profit': total_profit,
            'Runtime': m.Runtime
        }
    else:
        return None

def run_production_tests():
    test_cases = [
        {
            "name": "Cas Simple",
            "products": [
                {"name": "Produit A", "profit": 10},
                {"name": "Produit B", "profit": 15},
            ],
            "constraints": {
                "matériaux": {"values": [2, 1], "max": 8},
                "temps de traitement": {"values": [3, 2], "max": 10},
            }
        },
        {
            "name": "Cas Complexe",
            "products": [
                {"name": "Produit A", "profit": 10},
                {"name": "Produit B", "profit": 15},
                {"name": "Produit C", "profit": 20},
                {"name": "Produit D", "profit": 25},
            ],
            "constraints": {
                "matériaux": {"values": [2, 1, 3, 2], "max": 10},
                "temps de traitement": {"values": [3, 2, 4, 1], "max": 10},
                "coût de production": {"values": [1, 2, 1, 3], "max": 5},
            }
        },
        {
            "name": "Cas Limite",
            "products": [
                {"name": "Produit A", "profit": 10},
                {"name": "Produit B", "profit": 15},
            ],
            "constraints": {
                "matériaux": {"values": [2, 1], "max": 1},
            }
        },
        {
            "name": "Cas Large",
            "products": [
                {"name": "Produit A", "profit": 10},
                {"name": "Produit B", "profit": 15},
                {"name": "Produit C", "profit": 20},
                {"name": "Produit D", "profit": 25},
                {"name": "Produit E", "profit": 30},
                {"name": "Produit F", "profit": 35},
            ],
            "constraints": {
                "matériaux": {"values": [2, 1, 3, 2, 4, 1], "max": 15},
                "temps de traitement": {"values": [3, 2, 4, 1, 3, 2], "max": 20},
                "coût de production": {"values": [1, 2, 1, 3, 2, 1], "max": 10},
            }
        }
    ]
    
    results = []
    
    for test in test_cases:
        result = solve_production(test["products"], test["constraints"])
        if result:
            results.append({
                "Test Case": test["name"],
                "Production Levels": result["Production Levels"],
                "Total Profit": result["Total Profit"],
                "Runtime (s)": result["Runtime"]
            })
        else:
            results.append({
                "Test Case": test["name"],
                "Production Levels": None,
                "Total Profit": None,
                "Runtime (s)": None
            })
    
    return results

# Run the tests
results = run_production_tests()

# Analyze and present the results
df = pd.DataFrame(results)
print(tabulate(df, headers='keys', tablefmt='grid'))
