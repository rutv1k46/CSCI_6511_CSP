from collections import defaultdict

# Class to parse an input file representing a graph coloring CSP problem
class FileParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.parsed_payload = self.parse_file()
    
    # method to parse a grapg coloring problem input file
    # returns a dictionary with colors, neighbors and edges
    def parse_file(self) -> dict:
        neighbors = defaultdict(set)
        edges = []
        csp_payload = {}
        with open(self.filepath, "r") as file:
            for line in file:
                # Skip empty lines and comments
                if not line.strip() or line.strip().startswith('#'):
                    continue
                
                # Color line
                if line.lower().strip().startswith('colors'):
                    csp_payload["colors"] = int(line.split('=')[-1].strip())
                    
                # Edge line
                else:
                    edge = tuple(sorted(int(element.strip()) for element in line.strip().split(',')))
                    edges.append(edge)
                    neighbors[edge[0]].add(edge[1])
                    neighbors[edge[1]].add(edge[0])
                    
        csp_payload["edges"] = edges
        csp_payload["neighbors"] = neighbors
        return csp_payload