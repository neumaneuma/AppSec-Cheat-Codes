# AppSec Cheat Codes

A CTF web app designed to teach software developers application security by showcasing what vulnerable code looks like, how to write code to exploit the vulnerability, and how to write code to patch the vulnerability.

You can access the publicly available version [here](https://ctf.neumaneuma.com), or you can run it locally.

## How to run webapp locally

1. Install [docker](https://docs.docker.com/get-docker/) if it is not already installed (if you're on macOS I would recommend using [orbstack](https://orbstack.dev) instead).
2. Run `docker compose -f docker-compose.yaml up --build`.
3. The web server is now accessible at [`127.0.0.1:12300`](http://127.0.0.1:12300) (it may take some time for all the docker containers to start up on the first run).

## Miscellaneous

Any changes made to the server code locally will be automatically reloaded in the docker container. Feel free to make changes and play around with the code to help you understand how it works better!
