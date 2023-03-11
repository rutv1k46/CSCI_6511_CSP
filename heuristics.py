# Implementation of the Minimum-Remaining-Values Heuristic for ordering variables
# It chooses the variable with the fewest remaining legal values and also incorporates the tie breaking rule and returns the first value based on the ordering
def min_remaining_values(csp, assignment):
    unassigned_variables = []
    for variable in csp.variables:
        if variable not in assignment:
            
            # Collecting the variable, number of remaining legal values (values left in domain), and number of constraints 
            unassigned_variables.append((variable,  len(csp.domains[variable]), -len(csp.constraints[variable])))
            
    # Sort by remaining legal values, then by number of constraints (tie breaker)
    unassigned_variables.sort(key = lambda x: (x[1], x[2]))
    
    return unassigned_variables[0][0]


# Implementation of the Least-Constraining-Value heuristic 
# It sorts the domains by how mant conflicts the assignment creates in increasing order and returns a list of domain vlaues 
def least_constraining_values(csp, variable, assignment):
    return sorted(csp.domains[variable], key = lambda value: csp.count_conflicts(variable, value, assignment))
