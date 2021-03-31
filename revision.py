import os,re,checklists


def isgood(ng,caminho):
    try:
        jafoi = re.search('.*OK.*',caminho)
        if jafoi:
            pass
        else:
            if ng == 0:
                os.rename(caminho, caminho + ' - OK')
            else:
                os.rename(caminho, caminho + ' - NOK')
    except Exception as e:
        print(e)
        pass


def pastas(caminho):
    '''Procura as pastas dos testes checklists e FT e retorna
    uma lista com os caminhos absolutos.'''
    os.chdir(caminho)
    caminho_absoluto = []
    lista_de_pastas =os.listdir(caminho)
    for pastas in lista_de_pastas:
        pasta = re.search('.*PRI.*|.*FOTA.*|.*WDL.*|.*Power.*|.*Capability.*|.*FT.*',pastas)
        if pasta:
            caminho_absoluto.append(os.path.abspath(pasta.group()))
    return caminho_absoluto

def sub_pastas(caminhos_abs,dict):
    '''Acessar pastas e sub pastas, montando um dicionario do caminho+nome_checklist'''
    caminhos_abs = caminhos_abs
    sub_caminho=[]
    dict = dict
    list = []
    for x in caminhos_abs:

        if os.path.exists(x)==True:
            try:
                os.listdir(x)
                os.chdir(x)
            except:
                break
            for y in os.listdir(x):
                tipo = os.path.isfile(y)
                excel = re.search('.*XL.*',y.upper())
                if excel:
                    if x in dict and y not in dict[x]:
                        list.append(dict[x])
                        list.append(y)
                        dict[x]=list
                    else:
                        dict[x]=y
                if tipo == False:
                    sub_caminho.append(os.path.abspath(y))
    try:
        sub_pastas(sub_caminho,dict)
    except RecursionError:
        pass
    finally:
        return dict

def testes(caminho,checklist,data,caminho_def):
    capability = re.search('.*Capability Information CL.*xls.',str(checklist))
    pri = re.search('.*PRI_SIM_Lock.*xls.', str(checklist))
    wdl = re.search('.*WDL.*xls$', str(checklist))
    fota = re.search('.*FOTA.*xls$', str(checklist))
    power = re.search('.*Power.*xls', str(checklist))

    if pri:
        checklists.pri_checklist_review(caminho,checklist,data,caminho_def)
    if capability:
        checklists.capability_checklist_review(caminho,checklist,data,caminho_def)
    if wdl:
        checklists.wdl_checklist_review(caminho,checklist,data,caminho_def)
    if fota:
        checklists.fota_checklist_review(caminho,checklist,data,caminho_def)
    if power:
        checklists.power_checklist_review(caminho,checklist,data,caminho_def)


def test_select(dict,data,caminho_def):
    dict=dict
    for key,value in (dict.items()):
        if isinstance(value,list):
            for value_list in value:

                testes(key,value_list,data,caminho_def)
        else:
            testes(key, value,data,caminho_def)

