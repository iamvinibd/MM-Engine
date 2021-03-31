import pyautogui,time

def beagle(data,rootpath):

    def tab(qtdd):
        i= 0
        while i !=qtdd:
            pyautogui.press('\t')
            i+=1
    width, height = pyautogui.size()
    try:
        start = pyautogui.locateCenterOnScreen(rootpath+'\start.png', grayscale=True)
        pyautogui.click(start[0], start[1])
        if start != None:
             
             #pyautogui.click(width/2,height/2.45)
             pyautogui.typewrite(data['PDM']['SW'])
             time.sleep(0.5)
             tab(3)
             pyautogui.typewrite(data['PDM']['SWOV'])
             time.sleep(0.5)
             tab(6)
             pyautogui.typewrite(data['PDM']['Fingerprint'])
             time.sleep(0.5)
             tab(7)
             pyautogui.typewrite(data['PDM']['SWFV'])
             time.sleep(0.5)
             tab(8)
             pyautogui.typewrite(data['PDM']['LG_SP_TAG'])
             time.sleep(0.5)
             tab(9)
             pyautogui.typewrite(data['PDM']['vTAG'])
             time.sleep(0.5)
             tab(1)
             pyautogui.typewrite(data['PDM']['SAS'])
             time.sleep(0.5)
             tab(12)
             pyautogui.typewrite(data['PDM']['Modelo'] + '\n' + data['PDM']['spl'])
             time.sleep(0.5)
             tab(3)
             pyautogui.typewrite(data['PDM']['PR'])
             time.sleep(0.5)
             tab(16)
             pyautogui.typewrite(data['PDM']['WDL'])
             time.sleep(0.5)
             tab(17)
             pyautogui.typewrite(data['PDM']['FOTA'])
             time.sleep(0.5)
             tab(18)
             pyautogui.typewrite(data['PDM']['RST'])
             time.sleep(0.5)
             tab(19)
             pyautogui.typewrite(data['PDM']['GPRI'])
             time.sleep(0.5)
             tab(20)
             pyautogui.typewrite(data['PDM']['GPRI_BASE'])
             time.sleep(0.5)
             return 'Done'
    except Exception as e:
        return e
