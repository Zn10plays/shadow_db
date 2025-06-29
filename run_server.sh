#!/bin/bash

# the following envs must be set before running this script
# SQL_ROOT_PASSWORD: the root password for the MySQL database
# DB_PATH: the path to store the MySQL database files
# SQL_SERVER_PORT: the port on which the MySQL server will listen (NO default, must be set)

# Check if required environment variables are set
if [ -z "$SQL_ROOT_PASSWORD" ]; then
  echo "Error: SQL_ROOT_PASSWORD is not set."
  exit 1
fi

if [ -z "$DB_PATH" ]; then
  echo "Error: DB_PATH is not set."
  exit 1
fi

if [ -z "$SQL_SERVER_PORT" ]; then
  echo "Error: SQL_SERVER_PORT is not set."
  exit 1
fi

mkdir -p $DB_PATH

podman run --rm -d \
  --name shadowdb \
  -p $SQL_SERVER_PORT:$SQL_SERVER_PORT \
  -e MYSQL_ROOT_PASSWORD="$SQL_ROOT_PASSWORD" \
  -v $DB_PATH:/var/lib/mysql \
  docker.io/library/mysql:latest