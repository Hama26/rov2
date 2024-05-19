from optimization_solver import solve_knapsack, solve_production
import pandas as pd
from tabulate import tabulate


def run_tests():
    test_cases = [
        {
            "name": "Simple Case",
            "values": [10, 40, 30, 50],
            "constraints": {
                "weight": {"values": [5, 4, 6, 3], "max": 10},
                "volume": {"values": [2, 3, 1, 5], "max": 5}
            }
        },
        {
            "name": "Complex Case",
            "values": [20, 30, 10, 50, 40, 70],
            "constraints": {
                "weight": {"values": [2, 3, 1, 6, 7, 5], "max": 15},
                "volume": {"values": [3, 2, 4, 1, 5, 6], "max": 10},
                "cost": {"values": [4, 5, 6, 7, 8, 9], "max": 20}
            }
        },
        {
            "name": "Edge Case",
            "values": [10, 20, 30],
            "constraints": {
                "weight": {"values" : [1, 1, 1], "max": 2}
            }
        },
        {
            "name": "Large Case",
            "values": list(range(1, 101)),
            "constraints": {
                "weight": {"values": list(range(1, 101)), "max": 200},
                "volume": {"values": list(range(1, 101)), "max": 150}
            }
        }
    ]
    
    results = []
    
    for test in test_cases:
        selected_items, total_value, runtime = solve_knapsack(test["values"], test["constraints"])
        results.append({
            "Test Case": test["name"],
            "Selected Items": selected_items,
            "Total Value": total_value,
            "Runtime (s)": runtime
        })
    
    return results

# Run the tests
results = run_tests()

# Analyze and present the results
df = pd.DataFrame(results)
print(tabulate(df, headers='keys', tablefmt='grid'))