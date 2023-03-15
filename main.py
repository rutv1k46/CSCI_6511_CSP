from backtrack import backtracking_search
from graph_coloring import GraphColoringCSP

def solveGC(input_file):
    csp = GraphColoringCSP.from_file(input_file)

    solution = backtracking_search(csp)
    return solution

if __name__ == "__main__":
    file = 'data/gc_78317103208800.txt'
    solution = solveGC(file)
    
    if solution:
        print(f"\nSolution -> {(sorted(solution.items()))}\n")

    else:
        print(f"\nNo solution found.\n")
