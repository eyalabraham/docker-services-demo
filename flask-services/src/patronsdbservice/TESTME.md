# Tests for patrons REST service
Use CURL to test:
```
Request all records:            curl -i http://0.0.0.0:8003/patdb
Request specific record {pass}: curl -i http://0.0.0.0:8003/patdb/pnum/SKYWALKER444
                        {fail}: curl -i http://0.0.0.0:8003/patdb/pnum/SKYWALKER
Search by name:                 curl -i http://0.0.0.0:8003/patdb/key/Hatter
Test if patron in DB:   {pass}  curl -i http://0.0.0.0:8003/patdb/test/Pete_Dymond_BUFFALOBILL1
                        {pass}  curl -i http://0.0.0.0:8003/patdb/test/pete_Dymond_BUFFALOBILL1
                        {fail}  curl -i http://0.0.0.0:8003/patdb/test/Pete_Dymond_BUFFaLOBILL1
                        {fail}  curl -i http://0.0.0.0:8003/patdb/test/Dymond_Pete_BUFFALOBILL1
```
