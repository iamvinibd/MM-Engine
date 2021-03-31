import os,json,re,extract_msg,email

def tmp_folder(caminho):
    os.chdir(caminho) # Muda para caminho especificado
    os.mkdir('_tmp_') # cria pasta tmp nesse caminho

def data_json(caminho):
    os.chdir(caminho+'\_tmp_') # Entra na pasta tmp
    dados_json = open('dados.json','w') # cria um arquivo chamado "dados.json"
    dados_json.write('{}') # escreve nesse arquivo {}
    dados_json.close() # fecha arquivo

def append_json(caminho,nome_teste,dicionario):
    os.chdir(caminho+'\_tmp_') # entra na pasta tmp
    dados_json = open('dados.json','r') # abre o arquivo json em modo de leitura
    cl_json_string = dados_json.read() # le o conteudo do arquivo e passa para variável
    dados_json.close() # fecha o arquivo
    cl_json_parseado = json.loads(cl_json_string) # a partir do conteudo lido no arquivo json que estava em formato string, o load é utilizado para poder parsear o conteudo
    cl_json_parseado[nome_teste] = dicionario # insiro uma nova chave "nome_teste", e coloco dentro dessa chave o conteudo do dicionário
    dump = json.dumps(cl_json_parseado,indent = 4) # faço a identação do conteudo, para melhorar a aparencia no arquivo
    dados_json = open('dados.json','w') # abro o arquivo em modo de escrita
    dados_json.write(dump) # escrevo no arquivo o conteudo ja identado
    dados_json.close()# fecho o arquivo
    os.chdir(caminho)# volto para o caminho principal

def collect_json(caminho):
    os.chdir(caminho+'\_tmp_') # entro na pasta tmp
    dados_json = open('dados.json','r') # abro o arquivo json em modo leitura
    cl_json_string = dados_json.read()# leio o conteudo e passo para a variavel
    dados_json.close() # fecho o arquivo
    cl_json_parseado = json.loads(cl_json_string)# parseio a string para tranformala em formato json
    return cl_json_parseado # retorno o json

