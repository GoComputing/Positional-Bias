#!/bin/bash
CONTAINERS_BASENAME=ollama
START_PORT=11434
NUM_INSTANCES=8
CUDA_DEVICES=('"device=0"' '"device=1"' '"device=2"' '"device=3"' '"device=4"' '"device=5"' '"device=6"' '"device=7"')
OLLAMA_DATAPATH=$(pwd)/../ollama_data:/root/.ollama

# Stop running containers
echo "Stopping running containers..."
running_containers=$(docker container ls -f name=$CONTAINERS_BASENAME -q)
if [ ! -z "$running_containers" ]; then
       docker stop $running_containers
fi

# Remove containers
echo "Removing containers..."
containers=$(docker ps -a -f name=$CONTAINERS_BASENAME -q)
if [ ! -z "$containers" ]; then
        docker rm $containers
fi

# Launch containers
echo "Launching containers"
for (( i=0; $i<$NUM_INSTANCES; i=$i+1 )); do
       let port="$START_PORT+$i"
       name="${CONTAINERS_BASENAME}${i}"
       gpu_id=${CUDA_DEVICES[$i]}
       docker run -d --gpus "$gpu_id" -v "$OLLAMA_DATAPATH" -p $port:11434 --name $name ollama/ollama:0.11.4
done
