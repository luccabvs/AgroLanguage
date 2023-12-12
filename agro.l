%{
#include <stdio.h>
#include "parser.tab.h"
%}

digit           [0-9]
number          {digit}+
letter          [A-Za-z]
identifier      {letter}({letter}|{digit}|_)*
whitespace      [ \t\n]+

%%

"se"            { printf("SE\n"); return SE; }
"entao"         { printf("ENTAO\n"); return ENTAO; }
"senao"         { printf("SENAO\n"); return SENAO; }
"enquanto"      { printf("ENQUANTO\n"); return ENQUANTO; }
"comecar"       { printf("COMECAR\n"); return COMECAR; }
"terminar"      { printf("TERMINAR\n"); return TERMINAR; }
"plantar"       { printf("PLANTAR\n"); return PLANTAR; }
"colher"        { printf("COLHER\n"); return COLHER; }
"registrar"     { printf("REGISTRAR\n"); return REGISTRAR; }
"vacinar"       { printf("VACINAR\n"); return VACINAR; }
"em"            { printf("EM\n"); return EM; }
"gado"          { printf("GADO\n"); return GADO; }
"ovelha"        { printf("OVELHA\n"); return OVELHA; }
"porco"         { printf("PORCO\n"); return PORCO; }
"galinha"       { printf("GALINHA\n"); return GALINHA; }
{number}        { printf("NUMERO: %s\n", yytext); return NUMERO; }
{identifier}    { printf("IDENTIFICADOR: %s\n", yytext); return IDENTIFICADOR; }
"+"             { printf("MAIS\n"); return MAIS; }
"-"             { printf("MENOS\n"); return MENOS; }
"*"             { printf("MULTIPLICAR\n"); return MULTIPLICAR; }
"/"             { printf("DIVIDIR\n"); return DIVIDIR; }
"="             { printf("IGUAL\n"); return IGUAL; }
";"             { printf("PONTO_E_VIRGULA\n"); return PONTO_E_VIRGULA; }
"("             { printf("ABRE_PARENTESES\n"); return ABRE_PARENTESES; }
")"             { printf("FECHA_PARENTESES\n"); return FECHA_PARENTESES; }
{whitespace}    { /* ignora espaços em branco */ }
.               { printf("Caractere inesperado: %c\n", yytext[0]); }

%%