def pdm(caminho):
    smtca = 0
    arquivopdm = 0
    os.chdir(caminho) # entro no caminho especificado
    lista = os.listdir(caminho) # listo o conteudo desse diretorio
    for x in lista: # para cada arquivo 'x' na lista
        arquivo_pdm = re.search('.*RST.htm.*', x) # procuro no nome desse arquivo a palavra RST q possua um final htm
        if arquivo_pdm : # se eu achar esse arquivo
            arquivopdm = 1
            conteudo_pdm = open(arquivo_pdm.group(), 'r', encoding='Latin-1').read() # abro o arquivo no modo leitura, leio o conteudo e o passo para a variavel
            #print(conteudo_pdm)
            RST = re.search("RST-([0-9]{4})-[0-9]{5}", conteudo_pdm)# procura dentro do arquivo, o RST
            SW = re.search(
                "SWV\s*:\s*(L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)AT\-([0-9]{2})\-(V(([0-9]{2})[a-z]))\-([a-zA-Z0-9]+\-[a-zA-Z0-9]+)\-([A-Z]{3}\-[0-9]{2}\-([0-9]{4}))\+([0-9]+))\s*",
                conteudo_pdm)# Procuro o SWV dentro do arquivo
            SWOV = re.search(
                "SWOV\s*:\s*(L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)AT\-([0-9]{2})\-(V(([0-9]{2})[a-z]))\-([a-zA-Z0-9]+\-[a-zA-Z0-9]+)\-([A-Z]{3}\-[0-9]{2}\-([0-9]{4}))\+([0-9]+))\s*",
                conteudo_pdm) # Procuro o SWOV no conteudo
            SWFV = re.search("SWFV\s*:\s*([^\s<]+)\s*", conteudo_pdm) # Procuro o SWFV
            FP = re.search("lge.*keys", conteudo_pdm) # Procuro o fingerprint
            GPRI = re.search(
                "GPRI\s+Package\s*:\s*([^\s<]+)\s*([^\s<]+)|SmartCA\s*:\s*([^\s<]+\s*[^\s<]+\s*[^\s<]+)\s*",
                conteudo_pdm) # Procurando GPRI no conteudo
            GPRI_BASE = re.search(
                "Base\s*:\s*([^\s<]+)\s*([^\s<]+)\s*([^\s<]+)\s*(\s*([^\s<]+)\s*){3}",
                conteudo_pdm) # Procurando GPRI no conteudo
            FOTA = re.search(
                "(([a-zA-Z][0-9]+[a-zA-Z]*)(?:_(?:(dummy_pkg)|([0-9A-Z]{3})))(?:_(?:(V[0-9]{2}[a-zA-Z])_([0-9]{2})_([0-9]{4})\-(V[0-9]{2}[a-zA-Z])_([0-9]{2})_([0-9]{4})|(NOOSUPGRADE|NOMR)))?(_OSUPGRADE)?\.up)",
                conteudo_pdm) # Procurando FOTA no documento
            WDL = re.search(
                "((([a-zA-Z][0-9]+)[a-zA-Z]*)(([0-9]{2})[a-z])_([0-9]{2})_(?:([_A-Z]*)_OP_)?([0-9]{4})\.kdz)|((([a-zA-Z][0-9]+)[a-zA-Z]*)(([0-9]{2})[a-z])_([0-9]{2})).*kdz",
                conteudo_pdm)# Procurando WDL no conteudo
            MODEL = re.search("L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)\.[A-Z]([0-9A-Z]{5})", conteudo_pdm) #Procurando model.suffix no conteudo
            sas = re.search("sas.lge.com([^\s<]+)\s*", conteudo_pdm) # Procurando o SAS
            pr_number = re.search('PR\s+Number\s*:\s*([^\s<]+)\s*', conteudo_pdm) # Procurando PR
            hq_v_tag = re.search("HQ\s+Verified\s+.+?\s*:\s*([^\s<]+)?.xml\s*", conteudo_pdm) # Procurando hq_v_tag
            lgesp_tag = re.search("LGESP\s+Release\s+.+?\s*:\s*([^\s<]+)?.xml\s*", conteudo_pdm) # Procurando local tag
            spl = re.search("Google\s+Security\s+Patch\s+Level\s*:\s*([^\s<]+)\s*", conteudo_pdm) # Procurando SPL
    if arquivopdm == 1:
        if SW: # se eu achar o SW
            SW = SW.group().split() # Separo o SWV : L....
            SW = SW[len(SW) - 1] # Pega o ultimo item da lista
        if SWOV:# se eu achar o SWOV
            SWOV = SWOV.group().split()# Separo o SWOV : L....
            SWOV = SWOV[len(SWOV) - 1] # Pega o ultimo item da lista
        if SWFV:# se eu achar o SWFV
            SWFV = SWFV.group().split()# Separo o SWFV : L....
            SWFV = SWFV[len(SWFV) - 1]# Pega o ultimo item da lista
        if GPRI:# Se eu achar a PRI
            if GPRI.group().find("AVISO") != -1: #Se a PRI for da claro (Contem AVISO)
                GPRI = GPRI.group().split(":") #
                GPRI = GPRI[len(GPRI) - 1].replace("\n", "").strip()
                GPRI = re.sub(' +',' ',GPRI)
            else:
                GPRI = GPRI.group().split(':')
                GPRI = GPRI[len(GPRI) - 1].replace("\n", "").strip()
                GPRI = re.sub(' +', ' ', GPRI)
        else:
            GPRI = 'NF'
        if RST:
            RST = RST.group()
        if FP:
            FP = FP.group()
        if FOTA:
            FOTA = FOTA.group()
        if WDL:
            WDL = WDL.group()

        if MODEL:
            MODEL = MODEL.group()
        if sas:
            sas = sas.group()
        if pr_number:
            pr_number = pr_number.group().split()
            pr_number = pr_number[len(pr_number)-1]
        if lgesp_tag:
            lgesp_tag = lgesp_tag.group().split()
            lgesp_tag =lgesp_tag[len(lgesp_tag)-1]
        if hq_v_tag:
            hq_v_tag = hq_v_tag.group().split()
            hq_v_tag = hq_v_tag[len(hq_v_tag)-1]
        else:
            smtCA_tag = re.findall('Tag\s*:\s*([^\s<]+)?.xml\s*',conteudo_pdm)
            hq_v_tag = smtCA_tag[0]
            lgesp_tag = smtCA_tag[1]
        if spl:
            spl = spl.group().replace("\n", "").strip()
            spl = re.sub(' +', ' ', spl)
        if GPRI_BASE:# Se eu achar a PRI
            smtca = 1
            GPRI_BASE = GPRI_BASE.group().split(":")
            GPRI_BASE = GPRI_BASE[len(GPRI_BASE)-1].strip()
        if smtca == 0:
            GPRI_BASE = ""


        cont_parse = {
            'RST': RST,
            'SW': SW,
            'SWOV': SWOV,
            'SWFV': SWFV,
            'Fingerprint': FP,
            'GPRI': GPRI,
            'GPRI_BASE': GPRI_BASE,
            'FOTA': FOTA,
            'WDL': WDL,
            'Modelo': MODEL,
            'SAS': sas,
            'PR':pr_number,
            'vTAG':hq_v_tag,
            'LG_SP_TAG':lgesp_tag,
            "spl": spl
        }
        append_json(caminho, 'PDM', cont_parse)

