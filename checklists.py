import xlrd,extract_info, re, revision,os


def pri_checklist_review(caminho, nome_checklist, dados_json, caminho_def):
    os.chdir(caminho)
    ok = ng = nt = na = oss = erro = 0
    excel = xlrd.open_workbook(nome_checklist)
    num_abas = excel.nsheets
    aba_principal = excel.sheet_by_index(0)
    aba_sim_lock = excel.sheet_by_index(num_abas - 3)
    versao_pri = aba_principal.cell_value(rowx=2, colx=2).strip()
    versao_sw_aba_principal = aba_principal.cell_value(rowx=3, colx=2)
    versao_sw_aba_simlock = aba_sim_lock.cell_value(rowx=9, colx=2)
    if str(versao_pri).find(dados_json['PDM']['GPRI']) == -1 and str(dados_json['PDM']['GPRI']).find(str(versao_pri)) == -1 :
        erro += 1
    if str(versao_sw_aba_principal).find(dados_json['PDM']['SW']) == -1:
        erro += 1
    if (dados_json['PDM']['Modelo'].find('CAO') == -1 and dados_json['PDM']['Modelo'].find('TGO') == -1) and str(versao_sw_aba_simlock).find(dados_json['PDM']['SW']) == -1:
        erro += 1
    for sheet in range(num_abas):
        used_sheet = excel.sheet_by_index(sheet)
        tot_cols = used_sheet.ncols
        tot_rows = used_sheet.nrows
        for col in range(tot_cols):
            for row in range(tot_rows):
                if used_sheet.cell_value(rowx=row, colx=col) == 'Pass' or used_sheet.cell_value(rowx=row, colx=col) =='Passed' or used_sheet.cell_value(rowx=row, colx=col) =='OK':
                    ok+=1
                if used_sheet.cell_value(rowx=row, colx=col) == 'Failed' or used_sheet.cell_value(rowx=row, colx=col) =='Fail' or used_sheet.cell_value(rowx=row, colx=col) =='NG':
                    ng+=1
                if used_sheet.cell_value(rowx=row, colx=col) == 'O/S':
                    oss+=1
                if used_sheet.cell_value(rowx=row, colx=col) == 'NT':
                    nt+=1
                if used_sheet.cell_value(rowx=row, colx=col) == 'NA':
                    na+=1
    dicionario = {'GPRI': versao_pri,
                  'SW': versao_sw_aba_principal,
                  'erro': erro,
                  'OK': ok,
                  'NG': ng,
                  'NT': nt,
                  'NA': na,
                  'O/S': oss,
                  }
    extract_info.append_json(caminho_def, nome_checklist, dicionario)
    revision.isgood(ng, caminho)
    """ Revisando auto SIM LOCK"""
    ok = ng = nt = erro = autosl =  0
    if (dados_json['PDM']['Modelo'].find('CAO') != -1 or dados_json['PDM']['Modelo'].find('TGO') != -1):
        os.chdir(caminho)
        pri_files = os.listdir()
        for file in pri_files:
            autosimlock = re.search('.*Auto SIM Lock.*xl.*',file)
            if autosimlock:
                autosl = 1
                nome_checklist = autosimlock.group()
                excel = xlrd.open_workbook(str(nome_checklist))
                num_abas = excel.nsheets
                aba_principal = excel.sheet_by_index(0)
                versao_sw_aba_principal = aba_principal.cell_value(rowx=7, colx=2)
                if str(versao_sw_aba_principal).find(dados_json['PDM']['SW']) == -1:
                    erro += 1
                for sheet in range(num_abas):
                    used_sheet = excel.sheet_by_index(sheet)
                    tot_cols = used_sheet.ncols
                    tot_rows = used_sheet.nrows
                    for col in range(tot_cols):
                        for row in range(4,tot_rows):
                            if used_sheet.cell_value(rowx=row, colx=col) == 'PASSED':
                                ok += 1
                            if used_sheet.cell_value(rowx=row, colx=col) == 'FAILED':
                                ng += 1
                            if used_sheet.cell_value(rowx=row, colx=col) == 'NOT TESTED':
                                nt += 1
                dicionario = {'SW': versao_sw_aba_principal,
                              'erro': erro,
                              'OK': ok,
                              'NG': ng,
                              'NT': nt,
                              }
                extract_info.append_json(caminho_def, nome_checklist, dicionario)
                break
        if autosl == 0:
            dicionario = {'NG':1}
            nome_checklist = "Missing Auto SIM Lock"
            extract_info.append_json(caminho_def, nome_checklist, dicionario)

