FROM alpine:latest

RUN apk --no-cache add apache2-utils

ENTRYPOINT ["ab", "-n", "1000000", "-c", "20", "http://app:8001/stories/token1"]
# ENTRYPOINT ["ab", "-n", "10000", "-c", "10", "http://app:8001/stories/token1"]