def pdm_msg(caminho):
    smtca = 0
    arquivomsg = 0
    os.chdir(caminho) # entro no caminho especificado
    lista = os.listdir(caminho) # listo o conteudo desse diretorio
    for x in lista: # para cada arquivo 'x' na lista
        arquivo_msg = re.search('.*GPDM.*',x)
        if arquivo_msg:
            arquivomsg = 1
            f = arquivo_msg.group()
            #msg_eml = email.message_from_file(open(f,'r', encoding='Latin-1'))
            #print(msg_eml)
            msg = extract_msg.Message(f)
            msg_message = msg.body
            conteudo_pdm = msg_message
            #print(conteudo_pdm)
            RST = re.search("RST-([0-9]{4})-[0-9]{5}", conteudo_pdm)# procura dentro do arquivo, o RST
            SW = re.search(
                "SWV\s*:\s*(L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)AT\-([0-9]{2})\-(V(([0-9]{2})[a-z]))\-([a-zA-Z0-9]+\-[a-zA-Z0-9]+)\-([A-Z]{3}\-[0-9]{2}\-([0-9]{4}))\+([0-9]+))\s*",
                conteudo_pdm)# Procuro o SWV dentro do arquivo
            SWOV = re.search(
                "SWOV\s*:\s*(L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)AT\-([0-9]{2})\-(V(([0-9]{2})[a-z]))\-([a-zA-Z0-9]+\-[a-zA-Z0-9]+)\-([A-Z]{3}\-[0-9]{2}\-([0-9]{4}))\+([0-9]+))\s*",
                conteudo_pdm) # Procuro o SWOV no conteudo
            SWFV = re.search("SWFV\s*:\s*([^\s<]+)\s*", conteudo_pdm) # Procuro o SWFV
            FP = re.search("lge.*keys|lge\s*([^\s<]+)\s*\s*([^\s<]+)\s*keys", conteudo_pdm) # Procuro o fingerprint
            GPRI = re.search(
                "GPRI\s+Package\s*:\s*([^\s<]+)\s([^\s<]+)\s*|SmartCA\s*:\s*([^\s<]+)\s*([^\s<]+)\s*([^\s<]+)\s*|GPRI\s+Package\s*:\s*([^\s<]+)\s*",
                conteudo_pdm) # Procurando GPRI no conteudo
            GPRI_BASE = re.search(
                "Base\s*:\s*([^\s<]+)\s*([^\s<]+)\s*([^\s<]+)\s*(\s*([^\s<]+)\s*){3}",
                conteudo_pdm) # Procurando GPRI no conteudo
            FOTA = re.search(
                "(([a-zA-Z][0-9]+[a-zA-Z]*)(?:_(?:(dummy_pkg)|([0-9A-Z]{3})))(?:_(?:(V[0-9]{2}[a-zA-Z])_([0-9]{2})_([0-9]{4})\-(V[0-9]{2}[a-zA-Z])_([0-9]{2})_([0-9]{4})|(NOOSUPGRADE|NOMR)))?(_OSUPGRADE)?\.up)",
                conteudo_pdm) # Procurando FOTA no documento
            WDL = re.search(
                "((([a-zA-Z][0-9]+)[a-zA-Z]*)(([0-9]{2})[a-z])_([0-9]{2})_(?:([_A-Z]*)_OP_)?([0-9]{4})\.kdz)|((([a-zA-Z][0-9]+)[a-zA-Z]*)(([0-9]{2})[a-z])_([0-9]{2})).*kdz",
                conteudo_pdm)# Procurando WDL no conteudo
            MODEL = re.search("L[A-Z](([a-zA-Z][0-9]+)[a-zA-Z]*)\.[A-Z]([0-9A-Z]{5})", conteudo_pdm) #Procurando model.suffix no conteudo
            sas = re.search("sas.lge.com([^\s<]+)", conteudo_pdm) # Procurando o SAS
            pr_number = re.search('PR\s+Number\s*:\s*([^\s<]+)\s*', conteudo_pdm) # Procurando PR
            hq_v_tag = re.search("HQ\s+Verified\s+.+?\s*:\s*([^\s<]+)?.xml\s*", conteudo_pdm) # Procurando hq_v_tag
            lgesp_tag = re.search("LGESP\s+Release\s+.+?\s*:\s*([^\s<]+)?.xml\s*", conteudo_pdm) # Procurando local tag
            spl = re.search("Google\s+Security\s+Patch\s+Level\s*:\s*([^\s<]+)\s*", conteudo_pdm) # Procurando SPL
    if arquivomsg ==1:
        if SW: # se eu achar o SW
            SW = SW.group().split() # Separo o SWV : L....
            SW = SW[len(SW) - 1] # Pega o ultimo item da lista
        if SWOV:# se eu achar o SWOV
            SWOV = SWOV.group().split()# Separo o SWOV : L....
            SWOV = SWOV[len(SWOV) - 1] # Pega o ultimo item da lista
        if SWFV:# se eu achar o SWFV
            SWFV = SWFV.group().split()# Separo o SWFV : L....
            SWFV = SWFV[len(SWFV) - 1]# Pega o ultimo item da lista
        if GPRI:# Se eu achar a PRI
            #print(GPRI.group())
            if GPRI.group().find("AVISO") != -1: #Se a PRI for da claro (Contem AVISO)
                GPRI = GPRI.group().split(":") #
                GPRI = GPRI[len(GPRI) - 1].replace("\n", "").strip()
                GPRI = re.sub(' +',' ',GPRI)
            else:
                GPRI = GPRI.group().split(':')
                GPRI = GPRI[len(GPRI) - 1].replace("\n", "").strip()
                GPRI = re.sub(' +', ' ', GPRI)


        if RST:
            RST = RST.group()
        if FP:
            print(FP.group().replace("\r\n",""))
            FP = FP.group().replace("\r\n","")
        if FOTA:
            FOTA = FOTA.group()
        if WDL:
            WDL = WDL.group()

        if MODEL:
            MODEL = MODEL.group()
        if sas:
            sas = sas.group()
            #print(sas)
        if pr_number:
            pr_number = pr_number.group().split()
            pr_number = pr_number[len(pr_number)-1]
        if lgesp_tag:
            lgesp_tag = lgesp_tag.group().split()
            lgesp_tag =lgesp_tag[len(lgesp_tag)-1]
        if hq_v_tag:
            hq_v_tag = hq_v_tag.group().split()
            hq_v_tag = hq_v_tag[len(hq_v_tag)-1]
        else:
            smtCA_tag = re.findall('Tag\s*:\s*([^\s<]+)?.xml\s*',conteudo_pdm)
            hq_v_tag = smtCA_tag[0]
            lgesp_tag = smtCA_tag[1]
        if spl:
            spl = spl.group().replace("\n", "").strip()
            spl = re.sub(' +', ' ', spl)
        if GPRI_BASE:# Se eu achar a PRI
            smtca = 1
            GPRI_BASE = GPRI_BASE.group().split(":")
            GPRI_BASE = GPRI_BASE[len(GPRI_BASE)-1].strip()
            print(GPRI_BASE)
        if smtca == 0:
            GPRI_BASE = ""


        cont_parse = {
            'RST': RST,
            'SW': SW,
            'SWOV': SWOV,
            'SWFV': SWFV,
            'Fingerprint': FP,
            'GPRI': GPRI,
            'GPRI_BASE': GPRI_BASE,
            'FOTA': FOTA,
            'WDL': WDL,
            'Modelo': MODEL,
            'SAS': sas,
            'PR':pr_number,
            'vTAG':hq_v_tag,
            'LG_SP_TAG':lgesp_tag,
            "spl": spl
        }
        append_json(caminho, 'PDM', cont_parse)


#pdm_msg(r'D:\backup\BrisaMails\temp FTP\K420\CAO\MR1')