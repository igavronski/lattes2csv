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
    #print(attrib)
    if attrib.tag == 'DADOS-GERAIS':
        nome = attrib.get('NOME-COMPLETO')
    if attrib.tag == 'PRODUCAO-TECNICA':
        for paper in attrib:
            #print()
            #print('paper.tag=='+paper.tag)
            if paper.tag != 'TRABALHO-TECNICO':
                continue
            seq = paper.get('SEQUENCIA-PRODUCAO')
            autores = []
            resumo = ''
            for detail in paper:
                #print('detail.tag=='+detail.tag)
                tag = detail.tag
                if tag == 'DADOS-BASICOS-DO-TRABALHO-TECNICO':
                    titulo = detail.get('TITULO-DO-TRABALHO-TECNICO')
                    ano = detail.get('ANO')
                    url = detail.get('HOME-PAGE-DO-TRABALHO')
                    url = url.strip('[]')
                    doi = detail.get('DOI')
                    pais = detail.get('PAIS')
                if tag == 'DETALHAMENTO-DO-TRABALHO-TECNICO':
                    finalidade = detail.get('FINALIDADE')
                    duracao = detail.get('DURACAO-EM-MESES')
                    financ = detail.get('INSTITUICAO-FINANCIADORA')
                    cidade = detail.get('CIDADE-DO-TRABALHO')
                if tag == 'AUTORES':
                    autor = detail.get('NOME-PARA-CITACAO')
                    autor = autor.split(';')
                    autor = autor[0]
                    ordem = detail.get('ORDEM-DE-AUTORIA')
                    autores.append((ordem, autor))
                if tag == 'INFORMACOES-ADICIONAIS':
                    resumo = detail.get('DESCRICAO-INFORMACOES-ADICIONAIS')

            autores = sorted(autores)
            autores = "; ".join("%s" % autor for (ordem, autor) in autores) 
            line = [id_lattes, nome, seq, autores, ano, titulo, doi,
                    url, pais, cidade, finalidade, duracao, financ,
                    resumo]
            i = 0
            for field in line:
                #print(repr(field))
                line[i] = field.replace('\n',' ').replace('\r','')
                i += 1
            #line = '", "'.join(line) never use spaces after delimiting commas!
            line = '","'.join(line)
            line = '"' + line + '"\n'
            output += line
outfile = open(id_lattes+'.csv', 'w')
outfile.write(output)
outfile.close()
print('File {}.csv ({}) written'.format(id_lattes,nome))

