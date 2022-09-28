# OptiScheduler

For all your scheduling needs :)


## Prerequisites

 - [Docker](https://docs.docker.com/get-docker/)
 - That's it!

## Setup
Navigate to the repo directory, and run:

    docker-compose up --build

The frontend will be available at http://localhost:3000, the backend at http://localhost:5000. The first time running will be the longest. Changes made to either the backend or the frontend will be immediately reflected. Control+C to quit.
## Production
To build for production, run:

    docker-compose -f docker-compose.prod.yml up --build
   
 The production application will be available at http://localhost:5000

## Running into an error with docker?

Stop the container (Control+C), and run:

    docker system prune --volumes
