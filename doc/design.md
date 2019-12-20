# Containerized Microservices demo

## Services
- Database services
- Library business logic
- Web front-end

## Database services
Three independant database services, and one MySQL database. Schema and REST interface follows.

### Patron registry database
#### Service
This database holds the names of authorized patrons of the library. Patrons' full names and library ID card numbers (patronNum) are stored in the database, and can be retrieved by other services in order to validate a patron's account. If a patron's name exists in this database then the patron is authorized to lend a book from the library.
The service provides an interface for adding and removing patron names.
This service is bound to port 5003.

#### REST end-points

| Method | Patron service end-points                 | Action                       | 
|--------|-------------------------------------------|------------------------------| 
| GET    | http://[hostname]/patdb                   | All records                  |
| GET    | http://[hostname]/patdb/pnum/'patron_num' | Patron by membership number  |
| GET    | http://[hostname]/patdb/key/'name'        | All records containing name  |
| GET    | http://[hostname]/patdb/test/'qualifier'  | Test if patron exists        |
| POST   | http://[hostname]/patdb                   | Not implemented, returns 404 |
| PUT    | http://[hostname]/patdb                   | Not implemented, returns 404 |
| DELETE | http://[hostname]/patdb                   | Not implemented, returns 404 |

** 'qualifier' is a string of format ```<patron_first_name>_<patron_last_name>_<patron_membership_num>```

#### Database schema
```
CREATE TABLE IF NOT EXISTS patrons
(
  id           INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  firstName    VARCHAR(64) NOT NULL,
  lastName     VARCHAR(64) NOT NULL,
  patronNum    CHAR(12)    NOT NULL UNIQUE,
  role         CHAR(8)     NOT NULL,
  INDEX (patronNum)
);
```

#### JSON response formats
Get all patrons, get patrons by name key
```
{ "patrons":
    [ [id, firstName, lastName, patronNum, role],
      ...
    ]
}
```
Get patron by unique number
```
{ "patron":
    [ [id, firstName, lastName, role] ]
}
```
Test existance of parton qualifier
```
{
  "patron": <true | false>
}
```
HTTP 404
```
{ "error": 'Not found'}
```
HTTP 400
```
{ "error": 'Bad Request'}
```
HTTP 500
```
{ "error": 'Internal Server Error'}
```

### Catalog database
#### Service
This database holds the list of books available in the library. The database stored the book's title and author, as well as a URL to a thumbnail picture. Every book in the library has the max count of available copies. This count will be compared against the lended count of a book to determine if any are available for further lending.
This service is bound to port 5001.

#### REST end-points

| Method | Catalog service end-points            | Action                       | 
|--------|---------------------------------------|------------------------------| 
| GET    | http://[hostname]/catdb               | All records                  |
| GET    | http://[hostname]/catdb/'int:book_id' | Record with specific id      |
| GET    | http://[hostname]/catdb/author/'name' | Records of author            |
| GET    | http://[hostname]/catdb/title/'text'  | Records of title             |
| POST   | http://[hostname]/catdb               | Not implemented, returns 404 |
| PUT    | http://[hostname]/catdb               | Not implemented, returns 404 |
| DELETE | http://[hostname]/catdb               | Not implemented, returns 404 |

#### Database schema
```
CREATE TABLE IF NOT EXISTS catalog
(
  id           INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title        VARCHAR(256) NOT NULL,
  author       VARCHAR(128) NOT NULL,
  count        INT          NOT NULL DEFAULT 0,
  thumbnailUrl TEXT,
  FULLTEXT(title),
  INDEX (author)
);
```
#### JSON response formats
Get all books, by author name, by title
```
{ "books":
    [ [id, title, author, count, thumbnailUrl],
      ...
    ]
}
```
Get patron by unique number
```
{ "book":
    [ [id, title, author, count, thumbnailUrl] ]
}
```
HTTP 404
```
{ "error": 'Not found'}
```
HTTP 400
```
{ "error": 'Bad Request'}
```
HTTP 500
```
{ "error": 'Internal Server Error'}
```

### Borrowing database
#### Service
This database holds the book lending transactions. The other two databases are static and will only by used to retrieve information, while this database will be actively logging book lending activities. This setup keeps the service isolated.
This service is bound to port 5002.

#### REST end-points

