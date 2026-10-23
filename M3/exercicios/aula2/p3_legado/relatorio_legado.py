# relatorio.py - gera relatorio dos alunos
# feito as pressas em 2019, "funciona", nao mexer!!!
# uso: python relatorio_legado.py turma.csv
import csv, sys
from statistics import *

alunos = []
erros = 0


def le(arq, sep=';', lista=[]):
    f = open(arq)
    for l in csv.reader(f, delimiter=sep):
        if l[0] == 'matricula':
            continue
        lista.append(l)
    return lista


def calc(a):
    try:
        ns = [float(x.replace(',', '.')) for x in a[2:]]
        m = sum(ns) / 3
    except:
        global erros
        erros += 1
        return
    if m >= 7:
        s = 'aprovado'
    elif m > 5:
        s = 'recuperacao'
    else:
        s = 'reprovado'
    return [a[1], m, s]


def main():
    dados = le(sys.argv[1])
    for a in dados:
        r = calc(a)
        if r != None:
            alunos.append(r)
    alunos.sort(key=lambda x: x[1])
    print('=== MELHORES ALUNOS ===')
    for i in range(1, len(alunos)):
        print(i, alunos[i][0], round(alunos[i][1], 1), alunos[i][2])
    print('erros:', erros)
    print('media da turma:', round(mean([a[1] for a in alunos]), 2))


main()
