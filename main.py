import csv
from datetime import datetime
import json
import requests


def extrair_dados():
  """Consome uma API pública de cotações de moedas (Dólar, Euro, Bitcoin)."""
  url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
  resposta = requests.get(url)

  if resposta.status_code == 200:
    return resposta.json()
  else:
    raise Exception(f"Erro ao acessar a API: Status {resposta.status_code}")


def transformar_dados(dados_brutos):
  """Limpa os dados e adiciona um cálculo de taxa administrativa de 2%."""
  dados_tratados = []
  data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  for chave, info in dados_brutos.items():
    valor_compra = float(info["bid"])
    valor_com_taxa = round(valor_compra * 1.02, 4)

    registro = {
        "moeda": info["name"],
        "codigo": info["code"],
        "valor_mercado": valor_compra,
        "valor_final_cliente": valor_com_taxa,
        "data_hora": data_coleta,
    }
    dados_tratados.append(registro)

  return dados_tratados


def carregar_dados(dados_tratados):
  """Salva os dados processados em JSON e CSV."""
  # Salvando em JSON
  with open("cotacoes_processadas.json", "w", encoding="utf-8") as arquivo_json:
    json.dump(dados_tratados, arquivo_json, ensure_ascii=False, indent=4)

  # Salvando em CSV
  colunas = [
      "moeda",
      "codigo",
      "valor_mercado",
      "valor_final_cliente",
      "data_hora",
  ]
  with open(
      "cotacoes_processadas.csv", "w", newline="", encoding="utf-8"
  ) as arquivo_csv:
    escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)
    escritor.writeheader()
    escritor.writerows(dados_tratados)


if __name__ == "__main__":
  print("Iniciando pipeline ETL...")
  brutos = extrair_dados()
  tratados = transformar_dados(brutos)
  carregar_dados(tratados)
  print(
      "Sucesso! Arquivos 'cotacoes_processadas.json' e"
      " 'cotacoes_processadas.csv' gerados."
  )