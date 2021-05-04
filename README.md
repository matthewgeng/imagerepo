# Financial Risk Assessment
## Note, this is not close for kubernetes production but is for docker. Next steps:
1) Kubernetes files, support for environment variables (configmap?)
2) Add description associated with each survey and not the global description we have right now
3) Create service.tsx file for all requests

# Run

## Requirements

- [docker](https://docs.docker.com/install/)
- [k3d](https://k3d.io/) *not needed since kubernetes support not finished and if you only use `docker-compose up`

## Steps for Running
* ### Development
    * frontend
        1. `cd frontend`
        2. `npm start`

    * backend
        1. `cd backend`
        2. `python3 app.py`
* ### Docker
    1. `docker-compose up --build` or `docker-compose -f docker-compose.yml up --build` in the root folder.
    2. Access the frontend at `https://localhost:643`

## TODO
* remove `@ts-ignore` and actually type more things
* create kubernetes configuration files
