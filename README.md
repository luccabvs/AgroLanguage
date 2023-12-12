# AgroLanguage

```
programa = { declaracao ";" }

declaracao = atribuicao
           | estrutura_controle
           | bloco
           | operacao_cultivo
           | operacao_pecuaria

atribuicao = identificador, "=", expressao

expressao = termo { ( "+" | "-" ) , termo }

termo = fator { ( "*" | "/" ) , fator }

fator = numero | identificador | "(", expressao, ")"

numero = digito, { digito }

digito = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

identificador = letra, { letra | digito | "_" }

letra = "A" | "B" | "C" | ... | "Z" | "a" | "b" | "c" | ... | "z"

estrutura_controle = estrutura_se | estrutura_enquanto

estrutura_se = "se", "(", expressao, ")", "entao", declaracao, [ "senao", declaracao ]

estrutura_enquanto = "enquanto", "(", expressao, ")", declaracao

bloco = "comecar", { declaracao ";" }, "terminar"

operacao_cultivo = "plantar", identificador_cultura, "em", data
                 | "colher", identificador_cultura

operacao_pecuaria = "registrar", identificador_pecuaria, tipo_animal
                   | "vacinar", identificador_pecuaria, "em", data

identificador_cultura = identificador

identificador_pecuaria = identificador

tipo_animal = "gado" | "ovelha" | "porco" | "galinha"

data = digito, digito, "/", digito, digito, "/", digito, digito, digito, digito

```
