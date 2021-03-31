import extract_info, os,pyautogui

from tkinter import *


class Report(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.container = Frame(self)
        self.canvas = Canvas(self.container)
        self.scrollbar = Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.container.grid()
        self.canvas.grid(sticky='wnse')
        self.scrollbar.grid(sticky='wnse')

        heads = ['Origem\t\n', 'NG\t\n','ERROS\t\n', 'RST\t\n', 'SW\t\n', 'GPRI\t\n', 'WDL\t\n', 'FOTA\t\n']
        itens = ['teste', 'NG', 'erro', 'RST', 'SW', 'GPRI', 'WDL', 'FOTA']
        dados = extract_info.collect_json(os.getcwd())

        self.title('Fast Report')
        width, height = pyautogui.size()
        #self.geometry(str(width)+"x"+str(height))
        '''Define os cabeçalhos do report'''
        linha = 1
        coluna = 0
        for head in heads:
            self.head = Label(self.scrollable_frame, text=head, font="Verdana 12 bold")  # ,borderwidth=2,relief='solid')
            self.head.grid(row=0, column=coluna, sticky=W)
            coluna += 1
        coluna -= coluna

        for key in dados.keys():
            for item in itens:
                if item in itens:
                    try:
                        self.a = Label(self.scrollable_frame, text=str(key) + '\t\n', font="Verdana 10 bold", wraplength=600)
                        self.a.grid(column=0, row=linha, sticky=W)
                        if str(dados[key][item]).isnumeric() and int(dados[key][item]) > 0:
                            self.b = Label(self.scrollable_frame, text=str(dados[key][item]) + '\t\n', font='bold', bd=2, relief='ridge',
                                           wraplength=600)  # ,borderwidth=2,relief='solid')
                            self.b['fg'] = 'RED'
                            self.b.grid(column=itens.index(item), row=linha, sticky=W)

                        else:
                            self.b = Label(self.scrollable_frame, text=str(dados[key][item]) + '\t\n',
                                           wraplength=600)  # ,borderwidth=2,relief='solid')
                            self.b['fg'] = 'BLACK'
                            self.b.grid(column=itens.index(item), row=linha, sticky=W)
                        if str(dados['PDM'][item]).find(dados[key][item]) != -1 or str(dados[key][item]).find(
                                dados['PDM'][item]) != -1:
                            self.b['fg'] = 'GREEN'
                        else:
                            self.b['fg'] = 'RED'





                    except:
                        pass

            linha += 1
        self.canvas.config(width=width, height=height/1.5)
        #self.minsize(width, 600)
        #self.maxsize(width, 600)
        print(height/1.5)
    def quit_(self):
        Report.quit(self)
        self.destroy()
