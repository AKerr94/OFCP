# OFCP (WIP)
Open Face Chinese Poker v2 

This is a remake of my original OFCP project, aiming for better code quality and modularity. 

Open Face Chinese Poker is a variant of Chinese Poker popular in home games and between rounds at tournaments. For more information and the rules see the [wikipedia page](https://en.wikipedia.org/wiki/Open-face_Chinese_poker).

# Contents

This repository stores the code for the game including the build scripts, backend game logic and application layer which handles requests from the client and between components of the application such as requests between the database and backend. Jinja2 templating is used to generate web pages for the client using information from the game state. 

# Deployment

For ease of deploying the infrastructure, everything is handled through a minimalist setup with a single docker host with containers for the separate components, namely a database container, data container and a container for the application itself. To deploy, you will need a VM (ubuntu preferable) to serve as your docker host. Clone this repository and navigate to OFCP/build and run the docker_spawn.sh script, which will automatically handle building the appropriate images and spawning the containers for you. Once this is done you should be all set up, and the necessary ports will be forwarded from the docker host to the respective components.
