# imagerepo

## Todos

### Features
* possibly create UID for each user if duplicate usernames allowed
* add upload progress per image like google photos
    * https://www.nginx.com/resources/wiki/modules/upload_progress/
    * or I think there is axios support for upload progress?
        * https://www.youtube.com/watch?v=Ti8QNiRRzOA
* I guess better ui huh?  

### Optimziations
* move logic/api calls into parent component
* disable react dev tools + redux dev tools for production 
* change mongo user/pass to docker secrets and create defined readwrite user, don't use root
* create dev dockerfiles + dev dockercompose for dev workflow
    * binded volume mounts for hot reloading
* switch to one nginx instance
* implement chunked file uploading
* implement chucked file reponses


## Interesting links about file uploading practices
* https://stackoverflow.com/questions/4083702/posting-a-file-and-associated-data-to-a-restful-webservice-preferably-as-json
* https://stackoverflow.com/questions/53725760/does-multipart-form-data-sends-the-whole-file-data-at-one-go-or-in-a-stream
* https://stackoverflow.com/questions/2502596/python-http-post-a-large-file-with-streaming
