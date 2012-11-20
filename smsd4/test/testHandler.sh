curl -d "name=xbfool" 127.0.0.1:8080/auth?rt=json&type=abc
curl -d "{\"name\":\"xbfool1\"}" 127.0.0.1:8080/auth?type=json
curl -d "{\"name\":\"json\"}" 127.0.0.1:8080/auth?type=json&rt=json
curl -d "{\"name\":\"urlencode\"}" 127.0.0.1:8080/auth?type=json&rt=urlencode
