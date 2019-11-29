# Tests for borrowing logic REST service
Use CURL to test:
```
Request all records {fail}: curl -i http://0.0.0.0:8003/borrow
Add record:                 curl -i -H "Content-Type: application/json" -X POST -d '{"borrow": {"book_id":1,"patron_id":1}}' http://0.0.0.0:8003/borrow
Change record  {fail}:      curl -i -H "Content-Type: application/json" -X PUT -d '{"borrow": {"book_id":1,"patron_id":1}}' http://0.0.0.0:8003/borrow
Delete borrow transaction:  curl -i -H "Content-Type: application/json" -X DELETE -d '{"borrow": {"book_id":1,"patron_id":1}}' http://0.0.0.0:8003/borrow
```
