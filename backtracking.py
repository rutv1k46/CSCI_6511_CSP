from heuristics import least_constraining_values, min_remaining_values
from inference import arc_consistency

# Function to run the backtracking search, it wraps the backtrack method and passes it an initial empty assignment
def backtracking_search(csp):
    return backtrack(csp, {})

# Implementation of the backtracking algorithm, using MRV and LCV as heuristics
# it also utilizes AC3 for constraint propagation
def backtrack(csp, assignment):
    # Base case: if assignment is complete then return assignment
    if csp.valid_solution(assignment):
        return assignment

    # MRV to get unassigned variable
    variable = min_remaining_values(csp, assignment)

    for value in least_constraining_values(csp, variable, assignment):
        # if value is consistent with assignment then add {var = value} to assignment
        if csp.is_consistent(variable, {variable: value, **assignment}):
            csp.assign(variable, value, assignment)
            csp.add_assignment(variable, value)
            inferences = arc_consistency(csp, variable)

            # if AC3 does not lead to failure then add inferences to csp
            if inferences != 'failure':
                csp.add_inferences(inferences)
                result = backtrack(csp, assignment)

                # if result != failure then return result
                if result: 
                    return result
                
                csp.remove_inferences(inferences)
                
            # remove {var = value} from assignment
            del assignment[variable]
    return None