#!/bin/bash 

# if user didn't input the image path
if [ $# -eq 0 ]; then
    echo "Write your image path"
    exit 1
fi

image_path=$1
filename=$(basename "$image_path")
filepath=$(dirname "$image_path")

if [[ "$image_path" == /* ]]; then
    # if the input is absolute path
    docker run -it -v "$filepath":/app/assets/ haidhi/ktp -i assets/$filename 
else
    # if the input is relative path
    docker run -it -v "$(pwd)":/app/assets/ haidhi/ktp -i assets/$filename
fi

