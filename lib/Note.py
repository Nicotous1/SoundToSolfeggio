from __future__ import division

class Note:

#
#   FONCTION D'INITIALISATION
#

    def __init__(self, freq, time):
        self.time = time
        self.setFreq(freq)

        #Param
        self.elementary_time = 0.5



#
#   FONCTION DE TRAITEMENT
#

    #
    #   Retourn la frequence exact (theorique) -> plage de frequence
    #
    def adjustFreq(self,freq):
        if 520 <= freq and freq <= 560: #DO
            return 540

        if 560 <= freq and freq <= 630: #RE
            return 600

        if 630 <= freq and freq <= 695: #MI
            return 660

        if 695 <= freq and freq <= 770: #FA
            return 730

        if 770 <= freq and freq <= 840: #SOL
            return 800

        if 840 <= freq and freq <= 930: #LA
            return 880

        if 930 <= freq and freq <= 1030: #SI
            return 1000

        if 1030 <= freq and freq <= 1100: #DO2
            return 1080

        return 0 # DEFAULT

    #
    #   Retourne le nom de la note pour une frequence
    #
    def name_with_freq(self,freq):
        if freq == 540:
            return "Do"
        if freq == 600:
            return "Re"
        if freq == 660:
            return "Mi"
        if freq == 730:
            return "Fa"
        if freq == 800:
            return "Sol"
        if freq == 880:
            return "La"
        if freq == 1000:
            return "Si"
        if freq == 1080:
            return "Do2"

        return "Silence"



#
#   FONCTION D'INTERFACE
#

    def setBlack_Time(self, black_time):
        ratio = self.time / black_time
        if (ratio >= 1):
            self.time = round(ratio)
        else:
            self.time = round(ratio/self.elementary_time)*self.elementary_time

        return self

    def add(self,a):
        self.time += a.time

    def setSilence(self):
        self.freq = 0
        self.name = self.name_with_freq(self.freq)

    def isSilence(self):
        return (self.freq == 0)

    def isNote(self):
        return self.freq != 0

    def getFreq(self):
        return self.freq

    def setFreq(self,freq):
        self.freq = self.adjustFreq(freq)
        self.name = self.name_with_freq(self.freq)
        return self

    def getName(self):
        return self.name

    def getTime(self):
        return self.time


#
#   FONCTION D'AFFICHAGE
#

    # Retourne une string de description
    def __str__(self):
        return self.name + " || " + str(self.freq) + "Hz || " + str(self.time) + " beat"
