# Installation

Standard update stuff:
```
sudo apt update
sudo apt upgrade
```

Install docker (can't use `apt install`, it's not supported on Raspbian):
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Add 'pi' to docker group so you don't have to sudo everything:

```
sudo usermod -aG docker pi
```

Log off/log back in to take effect.

Then continue with Updating steps.

# Updating

On Raspberry Pi:

```
docker build -t cast-input-select https://github.com/simontaylor81/CastInputSelect.git
docker stop cast-input-select
docker rm cast-input-select
docker run --name=cast-input-select --network=host --restart=always -d cast-input-select
```