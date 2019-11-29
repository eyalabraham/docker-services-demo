# Tests for borrowing REST service
Use CURL to test:
```
Request all records:            curl -i http://0.0.0.0:8002/borrowdb
Request specific record {pass}: curl -i http://0.0.0.0:8002/borrowdb/0
                        {fail}: curl -i http://0.0.0.0:8002/borrowdb/2
Search by patron ID:            curl -i http://0.0.0.0:8002/borrowdb/patron/2
Count book ID borrowed out:     curl -i http://0.0.0.0:8002/borrowdb/count/3
Add borrow transaction:         curl -i -H "Content-Type: application/json" -X POST -d '{"borrow":{"book_id":1,"patron_id":1,"date_out":"2019-11-14","date_due":"2019-11-29"}}' http://0.0.0.0:8002/borrowdb
Delete borrow transaction:      curl -i -H "Content-Type: application/json" -X DELETE -d '{"return":{"book_id":1,"patron_id":1}}' http://0.0.0.0:8002/borrowdb
```
