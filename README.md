# thesis

From the root directory of the project execute the following command to get into the docker container

docker run -it \
--rm \
--user $(id -u) \
--workdir="/home/$USER" \
--env="DISPLAY" \
--env="LD_LIBRARY_PATH=/usr/local/lib" \
--volume="/etc/group:/etc/group:ro" \
--volume="/etc/passwd:/etc/passwd:ro" \
--volume="/etc/shadow:/etc/shadow:ro" \
--volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
--volume="$(pwd)/home:/home/$USER" \
--volume="$(pwd)/scripts:/scripts" \
--volume="$(pwd)/ferret:/ferret" \
--volume="$(pwd)/splitted_files:/splitted_files" \
strapro/thesis \
bash