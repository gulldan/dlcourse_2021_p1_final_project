# start redis
docker run --name redis --rm -p 6379:6379 -d redis:alpine

# TODO
- [ ] move TG_TOKEN to ENV
- [ ] use onnx for decrease docker image size
- [ ] draw scheme
- [ ] add antispam (redis)
- [ ] use [ya.cloud](https://habr.com/ru/company/rebrainme/blog/512206/)