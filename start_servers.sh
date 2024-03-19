#!/usr/bin/env bash

PYTHON=/home/agrawpri/.pyenv/shims/python3.12

echo "Starting backend server on port 3000" && $PYTHON ./be.py --port 3000 &
echo "Starting backend server on port 3001" && $PYTHON ./be.py --port 3001 &
echo "Starting backend server on port 3002" && $PYTHON ./be.py --port 3002 &
echo "Starting load-balancer server on port 8000" && $PYTHON ./lb.py --port 8000 -T 10 http://localhost:3000 http://localhost:3001 http://localhost:3002 &
