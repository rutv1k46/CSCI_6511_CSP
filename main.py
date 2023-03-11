import json
from backtracking import backtracking_search
from graphcoloring import GraphColoringCSP
from heuristics import least_constraining_values, min_remaining_values
from inference import arc_consistency

def solveGC(input_file):
    csp = GraphColoringCSP.from_file(input_file)

    solution = backtracking_search(csp)
    # solution = backtracking_search(csp, min_remaining_values, least_constraining_values, arc_consistency)
    return solution

if __name__ == "__main__":
    file = 'gc.txt'
    solution = solveGC(file)
    
    if solution:
        # print('Total vertices: ', len(solution))
        # print(f"\nSolution -> {json.dumps(solution)}\n")
        print(f"\nSolution -> {(sorted(solution.items()))}\n")
    else:
        print(f"\nNo solution found.\n")
