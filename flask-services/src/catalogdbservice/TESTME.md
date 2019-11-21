# Tests for catalog REST service
Use CURL to test:
```
Request all records:            curl -i http://0.0.0.0:8001/catdb
Request specific record {pass}: curl -i http://0.0.0.0:8001/catdb/1
                        {fail}: curl -i http://0.0.0.0:8001/catdb/21  
Search record author:           curl -i http://0.0.0.0:8001/catdb/author/Rogers
Search for title:               curl -i http://0.0.0.0:8001/catdb/title/king
```
