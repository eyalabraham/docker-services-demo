# Containerized Microservices demo

## Services
- Database services
- Library business logic
- Web front-end

## Database services
Three independant databases services, and one MySQL database. Schema and REST interface follows.

### Patron registry database
__Service__
This database holds the names of authorized patrons of the library. Patrons' full names and library ID card numbers (patronNum) are stored in the database, and can be retrieved by other services in order to validate a patron's account. If a patron's name exists in this database then the patron is authorized to lend a book from the library.
The service provides an interface for adding and removing patron names.
This service is bound to port 5003.

__REST end-points__

| Method | Patron service end-points                 | Action                      | 
|--------|-------------------------------------------|-----------------------------| 
| GET    | http://[hostname]/patdb                   | All records                 |
| GET    | http://[hostname]/patdb/pnum/<patron_num> | Patron by membership number |
| GET    | http://[hostname]/patdb/key/<name>        | All records containing name |
| GET    | http://[hostname]/patdb/test/<qualifier>  | Test if patron exists       |
| POST   | http://[hostname]/patdb                   | Add patron                  |
| PUT    | http://[hostname]/patdb                   | Update patron info          |
| DELETE | http://[hostname]/patdb                   | Remove patron               |

** 'qualifier' is a string of format ```<patron_first_name>_<patron_last_name>_<patron_membership_num>```

__Database schema__
```
CREATE TABLE IF NOT EXISTS patrons
(
  id           INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  firstName    VARCHAR(64) NOT NULL,
  lastName     VARCHAR(64) NOT NULL,
  patronNum    CHAR(12)    NOT NULL UNIQUE,
  INDEX (patronNum)
);
```

### Catalog database
__Service__
This database holds the list of books available in the library. The database stored the book's title and author, as well as a URL to a thumbnail picture. Every book in the library has the max count of available copies. This count will be compared against the lended count of a book to determine if any are available for further lending.
This service is bound to port 5001.

__REST end-points__

| Method | Catalog service end-points            | Action                  | 
|--------|---------------------------------------|-------------------------| 
| GET    | http://[hostname]/catdb               | All records             |
| GET    | http://[hostname]/catdb/<int:book_id> | Record with specific id |
| GET    | http://[hostname]/catdb/author/<name> | Records of author       |
| GET    | http://[hostname]/catdb/title/<text>  | Records of title        |
| POST   | http://[hostname]/catdb               | Add book                |
| PUT    | http://[hostname]/catdb               | Return 404              |
| DELETE | http://[hostname]/catdb               | Remove book             |

__Database schema__
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

### Borrowing database
__Service__
This database holds the book lending transactions. The other two databases are static and will only by used to retrieve information, while this database will be actively logging book lending activities. This setup keeps the service isolated.
This service is bound to port 5002.

__REST end-points__

| Method | Book borrowing end-point                          | Action                  | 
|--------|---------------------------------------------------|-------------------------| 
| GET    | http://[hostname]/borrowdb                        | All records             |
| GET    | http://[hostname]/borrowdb/<int:id>               | Specific id             |
| GET    | http://[hostname]/borrowdb/patron/<int:patron_id> | Specific patron's books | 
| GET    | http://[hostname]/borrowdb/due/<date>             | Books due on date       | 
| GET    | http://[hostname]/borrowdb/count/<int:book_id>    | Count books out         |
| POST   | http://[hostname]/borrowdb                        | Add a borrow entry      |
| PUT    | http://[hostname]/borrowdb                        | Return 404              |
| DELETE | http://[hostname]/borrowdb                        | Delete a borrow entry   |

__POST request format__
POST request will use the following JSON representation:
```
{
    "book_id"   : <integer_id>,
    "patron_id" : <integer_id>,
    "data_out"  : <date_string_YYYY-MM-DD>,
    "date_due"  : <data_string_YYYY-MM-DD>,
}
```

__DELETE request format__
DELETE request will use the following JSON representation:
```
{
    "book_id"   : <integer_id>,
    "patron_id" : <integer_id>,
}
```

__Database schema__
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

## Library business logic
### Borrowing logic service
__Service__
This service managest the borrowing logic.
1. Check if patron exists in the registry (unless we only allow registered patrons to log in and view the catalog).
2. For the requested book get count of borrowed copies and compare to the inventory count.
3. If patron exists, and borrowed count is less than available count and less than borrowing limit, then proceed to borrowing, otherwise return an error.
4. POST borrowing transaction to database and confirm borrow action.
This service is bound to port 5003.

TODO: GET output, POST, and DELETE JSON formats,

__REST end-points__

| Method | Book borrowing end-point              | Action                       | 
|--------|---------------------------------------|------------------------------| 
| GET    | http://[hostname]/borrow/<patron_num> | Book list borrowed by patron |
| POST   | http://[hostname]/borrow              | Add a borrow entry           |
| PUT    | http://[hostname]/borrow              | Return 404                   |
| DELETE | http://[hostname]/borrow              | Delete a borrow entry        |

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
