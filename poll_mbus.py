#!/usr/bin/python3

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import subprocess

# TODO: add custom exceptions/ErrorHandlers

class MBusSerialSensor():

    def __init__(self, name:str, addr:str, values:dict):
        self.name = name
        self.addr = addr
        self.messwerte = {}
        for key, value in values.items():
            self.messwerte[key] = [value, None]

    def getCSVHeaderStr(self):
        ret = "Datum;Zeit;"
        for x in self.messwerte.values():
            ret = ret + x[0] + ";"
        ret = ret + "\n"
        return ret

    def getOutputStr(self):
        ret = self.date + ";" + self.time + ";"
        for x in self.messwerte.values():
            ret = ret + x[1] + ";"
        ret = ret + "\n"
        return ret

    def checkFileExists(self, path):
        ret = False
        try:
            Path(path).resolve(strict=True)
        except FileNotFoundError:
            print("newfile det")
            ret = True
        return ret

    def readData(self):
        #using addr as filename for tests!
        try:
            proc = subprocess.run(["mbus-serial-request-data", "-b", "2400", "/dev/ttyUSB0", self.addr], stdout=subprocess.PIPE, timeout = 30, check=True, text=True)
        except subprocess.SubprocessError:
            print ("Fehler beim Auslesen an " + self.name + ", Adresse: " + self.addr)
        else:
            root = ET.fromstring(proc.stdout)
            for elem in root.findall('DataRecord'):
                for x in self.messwerte.keys():
                    if elem.get('id') == x:
                        self.messwerte[x][1] = elem.find('Value').text

    def Measure(self):
        try:
            self.readData()
        except:
            print ("Exception in readData()")
        else:
            fpre = datetime.now().strftime('%Y-%m')
            self.date = datetime.now().strftime('%Y-%m-%d')
            self.time = datetime.now().strftime('%H:%M:%S')
            fpath = Path("messwerte/" + fpre + "_" + self.name + ".csv")
            newfile = self.checkFileExists(fpath)
            with open(fpath, "a") as file:
                if newfile == True:
                    file.write(self.getCSVHeaderStr())
                file.write(self.getOutputStr())

class MBusSerialSDM230(MBusSerialSensor):
    def __init__(self, name:str, addr:str):
        super().__init__(name, addr, {'0': 'Energie[10Wh]'})

class MBusSerialSensoStarU(MBusSerialSensor):
    def __init__(self, name:str, addr:str):
        super().__init__(name, addr, {'1': 'Energie[kWh]', '7': 'Vorlauf[°C]', '8': 'Rücklauf[°C]', '9': 'Temperaturdifferenz[°C/100]'})

# example: create sensor objects
Strom1 = MBusSerialSDM230("Strom1", "0125704900000000")
Strom2 = MBusSerialSDM230("Strom2", "0125709500000000")
Waerme = MBusSerialSensoStarU("Waermemenge", "0")

# example: perform measurements
Strom1.Measure()
Strom2.Measure()
Waerme.Measure()

