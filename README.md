# AgroLanguage
## A linguagem do agronegócio

### Introdução
Em um mundo cada vez mais tecnológico, surge a necessidade da agricultura moderna de criar constantes soluções inovadoras e eficientes. É neste cenário que a linguagem de programação AgroLang se destaca, oferecendo uma ferramenta poderosa e adaptada às necessidades específicas do setor agrícola.

### Motivação
Ser criado no interior do Brasil, me aproximou cada vez mais do Agrnegócio, porém não quero ser apenas mais um fazendeiro comum, meu maior sonho é justamente empreender nesse setor por meio da tecnologia. Isso que me motivou a estudar Engenharia de Computação. Esse projeto é só o primeiro de muitos nesse setor.


## EBNF
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

## EXEMPLO DE USO
```
registrar animal1 gado;
plantar milho em 01/01/2023;
se (1) entao
    vacinar animal1 em 02/02/2023;
senao
    colher milho;

enquanto (1) comecar
    plantar trigo em 03/03/2023;
terminar
```
