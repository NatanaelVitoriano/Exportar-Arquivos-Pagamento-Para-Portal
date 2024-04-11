import requests
from pathlib import Path
from arquivoAFeAP import dataAF, dataAP
from itertools import groupby
from operator import itemgetter

print("Digite o codigo do municipio: ")
numMunicipio = input()
print("Digite a data de referencia: (OBS: com barras'/') ")
dataReferencia = input()

listaAPs = []
listaAFs = []
dicioAFs = []

dicioOrgaos = {}
orgDados = requests.get('https://api-dados-abertos.tce.ce.gov.br/orgaos?codigo_municipio=' + numMunicipio + '&exercicio_orcamento=202300')
json = orgDados.json()
listaDeOrgaos = json['data']

for orgao in listaDeOrgaos:
    dicioOrgaos[orgao['codigo_orgao']] = orgao['nome_orgao']

#Arquivo Remuneracao do AP
dataAF.sort(key = itemgetter(8))
groups = groupby(dataAF, itemgetter(8))
listaDataAFAgrupada = [[item for item in data] for (key, data) in groups]

for dataAFAgrupada in listaDataAFAgrupada:
    totalBruto = 0
    totalSubtraido = 0
    totalLiquido = 0

    for data in dataAFAgrupada:
        if data[14] != '""':
            totalBruto = totalBruto + float((data[13]).replace('"',""))
        else:
            totalSubtraido = totalSubtraido + float((data[13]).replace('"',""))

        totalLiquido = totalBruto - totalSubtraido

    index_row = [dataAP.index(row) for row in dataAP if dataAFAgrupada[0][8] in row]
    
    listaAFs.append((dataAP[index_row[0]][16]).replace('"',"").replace("  ","").strip() + ";" + dataReferencia + ";" + str("%.2f" % totalBruto) + ";" + str("%.2f" % totalSubtraido) + ";" + str("%.2f" % totalLiquido) + ";" + dataAFAgrupada[0][8])

arquivoRemuneracaoDoAgente = Path(numMunicipio + "_WEBSERFOL2" + dataReferencia.replace("/","") + ".MAX")
arquivoRemuneracaoDoAgente.write_text("\n".join(listaAFs), encoding="utf8")

#Arquivo Dados do AP
dataAP.sort(key = itemgetter(5))
groups = groupby(dataAP, itemgetter(5))
listaDataAPAgrupada = [[item for item in data] for (key, data) in groups]

for ap in listaDataAPAgrupada:
    for listaAux in listaAFs:
        if ap[0][5] in listaAux:
            listaAPs.append(str(ap[0][16].replace('"',"").strip() + ";" + ap[0][16].replace('"',"").strip() + ";" + ap[0][31] + ";" + ap[0][40].replace("\n","").upper() + ";" + ap[0][5] + ";"+ dicioOrgaos[ap[0][3].replace('"',"")].upper() + ";" + dataReferencia).replace("  ","").strip())

arquivoDadosDoAgente = Path(numMunicipio + "_WEBSERFOL1" + dataReferencia.replace("/","") + ".MAX")
arquivoDadosDoAgente.write_text("\n".join(listaAPs), encoding="utf8")