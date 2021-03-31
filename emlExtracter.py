import email
from email import policy
import os,shutil,re

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
        extract(msg_subject)
        os.chdir(msg_path)

    for msg in msg_list:
        msg_capability = re.search('.*Capability.*eml$',msg)
        msg_fota = re.search('.*FOTA.*eml$', msg)
        msg_power = re.search('.*Power.*eml$', msg)
        msg_pri = re.search('.*PRI.*eml$', msg)
        msg_wdl = re.search('.*WDL.*eml$', msg)


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


def extract(filename):
    """
    Try to extract the attachments from all files in cwd
    """
    # ensure that an output dir exists
    output_count = 0
    try:
        with open(filename, "r") as f:
            msg = email.message_from_file(f, policy=policy.default)
            for attachment in msg.iter_attachments():
                output_filename = attachment.get_filename()
                # If no attachments are found, skip this file
                if output_filename:
                    xls_file = re.search('.*xls$', output_filename)
                    xlsx_file = re.search('.*xlsx$', output_filename)
                    xlsm_file = re.search('.*xlsm$', output_filename)
                    if xls_file or xlsx_file or xlsm_file:
                        print(output_filename)
                        with open(output_filename, "wb") as of:
                            of.write(attachment.get_payload(decode=True))
                            output_count += 1
            if output_count == 0:
                print("No attachment found for file %s!" % f.name)
    # this should catch read and write errors
    except IOError:
        print("Problem with %s or one of its attachments!" % f.name)
    return 1, output_count

