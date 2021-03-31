import os,shutil,re,extract_msg

def folders_template(folders_path):
    os.chdir(folders_path)
    os.mkdir('1. FT - Pending')
    os.mkdir('2. PRI_SIMLock - Pending')
    os.mkdir('3. WDL - Pending')
    os.mkdir('4. FOTA - Pending')
    os.mkdir('5. Power - Pending')
    os.mkdir('6. TAG Compare_Model_Control - Pending')
    os.mkdir('7. Google CTS - Pending')
    os.mkdir('8. TD Defect Report - Pending')
    os.mkdir('9. Approval Letter - Pending')
    os.mkdir('10. Capability Information - Pending')
    os.mkdir('11. SUTEL - Pending')


def msg_in_folders(msg_path):
    os.chdir(msg_path)
    msg_list = os.listdir(msg_path)

    def folder_update(old_text, new_text, msg_subject):
        shutil.move(os.path.abspath(msg_subject), msg_path + old_text)
        os.rename(msg_path + old_text, msg_path + new_text)
        os.chdir(msg_path + new_text)
        CL = extract_msg.Message(msg_subject)
        for anexo in CL.attachments:
            xls_file = re.search('.*xls$', anexo.longFilename)
            xlsx_file = re.search('.*xlsx$', anexo.longFilename)
            xlsm_file = re.search('.*xlsm$', anexo.longFilename)
            if xls_file or xlsx_file or xlsm_file:
                anexo.save()
        CL.close()
        os.chdir(msg_path)

    for msg in msg_list:
        msg_capability = re.search('.*Capability.*msg$',msg)
        msg_fota = re.search('.*FOTA.*msg$', msg)
        msg_power = re.search('.*Power.*msg$', msg)
        msg_pri = re.search('.*PRI.*msg$', msg)
        msg_wdl = re.search('.*WDL.*msg$', msg)


        if msg_capability:
            old_text = r'\10. Capability Information - Pending'
            new_text = r'\10. Capability Information'
            msg_subject = msg_capability.group()
            folder_update(old_text, new_text, msg_subject)

        if msg_fota:
            old_text = r'\4. FOTA - Pending'
            new_text = r'\4. FOTA'
            msg_subject = msg_fota.group()
            folder_update(old_text, new_text, msg_subject)


        if msg_power:
            old_text = r'\5. Power - Pending'
            new_text = r'\5. Power'
            msg_subject = msg_power.group()
            folder_update(old_text, new_text, msg_subject)


        if msg_pri:
            old_text = r'\2. PRI_SIMLock - Pending'
            new_text = r'\2. PRI_SIMLock'
            msg_subject = msg_pri.group()
            folder_update(old_text, new_text, msg_subject)

        if msg_wdl:
            old_text = r'\3. WDL - Pending'
            new_text = r'\3. WDL'
            msg_subject = msg_wdl.group()
            folder_update(old_text, new_text, msg_subject)

def xls_in_folders(xls_path):
    os.chdir(xls_path)
    xls_list = os.listdir(xls_path)

    def file_in_folder(old_text, new_text, file_name, path):
        shutil.move(os.path.abspath(file_name), xls_path + old_text)
        os.rename(xls_path + old_text, xls_path + new_text)
        os.chdir(xls_path + new_text)
        os.chdir(path)

    for file in xls_list:
        capability = re.search('.*Capability.*xl.*',file)
        fota = re.search('.*FOTA.*xl.*', file)
        power = re.search('.*Power.*xl.*', file)
        pri = re.search('.*PRI.*xl.*', file)
        wdl = re.search('.*WDL.*xl.*', file)
        CTS = re.search('CTS.*png$|CTS.*PNG$', file)
        vTAG = re.search('vTAG.*png$|vTAG.*PNG$', file)
        TD = re.search('TD.*xlsx$', file)

        if TD:
            old_text = r'\8. TD Defect Report - Pending'
            new_text =  r'\8. TD Defect Report - OK'
            file_name = TD.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)


        if vTAG:
            old_text = r'\6. TAG Compare_Model_Control - Pending'
            new_text = r'\6. TAG Compare_Model_Control - OK'
            file_name = vTAG.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)

        if CTS:
            old_text = r'\7. Google CTS - Pending'
            new_text = r'\7. Google CTS - OK'
            file_name = CTS.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)

        if capability:
            old_text = r'\11. Capability Information - Pending'
            new_text = r'\11. Capability Information'
            file_name = capability.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)

        if fota:
            old_text = r'\4. FOTA - Pending'
            new_text = r'\4. FOTA'
            file_name = fota.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)

        if power:
            old_text = r'\5. Power - Pending'
            new_text = r'\5. Power'
            file_name = power.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)


        if pri:
            old_text = r'\2. PRI_SIMLock - Pending'
            new_text = r'\2. PRI_SIMLock'
            file_name = pri.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)


        if wdl:
            old_text = r'\3. WDL - Pending'
            new_text = r'\3. WDL'
            file_name = wdl.group()
            path = xls_path
            file_in_folder(old_text, new_text, file_name, path)


