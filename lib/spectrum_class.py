"""
    Module for holding a spectrum
"""

class Spectrum :
    def __init__(self) :
        #chans = []
        self.name = ""
        self.freq = []
        self.velocity = []
        self.data = []
        self.restFreq = 0.0
        self.startFreq = 0.0
        self.restVel = 0.0
        self.startVel = 0.0
        self.specMin = 10000.0
        self.specMax = -10000.0
        self.velStep = 0.0
        self.freqStep = 0.0
        self.specUnits = ""
        self.title = ""
        self.description = ""

    def putData(self, data) :
        self.data = data
        for i in range(0, len(data)) :
            if(self.specMin > data[i]) :
                self.specMin = data[i]
            elif(self.specMax < data[i]) :
                self.specMax = data[i]

        if(len(data) != len(self.freq)) :
            self.freq = []
        if(len(data) != len(self.velocity)) :
            self.velocity = []

        if((self.startFreq == 0.0 and self.startVel ==0.0 and self.velStep == 0.0 and self.freqStep == 0.0) or (len(self.freq) > 0 and len(self.velocity) > 0)) :
            return

        self.recalcAxis()

    def setTitle(self, title) :
        self.title = title

    def setDescription(self, desc) :
        self.description = desc

    def setRestFreq(self, freq) :
        self.restFreq = freq

    def setSpecUnits(self, units) :
        self.specUnits = units

    def setRestVel(self,  vel) :
        self.restVel = vel

    def setStartFreq(self,  freq) :
        self.startFreq = freq

    def setStartVel(self,  vel) :
        self.startVel = vel

    def setVelStep(self,  vel) :
        self.velStep = vel

    def setFreqStep(self,  freq) :
        self.freqStep = freq

    def putFreq(self, freqList) :
        self.freq = freqList

    def putVel(self,  velList) :
        self.velocity = velList

    def setFreqs(self, restFreq = 0.0,  startFreq = 0.0,  freqStep = 0.0) :
        if(restFreq > 0.0) :
            self.restFreq = restFreq
        if(startFreq >0.0) :
            self.startFreq = startFreq
        if(self.freqStep > 0.0) :
            self.freqStep = freqStep
        self.recalcAxis()

    def setVels(self, restVel = 0.0,  startVel = 0.0,  velStep = 0.0) :
        if(restVel > 0.0) :
            self.restVel = restVel
        if(startVel >0.0) :
            self.startVel = startVel
        if(self.velStep > 0.0) :
            self.velStep = velStep
        self.recalcAxis()

    def recalcAxis(self) :
        if(len(self.data) == 0) :
            return

        self.velocity = [0.0] * len(self.data)
        self.freq = [0.0] * len(self.data)

        for i in range(0, len(self.data)) :
            self.velocity = self.startVel + (self.freqStep * i)
            self.freq = self.startFreq + (self.velStep * i)

    def setName(self,  name) :
        self.name = name
