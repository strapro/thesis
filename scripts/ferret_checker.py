import os

command ='ferret/src/ferret'

originalOrParse = raw_input("Do you want to check the [o]riginal or the [p]arsed files?")

if originalOrParse == 'o':
    targetDirectory = 'splitted_files'
else:
    targetDirectoryCandidates = []
    i = 0
    for parsedDirectory in next(os.walk('splitted_parsed_files'))[1]:
        print "["+str(i)+"] "+parsedDirectory
        i += 1
        targetDirectoryCandidates.append(parsedDirectory)
    targetDirectoryCandidateIndex = raw_input("Which parsed files?")
    targetDirectory = 'splitted_parsed_files/'+targetDirectoryCandidates[int(targetDirectoryCandidateIndex)]


for directory in next(os.walk(targetDirectory))[1]:
    files = next(os.walk(targetDirectory+'/'+directory))[2]
    print(directory, files[0], files[1])
    commandWithFiles = command+" "+targetDirectory+"/"+directory+"/"+files[0]+" "+targetDirectory+"/"+directory+"/"+files[1]+" > "+targetDirectory+"/"+directory+"/ferret_result.txt"
    os.system(commandWithFiles)