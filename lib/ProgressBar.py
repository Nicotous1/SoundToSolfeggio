from __future__ import division
import Tkinter
import ttk
from threading import Thread
from time import sleep


class ProgressBar(Thread):

    def __init__(self, title="Analyse du fichier"):
        #self.progress = 0
        #return

        Thread.__init__(self)
        self.fenetre = None
        self.name = title
        self.widget = None

        self.daemon = True                            # Daemonize thread
        self.alive = False                            # Start the execution
        self.make_focus = True

    def create(self):
        #return self
        self.start()
        return self

    def run(self):
        #return self
        fenetre = Tkinter.Tk()
        fenetre.wm_title(self.name)
        fenetre.protocol("WM_DELETE_WINDOW", self.close)
        fenetre.geometry('500x50+50+50')
        fenetre.resizable(width=False, height=False)

        ft = Tkinter.Frame()

        ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

        self.widget = ttk.Progressbar(ft, orient='horizontal', mode='determinate')

        self.root = ft
        self.widget.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
        self.fenetre = fenetre
        self.alive = True

        while self.alive:
            self.widget["value"] = self.progress
            self.fenetre.wm_title(self.name + " (" +  str(int(self.progress)) + "%)")
            self.fenetre.update()
            if (self.make_focus): self.fenetre.focus_set()
            sleep(0.01)

        self.fenetre.destroy()
        return self

    def close(self):
        #return self
        self.alive = False
        return self

    def set(self, progress):
        if (progress >= 1):
            self.close()
        else:
            self.progress = progress * 100
            #print str(self.progress) + "%"
            self.focus()
        return self

    def focus(self):
        self.make_focus = True
        return self