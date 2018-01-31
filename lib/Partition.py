from lib.File import File
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np

class Partition:

#
#   FONCTION D'INITIALISATION
#

    def __init__(self,link):
        self.link = link

        #TRAITEMENT PRELIMINAIRE
        self.file = File(link)
        self.file.cut_low_sound()

        self.notes = []
        for e in self.file:
            self.notes.append(e.getNote())

        #Variable Boot
        self.black_time = None
        self.tempo_fixed = False

        # Variable d'iteration
        self.n_iter = -1

        #TRAITEMENT SUR PARTITION
        self.removeSpike().stick().silencestick().setBlackTime()



#
#   FONCTION DE TRAITEMENT
#

    #
    #   Supprime les pics (freq unique)
    #
    def removeSpike(self):
        n = self.getSize()

        notes = self.getNotes()

        # Traitement Echantillon 1
        if self[0].freq != self[1].freq:
            self[0].setSilence()

        b,c = self[0], self[1]
        for i in range(1 ,  n - 1 ):
            a,b,c = b,c,deepcopy(self[i+1]) #deepcopy pour ne pas tenir compte des modifications precedentes (equivalent a une duplication de la liste de depart)
            if a.freq != b.freq and b.freq != c.freq:
                self[i].setSilence()
        if c.freq != self[n - 1].freq :
            self[n - 1].setSilence()

        return self


    #
    #   Colle les notes ET silences
    #
    def stick(self):
        black_time = self.getBlack_Time()
        notes = []

        back = self[0]

        for i in range(1, self.getSize()):
            current = self[i]

            if (back == None):
                back = current
                continue

            if(back.getFreq() == current.getFreq()):
                back.add(current)
            else:
                notes.append(back)
                back = current

        #Traitement du dernier
        if(back != None):
            notes.append(back)
        self.notes = notes
        self.sticked = True
        return self


    #
    #   Collle les silences au notes en partant de notes et silences deja regroupes.
    #
    def silencestick(self):
        notes = []
        black_time = self.getBlack_Time(False) #Temps de la noire sans silence (false)

        #Retrait du premier silence
        if self[0].isSilence():
            notes.append(self[1])
            i_start = 2
        else:
            notes.append(self[0])
            i_start = 1

        #Scan des notes suivantes
        for i in range(i_start,self.getSize()):
            note = self[i]
            if note.isSilence():
                if note.getTime() >= black_time:
                    notes.append(note)
                else:
                    notes[len(notes)-1].add(note) #Silence trop court ajout a la note precedente
            else:
                notes.append(note)

        self.notes = notes
        return self


    #
    #   Definit les rythmes de chaque note, le tempo est donc ensuite fixe
    #
    def setBlackTime(self):
        black_time = self.getBlack_Time()
        for note in self.notes:
            note.setBlack_Time(black_time)
        self.tempo_fixed = True
        return self


    #
    #   Retourne le temps d'une noire
    #
    def getBlack_Time(self, silence = True):
        if self.tempo_fixed:
            return self.black_time
        fait = []
        black_time = None
        n_black_time = 0
        for e in self.getTime_List(silence):
            if e in fait:
                continue

            fait.append(e)
            n_e = self.getTime_List().count(e)
            if n_e > n_black_time:
                black_time = e
                n_black_time = n_e

        self.black_time = black_time

        return self.black_time



    #   Retourne tous les temps de notes
    def getTime_List(self, silence = True):
        time_list = []
        for note in self.notes:
            if (silence == False and note.isSilence() ):
                pass
            time_list.append(note.getTime())
        return time_list


#
#   FONCTION D'INTERFACE
#

    def getSize(self):
        return len(self.notes)

    def __getitem__(self,x):
        # Gestion des index trop grand
        max_x = self.getSize()
        if max_x <= x :
            if self.n_iter != -1: # Stop iteration boucle for
                self.n_iter = -1
                raise StopIteration
            else: # Raise error for array request
                raise ValueError("Index '" + str(x) + "' hors de la partition ! ( Size = " + str(self.getSize()) + " )")

        return self.notes[x]

    def getNotes(self):
        return self.notes

    def getSize(self):
        return len(self.getNotes())

    def getTempo(self):
        return int(60 / (self.black_time))



#
#   FONCTION D'AFFICHAGE
#

    def __str__(self):
        r = "\n--- Partition '" + str(self.link) + "' ---\n"
        r += "_ Taille : " + str(len(self.getNotes())) + " notes\n"

        if self.getSize() > 0:
            r += "_ Temps d'une noire : " + str(self.getBlack_Time()) + "s\n"
            r += "_ Tempo : " + str(self.getTempo()) + "BPM\n"
            r += "_ Notes :\n"
            for note in self:
                r += "    _ " + str(note) + "\n"
        else:
            r += "Aucune Note\n"
        r += "\n"
        return r



    def plotNotes(self, name="Notes"):
        x = []
        f = []
        t = 0
        for note in self:
            #Ajout des temps
            x.append(t)
            t += note.getTime()
            x.append(t)
            #Ajout de la freq
            f.append(note.getFreq())
            f.append(note.getFreq())
            #Ajout de la transition
            x.append(t)
            f.append(0)

        plt.figure(name)
        plt.plot(x,f)
        plt.axis([0,t,100,1600])
        plt.suptitle(name + "\n'" + self.link + "'")

        plt.ylabel("Frequence")
        plt.xlabel("Echantillon")
        return self



    def plotPartition(self, name="Partition"):
        elementary_notes = []
        for note in self:
            n = int(note.getTime()/note.elementary_time)
            elementary_notes += [note.getFreq()] * n
            elementary_notes.append(0)

        n = len(elementary_notes)
        beat_final = n*self[0].elementary_time
        x = np.linspace(0, beat_final, n)

        plt.figure(name)
        plt.plot(x,elementary_notes)
        plt.axis([0,beat_final,100,1600])
        plt.suptitle(name)

        plt.ylabel("Frequence")
        plt.xlabel("Beat")
        plt.grid(True)
        return self



#
#   FONCTION D'ITERATION
#

    def __iter__(self):
    	# Initialision Variable d'iteration
    	self.n_iter = -1
    	return self



    def next(self):
        self.n_iter += 1
    	return self.__getitem__(self.n_iter)