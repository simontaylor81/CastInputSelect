# Updating

On Raspberry Pi:

```
docker build -t cast-input-select https://github.com/simontaylor81/CastInputSelect.git
docker tag cast-input-select simontaylor81/cast-input-select
docker push simontaylor81/cast-input-select
docker stop cast-input-select
docker rm cast-input-select
docker run --name=cast-input-select --network=host --restart=always -d simontaylor81/cast-input-select
```