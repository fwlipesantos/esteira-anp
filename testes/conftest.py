import os
import sys

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
projetos = os.path.dirname(raiz)

for caminho in [raiz, os.path.join(projetos, "precos-anp"), os.path.join(projetos, "qualidade-anp")]:
    if caminho not in sys.path:
        sys.path.insert(0, caminho)
