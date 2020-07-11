[![](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/cjkjvfnby/declared_env)
[![](https://img.shields.io/badge/platform%20independent-yes-green.svg)](https://github.com/cjkjvfnby/declared_env)
[![](https://img.shields.io/badge/dependency-None-green.svg)](https://github.com/cjkjvfnby/declared_env)
[![](https://github.com/cjkjvfnby/declared_env/workflows/Lint/badge.svg)](https://github.com/cjkjvfnby/declared_env/actions)
[![](https://github.com/cjkjvfnby/declared_env/workflows/Test/badge.svg)](https://github.com/cjkjvfnby/declared_env/actions)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/cjkjvfnby/declared_env)
[![](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/cjkjvfnby/declared_env/blob/master/LICENSE)

# Declared env

I tired of collecting env variables in code to make a description and decide to write a helper library.
I like to write code in declarative declare what you want and use it with benefits:
- autocomplete: no more string literals around a file
- enforce best practices: each variable has a prefix, all names in uppercase
- error reports:, you got full report, if you missed something
- help: get list of variables to make an instruction for admins 

Array, dict and json types not supported. 
If you need complex structures probably environment is not the best way to configure your app.

All these flake8 plugins is a little overkill.

Platform independent.

# Dependencies
Python3.6+ because of f-strings. Nothing more.

# Examples
## Simple example
```python
class MyEnv(EnvironmentDeclaration):
    prefix = "FOO"
    host = EnvironmentString(default="localhost")  # env: FOO_HOST

my_env = MyEnv()
my_env.host
# 'localhost'
```
## Django example

```python
class Environment(EnvironmentDeclaration):
    prefix = "MYSITE"
    secret_key = EnvironmentString(
        default="foo",
        help_text="see https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key "
    )


ENVIRONMENT = Environment()  # make it in caps to use in `from django.conf import settings`

SECRET_KEY = ENVIRONMENT.secret_key
```

If you assign declaration into variable with name in caps, you can access it via settings.
In that case to get list of environment variables you can create manage py command.
Create a [manage.py](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/) command to show help.

`mysite/polls/management/commands/show_env.py`
```python
from django.conf import settings
from django.core.management.base import BaseCommand

from declared_env import EnvironmentDeclaration


class Command(BaseCommand):
    help = "Collect all env variables"

    def handle(self, *args, **options):
        for x in dir(settings):
            val = getattr(settings, x)
            if isinstance(val, EnvironmentDeclaration):
                print(val.get_help())


``` 

```shell script
mysite> manage.py show_env
MYSITE_SECRET_KEY   see https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key , default=foo
```

Or you can just run `python settings.py` and print help.
```python
if __name__ == '__main__':
    print(ENVIRONMENT.get_help())
```

# Development

## Install dev requirements
`pip install -r dev-requirements.pip`

## Formatting
- `black .`

## Check

- `flake8`

## Run test
- `pytest --cov=declared_env` run test
- `pytest --cov=declared_env --cov-report html` run test with html report
