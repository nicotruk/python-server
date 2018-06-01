#!/bin/bash
docker login --username=_ --password=$HEROKU_TOKEN registry.heroku.com
docker build -t registry.heroku.com/app-server-stories/web .
docker push registry.heroku.com/app-server-stories/web