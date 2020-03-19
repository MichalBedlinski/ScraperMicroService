# ScraperMicroService
Micro service for scraping Images/Text from websites

## Build and Run ##
```bash
    docker-compose up --build
```

## Exmaples of use ##
```bash
    curl -X POST 127.0.0.1:5000/images -d "url=https://www.google.com"
    curl -X GET 127.0.0.1:5000/statuses/<id>
    curl -X GET 127.0.0.1:5000/images/<id> > result.zip
```

## API ##
- /images 
  - POST
  - Codes:
    * 202 - When succesfuly accepted a task
    * 400 - When ther is no URL
  - Result:
    * id - Of the task


- /texts 
  - POST
  - Codes:
    * 202 - When succesfuly accepted a task
    * 400 - When ther is no URL
  - Result:
    * id - Of the task


- /statuses/{id} 
  - GET
  - Codes:
    * 200 - When succesfuly get a task status
    * 404 - When task doesn't exist
  - Result
    * status - of the task


- /images/{id} 
  - GET
  - Codes:
    * 200 - When task is succesfuly done
    * 404 - When task dosen't exists
    * 409 - When task status is not ready for retrive of results
  - Result
    * files - (images.zip)


- /texts/{id} 
  - GET
  - Codes:
    * 200 - When task is succesfuly done
    * 404 - When task dosen't exists
    * 409 - When task status is not ready for retrive of results
  - Result
    * files - (text.txt)


## What to improve ##
- Tests
- Error hnadling
- Leaving download of files for Nginx
