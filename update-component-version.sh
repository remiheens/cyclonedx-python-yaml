#!/bin/bash
COMPONENT=$1
NEW_VERSION=$2
yq -i -Y '.components = (.components | map(if .name == "'$COMPONENT'" then .version = "'$NEW_VERSION'" else . end))' example.yaml