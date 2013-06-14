from astropy.io.votable.tree import VOTableFile, Resource, Table, Field, Group, Param
import math
from astropy.io.votable import parse
import spectrum_class as sc

c = 299792458.0 / 1000.0


class VOTable :
    def __init__(self):
        # for writing
        self.votable = VOTableFile()
        self.index = 0

        #for reading
        self.spec = []
        self.specName = []
        self.images = []

    #writer methods
    def addSpectrum(self, freq, labels, data, restVel = 0.0, restFreq = 0.0, fluxUnit = "Jy", title = "", description = "") :
        global c
        if(len(labels) != len(data)) :
            raise Exception("Length of label and data lists do not match.")
        for i in range(0, len(data)) :
            self.lengthCheck(data[i], labels[i], len(freq))
        resource = Resource()
        resource.utype = "spec:Spectrum:" + str(self.index)
        self.votable.resources.append(resource)
        vel = [0.0] * len(freq)
        if(restFreq != 0.0) :
            for i in range(0, len(freq)) :
                vel[i] = restVel + (restFreq * math.pow(10, 9) - freq[i] * math.pow(10, 9)) * c / (freq[i] * math.pow(10, 9))
        for i in range(0, len(labels)) :
            table = Table(self.votable)
            resource.tables.append(table)
            table.fields.extend([Field(self.votable, name="DataFluxValue", datatype="double", arraysize="1"),Field(self.votable, name="DataSpectralFreqValue", datatype="double", arraysize="1"),Field(self.votable, name="DataSpectralVelValue", datatype="double", arraysize="1")])
            table.create_arrays(len(freq))
            for j in range(0, len(freq)) :
                table.array[j] = (data[i][j], freq[j], vel[j])
            table.name = labels[i]
            charGroup = Group(table)
            charGroup.name = "Characterization"
            descGroup = Group(table)
            descGroup.name = "Description"
            titleParam = Param(self.votable, name="Title", value=title, datatype="char", arraysize="*")
            descParam = Param(self.votable, name="Desc", value=description, datatype="char", arraysize="*")
            descGroup.entries.append(titleParam)
            descGroup.entries.append(descParam)
            charGroup.entries.append(descGroup)
            fluxAxis = Group(table)
            fluxAxis.name = "Char.FluxAxis"
            fluxUnitParam = Param(self.votable,name="FluxAxisUnit",value=fluxUnit,datatype="char",arraysize="*")
            fluxAxis.entries.append(fluxUnitParam)
            charGroup.entries.append(fluxAxis)
            specAxis = Group(table)
            specAxis.name = "Char.SpectralAxis"
            velRes = str(vel[1] - vel[0])
            freqRes = str(freq[1] - freq[0])
            freqResolution = Param(self.votable,name="SpectralAxisResolution",value=freqRes,datatype="double",arraysize="1")
            velResolution = Param(self.votable,name="SpectralAxisVelResolution",value=velRes,datatype="double",arraysize="1")
            axisRestFreq=  Param(self.votable,name="SpectralAxisRestFreq",value=str(restFreq),datatype="double",arraysize="1")
            axisRestVel =  Param(self.votable,name="SpectralAxisRestVel",value=str(restVel),datatype="double",arraysize="1")
            specAxis.entries.append(freqResolution)
            specAxis.entries.append(velResolution)
            specAxis.entries.append(axisRestFreq)
            specAxis.entries.append(axisRestVel)
            charGroup.entries.append(specAxis)
            table.groups.append(charGroup)
        self.index += 1

    def writeFile(self, fileName) :
        self.votable.to_xml(fileName)

    def lengthCheck(self, data,  label, length) :
        if(len(data) != length) :
            raise Exception("Length of %s data does not match the frequency axis." % label)

    #reader methods
    def getSpec(self) :
        return self.spec

    def getImages(self) :
        return self.images

    def read(self, xmlFile) :
        #global plt
        votable = parse(xmlFile)
        print len(votable.resources)
        for resource in votable.resources :
            print "RES", resource.utype
            if(resource.utype == "header"):
                table = resource.tables[0]
                #parseHeader(table, )
            elif("spec:Spectrum" in resource.utype) :
                currSpec = []
                for table in resource.tables :
                    newSpec = sc.Spectrum()
                    newSpec.setName(table.name)
                    for group in table.groups :
                        if(group.name == "Characterization") :
                            for entry in group.entries :
                                if(entry.name == "Desciption") :
                                    for en in entry.entries :
                                        if(en.name == "Title") :
                                            newSpec.setTitle(en.value)
                                        elif(en.name == "Desc") :
                                            newSpec.setDescription(en.value)
                                elif(entry.name == "Char.FluxAxis") :
                                    for en in entry.entries :
                                        if(en.name == "FluxAxisUnit") :
                                            newSpec.setSpecUnits(en.value)
                                elif(entry.name == "Char.SpectralAxis") :
                                    for en in entry.entries :
                                        if(en.name == "SpectralAxisResolution") :
                                            newSpec.setFreqStep(en.value)
                                        elif(en.name == "SpectralAxisVelResolution") :
                                            newSpec.setVelStep(en.value)
                                        elif(en.name == "SpectralAxisRestFreq") :
                                            newSpec.setRestFreq(en.value)
                                        elif(en.name == "SpectralAxisRestVel") :
                                            newSpec.setRestVel(en.value)
                    newSpec.putData(table.array["DataFluxValue"].data)
                    newSpec.putFreq(table.array["DataSpectralFreqValue"].data)
                    newSpec.putVel(table.array["DataSpectralVelValue"].data)
                    currSpec.append(newSpec)
                self.spec.append(currSpec)
            elif(resource.type == "image"):
                pass

