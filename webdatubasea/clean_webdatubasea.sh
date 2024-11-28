#!/usr/bin/env bash

docker stop webdatubasea_web_1
docker stop webdatubasea_db_1
docker rm webdatubasea_web_1
docker rm webdatubasea_db_1