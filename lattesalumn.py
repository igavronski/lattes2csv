#!/usr/bin/python3
# https://stackoverflow.com/questions/31844713/python-convert-xml-to-csv-file

import sys
from xml.etree import ElementTree
tree = ElementTree.parse('curriculo.xml')
def recode(var):
    # Py2: return var.decode('iso-8859-1').encode('utf8')
    return bytes(var, 'iso-8859-1').decode('utf8')
root = tree.getroot()
id_lattes = root.get('NUMERO-IDENTIFICADOR')
dt_upd = root.get('DATA-ATUALIZACAO')
hr_upd = root.get('HORA-ATUALIZACAO')

output = ''
line = [id_lattes]
gr_curso = ''
me_ = 0 # nro de mestrados
dr_ = 0 # nro de doutorados
pd_ = 0 # nro de pós-doutorados

for attrib in root:
    #print(attrib)
    if attrib.tag == 'DADOS-GERAIS':
        nome = attrib.get('NOME-COMPLETO')
        line += [nome, dt_upd, hr_upd]
        for part in attrib:
            '''
            print(part.tag)
            continue

            RESUMO-CV
            OUTRAS-INFORMACOES-RELEVANTES
            ENDERECO
            FORMACAO-ACADEMICA-TITULACAO
            ATUACOES-PROFISSIONAIS
            AREAS-DE-ATUACAO
            IDIOMAS
            PREMIOS-TITULOS
            '''
            for detail in part:
                '''
                print('detail.tag=='+detail.tag)
                continue
                '''
                tag = detail.tag
                if tag == 'ENDERECO-PROFISSIONAL':
                    empresa = detail.get('NOME-INSTITUICAO-EMPRESA')
                    orgao = detail.get('NOME-ORGAO')
                    unidade = detail.get('NOME-UNIDADE')
                    cidade = detail.get('CIDADE')
                    uf = detail.get('UF')
                    pais = detail.get('PAIS')
                    line += [empresa, orgao, unidade, cidade, uf, pais]
                if tag == 'GRADUACAO' and gr_curso == '': # considera a 1a graduacao
                    gr_curso = detail.get('NOME-CURSO')
                    gr_ies = detail.get('NOME-INSTITUICAO')
                    gr_concl = detail.get('ANO-DE-CONCLUSAO')
                    line += [gr_curso, gr_ies,gr_concl]
                if tag == 'MESTRADO':
                    me_ += 1
                    me_curso = detail.get('NOME-CURSO')
                    me_ies = detail.get('NOME-INSTITUICAO')
                    me_ini = detail.get('ANO-DE-INICIO')
                    me_concl = detail.get('ANO-DE-CONCLUSAO')
                    me_per = me_ini+'-'+me_concl
                    me_titulo = detail.get('TITULO-DA-DISSERTACAO-TESE')
                    me_orient = detail.get('NOME-COMPLETO-DO-ORIENTADOR')
                    me_id_or = detail.get('NUMERO-ID-ORIENTADOR')
                    if me_ > 1 and me_concl == '': # desprezar novo mestrado em andamento
                        continue
                    else:
                        line += [str(me_), me_curso, me_ies, me_per, 
                                me_titulo, me_orient, me_id_or]
                if tag == 'DOUTORADO':
                    dr_ += 1
                    dr_curso = detail.get('NOME-CURSO')
                    dr_ies = detail.get('NOME-INSTITUICAO')
                    dr_ini = detail.get('ANO-DE-INICIO')
                    dr_concl = detail.get('ANO-DE-CONCLUSAO')
                    dr_per = dr_ini+'-'+dr_concl
                    dr_titulo = detail.get('TITULO-DA-DISSERTACAO-TESE')
                    dr_orient = detail.get('NOME-COMPLETO-DO-ORIENTADOR')
                    dr_id_or = detail.get('NUMERO-ID-ORIENTADOR')
                    if dr_ > 1 and dr_concl == '': # desprezar novo doutorado em andamento
                        continue
                    else:
                        line += [str(dr_), dr_curso, dr_ies, dr_per, 
                                dr_titulo, dr_orient, dr_id_or]
                if tag == 'POS-DOUTORADO':
                    pd_ += 1
                    pd_ies = detail.get('NOME-INSTITUICAO')
                    pd_ini = detail.get('ANO-DE-INICIO')
                    pd_concl = detail.get('ANO-DE-CONCLUSAO')
                    pd_per = pd_ini+'-'+pd_concl
                    pd_titulo = detail.get('TITULO-DO-TRABALHO')
                    #pd_orient = detail.get('NOME-COMPLETO-DO-ORIENTADOR')
                    pd_id_or = detail.get('NUMERO-ID-ORIENTADOR')
                    line += [str(pd_), pd_ies, pd_per, 
                            pd_titulo, pd_id_or]

i = 0
for field in line:
    #print(repr(field))
    line[i] = field.replace('\n',' ').replace('\r','')
    i += 1
#line = '", "'.join(line) never use spaces after delimiting commas!
line = '","'.join(line)
line = '"' + line + '"\n'
output += line
fn = id_lattes+'_alu.csv'
outfile = open(fn, 'w')
outfile.write(output)
outfile.close()
print('File {} ({}) written'.format(fn,nome))

