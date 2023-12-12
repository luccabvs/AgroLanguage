from abc import ABC, abstractmethod
import sys

class PrePro:
    @staticmethod
    def filter(code):
        return '\n'.join([line.split('//')[0] for line in code.split('\n')])


class Symbol_Table:
    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        else:
            raise Exception(f"Variável {identifier} não declarada")

    def set(self, identifier, value):
        if identifier in self.symbol_table:
            self.symbol_table[identifier] = value
        else:
            raise Exception(f"Variável {identifier} não declarada")
        
    def create(self, identifier, value):
        if identifier in self.symbol_table:
            raise Exception(f"Variável {identifier} já declarada")
        else:
            self.symbol_table[identifier] = value


class Node(ABC):
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def evaluate(self, symbol_table):
        pass

class Atribuicao(Node):
    def __init__(self, identifier, expression):
        super().__init__(value=None, children=[identifier, expression])

    def evaluate(self, symbol_table):
        identifier = self.children[0].value
        value = self.children[1].evaluate(symbol_table)

        symbol_table.set(identifier, value)
        return value

class EstruturaControle(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__()
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def evaluate(self, symbol_table):
        if self.condition.evaluate(symbol_table):
            self.true_block.evaluate(symbol_table)
        elif self.false_block is not None:
            self.false_block.evaluate(symbol_table)

class EstruturaControle(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__()
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def evaluate(self, symbol_table):
        if self.condition.evaluate(symbol_table):
            self.true_block.evaluate(symbol_table)
        elif self.false_block is not None:
            self.false_block.evaluate(symbol_table)

class OperacaoCultivo(Node):
    def __init__(self, operation_type, culture, date=None):
        super().__init__(value=operation_type, children=[culture, date] if date else [culture])
        self.operation_type = operation_type

    def evaluate(self, symbol_table):
        culture_identifier = self.children[0]
        date = self.children[1] if len(self.children) > 1 else None

        if self.operation_type == "plantar":
            symbol_table.create(culture_identifier, {"data_plantio": date, "estado": "não colhida"})
        
        elif self.operation_type == "colher":
            if culture_identifier not in symbol_table.symbol_table:
                raise Exception(f"Cultura '{culture_identifier}' não plantada")
            cultura_info = symbol_table.get(culture_identifier)
            cultura_info["estado"] = "colhida"
            symbol_table.set(culture_identifier, cultura_info)
        
        else:
            raise Exception(f"Operação de cultivo não suportada: {self.operation_type}")

class OperacaoPecuaria(Node):
    def __init__(self, operation_type, livestock_identifier, additional_info=None):
        super().__init__(value=operation_type, children=[livestock_identifier, additional_info] if additional_info else [livestock_identifier])
        self.operation_type = operation_type

    def evaluate(self, symbol_table):
        livestock_identifier = self.children[0].value
        if self.operation_type == "registrar":
            animal_type = self.children[1].value if len(self.children) > 1 else None
            symbol_table.create(livestock_identifier, {"tipo": animal_type, "vacinado": False})
        
        elif self.operation_type == "vacinar":
            if livestock_identifier not in symbol_table.symbol_table:
                raise Exception(f"Animal '{livestock_identifier}' não registrado")
            animal_info = symbol_table.get(livestock_identifier)
            animal_info["vacinado"] = True
            symbol_table.set(livestock_identifier, animal_info)
        
        else:
            raise Exception(f"Operação de pecuária não suportada: {self.operation_type}")

class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class Expressao(Node):
    def __init__(self, left, operator, right):
        super().__init__(value=operator, children=[left, right])
        self.operator = operator

    def evaluate(self, symbol_table):
        left = self.children[0].evaluate(symbol_table)
        right = self.children[1].evaluate(symbol_table)

        if self.operator == '+':
            return left + right
        elif self.operator == '-':
            return left - right
        elif self.operator == '*':
            return left * right
        elif self.operator == '/':
            return left / right
        else:
            raise Exception(f"Operador não suportado: {self.operator}")

class Termo(Node):
    def __init__(self, left, operator, right):
        super().__init__(value=operator, children=[left, right])
        self.operator = operator

    def evaluate(self, symbol_table):
        left = self.children[0].evaluate(symbol_table)
        right = self.children[1].evaluate(symbol_table)

        if self.operator == '*':
            return left * right
        elif self.operator == '/':
            return left / right
        else:
            raise Exception(f"Operador não suportado em Termo: {self.operator}")

class Fator(Node):
    def __init__(self, child):
        super().__init__(value=None, children=[child])

    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)

class Numero(Node):
    def __init__(self, value):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return self.value

class Identificador(Node):
    def __init__(self, name):
        super().__init__(value=name)

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class EstruturaSe(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__(value=None, children=[condition, true_block, false_block] if false_block else [condition, true_block])

    def evaluate(self, symbol_table):
        condition = self.children[0].evaluate(symbol_table)
        if condition:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)

class EstruturaEnquanto(Node):
    def __init__(self, condition, block):
        super().__init__(value=None, children=[condition, block])

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

        self.tokens = {
            "=": "IGUAL",
            "+": "MAIS",
            "-": "MENOS",
            "*": "VEZES",
            "/": "DIVISAO",
            "(": "ESQ_PARENTESES",
            ")": "DIR_PARENTESES",
            "{": "ESQ_CHAVES",
            "}": "DIR_CHAVES",
            ";": "PONTO_VIRGULA",
            ",": "VIRGULA",
            "se": "SE",
            "entao": "ENTAO",
            "senao": "SENAO",
            "enquanto": "ENQUANTO",
            "comecar": "COMECAR",
            "terminar": "TERMINAR",
            "plantar": "PLANTAR",
            "colher": "COLHER",
            "registrar": "REGISTRAR",
            "vacinar": "VACINAR",
            "gado": "GADO",
            "ovelha": "OVELHA",
            "porco": "PORCO",
            "galinha": "GALINHA"
        }

    def select_next(self):
        while self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isspace():
                self.position += 1
                continue

            if current_char.isalpha() or current_char == "_":
                word = ''
                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    word += self.source[self.position]
                    self.position += 1
                if word in self.tokens:
                    self.next = Token(self.tokens[word], word)
                else:
                    self.next = Token("IDENTIFICADOR", word)
                return

            if current_char.isdigit():
                number = ''
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("NUMERO", int(number))
                return

            if current_char in self.tokens:
                self.next = Token(self.tokens[current_char], current_char)
                self.position += 1
                return

            raise ValueError(f"Caractere inválido na posição {self.position}: '{current_char}'")

        self.next = Token("EOF", "")
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = 0

    def advance(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1

    def match(self, expected_type, expected_value=None):
        if self.current_token.type == expected_type:
            if expected_value is None or self.current_token.value == expected_value:
                self.advance()
                return True
        return False

    @staticmethod
    def parse_program(tokenizer):
        nodes = []
        while tokenizer.next.type != "EOF":
            if tokenizer.next.type == "PONTO_VIRGULA":
                tokenizer.select_next()
                continue
            if tokenizer.next.type == "IDENTIFICADOR":
                nodes.append(Parser.parse_atribuicao(tokenizer))
            elif tokenizer.next.type == "SE" and tokenizer.next.value == "se":
                nodes.append(Parser.parse_estrutura_se(tokenizer))
            elif tokenizer.next.type == "ENQUANTO" and tokenizer.next.value == "enquanto":
                nodes.append(Parser.parse_estrutura_enquanto(tokenizer))
            elif tokenizer.next.type in ["PLANTAR", "COLHER"] and tokenizer.next.value in ["plantar", "colher"]:
                nodes.append(Parser.parse_operacao_cultivo(tokenizer))
            elif tokenizer.next.type in ["REGISTRAR", "VACINAR"] and tokenizer.next.value in ["registrar", "vacinar"]:
                nodes.append(Parser.parse_operacao_pecuaria(tokenizer))
            else:
                raise Exception(f"Comando inesperado: {tokenizer.next.value}")
        return Block("Block", nodes)

    @staticmethod
    def parse_atribuicao(tokenizer):
        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Esperado um identificador para atribuição")

        identificador = tokenizer.next.value
        tokenizer.select_next()

        if tokenizer.next.type != "IGUAL" or tokenizer.next.value != "=":
            raise Exception("Esperado '=' após identificador")

        tokenizer.select_next()

        expressao = Parser.parse_expressao(tokenizer)  

        return Atribuicao(Identificador(identificador), expressao)

    @staticmethod
    def parse_estrutura_se(tokenizer):
        tokenizer.select_next()

        if tokenizer.next.type != "ESQ_PARENTESES":
            raise Exception("Esperado '(' após 'se'")
        tokenizer.select_next()

        condicao = Parser.parse_expressao(tokenizer)

        if tokenizer.next.type != "DIR_PARENTESES":
            raise Exception("Esperado ')' após condição")
        tokenizer.select_next()

        if tokenizer.next.type != "ENTAO":
            raise Exception("Esperado 'entao' após condição")
        tokenizer.select_next()

        bloco_verdadeiro = Parser.parse_declaracoes(tokenizer)

        bloco_falso = None
        if tokenizer.next.type == "SENAO":
            tokenizer.select_next()
            bloco_falso = Parser.parse_declaracoes(tokenizer)

        return EstruturaSe(condicao, bloco_verdadeiro, bloco_falso)

    @staticmethod
    def parse_declaracoes(tokenizer):
        declaracoes = []
        while tokenizer.next.type not in ["SENAO", "EOF"]:
            if tokenizer.next.type == "PONTO_VIRGULA":
                tokenizer.select_next()
                continue
            declaracao = Parser.parse_declaracao(tokenizer)
            declaracoes.append(declaracao)
        return Block(None, declaracoes)
    
    @staticmethod
    def parse_declaracao(tokenizer):
        if tokenizer.next.type == "IDENTIFICADOR":
            return Parser.parse_atribuicao(tokenizer)
        elif tokenizer.next.type == "SE":
            return Parser.parse_estrutura_se(tokenizer)
        elif tokenizer.next.type == "ENQUANTO":
            return Parser.parse_estrutura_enquanto(tokenizer)
        elif tokenizer.next.type in ["PLANTAR", "COLHER"]:
            return Parser.parse_operacao_cultivo(tokenizer)
        elif tokenizer.next.type in ["REGISTRAR", "VACINAR"]:
            return Parser.parse_operacao_pecuaria(tokenizer)
        else:
            raise Exception(f"Tipo de declaração não reconhecido: {tokenizer.next.value}")

    @staticmethod
    def parse_estrutura_enquanto(tokenizer):
        tokenizer.select_next() 

        if tokenizer.next.type != "ESQ_PARENTESES" or tokenizer.next.value != "(":
            raise Exception("Esperado '(' após 'enquanto'")

        tokenizer.select_next()

        condicao = Parser.parse_expressao(tokenizer) 

        if tokenizer.next.type != "DIR_PARENTESES" or tokenizer.next.value != ")":
            raise Exception("Esperado ')' após condição")

        tokenizer.select_next()

        bloco = Parser.parse_bloco(tokenizer)  

        return EstruturaEnquanto(condicao, bloco)
    
    @staticmethod
    def parse_operacao_cultivo(tokenizer):
        operacao = tokenizer.next.value 
        tokenizer.select_next()

        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Esperado identificador de cultura após operação de cultivo")

        cultura = tokenizer.next.value
        tokenizer.select_next()

        data = None
        if operacao == "plantar":
            tokenizer.select_next()
            data = Parser.parse_data(tokenizer)

        return OperacaoCultivo(operacao, cultura, data)
    
    @staticmethod
    def parse_operacao_pecuaria(tokenizer):
        operacao = tokenizer.next.value 
        tokenizer.select_next()

        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Esperado identificador de pecuária após operação pecuária")

        identificador_pecuaria = tokenizer.next.value
        tokenizer.select_next()
        if operacao == "registrar":
            tipo_animal = tokenizer.next.value
            tokenizer.select_next()
            return OperacaoPecuaria(operacao, Identificador(identificador_pecuaria), Identificador(tipo_animal))

        elif operacao == "vacinar":
            tokenizer.select_next()
            data = Parser.parse_data(tokenizer)
            return OperacaoPecuaria(operacao, Identificador(identificador_pecuaria), data)

        else:
            raise Exception(f"Operação pecuária não suportada: {operacao}")


    @staticmethod
    def parse_bloco(tokenizer):
        if tokenizer.next.type != "COMECAR":
            raise Exception("Esperado 'comecar' para iniciar um bloco")

        tokenizer.select_next()

        declaracoes = []
        while tokenizer.next.type != "TERMINAR":
            if tokenizer.next.type == "PONTO_VIRGULA":
                tokenizer.select_next()
                continue
            declaracao = Parser.parse_declaracao(tokenizer)
            declaracoes.append(declaracao)

        if tokenizer.next.type != "TERMINAR":
            raise Exception("Esperado 'terminar' para fechar um bloco")
        tokenizer.select_next()

        return Block(None, declaracoes)

    
    @staticmethod
    def parse_data(tokenizer):
        if tokenizer.next.type != "NUMERO":
            raise Exception("Esperado um número para o dia na data")
        dia = tokenizer.next.value
        tokenizer.select_next()

        if tokenizer.next.type != "DIVISAO" or tokenizer.next.value != "/":
            raise Exception("Esperado '/' após o dia na data")
        tokenizer.select_next()

        if tokenizer.next.type != "NUMERO":
            raise Exception("Esperado um número para o mês na data")
        mes = tokenizer.next.value
        tokenizer.select_next()

        if tokenizer.next.type != "DIVISAO" or tokenizer.next.value != "/":
            raise Exception("Esperado '/' após o mês na data")
        tokenizer.select_next()

        if tokenizer.next.type != "NUMERO":
            raise Exception("Esperado um número para o ano na data")
        ano = tokenizer.next.value
        tokenizer.select_next()

        return {"dia": dia, "mes": mes, "ano": ano}
    
    @staticmethod
    def parse_expressao(tokenizer):
        result = Parser.parse_termo(tokenizer)
        while tokenizer.next.type in ["MAIS", "MENOS"]:
            if tokenizer.next.type == "MAIS":
                tokenizer.select_next()
                result = Expressao(result, '+', Parser.parse_termo(tokenizer))
            elif tokenizer.next.type == "MENOS":
                tokenizer.select_next()
                result = Expressao(result, '-', Parser.parse_termo(tokenizer))
        return result

    @staticmethod
    def parse_termo(tokenizer):
        result = Parser.parse_fator(tokenizer)
        while tokenizer.next.type in ["VEZES", "DIVISAO"]:
            if tokenizer.next.type == "VEZES":
                tokenizer.select_next()
                result = Termo(result, '*', Parser.parse_fator(tokenizer))
            elif tokenizer.next.type == "DIVISAO":
                tokenizer.select_next()
                result = Termo(result, '/', Parser.parse_fator(tokenizer))
        return result

    @staticmethod
    def parse_fator(tokenizer):
        if tokenizer.next.type == "NUMERO":
            value = tokenizer.next.value
            tokenizer.select_next()
            return Numero(value)
        elif tokenizer.next.type == "IDENTIFICADOR":
            name = tokenizer.next.value
            tokenizer.select_next()
            return Identificador(name)
        elif tokenizer.next.type == "ESQ_PARENTESES":
            tokenizer.select_next()
            result = Parser.parse_expressao(tokenizer)
            if tokenizer.next.type != "DIR_PARENTESES":
                raise Exception("Parênteses não fechado")
            tokenizer.select_next()
            return result
        else:
            raise Exception(f"Token inesperado: {tokenizer.next.value}")

    @staticmethod
    def run(tokenizer):
        # Inicializa o tokenizer e gera a lista de tokens
        tokenizer = Tokenizer(code)

        # Inicializa o primeiro token para o parser
        tokenizer.select_next()

        # Parseia o programa a partir dos tokens
        root = Parser.parse_program(tokenizer)

        # Cria uma tabela de símbolos para avaliação
        symbol_table = Symbol_Table()

        # Avalia o programa na tabela de símbolos
        root.evaluate(symbol_table)

        return symbol_table

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        code = file.read()
    
    tokenizer = Tokenizer(code)

    result = Parser.run(tokenizer)

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        code = file.read()
    
    content_filtered = PrePro.filter(code)

    tokenizer = Tokenizer(content_filtered)

    parser = Parser(tokenizer)

    st = parser.run(tokenizer=tokenizer)

    print(st.symbol_table)