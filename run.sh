#!/bin/bash

#my dockerhub repo is public and thus i did not include a build step

for manifest in $(ls k8s_manifests); do
    kubectl apply -f "${manifest}";
done
