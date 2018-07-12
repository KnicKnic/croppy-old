# Old Croppy
Contains the files for the website croppy_old. The purpose of this website was to help people to take one long comic strip (think long narrow picture), and split it up into shorter sections that can be used on [line webtoon](https://www.webtoons.com/en/) and [tapas](https://tapas.io/)

## Info
It used the following components
* [ImageMagick](https://www.imagemagick.org/script/index.php) 
    * for splitting pictures
* [Flask](http://flask.pocoo.org/) & [python](https://www.python.org/)
    * For hosting the website
* [Docker](https://www.docker.com/)
    * For packaging & distribution
* [Debian](https://www.debian.org/)
    * Linux that had all dependencies

## Files
* [flask_prog.py](flask_prog.py)
    * python program that shells out to imagemagick
    * important logic is located in get_zip
* [templates/index.html](templates/index.html)
    * the single page website
* [static/out.png](static/out.png) & [static/Croppy.png](static/Croppy.png)
    * Log pic & shrunk logo pic provided by [Laht](https://tapas.io/Laht) for croppy.
* [Dockerfile](Dockerfile) & [Dockerfile.old](Dockerfile.old) & [docker-compose.yaml](docker-compose.yaml)
    * docker files to build & run website
* [policy.xml](policy.xml)
    * over wrote existing policy to enable larger memory usage and allow more formats
    * doing so may be bad as I may allow attacks?
        * See [https://imagetragick.com/](https://imagetragick.com/) on hacks

## Running
You probably want to edit docker-compose.yaml volume first.

```
docker build -t oldy . -f Dockerfile.oldy
docker-compose up -d
```