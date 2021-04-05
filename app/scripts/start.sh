#!/bin/bash

[[ -z "$PORT" ]] && export PORT=8050
gunicorn main:server -b "$HOST:$PORT"