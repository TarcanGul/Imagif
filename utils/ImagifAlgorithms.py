from wand.image import Image
import os
import random

class Imagif:
    def __init__(self, readDirectory = os.getcwd(), writeDirectory = os.getcwd()):
        self.readDirectory = readDirectory
        self.writeDirectory = writeDirectory
    
    def getReadDir(self):
        return self.readDirectory

    def use_plain(self, input):
        filename = extractFilename(input)
        output_filename = str(random.randint(1, 2**16)) + "_" + filename + ".gif"
        with Image() as output:
            with Image(filename=os.path.join(self.readDirectory, input)) as img:
                output.sequence.append(img)
            output.type = 'optimize'
            output.format = 'gif'
            with open(os.path.join(self.writeDirectory, output_filename), "wb+") as f:
                output.save(file=f)
        return output_filename
    
    def use_noise_switch(self, input):
        filename = extractFilename(input)
        output_filename = str(random.randint(1, 2**16)) + "_" + filename + ".gif"
        with Image() as output:
            with Image(filename=os.path.join(self.readDirectory, input)) as img:
                output.sequence.append(img)
                with img.clone() as transformation:
                    transformation.noise('poisson',attenuate=1.0)
                    output.sequence.append(transformation)
            output.sequence[0].delay = 40 
            output.sequence[1].delay = 40 
            output.format = 'gif'
            output.type = 'optimize' 
            with open(os.path.join(self.writeDirectory, output_filename), "wb+") as f:
                output.save(file=f)
        return output_filename

    def use_party_mode(self, input):
        filename = extractFilename(input)
        output_filename = str(random.randint(1, 2**16)) + "_" + filename + ".gif"
        with Image() as output:
            with Image(filename=os.path.join(self.readDirectory, input)) as img:
                output.sequence.append(img)
                with img.clone() as transformation:
                    transformation.gaussian_blur(9,1)
                    with Image(width=100, height=1, pseudo="plasma:") as affinity:
                        transformation.remap(affinity)
                    output.sequence.append(transformation)
            for cursor in range(2):
                with output.sequence[cursor] as frame:
                    frame.delay = 100 * (cursor + 1)
            output.format = 'gif'
            output.type = 'optimize'
            with open(os.path.join(self.writeDirectory, output_filename), "wb+") as f:
                output.save(file=f)
        return output_filename
        
'''
Helpers
'''
def extractFilename(input):
    lastIndex  = input.rfind('/')
    filename = ""
    if lastIndex == -1: #There is no slash.
        filename = input
    else:
        filename = input[lastIndex+1:]
    if len(filename) > 4 and filename[-4] == '.':
        dotIndex = len(filename) - 4
        filename = filename[0:dotIndex]
    return filename



    

