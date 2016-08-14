import os

command ='ferret/src/ferret'

for directory in next(os.walk('splitted_files'))[1]:
    files = next(os.walk('splitted_files/'+directory))[2]
    print(directory, files[0], files[1])
    commandWithFiles = command+" splitted_files/"+directory+"/"+files[0]+" splitted_files/"+directory+"/"+files[1]+" > splitted_files/"+directory+"/ferret_result.txt"
    os.system(commandWithFiles)