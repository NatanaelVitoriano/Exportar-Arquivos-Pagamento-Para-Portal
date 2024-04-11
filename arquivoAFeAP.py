from pathlib import Path
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "arquivos/"
caminho = os.path.join(script_dir, rel_path)

aps = 'AP'
afs = 'AF'
listaDeAPsNaPasta = []
listaDeAFsNaPasta = []
dataAF = []
dataAP = []

pathLote = Path(caminho)

if pathLote.exists():
    for f in os.listdir(pathLote):
        if aps in f:
            listaDeAPsNaPasta.append(f)
    for f in os.listdir(pathLote):
        if afs in f:
            listaDeAFsNaPasta.append(f)

for ap in listaDeAFsNaPasta:
    with open(caminho + ap, "r") as arquivoAF:
        linhasDoArquivo = arquivoAF.readline()
        while linhasDoArquivo:
            dataAF.append(linhasDoArquivo.split(","))
            linhasDoArquivo = arquivoAF.readline()
        
for ap in listaDeAPsNaPasta:
    with open(caminho + ap, "r") as arquivoAP:
        linhasDoArquivo = arquivoAP.readline()
        while linhasDoArquivo:
            dataAP.append(linhasDoArquivo.split(","))
            linhasDoArquivo = arquivoAP.readline()