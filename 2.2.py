#Implementar um algoritmo usando pilha para checar se os símbolos de abertura e
#fechamento de tags de arquivos json estão corretos. Apresentar 03 casos de teste.

# Verificador de Símbolos JSON usando Pilha

# Classe Pilha com todas as operações necessárias
class Pilha:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Empilha novo elemento"""
        self.items.append(item)
    
    def pop(self):
        """Remove e retorna o elemento do topo da pilha"""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def top(self):
        """Retorna o elemento do topo sem remover"""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self):
        """Verifica se a pilha está vazia"""
        return len(self.items) == 0


def verificar_json(json_string):
    """
    Verifica se os símbolos de abertura e fechamento do JSON estão corretos.
    Verifica: { }, [ ]
    Retorna (bool, str): (está correto, mensagem)
    """
    pilha = Pilha()
    pares = {'}': '{', ']': '['}
    
    # Remove strings entre aspas para evitar falsos positivos
    json_limpo = remover_strings(json_string)
    
    for i, char in enumerate(json_limpo):
        if char in '{[':
            pilha.push((char, i))
        elif char in '}]':
            if pilha.is_empty():
                return False, f"Símbolo de fechamento '{char}' na posição {i} sem abertura correspondente"
            
            simbolo_abertura, pos_abertura = pilha.pop()
            if pares[char] != simbolo_abertura:
                return False, f"Símbolo incorreto na posição {i}: esperava '{get_fechamento(simbolo_abertura)}', encontrou '{char}'"
    
    if not pilha.is_empty():
        simbolos_abertos = []
        while not pilha.is_empty():
            simbolo, pos = pilha.pop()
            simbolos_abertos.append(f"'{simbolo}' na posição {pos}")
        return False, f"Símbolos não fechados: {', '.join(reversed(simbolos_abertos))}"
    
    return True, "JSON válido. Todos os símbolos estão balanceados corretamente."


def remover_strings(json_string):
    """
    Remove conteúdo entre aspas para evitar que símbolos dentro de strings sejam verificados.
    """
    resultado = []
    dentro_string = False
    escape = False
    
    for char in json_string:
        if escape:
            escape = False
            resultado.append(' ')
            continue
        
        if char == '\\':
            escape = True
            resultado.append(' ')
            continue
        
        if char == '"':
            dentro_string = not dentro_string
            resultado.append(' ')
        elif dentro_string:
            resultado.append(' ')
        else:
            resultado.append(char)
    
    return ''.join(resultado)


def get_fechamento(abertura):
    """Retorna o símbolo de fechamento correspondente."""
    return '}' if abertura == '{' else ']'


# CASOS DE TESTE

print("=" * 70)
print("CASO DE TESTE 1: JSON Correto")
print("=" * 70)

json1 = """{
    "nome": "João Silva",
    "idade": 30,
    "endereço": {
        "rua": "Rua das Flores",
        "numero": 123,
        "cidade": "São Paulo"
    },
    "telefones": [
        "11-1234-5678",
        "11-9876-5432"
    ],
    "ativo": true
}"""

print("JSON:")
print(json1)
resultado, mensagem = verificar_json(json1)
print(f"\nResultado: {mensagem}\n")


print("=" * 70)
print("CASO DE TESTE 2: JSON com colchete não fechado")
print("=" * 70)

json2 = """{
    "nome": "Maria Santos",
    "hobbies": [
        "leitura",
        "música",
        "esportes"
    ,
    "email": "maria@email.com"
}"""

print("JSON:")
print(json2)
resultado, mensagem = verificar_json(json2)
print(f"\nResultado: {mensagem}\n")


print("=" * 70)
print("CASO DE TESTE 3: JSON com símbolos em ordem errada")
print("=" * 70)

json3 = """{
    "empresa": "Tech Company",
    "funcionários": [
        {
            "nome": "Carlos",
            "cargo": "Desenvolvedor"
        ]
    },
    "ativo": true
}"""

print("JSON:")
print(json3)
resultado, mensagem = verificar_json(json3)
print(f"\nResultado: {mensagem}\n")