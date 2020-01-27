# Telia

## How to start a project

Clone This Project (Make Sure You Have Git Installed)
```
https://github.com/mazvydasnorkus/Telia.git
```
Download docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```
Run Docker

```
sudo docker-compose up
```

# Task nr. 1

All details, modifications and suggestions you can find in script1_mod.py file.

# Task nr. 2

All details about my REST API you can find below README.md file and the script which uploads and downloads data from Emploee Registry Service called script2.py

# Employee Registry Service

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all employees

**Definition**

`GET /employees`

**Response**

- `200 OK` on success

```json
[
    {
        "name": "Michael",
        "last_name": "Scott",
        "birth_date": "1889-02-02"
    },
    {
        "name": "Dwight",
        "last_name": "Schrute",
        "birth_date": "1902-01-01"
    }
]
```

### Registering a new employee

**Definition**

`POST /employees`

**Arguments**

- `"name":string` a name for this employee
- `"last_name":string` a last name of this employee
- `"birth_date":string` employee's birthday

If a employee with the given name already exists, the existing employee will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "name": "Michael",
    "last_name": "Scott",
    "birth_date": "1889-02-02"
}
```

## Lookup employee details

`GET /employee/<name>`

**Response**

- `404 Not Found` if the employee does not exist
- `200 OK` on success

```json
{
    "name": "Michael",
    "last_name": "Scott",
    "birth_date": "1889-02-02"
}
```

## Delete a employee

**Definition**

`DELETE /employees/<name>`

**Response**

- `404 Not Found` if the employee does not exist
- `204 No Content` on success
