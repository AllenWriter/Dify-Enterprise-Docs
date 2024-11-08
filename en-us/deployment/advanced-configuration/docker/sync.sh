#!/bin/bash

# Set the following environment variables
REGISTRY_URL="xxxx"
NAMESPACE="xxx"

# Ensure script receives required parameters
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <image> <version>"
    exit 1
fi

IMAGE=$1
VERSION=$2

BASE_IMAGE=langgenius/$IMAGE:$VERSION
echo "BASE_IMAGE: $BASE_IMAGE"

TARGET_IMAGE_FOR_AMD64=$REGISTRY_URL/$NAMESPACE/$IMAGE:$VERSION-amd64
echo "TARGET_IMAGE_FOR_AMD64: $TARGET_IMAGE_FOR_AMD64"

TARGET_IMAGE_FOR_ARM64=$REGISTRY_URL/$NAMESPACE/$IMAGE:$VERSION-arm64
echo "TARGET_IMAGE_FOR_ARM64: $TARGET_IMAGE_FOR_ARM64"

TARGET_IMAGE=$REGISTRY_URL/$NAMESPACE/$IMAGE:$VERSION
echo "TARGET_IMAGE: $TARGET_IMAGE"

docker pull --platform linux/amd64 $BASE_IMAGE
docker tag $BASE_IMAGE $TARGET_IMAGE_FOR_AMD64
docker push $TARGET_IMAGE_FOR_AMD64

docker pull --platform linux/arm64 $BASE_IMAGE
docker tag $BASE_IMAGE $TARGET_IMAGE_FOR_ARM64
docker push $TARGET_IMAGE_FOR_ARM64

docker manifest create $TARGET_IMAGE --amend $TARGET_IMAGE_FOR_AMD64 --amend $TARGET_IMAGE_FOR_ARM64
docker manifest push $TARGET_IMAGE