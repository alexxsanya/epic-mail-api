# EPIC MAIL API

## Project Status
[![Build Status](https://travis-ci.org/alexxsanya/EPIC-MAIL-API.svg?branch=develop)](https://travis-ci.org/alexxsanya/EPIC-MAIL-API)
[![Coverage Status](https://coveralls.io/repos/github/alexxsanya/EPIC-MAIL-API/badge.svg?branch=develop)](https://coveralls.io/github/alexxsanya/EPIC-MAIL-API?branch=develop)

## Project Overview

EPICMAIL is an online system which enables you to exchange messages/information over the internet



## Getting started

### Prerequisites

You will need the following software running on your machine to get started

* Python 3.6  - ( [download python](https://www.python.org/getit/) )

* pip ([download pip](https://pip.pypa.io/en/stable/reference/pip_download/))


### Technologies

Flask (Python framework) -

Pytest (Python testing framework)

Pylint (Bug and quality checker for the Python programming language)

### Project Setup
These are the steps on how to get the application running on your machine

 - In your terminal, cd to where you want to create your repository

- Clone the project repo
```
$ git clone https://github.com/alexxsanya/EPIC-MAIL-API.git
```

- Install a virtual environment via pip
``` 
$ pip install virtualenv 
```

- Create a virtual environment
```
$ virtualenv venv
```
- Activate the virtual environment
```
$ EPIC-MAIL-API/venv/scripts/activate
```

- Install project dependencies 

```
$ pip install -r requirements.txt
```

### Run the app locally

- Run the app locally with the command

```
$ python app.py
```

## Tests coverage:

*  Run this command in the project directory.
  ``` pytest --cov=api```



## API

All APIs are prefixed with  `/api/v1`

| VERB   | API                    | ACTION                    |
| ------ | ---------------------- | ------------------------- |
| POST   | /auth/signup           | Create User Account       |
| POST   | /auth/login            | Login user                |
| POST   | /messages              | Creates a Message         |
| GET    | /messages              | Get all received messages |
| GET    | /messages/unread       | Get all unread messages   |
| GET    | /messages/sent         | Get all sent messages     |
| GET    | /messages/<message-id> | Get specific message      |
| DELETE | /messages/<message-id> | Delete message            |



## Responses

#### On Success

```json
{
  "status" : 200, 
  "data" : { }
}

```

#### On Error

```json
{
  "status" : 404,
  "error" : "relevant-error-message"
}

```

## Request & Response Examples

### API Resources

- [GET /messages](#get-messages)
- [GET /messages/[id]](#get-messagesid)
- [POST /messages](#post-messenges)

### GET /messages

Response body:

```json
{
  "status" : "Integer", 
  "data" : [
    {
      "id" : "Integer", 
      "createdOn" : "DateTime",
      "subject" : "String",
      "message" : "String",
      "senderId" : "Integer",
      "receiverId" : "Integer",
      "parentMessageId" : "Integer",
      "status" : "String",
    }, 
    { },
    { },
    ]
 }
```

### GET /messages/<id>

Response body:

```json
{
  "status" : "Integer", 
  "data" : [{
      "id" : "Integer", 
      "createdOn" : "DateTime",
      "subject" : "String",
      "message" : "String",
      "senderId" : "Integer",
      "receiverId" : "Integer",
      "parentMessageId" : "Integer",
      "status" : "String",
  }]
}

```

### POST /messages

Request body:

```json
{
  "status" : "Integer", 
  "data" : [{
     "createdOn" : "DateTime",        
     "subject" : "String",
     "message" : "String",
     "parentMessageId" : "Integer",
     "status" : "String",
  }]
}

```



## Deployment

*  [Heroku](https://api-epicmail.herokuapp.com/api/v1/)
*  [API Documentation](https://api-epicmail.herokuapp.com/api/v1/doc)
*  [Front-end](https://alexxsanya.github.io/EPIC-MAIL/UI/login.html)