| Method | Book borrowing end-point                          | Action                       |
|--------|---------------------------------------------------|------------------------------| 
| GET    | http://[hostname]/borrowdb                        | All records                  |
| GET    | http://[hostname]/borrowdb/'int:id'               | Specific id                  |
| GET    | http://[hostname]/borrowdb/patron/'int:patron_id' | Specific patron's books      | 
| GET    | http://[hostname]/borrowdb/due/'date'             | Books due on date            | 
| GET    | http://[hostname]/borrowdb/count/'int:book_id'    | Count books out              |
| POST   | http://[hostname]/borrowdb                        | Add a borrow entry           |
| PUT    | http://[hostname]/borrowdb                        | Not implemented, returns 404 |
| DELETE | http://[hostname]/borrowdb                        | Delete a borrow entry        |

#### Database schema
```
CREATE TABLE IF NOT EXISTS borrowed
(
  id           INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  bookId       INT      NOT NULL,
  partonId     INT      NOT NULL,
  dateOut      DATE     NOT NULL, 
  dateDue      DATE     NOT NULL,
  INDEX (dateDue)
);
```
#### JSON response formats
All borrows, patron's borrows, by date
```
{
  "transactions":
  [ [id, bookId, patronId, dateOut, dateDue],
    ...
  ]
}

{ "transactions": Null }
```
Borrow transaction by ID
```
{
  "transaction":
  [ [id, bookId, patronId, dateOut, dateDue] ]
}

{ "transaction": Null }
```
Book count
```
{
  "transactions":
  [ [ <integer> ]
  ]
}
```
Response to POST and DELETE, 0 if not completed positive integer is completed
```
{ "transaction": <integer> }
```
HTTP 404
```
{ "error": 'Not found'}
```
HTTP 400
```
{ "error": 'Bad Request'}
```
HTTP 500
```
{ "error": 'Internal Server Error'}
```

#### POST request format
POST request will use the following JSON representation:
```
{ "borrow":
  { "book_id"   : <integer_id>,
    "patron_id" : <integer_id>,
    "date_out"  : <date_string_YYYY-MM-DD>,
    "date_due"  : <data_string_YYYY-MM-DD>,
  },
}
```

#### DELETE request format
DELETE request will use the following JSON representation:
```
{ "return":
  { "book_id"   : <integer_id>,
    "patron_id" : <integer_id>,
  },
}
```

## Library business logic
### Borrowing logic service
#### Service
This service manages the borrowing logic.
1. Check if patron exists in the registry.
2. For the requested book get count of borrowed copies and compare to the inventory count.
3. If patron exists, and borrowed count is less than available count and less than borrowing limit, then proceed to borrowing, otherwise return an error.
4. POST borrowing transaction to database and confirm borrow action.
5. This service is bound to port 5004.

#### REST end-points

| Method | Book borrowing end-point  | Action                       | 
|--------|---------------------------|------------------------------| 
| GET    | http://[hostname]/borrow  | Not implemented, returns 404 |
| POST   | http://[hostname]/borrow  | Patron book borrow request   |
| PUT    | http://[hostname]/borrow  | Not implemented, returns 404 |
| DELETE | http://[hostname]/borrow  | Not implemented, returns 404 |

#### JSON response formats
Response to POST request
```
{ "transaction": <True | False> }
```
HTTP 404
```
{ "error": 'Not found'}
```
HTTP 400
```
{ "error": 'Bad Request'}
```
HTTP 500
```
{ "error": 'Internal Server Error'}
```

#### POST (and DELETE) request format
POST and DELETE request will use the following JSON representation:
```
{ "borrow":
  { "book_id"   : <integer_id>,
    "patron_id" : <integer_id>,
  },
}
```

### Email notification service
TODO: not implemented

## Web access services
### Frontend
The web frontend is the access method for library patrons. It provides a book catalog view and a book borrowing interface. The front end is built using a Django web framework and includes:
- Home page dislaying library book catalog with a 'Borrow' botton/link
- Patron login for borrowing or displaying patron's borrowed books. The page will ask for patron's first and last name, and patron's library ID.
- Patron's borrowed book list. Displayed afer successful borrowing, or when requested through link on the catalog page.

The front end service will communicate with the catalog services, the patron registry service, and the library borrowing logic service through their respective RSET interfaces.

### Administration
TODO: not implemented

## Access infrastructure
TODO: not implemented
