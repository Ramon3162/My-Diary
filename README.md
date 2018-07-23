[![Maintainability](https://api.codeclimate.com/v1/badges/92ae5552eeceac6cd893/maintainability)](https://codeclimate.com/github/Ramon3162/My-Diary/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/92ae5552eeceac6cd893/test_coverage)](https://codeclimate.com/github/Ramon3162/My-Diary/test_coverage) [![Build Status](https://travis-ci.org/Ramon3162/My-Diary.svg?branch=develop)](https://travis-ci.org/Ramon3162/My-Diary) [![Coverage Status](https://coveralls.io/repos/github/Ramon3162/My-Diary/badge.svg?branch=develop)](https://coveralls.io/github/Ramon3162/My-Diary?branch=develop)

## My-Diary

Andela Developer Challenge (Cohort 30)

## Description

It is an API that enables CRUD functionality for creating, viewing, editing, and deeting diary entries.

## Development

Clone the repository:

```git clone https://github.com/Ramon3162/My-Diary.git```


## Prerequisites

* Python 3.6 or later
* Git 
* Virtualenv
* Postman

Create a virtual environment and activate it.[Refer here](https://docs.python.org/3/tutorial/venv.html)

## Dependencies
- Install the project dependencies:
> $ pip install -r requirements.txt

After setting up the above, run.

```python run.py```

## API endpoints

Test | API-endpoint | HTTP-Verb
------------ | -------------- | ------------ 

Test the endpoints:
User can create a diary entry | /api/v1/entries | POST
------------ | -------------- | ------------ 
User can view all diary entries | /api/v1/entries | GET
------------ | -------------- | ------------ 
User can view a single diary entry | /api/v1/entries/<entry_id> | GET
------------ | -------------- | ------------ 
User can update a diary entry | /api/v1/entries/<entry_id> |PUT
------------ | -------------- | ------------ 
User can delete a diary entry | /api/v1/entries/<entry_id> | DELETE
------------ | -------------- | ------------ 

## Testing
Test the endpoints using Postman or curl

*this readme will be updated periodically*

## Author

*Ian Omondi*

## Acknowledgement

*Andela Kenya*
