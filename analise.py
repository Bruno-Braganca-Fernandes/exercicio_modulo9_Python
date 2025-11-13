import time
import json
import sys
from random import random
from datetime import datetime

import requests
import pandas as pd
import seaborn as sns


def extrair_dados():
    print("Iniciando extração dos dados...")
    URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'
    dado = None

    try:
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError:
        print("Dado não encontrado, parando execução.")
        return False 
    except Exception as exc:
        print("Erro na extração, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)[-1]['valor']
        print("Taxa base do CDI capturada com sucesso.")

    with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
        fp.write('data,hora,taxa\n')

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(1)

    print("Extração de dados concluída. Arquivo 'taxa-cdi.csv' gerado.")
    return True


def gerar_grafico(meu_relatorio_final: str):
    print(f"Gerando gráfico com o nome '{meu_relatorio_final}.png'...")
    
    df = pd.read_csv('./taxa-cdi.csv')

    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    
    try:
        grafico.get_figure().savefig(f"{meu_relatorio_final}.png")
        print("Gráfico salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o gráfico: {e}")


def main():
    if len(sys.argv) < 2:
        print("Erro: Você precisa passar um nome para o gráfico.")
        print("Exemplo: python analise.py meu_grafico_cdi")
        return

    meu_relatorio_final = sys.argv[1]

    sucesso_extracao = extrair_dados()

    if sucesso_extracao:
        gerar_grafico(meu_relatorio_final=meu_relatorio_final)

if __name__ == "__main__":
    main()