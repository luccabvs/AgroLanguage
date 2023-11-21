
%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
extern int yylineno;
void yyerror(const char *s);
%}

%union {
    int num;
    char* id;
}

%token <num> NUMBER
%token STRING
%token <id> IDENTIFIER
%token IF THEN ELSE WHILE BEGIN_BLOCK END_BLOCK
%token PLUS MINUS MULTIPLY DIVIDE EQUALS SEMICOLON
%token LPAREN RPAREN
%token PLANT HARVEST REGISTER VACCINATE
%token CATTLE SHEEP PIG CHICKEN ON

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%
program:
    | program statement SEMICOLON
    ;

statement:
      assignment
    | control_structure
    | block
    | crop_operation
    | livestock_operation
    ;

assignment:
    IDENTIFIER EQUALS expression
    ;

expression:
    term
    | expression PLUS term
    | expression MINUS term
    ;

term:
    factor
    | term MULTIPLY factor
    | term DIVIDE factor
    ;

factor:
    NUMBER
    | IDENTIFIER
    | LPAREN expression RPAREN
    ;

control_structure:
      if_structure
    | while_structure
    ;
  
if_structure:
    IF LPAREN expression RPAREN THEN statement %prec LOWER_THAN_ELSE
    | IF LPAREN expression RPAREN THEN statement ELSE statement
    ;

while_structure:
    WHILE LPAREN expression RPAREN statement
    ;

block:
    BEGIN_BLOCK program END_BLOCK
    ;

crop_operation:
      PLANT IDENTIFIER ON NUMBER
    | HARVEST IDENTIFIER
    ;

livestock_operation:
      REGISTER IDENTIFIER CATTLE
    | REGISTER IDENTIFIER SHEEP
    | REGISTER IDENTIFIER PIG
    | REGISTER IDENTIFIER CHICKEN
    | VACCINATE IDENTIFIER ON NUMBER
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s at line %d\n", s, yylineno);
}

int main(void) {
    yyparse();
    return 0;
}

