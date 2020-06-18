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
    papers = attrib.find('ARTIGOS-PUBLICADOS')
    if papers == None:
        continue
    #print(papers)
    for paper in papers:
        #print()
        #print(paper.tag)
        seq = paper.get('SEQUENCIA-PRODUCAO')
        autores = []
        for detail in paper:
            #print(detail.tag)
            tag = detail.tag
            if tag == 'DADOS-BASICOS-DO-ARTIGO':
                titulo = detail.get('TITULO-DO-ARTIGO')
                ano = detail.get('ANO-DO-ARTIGO')
                url = detail.get('HOME-PAGE-DO-TRABALHO')
                url = url.strip('[]')
                doi = detail.get('DOI')
            if tag == 'DETALHAMENTO-DO-ARTIGO':
                periodico = detail.get('TITULO-DO-PERIODICO-OU-REVISTA')
                issn = detail.get('ISSN')
                vol = detail.get('VOLUME')
                issue = detail.get('SERIE')
                pgini = detail.get('PAGINA-INICIAL')
                pgfim = detail.get('PAGINA-FINAL')
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
        line = [id_lattes, nome, seq, autores, ano, titulo, periodico, issn, doi,
                url, vol, issue, pgini, pgfim]
        #line = '", "'.join(line) never use spaces after delimiting commas!
        line = '","'.join(line)
        line = '"' + line + '"\n'
        output += line
file = open(id_lattes+'.csv', 'w')
file.write(output)
file.close()
print('File {}.csv ({}) written'.format(id_lattes,nome))

