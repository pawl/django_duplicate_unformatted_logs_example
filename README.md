This is a demonstration of a bug that can cause duplicate unformatted log messages in a Django project.

## Problem Background

Example of logs with the problem: [Link](before.txt)

The problem is caused by an [accidental call to `logging.warning`](myapp/views.py#L16) (without using specific logger from `logging.getLogger(__name__)` ) while the [root logger isn't already configured](mysite/settings.py#L133).

Python will automatically configure the root logger to log with a StreamHandler to `stderr` the first time you log to an unconfigured root logger. You can demonstrate this with the python REPL:
```
>>> import logging
>>> root_logger = logging.getLogger()  # FYI: calling getLogger without an argument gets the root logger
>>> root_logger.handlers
[]
>>> logging.info('test')  # automatically uses the root logger
>>> root_logger.handlers
[<StreamHandler <stderr> (NOTSET)>]
```

Why isn't the root logger already configured? Because `'disable_existing_loggers': True` in [settings.py](mysite/settings.py#L134) unconfigures it, and the other loggers in [settings.py](mysite/settings.py#L159) are set to `'propagate': True` (the default) which makes the logs bubble up to the newly configured root logger.

## Solution

First you should switch [the calls to `logging.warning`](myapp/views.py#L16) to use a logger from `logger.getLogger(__name__)`.

Here's what the logs look like after doing that: [Link](after.txt)

It's also probably a good idea to set `disable_existing_loggers` to `False`, configure the root logger in settings.py, and set all your specific loggers to `'propagate': False`.

This has a few benefits:

* You won't accidentally configure the root logger automatically because it's already configured.
* You can remove loggers that match your root logger settings (no need to override it if it's already default).
* You won't need to remember to add new packages to your loggers, unless you want to override the default logging levels set by your root logger.
* You probably currently have a bunch of packages that aren't logging because you forgot to add those to the loggers in settings.

## Installation

Run: `docker-compose up web`

## Usage

Visit: http://localhost:8080/

## Why does the example use uwsgi + docker + json formatted logs?

I ended up making a minimal threaded uwsgi + docker + django website that uses JSON formatted logging to troubleshoot this, but a lot of that ended up having nothing to do with the problem. I think this boilerplate is still useful though, so I'm keeping it in here.
