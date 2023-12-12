%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
extern int yylineno;
void yyerror(const char *s);
%}

%token NUMERO IDENTIFICADOR SE ENTAO SENAO ENQUANTO COMECAR TERMINAR
%token MAIS MENOS MULTIPLICAR DIVIDIR IGUAL PONTO_E_VIRGULA
%token ABRE_PARENTESES FECHA_PARENTESES
%token PLANTAR COLHER REGISTRAR VACINAR EM
%token GADO OVELHA PORCO GALINHA

%nonassoc MENOR_QUE_SENAO
%nonassoc SENAO
%%
programa:
    | programa declaracao PONTO_E_VIRGULA
    ;

declaracao:
      atribuicao
    | estrutura_controle
    | bloco
    | operacao_cultivo
    | operacao_pecuaria
    ;

atribuicao:
    IDENTIFICADOR IGUAL expressao
    ;

expressao:
    termo
    | expressao MAIS termo
    | expressao MENOS termo
    ;

termo:
    fator
    | termo MULTIPLICAR fator
    | termo DIVIDIR fator
    ;

fator:
    NUMERO
    | IDENTIFICADOR
    | ABRE_PARENTESES expressao FECHA_PARENTESES
    ;

estrutura_controle:
      estrutura_se
    | estrutura_enquanto
    ;

estrutura_se:
    SE ABRE_PARENTESES expressao FECHA_PARENTESES ENTAO declaracao %prec MENOR_QUE_SENAO
    | SE ABRE_PARENTESES expressao FECHA_PARENTESES ENTAO declaracao SENAO declaracao
    ;

estrutura_enquanto:
    ENQUANTO ABRE_PARENTESES expressao FECHA_PARENTESES declaracao
    ;

bloco:
    COMECAR programa TERMINAR
    ;

operacao_cultivo:
      PLANTAR IDENTIFICADOR EM NUMERO
    | COLHER IDENTIFICADOR
    ;

operacao_pecuaria:
      REGISTRAR IDENTIFICADOR tipo_animal
    | VACINAR IDENTIFICADOR EM NUMERO
    ;

tipo_animal:
      GADO
    | OVELHA
    | PORCO
    | GALINHA
    ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s na linha %d\n", s, yylineno);
}

int main(void) {
    yyparse();
    return 0;
}
