from GPIO import GPIO

class GPIOProcessor:

    def __init__(self):
        self.GPIOList = []
        from GPIO import GPIO
        
    def getPin(self, pin_number):
        pin = GPIO(pin_number)
        pin.openPin()
        self.GPIOList.append(pin)
        return pin

    def getPin23(self):
        return self.getPin(36)

    def getPin24(self):
        return self.getPin(12)

    def getPin25(self):
        return self.getPin(13)  

    def getPin26(self):
        return self.getPin(69)

    def getPin27(self):
        return self.getPin(115)

    def getPin28(self):
        return self.getPin(4)   #MPP

    def getPin29(self):
        return self.getPin(24)

    def getPin30(self):
        return self.getPin(25)
    
    def getPin31(self):
        return self.getPin(35)
    
    def getPin32(self):
        return self.getPin(34)

    def getPin33(self):
        return self.getPin(28)
    
    def getPin34(self):
        return self.getPin(33)
    
    def cleanup(self):
        for pin in self.GPIOList:
            pin.input()
            pin.closePin()
            self.GPIOList.remove(pin)
        







        
        
