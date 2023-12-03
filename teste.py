import re

texto = """
Exemplo de texto com informações:
12345678
AB
Nome Sobrenome/ Outro Nome
98765432
CD
Nome2 Sobrenome2 / Outro Nome2
"""

padrao = r'\d{8}\n[A-Z]{2}\n([A-Za-z\s]+)\/ ([A-Za-z\s]+)'

resultados = re.findall(padrao, texto)

for resultado in resultados:
    nome1, nome2 = resultado
    print(f"Nome 1: {nome1.strip()}")
    print(f"Nome 2: {nome2.strip()}")
    print('---')
