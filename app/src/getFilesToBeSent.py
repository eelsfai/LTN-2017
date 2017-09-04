import os



def getFilesToBeSent():

    filesInDirectory = os.listdir(".") # Can specify location instead, "/home/username/..."
    index = []
    filesToBeSent = []
    for i in range(0,len(filesInDirectory)):     #Gets location of elements not containing .py
        if not(filesInDirectory[i].endswith(".py")):
            index.append(i)
    for i in index:    #Puts files not containing .py in a list.
        filesToBeSent.append(filesInDirectory[i])     
    return filesToBeSent
