#!/usr/bin/python3
# https://stackoverflow.com/questions/31844713/python-convert-xml-to-csv-file

from xml.etree import ElementTree
tree = ElementTree.parse('curriculo.xml')
def recode(var):
    # Py2: return var.decode('iso-8859-1').encode('utf8')
    return bytes(var, 'iso-8859-1').decode('utf8')
root = tree.getroot()
id_lattes = root.get('NUMERO-IDENTIFICADOR')

output = ''

for attrib in root:
    if attrib.tag == 'DADOS-GERAIS':
        nome = attrib.get('NOME-COMPLETO')
    papers = attrib.find('TRABALHOS-EM-EVENTOS')
    if papers == None:
        continue
    #print(papers)
    for paper in papers:
        #print()
        #print(paper.tag)
        seq = paper.get('SEQUENCIA-PRODUCAO')
        id_seq = id_lattes + seq
        autores = []
        for detail in paper:
            #print(detail.tag)
            tag = detail.tag
            if tag == 'DADOS-BASICOS-DO-TRABALHO':
                natureza = detail.get('NATUREZA')
                titulo = detail.get('TITULO-DO-TRABALHO')
                ano = detail.get('ANO-DO-TRABALHO')
                url = detail.get('HOME-PAGE-DO-TRABALHO')
                url = url.strip('[]')
                doi = detail.get('DOI')
                pais = detail.get('PAIS-DO-EVENTO')
            if tag == 'DETALHAMENTO-DO-TRABALHO':
                classe = detail.get('CLASSIFICACAO-DO-EVENTO')
                evento = detail.get('NOME-DO-EVENTO')
                cidade = detail.get('CIDADE-DA-EDITORA')
            if tag == 'AUTORES':
                autor = detail.get('NOME-PARA-CITACAO')
                autor = autor.split(';')
                autor = autor[0]
                ordem = detail.get('ORDEM-DE-AUTORIA')
                autores.append((ordem, autor))

        #second = subatt.find('TITULO-DO-ARTIGO')
        autores = sorted(autores)
        autores = "; ".join("%s" % autor for (ordem, autor) in autores) 
        #print('"{}","{}",{},"{}","{}"'.join(id_lattes, titulo, ano, periodico, issn))
        line = [id_lattes, seq, id_seq, nome, autores, ano, titulo, 
                evento, natureza,
                cidade, pais, classe,
                url, doi]
        #line = '", "'.join(line) never use spaces after delimiting commas!
        line = '","'.join(line)
        line = '"' + line + '"\n'
        output += line
fn = id_lattes+'evt.csv'
file = open(fn, 'w')
file.write(output)
file.close()
print('File {} ({}) written'.format(fn,nome))

