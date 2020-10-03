# Naval Warfare

## What you can find here?

You'll find here a terminal-based Naval Warfare game that plays by itself! You only need to pass the initial configuration, and then the program will simulate a game!

It uses Docker to setup the environment, so you don't need to install on your system the Python project dependencies! But, if you prefer, the `pipenv` files ([`Pipfile`](Pipfile) and [`Pipfile.lock`](Pipfile.lock)) is also available so you can install everything on your computer!

## How to run?

There's a game already setup that you can find [here](games/game_1.in), so if you only want to see a game being played, just type on your favorite shell:

- If you have `docker-compose`:

```bash
docker-compose run play-game < games/game_1.in
```

- If you don't have Docker, be sure that you have at least Python 3.8:

```bash
python main.py < games/game_1.in
```

## And the tests?

Wanna run the tests:

- With `docker-compose`:

```bash
docker-compose run tests
```

- If you don't have Docker, install the `dev-packages` from [`Pipfile`](Pipfile) and run:

```bash
pipenv run tox
```