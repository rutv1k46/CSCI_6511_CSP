from collections import defaultdict

def empty_domain(csp, variable, inferences):
    return len([value for value in csp.domains[variable] if not value in inferences[variable]]) == 0

# Implementation of the AC3 constraint propagation 
# return CSP with possibly reduced domains
def ac3(csp, queue = None):
    inferences = defaultdict(list)
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
        
    while queue:
        xi, xj = queue.pop()
        revised = revise(csp, xi, xj)
        
        if revised:
            inferences[xi].extend(revised)
            if empty_domain(csp, xi, inferences):
                return 'failure'
            
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
                    
    return inferences


def revise(csp, Xi, Xj):
    revised = []
    
    for x in csp.domains[Xi]:
        value_exists = False # if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj
        
        for y in csp.domains[Xj]:
            if csp.constraint_function(Xi, x, Xj, y): # If this is true then a value exists, so no revision
                value_exists = True
                break
            
        if not value_exists: # No value satisfies the constraint, so remove it
            revised.append(x)
            
    return revised


def arc_consistency(csp, variable):
    queue = [(x, variable) for x in csp.neighbors[variable]]
    return ac3(csp, queue = queue)