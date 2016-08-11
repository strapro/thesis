import os
import sys

command ='docker run -it --rm  --user $(id -u) --workdir="/home/$USER" --env="DISPLAY" --env="LD_LIBRARY_PATH=/usr/local/lib" --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --volume="$(pwd)/home:/home/$USER"  --volume="$(pwd)/splitted_files:/splitted_files" strapro/thesis /src/ferret/src/ferret'

for directory in next(os.walk('splitted_files'))[1]:
    files = next(os.walk('splitted_files/'+directory))[2]
    commandWithFiles = command+" /splitted_files/"+directory+"/"+files[0]+" /splitted_files/"+directory+"/"+files[1]+" > $(pwd)/splitted_files/"+directory+"/ferret_result.txt"
    os.system(commandWithFiles) 
    print(directory, files[0], files[1])
    sys.exit(0)