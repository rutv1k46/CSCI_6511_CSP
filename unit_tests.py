import os
import unittest

from backtracking import backtracking_search
from graphcoloring import GraphColoringCSP
from fileparser import FileParser
from heuristics import least_constraining_values, min_remaining_values
from inference import arc_consistency, revise, ac3

class TestFileParser(unittest.TestCase):

    # Unit test for parsing an input file and comparing the output 
    def test_file_parser(self):
        expected_colors = 4
        expected_edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), 
            (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5),
            (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        
        filepath = os.path.join("data", "gc_1378296846561000.txt")
        file_parser = FileParser(filepath)
        parsed_payload = file_parser.parsed_payload
        
        # Test colors
        colors = parsed_payload["colors"]
        self.assertEqual(colors, expected_colors, "Unexpected colors: {colors}")
        
        # Test edges: length of edges
        edges = parsed_payload["edges"]
        self.assertEqual(len(edges), len(expected_edges), f"Unexpected edge length: {len(edges)}")
        
        # Test edges: test each edge is in expected edges
        for edge in edges:
            self.assertIn(edge, expected_edges, f"Unexpected edge: {edge}")
            
            
# Test cases for GraphColoringCSP class
class TestGraphColoringCSP(unittest.TestCase):

    def test_count_conflicts(self):
        assignment = {
            0: 0, # WA = red
            1: 1  # NT = green
        }
        
        csp = GraphColoringCSP.from_file(os.path.join("data", "australia.txt"))
        csp.add_assignments(assignment)
        
        # WA = red, NT = green, now we try assigning SA = 0, which should yield 1 conflict
        conflicts = csp.count_conflicts(2, 0, assignment)
        self.assertEqual(conflicts, 1, f"Expected 1 conflict, got {conflicts}")

# Test cases for heuristics
class TestHeuristics(unittest.TestCase):
    # Unit test for least constrainin values heuristics
    def test_least_constraining_values(self):
        assignment = {
            0: 0, # WA = red
            1: 1  # NT = green
        }
        
        csp = GraphColoringCSP.from_file(os.path.join("data", "australia.txt"))
        csp.add_assignments(assignment)
        self.assertEqual(least_constraining_values(csp, 3, assignment)[0], 0, "Should be 0")
    
    # unit test for minimum remaining values heuristic with tie breaking
    def test_min_remaining_values(self):
        filepath = os.path.join("data", "australia.txt")
        csp = GraphColoringCSP.from_file(filepath)
        assignment = {}
        
        variable = min_remaining_values(csp, assignment)
        self.assertEqual(variable, 2, f"MRV heuristic failed: expected 2, got {variable}")

# Test cases for constraint propagation
class TestInference(unittest.TestCase):

    # unit test for revise function
    # to ensure that the function doesnt revise if no conflicts exists, but does revise the doamin if it encounters a conflict
    def test_revise(self):
        csp = GraphColoringCSP.from_file(os.path.join("data", "australia.txt"))
        assignment = {}
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        
        # Once we've assigned {0: 0}, which has neighbors 1 and 2, we expect the domains for 1 and 2 to not have 0 in them
        expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        
        # Loop through the neighbors to revise as needed
        queue = [(x, variable) for x in csp.neighbors[variable]]
        
        for Xi, Xj in queue:
            revised = revise(csp, Xi, Xj)
            csp.add_inferences({Xi: revised})
            
        self.assertEqual(csp.domains, expected_domains)

    # unit test for AC3
    def test_ac3(self):
        csp = GraphColoringCSP.from_file(os.path.join("data", "australia.txt"))
        assignment = {}
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        
        # Once we've assigned {0: 0}, which has neighbors 1 and 2, we expect the domains for 1 and 2 to not have 0 in them
        expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        
        queue = [(x, variable) for x in csp.neighbors[variable]]
        inferences = ac3(csp, queue)
        csp.add_inferences(inferences)
        self.assertEqual(csp.domains, expected_domains)
    
    # unit test for maintaining arc consistency
    def test_arc_consistency(self):
        csp = GraphColoringCSP.from_file(os.path.join("data", "australia.txt"))
        assignment = {}
        variable = 0
        value = 0
        
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        inferences = arc_consistency(csp, variable)
        csp.add_inferences(inferences)
        
        expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        self.assertEqual(csp.domains, expected_domains)


class TestBacktracking(unittest.TestCase):

    # unit test for backtracking search with maintaining arc consistency using AC3    
    def test_backtracking_search_mac(self):
        folder = os.path.join("data")
        files = [file for file in os.listdir(folder) if not 'gc_1377121623225900' in file]
        no_solution = "gc_78317097930401.txt"
        
        for file in files:
            filepath = os.path.join(folder, file)
            csp = GraphColoringCSP.from_file(filepath)
            solution = backtracking_search(csp)
            
            if file == no_solution:
                self.assertIsNone(solution, f"Search returned solution for file {file}, although no solution exists")
                
            else:
                self.assertIsNotNone(solution, f"Search returned no solution for file {file}, although a solution exists")
                self.assertTrue(csp.valid_solution(solution))

if __name__ == "__main__":
    unittest.main()
