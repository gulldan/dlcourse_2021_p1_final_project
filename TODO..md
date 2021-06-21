# start redis
docker run --name redis --rm -p 6379:6379 -d redis:alpine

# TODO
- [ ] move TG_TOKEN to ENV
- [ ] use onnx for decrease docker image size
- [ ] draw scheme
- [ ] add antispam (redis)
- [ ] https://github.com/pytorch/pytorch/blob/master/test/onnx/model_defs/super_resolution.py
- [ ] use [ya.cloud](https://habr.com/ru/company/rebrainme/blog/512206/)
- [ ] check if similar, phash?
