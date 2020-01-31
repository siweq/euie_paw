#!/bin/bash

gpath = /usr/bin/git
git add .
$gpath status
sleep 
git commit -a
git status
git commit -m"Daily"
git push

