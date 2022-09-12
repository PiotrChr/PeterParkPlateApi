#!/bin/bash

pwd
ls -a config
source ./config/.env.test

#pytest src/tests/ --cov=src