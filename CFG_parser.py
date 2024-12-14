import csv
import argparse

class CFG:

    def __init__(self, name, V, sigma, R, S):
        self.name = name
        self.V = V
        self.sigma = sigma
        self.R = R
        self.S = S

    # parse input string using formal definition of CFG
    def parse_string(self, input_string, max_depth):
        # Store derivation steps
        self.derivation_steps = []
        self.parse_result = None

         # Find rule with nonterminal for leftmost derivation
        def get_leftmost_rules(symbol):
            def has_nonterminal(s):
                return any(char in self.V for char in s)
            return sorted(self.R[symbol].copy(), key=lambda x: not has_nonterminal(x))


        def try_rule(symbol, remaining_string, depth, current_derivation):
            # Return if exceeded max depth  REJECT
            if depth > max_depth:
                self.parse_result = 'MAX DEPTH EXCEEDED'
                return False
            
            # Return if both symbol and remaining_string are empty  ACCEPT
            if not symbol and not remaining_string:
                self.derivation_steps = current_derivation
                self.parse_result = 'ACCEPT'
                return True
            # Return if either has remaining symbols (not match)  REJECT
            if not symbol or not remaining_string:
                self.parse_result = 'REJECT'
                return False

            # If the first character of our symbol is a terminal
            if symbol[0] in self.sigma:
                if symbol[0] == remaining_string[0]:
                    return try_rule(symbol[1:], remaining_string[1:], depth, current_derivation)
                return False

            # If the first character is a non-terminal
            if symbol[0] in self.R:
                # Sort rules with non-terminals first => for leftmost derivation
                sorted_rules = get_leftmost_rules(symbol[0])
                # Try each production rule
                for production in sorted_rules:
                    # Create new derivation step
                    new_derivation = current_derivation.copy()
                    new_derivation.append((symbol[0], production))
                    
                    result = try_rule(production + symbol[1:], remaining_string, depth + 1, new_derivation)
                    if result:
                        return True
                    
                    if self.parse_result == 'MAX DEPTH EXCEEDED':
                        return False
                    
                return False

        # Start parsing from the start symbol
        result = try_rule(self.S, input_string, 0, [])
        return result if result is not False else None
    
    # Print 'parse' tree of string derivation
    def print_derivation(self):
        if not self.derivation_steps:
            print('No valid derivation found.')
            return

        print('\nLeftmost Derivation:')
        print(f'-- {self.S}')  # Start symbol
        
        current = self.S
        for step, (non_terminal, replacement) in enumerate(self.derivation_steps, 1):
            # Find the leftmost occurrence of the non-terminal
            pos = current.find(non_terminal)
            if pos != -1:
                # Replace the leftmost occurrence
                current = current[:pos] + replacement + current[pos + 1:]
                print(f'{'  ' * step}-- {current} (replaced {non_terminal} → {replacement})')

def process_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)

        # Process the first 4 lines of the file
        name = next(csv_reader)[0]
        V = next(csv_reader)
        sigma = next(csv_reader)
        S = next(csv_reader)[0]
        
        # Process Production Rules
        R = {}
        for line in csv_reader:
            start, rules = line
            list_rules = rules.split('|')
            
            if start in R:
                R[start] += list_rules
            else:
                R[start] = list_rules

    return CFG(name, V, sigma, R, S )   

def __main__():
    # parse cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('CSV_file', type=str)
    parser.add_argument('input_string', type=str)
    parser.add_argument('max_depth', type=int)
    args = parser.parse_args()

    # Convert csv to CFG and check if input string is in the language
    cfg = process_csv(args.CSV_file)
    result = cfg.parse_string(args.input_string, args.max_depth)
    status = cfg.parse_result
    
    if status == 'MAX DEPTH EXCEEDED':
        print(f"Could not determine if '{args.input_string}' is in the language of {cfg.name} (max depth {args.max_depth} exceeded)")
    else:
        print(f"String '{args.input_string}' is {'in' if result else 'not in'} the language of {cfg.name}")
        if result:
            cfg.print_derivation()


if __name__ == '__main__':
    __main__() 