def capability_checklist_review(caminho, nome_checklist, dados_json, caminho_def):
    os.chdir(caminho)
    erro = 0
    excel = xlrd.open_workbook(nome_checklist)
    aba_verificada = excel.sheet_by_index(2)
    versao_sw = aba_verificada.cell_value(rowx=9, colx=1)
    result = aba_verificada.cell_value(rowx=6, colx=1)
    if result == 'PASS':
        ng = 0
    else:
        ng = 1
    if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
        erro += 1
    dicionario = {
        'SW': versao_sw,
        'erro': erro,
        'NG': ng
    }
    extract_info.append_json(caminho_def, nome_checklist, dicionario)
    revision.isgood(ng, caminho)


def wdl_checklist_review(caminho, nome_checklist, dados_json, caminho_def):
    os.chdir(caminho)
    ok = ng = nt = na = erro = 0
    excel = xlrd.open_workbook(nome_checklist)
    num_abas = excel.nsheets
    for sheet in range(num_abas-1):
        aba_verificada = excel.sheet_by_index(sheet)
        tot_cols = aba_verificada.ncols
        tot_rows = aba_verificada.nrows
        if num_abas < 3:  # se tiver menos que 4 abas é WDL comm
            numero_rst = aba_verificada.cell_value(rowx=6, colx=1)
            versao_kdz = aba_verificada.cell_value(rowx=5, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw1 = 'NA'
            versao_sw2 = 'NA'
            if str(versao_kdz).find(dados_json['PDM']['WDL']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        elif (num_abas < 5):  # se tiver menos que 5 é o WDL normal
            numero_rst = aba_verificada.cell_value(rowx=8, colx=1)
            versao_kdz = aba_verificada.cell_value(rowx=5, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw1 = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw2 = 'NA'
            if str(versao_kdz).find(dados_json['PDM']['WDL']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        else:  # se não é o wdl +1 MR
            numero_rst = aba_verificada.cell_value(rowx=8, colx=1)
            versao_kdz = aba_verificada.cell_value(rowx=7, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=6, colx=1)
            versao_sw1 = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw2 = aba_verificada.cell_value(rowx=3, colx=1)
            if str(versao_kdz).find(dados_json['PDM']['WDL']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        for col in range(tot_cols):
            for row in range(16,tot_rows):
                if aba_verificada.cell_value(rowx=row, colx=col) =='OK':
                    ok+=1
                if aba_verificada.cell_value(rowx=row, colx=col) =='NG':
                    ng+=1
                if aba_verificada.cell_value(rowx=row, colx=col) == 'NOT TESTED':
                    nt+=1
                if aba_verificada.cell_value(rowx=row, colx=col) == 'NA':
                    na+=1
    dicionario = {'Previous_2': versao_sw2,
                  'Previous_1': versao_sw1,
                  'SW': versao_sw,
                  'WDL': versao_kdz,
                  'RST': numero_rst,
                  'OK': ok,
                  'NG': ng,
                  'NT': nt,
                  'NA': na,
                  'erro': erro
                  }
    extract_info.append_json(caminho_def, nome_checklist, dicionario)
    revision.isgood(ng, caminho)


def fota_checklist_review(caminho, nome_checklist, dados_json, caminho_def):
    os.chdir(caminho)
    ok = ng = nt = na = erro = 0
    excel = xlrd.open_workbook(nome_checklist)
    num_abas = excel.nsheets
    for sheet in range(num_abas-1):
        aba_verificada = excel.sheet_by_index(sheet)
        tot_cols = aba_verificada.ncols
        tot_rows = aba_verificada.nrows
        if num_abas < 3:  # se tiver menos que 3 abas é FOTA dummy
            numero_rst = aba_verificada.cell_value(rowx=7, colx=1)
            versao_up = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=3, colx=1)
            versao_sw1 = 'NA'
            versao_sw2 = 'NA'
            if str(versao_up).find(dados_json['PDM']['FOTA']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        elif (num_abas < 5):  # se tiver menos que 5 é o FOTA normal
            numero_rst = aba_verificada.cell_value(rowx=7, colx=1)
            versao_up = aba_verificada.cell_value(rowx=4, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=3, colx=1)
            versao_sw1 = aba_verificada.cell_value(rowx=2, colx=1)
            versao_sw2 = 'NA'
            if str(versao_up).find(dados_json['PDM']['FOTA']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        else:  # se não é o FOTA +1 MR
            numero_rst = aba_verificada.cell_value(rowx=7, colx=1)
            versao_up = aba_verificada.cell_value(rowx=6, colx=1)
            versao_sw = aba_verificada.cell_value(rowx=5, colx=1)
            versao_sw1 = aba_verificada.cell_value(rowx=3, colx=1)
            versao_sw2 = aba_verificada.cell_value(rowx=2, colx=1)
            if str(versao_up).find(dados_json['PDM']['FOTA']) == -1:
                erro += 1
            if str(versao_sw).find(dados_json['PDM']['SW']) == -1:
                erro += 1
            if str(numero_rst).find(dados_json['PDM']['RST']) == -1:
                erro += 1
        for col in range(tot_cols):
            for row in range(13, tot_rows):
                if aba_verificada.cell_value(rowx=row, colx=col) == 'OK':
                    ok += 1
                if aba_verificada.cell_value(rowx=row, colx=col) == 'NG':
                    ng += 1
                if aba_verificada.cell_value(rowx=row, colx=col) == 'NOT TESTED':
                    nt += 1
                if aba_verificada.cell_value(rowx=row, colx=col) == 'NA':
                    na += 1
    dicionario = {'Previous_2': versao_sw2,
                  'Previous_1': versao_sw1,
                  'SW': versao_sw,
                  'FOTA': versao_up,
                  'RST': numero_rst,
                  'OK': ok,
                  'NG': ng,
                  'NT': nt,
                  'NA': na,
                  'erro': erro
                  }
    extract_info.append_json(caminho_def, nome_checklist, dicionario)
    revision.isgood(ng, caminho)


def power_checklist_review(caminho, nome_checklist, dados_json, caminho_def):
    os.chdir(caminho)
    ok = ng = nt = na = erro = 0
    excel = xlrd.open_workbook(nome_checklist)
    aba_verificada = excel.sheet_by_index(0)
    versao_sw_previous = aba_verificada.cell_value(rowx=10, colx=1)
    versao_sw = aba_verificada.cell_value(rowx=5, colx=1)
    total_de_linhas = aba_verificada.nrows
    total_de_colunas = aba_verificada.ncols
    if str(versao_sw).find((dados_json['PDM']['SW'])) == -1:
        erro += 1
    for coluna in range(total_de_colunas):
        for linha in range(total_de_linhas):
            cel = aba_verificada.cell_value(rowx=linha, colx=coluna)
            achar_coluna_status = re.search("^Test Status$", str(cel))
            if (achar_coluna_status):
                coluna_de_status = aba_verificada.col(coluna)
                for linha in range(len(coluna_de_status)):
                    celula_verificada = aba_verificada.cell_value(rowx=linha, colx=coluna)
                    if celula_verificada == 'OK':
                        ok += 1
                    if celula_verificada == 'NG':
                        ng += 1
                    if celula_verificada == 'NOT TESTED':
                        nt += 1
                    if celula_verificada == 'NA':
                        na += 1
    dicionario = {
        'Previous': versao_sw_previous,
        'SW': versao_sw,
        'OK': ok,
        'NG': ng,
        'NT': nt,
        'NA': na,
        'erro': erro
    }

    extract_info.append_json(caminho_def, nome_checklist, dicionario)
    revision.isgood(ng, caminho)
