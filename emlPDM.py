import email,os

from email import policy
from email import message_from_string

import glob

def extractPDM(filename):
    with open(filename, "r") as f:
        oi = message_from_string(f.read())
        msg = email.message_from_file(f, policy=policy.default)

        print(oi)
print('oi')
os.chdir(r'D:\backup\BrisaMails\temp FTP\K420\TFS\11. SUTEL - Pending')
extractPDM('[GPDM MC  Request] RST-2007-00689_LM-K420HM_TFS_QP requested to tester._20210318_2151.eml')