import os, organizeFiles, extract_info,revision, report, project, emlExtracter
from tkinter import *

rootpath = os.getcwd()
class MainWindow():

    def __init__(self,master=None):

        self.frame = Frame(master)
        self.frame.grid()

        self.lbl_rst_path = Label(self.frame, text="RST Path")
        self.lbl_rst_path.grid(column=0, row=1)

        self.ipt_rst_path = Entry(self.frame, width=40)
        self.ipt_rst_path.grid(column=1, row=1)

        self.lbl_engine_status = Label(self.frame, text="", wraplength=200)
        self.lbl_engine_status.grid(column=1, row=3)

        self.btn_verify = Button(self.frame, text="Verify", command=self.verify)
        self.btn_verify.grid(column=0, row=4, padx=5, sticky=W + E + N + S)

        self.btn_organize = Button(self.frame, text="Organize", command=self.organize)
        self.btn_organize.grid(column=0, row=5, padx=5, sticky=W + E + N + S)

        self.btn_folders = Button(self.frame, text="Folders", command=self.folders)
        self.btn_folders.grid(column=0, row=6, padx=5, sticky=W + E + N + S)

        self.btn_beagle = Button(self.frame, text="Beagle", command=self.beagle)
        self.btn_beagle.grid(column=0, row=7, padx=5, sticky=W + E + N + S)


        #self.btn_plus = Button(self.frame, text="+", command=self.plus, font ="-weight bold -size 9")
        #self.btn_plus.grid(column=3, row=1, padx=2, sticky=N + S)




    """def plus(self):
        self.plus = 0
        if self.btn_plus['text'] == '-':
            self.lbl_previous.grid_remove()
            self.ipt_previous.grid_remove()
            self.btn_plus['text'] = '+'
            self.plus=1
            self.btn_plus.update()
        if self.plus == 0 and self.btn_plus['text'] == '+':

            self.lbl_previous = Label(self.frame, text="Previous", font="-weight bold")
            self.lbl_previous.grid(column=0, row=2)
            self.ipt_previous = Entry(self.frame, width=40)
            self.ipt_previous.grid(column=1, row=2)
            self.btn_plus['text'] = '-'
            self.btn_plus['font'] = "-weight bold -size 9"
            self.btn_plus.update()"""


    def path_is_true(self):
        """Função que valida a existencia do caminho, e retorna resposta na label + variável Y/N """
        if os.path.exists(self.ipt_rst_path.get()) == True:
            self.lbl_engine_status['text'] = 'Valid Directory !'
            self.lbl_engine_status['fg'] = 'GREEN'
            path_exists = 'Y'
        else:
            self.lbl_engine_status['text'] = 'Invalid Directory !'
            self.lbl_engine_status['fg'] = 'RED'
            path_exists = 'N'

        return path_exists

    def default_status(self):
        self.lbl_engine_status['text'] = ''
        self.lbl_engine_status['fg'] = 'BLACK'
        self.lbl_engine_status['bg'] = 'SystemButtonFace'
        self.lbl_engine_status.update()

    def folders(self):
        self.default_status()
        if self.path_is_true() == 'Y':
            try:
                folders_path = self.ipt_rst_path.get()
                organizeFiles.folders_template(folders_path)
                self.lbl_engine_status['text'] = 'Created !'
                self.lbl_engine_status['fg'] = 'GREEN'
            except Exception as e:
                self.lbl_engine_status['text'] = 'Folders exception: '+str(e)
                self.lbl_engine_status['fg'] = 'RED'
        os.chdir(rootpath)
    def organize(self):
        self.default_status()
        if self.path_is_true() == 'Y':
            organized_path = self.ipt_rst_path.get()
            try:
                organizeFiles.xls_in_folders(organized_path)
                #organizeFiles.msg_in_folders(organized_path)
                emlExtracter.msg_in_folders(organized_path)
                self.lbl_engine_status['text'] = 'Organized !'
                self.lbl_engine_status['fg'] = 'GREEN'
            except Exception as e:
                self.lbl_engine_status['text'] = 'Organize exception: '+str(e)
                self.lbl_engine_status['fg'] = 'RED'
        os.chdir(rootpath)


    def verify(self):
        self.default_status()
        if self.path_is_true() == 'Y':
            rst_path = self.ipt_rst_path.get()
            """Tenta criar pasta _tmp """
            try:
                extract_info.tmp_folder(rst_path)
                """Caso a pasta ja exista cria arquivo 'dados.json' neste diretorio, isso apaga o anterior"""
            except FileExistsError:
                extract_info.data_json(rst_path)
            else:
                extract_info.data_json(rst_path)
            try:
                extract_info.pdm(rst_path)
                extract_info.pdm_msg(rst_path)
                data = extract_info.collect_json(rst_path)
                revision.test_select(revision.sub_pastas(revision.pastas(rst_path), dict={}), data,rst_path)
                self.lbl_engine_status['text'] = 'Verified!'
                self.lbl_engine_status['fg'] = 'GREEN'
                self.lbl_engine_status.update()
                os.chdir(rst_path)
                repor = report.Report()
                repor.mainloop()
            except Exception as e:
                self.lbl_engine_status['text'] = 'Verify exception: '+str(e)
                self.lbl_engine_status['fg'] = 'RED'
                self.lbl_engine_status.update()
        os.chdir(rootpath)

    def beagle(self):
        os.chdir(rootpath)
        self.default_status()
        rst_path = self.ipt_rst_path.get()
        if self.path_is_true() == 'Y':
            """Tenta criar pasta _tmp """
            try:
                extract_info.tmp_folder(rst_path)
                """Caso a pasta ja exista cria arquivo 'dados.json' neste diretorio, isso apaga o anterior"""
            except FileExistsError:
                extract_info.data_json(rst_path)
            else:
                extract_info.data_json(rst_path)
            try:
                extract_info.pdm(rst_path)
                extract_info.pdm_msg(rst_path)
                data = extract_info.collect_json(rst_path)
                status = project.beagle(data,rootpath)
                self.lbl_engine_status['text'] = 'Beagle: ' + str(status)
                if status == 'Done':
                    self.lbl_engine_status['fg'] = 'GREEN'
                else:
                    self.lbl_engine_status['fg'] = 'RED'
                self.lbl_engine_status.update()
                #os.chdir(rst_path)
            except FileExistsError:
                extract_info.data_json(rst_path)
                self.lbl_engine_status['text'] = 'Stopped !'
                self.lbl_engine_status['fg'] = 'RED'
            else:
                extract_info.data_json(rst_path)





root=Tk()
root.maxsize(360,220)
root.minsize(360,220)
root.geometry('360x220')
root.title("MM Engine")
root.iconbitmap(os.getcwd()+'\lg_2V1_icon.ico')

MainWindow(root)
root.mainloop()