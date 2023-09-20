#!/bin/sh
docker build --network=host -f docker/Dockerfile -t octgnify .
