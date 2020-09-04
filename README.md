In this repository, I demonstrate a bug that can cause duplicate unformatted log messages in a Django project.


## Problem Background

The problem is caused by an accidental call to `logging.info` (without using `logging.getLogger` to get a specific logger). Python will automatically configure the root logger with defaults the first time you log to an unconfigured root logger.

You can demonstrate this with the python REPL:
```
>>> import logging
>>> root_logger = logging.getLogger()  # FYI: calling getLogger without an argument gets the root logger
>>> root_logger.handlers
[]
>>> logging.info('test')  # automatically uses the root logger
>>> root_logger.handlers
[<StreamHandler <stderr> (NOTSET)>]
```

Why isn't the root logger already set up? Because `'disable_existing_loggers': True` in settings.py unconfigures it, and the other loggers in settings.py are set to `'propagate': True` (the default) which makes the logs bubble up to the newly configured root logger.

## Solution

It's probably a good idea to set `disable_existing_loggers` to `False`, configure the root logger, and all your specific loggers to `'propagate': True`. This has a few benefits:

* You won't accidentally configure the root logger automatically because it's already configured.
* You won't need to remember to add new packages to your loggers, unless you want to override the default logging levels set by your root logger.
* You probably currently have a bunch of packages that aren't logging because you forgot to add those to the loggers in settings.


## Installation

Run: `docker-compose up web`

## Usage

Visit: http://localhost:8080/

## Why does the example use uwsgi + docker + json formatted logs?

I ended up making a minimal threaded uwsgi + docker + django website that uses JSON formatted logging to troubleshoot this, but a lot of that ended up having nothing to do with the problem. I think this boilerplate is still useful though, so I'm keeping it in here.
