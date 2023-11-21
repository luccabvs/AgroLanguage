
%{
#include "parser.tab.h"
%}

digit           [0-9]
letter          [A-Za-z]
identifier      {letter}({letter}|{digit}|_)*
whitespace      [ \t\n]+

%%

"if"            { return IF; }
"then"          { return THEN; }
"else"          { return ELSE; }
"while"         { return WHILE; }
"begin"         { return BEGIN_BLOCK; }
"end"           { return END_BLOCK; }
"plant"         { return PLANT; }
"harvest"       { return HARVEST; }
"register"      { return REGISTER; }
"vaccinate"     { return VACCINATE; }
"cattle"        { return CATTLE; }
"sheep"         { return SHEEP; }
"pig"           { return PIG; }
"chicken"       { return CHICKEN; }
"on"            { return ON; }
{digit}+        { return NUMBER; }
\"(\\.|[^\"\n])*\" { return STRING; }
{identifier}    { return IDENTIFIER; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULTIPLY; }
"/"             { return DIVIDE; }
"="             { return EQUALS; }
";"             { return SEMICOLON; }
"("             { return LPAREN; }
")"             { return RPAREN; }
{whitespace}    { /* ignore whitespace */ }
.               { printf("Unexpected character: %c\n", yytext[0]); }

%%
