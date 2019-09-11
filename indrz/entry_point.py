#!/bin/bash
import os
import subprocess

os.chdir("/src")

subprocess.call('python', 'manage.py', 'makemigrations')
subprocess.call('python', 'manage.py', 'migrate', '--noinput')

print("Django is ready.")
subprocess.run('python', 'manage.py', 'runserver', '0.0.0.0:8000')
