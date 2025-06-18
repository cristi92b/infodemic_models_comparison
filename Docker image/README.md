# ABM Misinformation Docker Image
## Prerequisites

**Step 1:** Make sure you have **docker** installed. To check, type in a terminal `docker --version` or `docker info`.
If docker is not installed, follow the installation steps on the [official docker installation guide](https://docs.docker.com/engine/install/).

## Building the image

**Step 2:** Download the git repository

If you have git installed, you can clone the repository using the following command:
`git clone git@github.com:cristi92b/abm_docker.git`

If you do not have git installed, you can simply download a zip archive of this repository and extract it.

**Step 3:** Build the docker image

Go to the local folder of this git repository and run the following command in the terminal to build the docker image:

`docker build -t abm_image --no-cache --progress=plain --build-arg="CASE=1"  . &> build.log`

- For case 2 replace `--build-arg="CASE=1"` with `--build-arg="CASE=2"`.
- To see the list of available docker images run `docker images`
- To remove a docker image run `docker rmi <image-name>`

## Creating the docker container

**Step 4:** Using the image built at step 3, create a new docker container using the following command: (you can run it either in the foreground or in the background)

- Run in the foreground
`docker run --name abm_container --volume experiments:/root/experiments abm_image`

- Run in the background
`docker run --name abm_container --volume experiments:/root/experiments -d abm_image`

## Checking the results

**Step 5:** Go to `/var/lib/docker/volumes` and check the results.

Here you should find the `experiments` folder which is the name of the volume defined at step 4.
This folder contains the results and the logs of case 1 or case 2.




