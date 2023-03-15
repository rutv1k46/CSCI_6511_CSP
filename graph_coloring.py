from collections import defaultdict
from typing import List, Set, Tuple, Union
from fileparser import FileParser

# Class for the graph coloring constraint, where the neighbors cannot have the same color
class GraphColoringConstraint:
    def __init__(self, vertex1, vertex2):
        self.variables = [vertex1, vertex2]
        self.vertex1 = vertex1
        self.vertex2 = vertex2
    
    def __repr__(self) -> str:
        return "<Constraint: [vertex1: {self.vertex1}, vertex2: {self.vertex2}]>"
    
    # returns whether neighbors A and B satisfy the constraints when they have values A = a and B = b
    def is_satisfied(self, assignment: dict):
        # If either vertex is unassigned, return True
        if self.vertex1 not in assignment or self.vertex2 not in assignment:
            return True
        
        # Otherwise return whether the vertices are the same color
        return assignment[self.vertex1] != assignment[self.vertex2]


# Class for the graph coloring problem, where 
# X (variables) {X1, ..., Xn} are the vertices in the graph.
# D (domains) {D1, ..., Dn} are the possible colors for each variable, initially all colors.
# C (constraints) <(Xi, Xj), ci != cj>, where ci and cj are the colors assigned to adjacent vertices Xi and Xj.
class GraphColoringCSP:
    def __init__(self, edges: Union[List[Tuple[int, int]], Set[Tuple[int, int]]], colors: int, neighbors:dict=None):
        self.neighbors = neighbors
        self.edges = edges
        self.neighbors = neighbors
        self.constraints: dict = defaultdict(list) # Equivalent to lazily instantiating each value as []
        self.colors = colors
        self.variables = set(vertex for edge in edges for vertex in edge)
        self.domains = {vertex: list(range(colors)) for vertex in self.variables}
        self.assignment_counts = 0
        
        # add constraints
        for vertex1, vertex2 in self.edges:
            self.add_constraint(GraphColoringConstraint(vertex1, vertex2))
    
    # constraint for where the neighbors X and Y cannot have the same values
    def constraint_function(self, X, x, Y, y):
        return x != y

    # method to add constraints
    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Variable: {variable} not in constraint satisfaction problem.")
            self.constraints[variable].append(constraint)
    
    # method to determine if an assignement is consistent with all the constraints
    def is_consistent(self, variable, assignment: dict):
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True

    # method to update domain attribute to account for var = value
    def add_assignment(self, variable, value):
        removals = [(variable, a) for a in self.domains[variable] if a != value]
        self.domains[variable] = [value]
        return removals

    # method to update domain attribute based on an assignment    
    def add_assignments(self, assignments):
        removals = []
        for variable, value in assignments.items():
            removals.append(self.add_assignment(variable, value))
        return removals

    # method to add variable = value to assignment and updates the assignment count
    def assign(self, variable, value, assignment):
        assignment[variable] = value
        self.assignment_counts += 1

    # method to add inference the CSP during the backtracking, it updates the domain attirbute    
    def add_inferences(self, inferences):
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].remove(value)

    # method to restore removed values from the domain back into the domains attribute
    def remove_inferences(self, inferences):
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].append(value)

    # method that returns the number of conflicts var = val has with other variables already assigned 
    # check if assigning var = val will cause csp.is_consistent to return False
    def count_conflicts(self, var, val, assignment):
        count = 0
        temp_assignment = assignment.copy()
        temp_assignment[var] = val
        for v in self.neighbors[var]: # iterate through the neighbors of var    
            if v in assignment and not self.is_consistent(v, temp_assignment): # Check if the assignment causes any conflicts with a neighbor
                count += 1
        return count
    
    # method to check of an assignment is a complete and valid solution
    # it attempts to assign all variables with all constraints satisfied
    def valid_solution(self, assignment):
        if not assignment:
            return False
        
        return (len(assignment) == len(self.variables)
                and all(self.count_conflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # method to create a GraphColoringCSP object from an input file
    @classmethod
    def from_file(cls, filepath):
        fileparse = FileParser(filepath=filepath)
        return cls(**fileparse.parsed_payload)
