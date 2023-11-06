# AgroLanguage

```
program = { statement ";" } 

statement = assignment 
          | control_structure 
          | block 
          | crop_operation 
          | livestock_operation 

assignment = identifier, "=", expression 

expression = term { ( "+" | "-" ) , term } 

term = factor { ( "*" | "/" ) , factor } 

factor = number | identifier | "(", expression, ")" 

number = digit, { digit } 

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" 

identifier = letter, { letter | digit | "_" } 

letter = "A" | "B" | "C" | ... | "Z" | "a" | "b" | "c" | ... | "z" 

control_structure = if_structure | while_structure 

if_structure = "if", "(", expression, ")", "then", statement, [ "else", statement ] 

while_structure = "while", "(", expression, ")", statement 

block = "begin", { statement ";" }, "end" 

crop_operation = "plant", crop_identifier, "on", date 
               | "harvest", crop_identifier 

livestock_operation = "register", livestock_identifier, animal_type 
                    | "vaccinate", livestock_identifier, "on", date 

crop_identifier = identifier 

livestock_identifier = identifier 

animal_type = "cattle" | "sheep" | "pig" | "chicken" 

date = digit, digit, "/", digit, digit, "/", digit, digit, digit, digit 
```
