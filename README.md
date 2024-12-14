# theory-ec-cfg

On Exam 2, I did poorly on CFG questions. When asked to create a CFG, I would simply display the set of production rules and forget the rest of the tuple (sigma, V, S). Additionally, on question 6, I did not follow leftmost derivation when building my parse tree.   
   
For this extra credit, I built a cfg parser. It takes a csv and input string, then checks if the string is in the grammar. If so, it will print the leftmost derivation parse tree.   
I chose this as my project because I felt that this would help me understand leftmost derivation at a deeper level. Coding a whole parser around the principle would help it stick in. Additionally, when coding the parser, I often used V, sigma, and S. When I was buildign the parser, I realized how often I had to use those parts, and therefore how important the formal definition of the CFG is.   

USAGE:   
   
using the following command:   
python3 CFG_parser.py <csv_file> <input_string> <max_depth>   
for example:   
python3 CFG_parser.py CFG_csvs/q6.csv 00110101 20   
   
it will build a cfg from the csv, and check to see if the input string is in the grammar.   
   
in the CFG_csvs/ directory, I have included the CFGs from EXAM 2 to test on.