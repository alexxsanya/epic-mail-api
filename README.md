# EPIC MAIL API

## Project Status
[![Build Status](https://travis-ci.org/alexxsanya/EPIC-MAIL-API.svg?branch=ft-as_user_can_create_account-164792652)](https://travis-ci.org/alexxsanya/EPIC-MAIL-API)
[![Coverage Status](https://coveralls.io/repos/github/alexxsanya/EPIC-MAIL-API/badge.svg?branch=ft-as_user_can_create_account-164792652)](https://coveralls.io/github/alexxsanya/EPIC-MAIL-API?branch=ft-as_user_can_create_account-164792652)

## Project Overview

The internet is increasingly becoming an integral part of lives. Ever since the invention of [electronic mail](https://en.wikipedia.org/wiki/Email) by [Ray Tomlinson](https://en.wikipedia.org/wiki/Ray_Tomlinson), emails have grown to become the primary medium of exchanging information over the internet between two or more people, until the advent of Instant Messaging (IM) Apps.

As EPIC Andelan who work towards advancing human potential and giving back to the society, we wish to empower others by building a web app that helps people exchange messages/information over the internet.

## EPIC Mail APIs

This project will define the following APIs below

- Create a user account.

- Sign in a user.

- Get all received emails for a user.

- Get all unread emails for a user.

- Get all emails sent by a user.

- Get a specific user’s email.

- Send email to individuals**.**

- Delete an email in a user’s inbox.

  

## HTTP Verbs

HTTP verbs, or methods, should be used in compliance with their definitions under the [HTTP/1.1](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) standard.
The action taken on the representation will be contextual to the media type being worked on and its current state. Here's an example of how HTTP verbs map to create, read, update, delete operations in a particular context:

| HTTP METHOD      | POST                | GET                       | PUT            | DELETE         |
| ---------------- | ------------------- | ------------------------- | -------------- | -------------- |
| CRUD OP          | CREATE              | READ                      | UPDATE         | DELETE         |
| /auth/signup     | Create User Account |                           |                |                |
| /auth/login      | Login User          |                           |                |                |
| /messages        | Create a Message    | Get all received messages |                |                |
| /messages/unread |                     | Get all unread messages   |                |                |
| /messages/sent   |                     | Get all sent messages     |                |                |
| /message/<id>    |                     | get single message        | update message | delete message |
|                  |                     |                           |                |                |

## Responses

#### On Success

```json
{
  "status" : 200, 
  "data" : {...}
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
  "status" : Integer, 
  "data" : [
    {
      "id" : Integer, 
      "createdOn" : DateTime,
      "subject" : String,
      "message" : String,
      "senderId" : Integer,
      "receiverId" : Integer,
      "parentMessageId" : Integer,
      "status" : String,
    }, 
    {....},
    {....},
    ]
 }
```

### GET /messages/<id>

Response body:

```json
{
  "status" : Integer, 
  "data" : [{
      "id" : Integer, 
      "createdOn" : DateTime,
      "subject" : String,
      "message" : String,
      "senderId" : Integer,
      "receiverId" : Integer,
      "parentMessageId" : Integer,
      "status" : String,
  }]
}

```

### POST /messages

Request body:

```json
{
  "status" : Integer, 
  "data" : [{
     "createdOn" : DateTime,        
     "subject" : String,
     "message" : String,
     "parentMessageId" : Integer,
     "status" : String,
  }]
}

```