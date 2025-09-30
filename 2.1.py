# Verificador de Tags HTML usando Pilha

import re

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


def extrair_tags(html):
    """
    Extrai todas as tags HTML do código.
    Retorna lista de tuplas (tipo, nome_tag).
    """
    padrao = r'<(/?)(\w+)[^>]*?(?<!/)>'
    tags = []
    
    for match in re.finditer(padrao, html):
        eh_fechamento = match.group(1) == '/'
        nome_tag = match.group(2).lower()
        tipo = 'fechamento' if eh_fechamento else 'abertura'
        tags.append((tipo, nome_tag))
    
    return tags


def verificar_tags_html(html):
    """
    Verifica se as tags HTML estão balanceadas corretamente.
    Retorna (bool, str): (está correto, mensagem)
    """
    pilha = Pilha()
    tags = extrair_tags(html)
    
    if not tags:
        return True, "Nenhuma tag encontrada"
    
    for tipo, nome_tag in tags:
        if tipo == 'abertura':
            pilha.push(nome_tag)
        else:
            if pilha.is_empty():
                return False, f"Tag de fechamento </{nome_tag}> sem abertura correspondente"
            
            tag_abertura = pilha.pop()
            if tag_abertura != nome_tag:
                return False, f"Tag incorreta: esperava </{tag_abertura}>, encontrou </{nome_tag}>"
    
    if not pilha.is_empty():
        tags_abertas = []
        while not pilha.is_empty():
            tags_abertas.append(pilha.pop())
        return False, f"Tags não fechadas: {', '.join(f'<{tag}>' for tag in reversed(tags_abertas))}"
    
    return True, "HTML válido. Todas as tags estão balanceadas corretamente."


# CASOS DE TESTE

print("=" * 70)
print("CASO DE TESTE 1: HTML Correto")
print("=" * 70)

html1 = """
<html>
    <head>
        <title>Minha Página</title>
    </head>
    <body>
        <h1>Bem-vindo</h1>
        <p>Este é um parágrafo.</p>
        <div>
            <span>Texto dentro de span</span>
        </div>
    </body>
</html>
"""

print("HTML:")
print(html1)
resultado, mensagem = verificar_tags_html(html1)
print(f"Resultado: {mensagem}\n")


print("=" * 70)
print("CASO DE TESTE 2: HTML com tag não fechada")
print("=" * 70)

html2 = """
<html>
    <head>
        <title>Página com Erro</title>
    </head>
    <body>
        <h1>Título
        <p>Parágrafo sem fechar</p>
    </body>
</html>
"""

print("HTML:")
print(html2)
resultado, mensagem = verificar_tags_html(html2)
print(f"Resultado: {mensagem}\n")


print("=" * 70)
print("CASO DE TESTE 3: HTML com tags em ordem errada")
print("=" * 70)

html3 = """
<html>
    <body>
        <div>
            <p>Texto
        </div>
        </p>
    </body>
</html>
"""

print("HTML:")
print(html3)
resultado, mensagem = verificar_tags_html(html3)
print(f"Resultado: {mensagem}\n")