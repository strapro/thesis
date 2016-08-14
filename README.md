# Thesis

From the root directory of the project execute the following command to get into a new docker container
```
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
--volume="$(pwd):/thesis" \
strapro/thesis \
bash
```

The docker container contains a compiled from source executable of the Ferret plagiarism checker tool.

For more information about the docker image you can visit [the docker hub page](https://hub.docker.com/r/strapro/thesis)

For more information about the Ferret plagiarism checker tool you can visit [the project's github page](https://github.com/petercrlane/ferret)