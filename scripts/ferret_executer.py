import os


def execute_ferret(target_directory):
    command = 'ferret/src/ferret'

    for directory in next(os.walk(target_directory))[1]:
        files = next(os.walk(target_directory+'/'+directory))[2]
        print(directory, files[0], files[1])
        command_with_files = command+" "+target_directory+"/"+directory+"/"+files[0]+" "+target_directory+"/"+directory+"/"+files[1]+" > "+target_directory+"/"+directory+"/ferret_result.txt"
        os.system(command_with_files)
