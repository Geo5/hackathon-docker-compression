# Hackathon CVRP

This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information. My participant ID in the challenge was: CC-VOL1-4

## How to run

```bash
git clone https://github.com/Geo5/hackathon-docker-compression.git
cd hackathon-docker-compression
docker build -t docker-compression .
docker run -it docker-compression [Dockerfile or Dockerfile.compressed]
```

## Idea

Used the zstd compression program, after blank line removal, comment removal, removing of line continuations ("\"). Does also lowercase the commands and shorten them to 1-3 chars.
