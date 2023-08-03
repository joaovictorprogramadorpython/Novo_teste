import time
from iqoptionapi.stable_api import IQ_Option
import pandas as pd
import datetime
from os import chdir
import re

#O Arquivo do Robo de Teste é Para Criar um codito de Teste de Verificação de estrategia.E construção da logica do robo para operar sua Minha estrategia
chdir(r'C:\Users\jvmir\PycharmProjects\Robo_Iq_Option')
# Arquivos contendo as informações de padrão de velas. OBS: OS Arquivos estão na pasto do Projecto!
velas_padrao = pd.read_excel("VELAS_PADRÃO.xlsx")
# Arquivo de armazenamento de dados para avaliar se a estrategia esta funcionando no mes!
base_teste = pd.read_csv("Base_teste_estrategia.csv")
# Codigo de Loguin Iq
email = 'j.v.mirandatorres@gmail.com'
senha = '8426mirandatorres'
# Iniciando o navegador webdrive edgs
#-------- primeira parte conecção da api ------------------
API = IQ_Option(email,senha)


check,reason = API.connect()

#-------- primeira parte conecção da api ------------------
# Verificar se conecção foi bem sussedida
if check:
    print('conectado co sucesso')
# Criando essa função para coletar as informações nessesaria para verificar se a minha estrategia funciona
def Teste_Estrategia_mercado_normal():
    # O objetivo da função e coletar dados e adicionar na base de teste.
    dia_semana = datetime.datetime.today().weekday()
    if dia_semana == 4:
        try:
            while True:
                horas = str(datetime.datetime.today().time().strftime("%H:%M"))
                if (horas in ['05:00','06:00','07:00', '08:00', '09:00']):
                    print(horas)
                    EURJPY = [123.45]
                    EURUSD = [124.67]
                    EURGPB = [123.99]
                    count = 0
                    while True:
                        time.sleep(0.1)
                        minuto = datetime.datetime.fromtimestamp(API.get_server_timestamp()).strftime("%M.%S")[3:]
                        if minuto == '50':
                            count += 1
                            if count == 26:
                                horas1 = str(datetime.datetime.today().time().strftime("%H:%M"))
                                print(f'Completou 25 repetição em tempo {horas1} Vai sair do loop e entra no outro! ')
                                base_teste.to_csv('Base_teste_estrategia.csv', index=False)
                                break
                            else:
                                data_atual = datetime.datetime.today()
                                timest = datetime.datetime.today().timestamp()
                                for ativo in ['EURUSD', 'EURJPY', 'EURGBP']:
                                    parmoeda = ativo
                                    velas = API.get_candles(parmoeda, 10, 3, API.get_server_timestamp())
                                    vela1 = []
                                    vela2 = []
                                    vela3 = []
                                    gep = []
                                    # Verificando Gep de Velas Verde
                                    if (velas[1]['open'] < velas[1]['close']) and (velas[1]['close'] < velas[2]['open']):
                                        gep.append('ALTA')
                                    elif (velas[1]['open'] < velas[1]['close']) and (velas[1]['close'] > velas[2]['open']):
                                        gep.append('NEUTRO')
                                    elif (velas[1]['open'] < velas[1]['close']) and (velas[1]['close'] == velas[2]['open']):
                                        gep.append('NEUTRO')
                                    # Verificando Velas Vermelhas
                                    elif (velas[1]['open'] > velas[1]['close']) and (velas[1]['close'] > velas[2]['open']):
                                        gep.append('ALTA')
                                    elif (velas[1]['open'] > velas[1]['close']) and (velas[1]['close'] < velas[2]['open']):
                                        gep.append('NEUTRO')
                                    elif (velas[1]['open'] > velas[1]['close']) and (velas[1]['close'] == velas[2]['open']):
                                        gep.append('NEUTRO')
                                    # Coletando informações das 3 primeiras velas
                                    for n in [0, 1, 2]:
                                        if n == 0:
                                            if (velas[n]['close'] > velas[n]['open']) and (velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(6)
                                                else:
                                                    vela1.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(6)
                                                else:
                                                    vela1.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(7)
                                                else:
                                                    vela1.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(7)
                                                else:
                                                    vela1.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela1.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela1.append(0)
                                            else:
                                                vela1.append('dj')
                                        elif n == 1:
                                            if (velas[n]['close'] > velas[n]['open']) and (velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(6)
                                                else:
                                                    vela2.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(6)
                                                else:
                                                    vela2.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(7)
                                                else:
                                                    vela2.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(7)
                                                else:
                                                    vela2.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela2.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela2.append(0)
                                            else:
                                                vela2.append('dj')
                                        else:
                                            if (velas[n]['close'] > velas[n]['open']) and (velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(6)
                                                else:
                                                    vela3.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(6)
                                                else:
                                                    vela3.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(7)
                                                else:
                                                    vela3.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(7)
                                                else:
                                                    vela3.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela3.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela3.append(0)
                                            else:
                                                vela3.append('dj')

                                    if ('dj' in vela1) or ('dj' in vela2) or ('dj' in vela3):
                                        pass
                                    else:
                                        padrao = velas_padrao.loc[
                                            (velas_padrao['GEP'] == gep[0]) & (velas_padrao['VELA 1'] == vela1[0]) & (
                                                    velas_padrao['VELA 2'] == vela2[0]) & (
                                                    velas_padrao['VELA 3'] == vela3[0]), 'RESULTADO']
                                        if 'EURUSD' == parmoeda:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                                        elif 'EURJPY' == parmoeda:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                                        else:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp', 'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao', 'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                elif horas in ['10:00']:
                    base_teste.to_csv('Base_teste_estrategia.csv', index=False)
                    break
                else:
                    time.sleep(3)
        except:
            print('Erro de Codigo Interrompido ')
            base_teste.to_csv('Base_teste_estrategia.csv', index=False)
    elif dia_semana in [5,6]:
        print('Mercado OTC Não funcionan!')
        pass
    else:
        try:
            while True:
                horas = str(datetime.datetime.today().time().strftime("%H:%M"))
                if (horas in ['05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00']) or (
                        horas in ['21:30', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00']):
                    print(horas)
                    EURJPY = [123.45]
                    EURUSD = [124.67]
                    EURGPB = [123.99]
                    count = 0
                    while True:
                        time.sleep(0.1)
                        minuto = datetime.datetime.fromtimestamp(API.get_server_timestamp()).strftime("%M.%S")[3:]
                        if minuto == '50':
                            count += 1
                            if count == 26:
                                horas1 = str(datetime.datetime.today().time().strftime("%H:%M"))
                                print(f'Completou 25 repetição em tempo {horas1} Vai sair do loop e entra no outro! ')
                                base_teste.to_csv('Base_teste_estrategia.csv', index=False)
                                break
                            else:
                                data_atual = datetime.datetime.today()
                                timest = datetime.datetime.today().timestamp()
                                for ativo in ['EURUSD', 'EURJPY', 'EURGBP']:
                                    parmoeda = ativo
                                    velas = API.get_candles(parmoeda, 10, 3, API.get_server_timestamp())
                                    vela1 = []
                                    vela2 = []
                                    vela3 = []
                                    gep = []
                                    # Verificando Gep de Velas Verde
                                    if (velas[1]['open'] < velas[1]['close']) and (
                                            velas[1]['close'] < velas[2]['open']):
                                        gep.append('ALTA')
                                    elif (velas[1]['open'] < velas[1]['close']) and (
                                            velas[1]['close'] > velas[2]['open']):
                                        gep.append('NEUTRO')
                                    elif (velas[1]['open'] < velas[1]['close']) and (
                                            velas[1]['close'] == velas[2]['open']):
                                        gep.append('NEUTRO')
                                    # Verificando Velas Vermelhas
                                    elif (velas[1]['open'] > velas[1]['close']) and (
                                            velas[1]['close'] > velas[2]['open']):
                                        gep.append('ALTA')
                                    elif (velas[1]['open'] > velas[1]['close']) and (
                                            velas[1]['close'] < velas[2]['open']):
                                        gep.append('NEUTRO')
                                    elif (velas[1]['open'] > velas[1]['close']) and (
                                            velas[1]['close'] == velas[2]['open']):
                                        gep.append('NEUTRO')
                                    # Coletando informações das 3 primeiras velas
                                    for n in [0, 1, 2]:
                                        if n == 0:
                                            if (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(6)
                                                else:
                                                    vela1.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(6)
                                                else:
                                                    vela1.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(7)
                                                else:
                                                    vela1.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela1.append(7)
                                                else:
                                                    vela1.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela1.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela1.append(0)
                                            else:
                                                vela1.append('dj')
                                        elif n == 1:
                                            if (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(6)
                                                else:
                                                    vela2.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(6)
                                                else:
                                                    vela2.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(7)
                                                else:
                                                    vela2.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela2.append(7)
                                                else:
                                                    vela2.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela2.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela2.append(0)
                                            else:
                                                vela2.append('dj')
                                        else:
                                            if (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(6)
                                                else:
                                                    vela3.append(5)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] > velas[n]['min']) and (
                                                    velas[n]['close'] == velas[n]['max']):
                                                if (velas[n]['close'] > velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(6)
                                                else:
                                                    vela3.append(4)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] == velas[n]['min']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(7)
                                                else:
                                                    vela3.append(3)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['close'] > velas[n]['min']) and (
                                                    velas[n]['open'] == velas[n]['max']):
                                                if (velas[n]['close'] < velas[n]['open']) and (
                                                        velas[n]['close'] == velas[n]['min']) and (
                                                        velas[n]['open'] == velas[n]['max']):
                                                    vela3.append(7)
                                                else:
                                                    vela3.append(2)
                                            elif (velas[n]['close'] > velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela3.append(1)
                                            elif (velas[n]['close'] < velas[n]['open']) and (
                                                    velas[n]['open'] != velas[n]['min']) and (
                                                    velas[n]['close'] != velas[n]['max']):
                                                vela3.append(0)
                                            else:
                                                vela3.append('dj')

                                    if ('dj' in vela1) or ('dj' in vela2) or ('dj' in vela3):
                                        pass
                                    else:
                                        padrao = velas_padrao.loc[
                                            (velas_padrao['GEP'] == gep[0]) & (velas_padrao['VELA 1'] == vela1[0]) & (
                                                    velas_padrao['VELA 2'] == vela2[0]) & (
                                                    velas_padrao['VELA 3'] == vela3[0]), 'RESULTADO']
                                        if 'EURUSD' == parmoeda:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURUSD[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                                        elif 'EURJPY' == parmoeda:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURJPY[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                                        else:
                                            if (padrao == 'CALL').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'CALL', 'nada']
                                            elif (padrao == 'PUT').any():
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'PUT', 'nada']
                                            else:
                                                base_teste.loc[
                                                    len(base_teste), ['parmoeda', 'frequencia', 'datetime', 'timestamp',
                                                                      'GEP',
                                                                      'vela1', 'vela2', 'vela3', 'operacao',
                                                                      'ultima_vela']] = [
                                                    parmoeda, EURGPB[0], data_atual, timest, gep[0], vela1[0], vela2[0],
                                                    vela3[0], 'ainda_falta', 'nada']
                elif horas in ['11:30']:
                    base_teste.to_csv('Base_teste_estrategia.csv', index=False)
                    print('Esperar ate 21:30')
                    time.sleep(35400)
                elif horas in ['03:30']:
                    break
                else:
                    time.sleep(3)
        except:
            print('Erro de Codigo Interrompido ')
            base_teste.to_csv('Base_teste_estrategia.csv', index=False)
def Adicionando_Vela_Abertura_Ultima():
    for indx in base_teste[base_teste['ultima_vela'] == 'nada'].index:
        mod = base_teste.loc[indx,'parmoeda']
        timstpe = float(base_teste.loc[indx,'timestamp'])
        vela_abertura = API.get_candles(mod, 10, 2, timstpe + 10.0)[0]
        ultima_vela = API.get_candles(mod,10,2,timstpe+70.0)
        base_teste.loc[indx,'ultima_vela'] = ultima_vela[0]['close']
        base_teste.loc[indx, 'vela_abertura'] = vela_abertura['open']

    base_teste.to_csv('Base_teste_estrategia.csv',index=False)


Teste_Estrategia_mercado_normal()


