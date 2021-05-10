# imagerepo

## Running

### Docker

Production:
1. `docker-compose up` in root `PROD=true` in the `.env` file

Develop:
* Not really a dev workflow at the moment, since not hot reloading --> should be different docker-compose file
1. `docker-compose up` in root `PROD=false` in the `.env` file

### Normal
Frontend:
1. `cd frontend`
2. `npm i`
2. `npm start`

Backend:
1. `cd backend`
2. install requirements in your virtual env of choice! 
3. `python3 main.py`

Mongo: 
1. Spin up a mongo instance, I used docker with the `docker-compose-dev.yml` file
2. Otherwise spin up mongo and fill in the connection details in `main.py`. I used defaults of port `27017` and user/pass as `root/rootpassword`



## Todos

### Features
* possibly create UID for each user if duplicate usernames allowed
* add upload progress per image like google photos
    * https://www.nginx.com/resources/wiki/modules/upload_progress/
    * or I think there is axios support for upload progress?
        * https://www.youtube.com/watch?v=Ti8QNiRRzOA
* I guess better ui huh?  
* add better error codes/catching
* proper 3rd party ssl certificates which will remove need for checking ip or domain accessed

### Optimizations

* move logic/api calls into parent component
* disable react dev tools + redux dev tools for production 
* change mongo user/pass to docker secrets and create defined readwrite user, don't use root
* create dev dockerfiles + dev dockercompose for dev workflow
    * binded volume mounts for hot reloading
* possibly switch to one nginx instance?
* implement chunked file uploading frontend
* implement chucked file reponses
* optimize image preprocessing --> merge processed file and thumb fail to one function?
* optimize image stuff --> blobs, urls? 
    * https://www.bignerdranch.com/blog/dont-over-react-rendering-binary-data/


## Interesting links/searches about file uploading practices
* https://stackoverflow.com/questions/4083702/posting-a-file-and-associated-data-to-a-restful-webservice-preferably-as-json
* https://stackoverflow.com/questions/53725760/does-multipart-form-data-sends-the-whole-file-data-at-one-go-or-in-a-stream
* https://stackoverflow.com/questions/2502596/python-http-post-a-large-file-with-streaming
* axios can't start download notif with content-disposition header --> nasty workaround
   * create objectFromUrl, create and click on link :(
* send url back for images 
