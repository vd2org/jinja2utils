# jinja2utils

Useful utils for jinja2

## Install

```bash
pip install jinja2utils
```

## t_factory

t_factory is a small tool which helps prefixed templates easily.

See examples below.

#### Example:

- ./templates/en/home/welcome

```text
Welcome, {{username}}!
```

- ./templates/en/home/goodbye

```text
Welcome, {{username}}!
```

- ./templates/ru/home/welcome

```text
Welcome, {{username}}!
```

- ./templates/ru/home/goodbye

```text
Goodbye, {{username}}!
```

- ./main.py

```python
from jinja2 import Environment, PrefixLoader, FileSystemLoader
from jinja2utils import t_factory

loader = PrefixLoader({
    'en': FileSystemLoader('./templates/en'),
    'ru': FileSystemLoader('./templates/ru'),
})

jinja = Environment(loader=loader)
get_t = t_factory(jinja)


def print_templates(t, username):
    rendered1 = t('home/welcome', username=username)
    print(rendered1)

    rendered2 = t('home/goodbye', username=username)
    print(rendered2)


print_templates(get_t('en'), 'John Doe')
# Expected output:
# Welcome, John Doe!
# Goodbye, John Doe!

print_templates(get_t('ru'), 'Иван')
# Expected output:
# Привет, Иван!
# Пока, Иван!
``` 

## plural

`plural` is jinja2 filter function for easy text pluralization.

#### Example:

- ./templates/info/users

```text
System have {{users}} active {{users|plural('en','user','users')}}.
```

```python
# main.py
from jinja2 import Environment, FileSystemLoader
from jinja2utils import plural

jinja = Environment(loader=FileSystemLoader('./templates'))
jinja.filters['plural'] = plural

template1 = jinja.get_template('info/users')
rendered1 = template1.render(users=1)
print(rendered1)  # System have 1 active user.
rendered2 = template1.render(users=23)
print(rendered2)  # System have 23 active users.
``` 

## elapsed and remaining

Calculates and formats elapsed time to string like this:
`25d 4h 3m 35s`. Can be used as jinja2 filter.

#### Example:

- ./templates/info

```text
System uptime: {{started|elapsed(show_seconds=True)}}.
``` 

- ./templates/newyear

```text
System uptime: {{started|elapsed(show_seconds=True)}}.
```

```python
# main.py
from jinja2 import Environment, FileSystemLoader
from jinja2utils import elapsed, remaining
import datetime

jinja = Environment(loader=FileSystemLoader('./templates'))
jinja.filters['elapsed'] = elapsed
jinja.filters['remaining'] = remaining

started = datetime.datetime.now()
newyear = datetime.datetime(2025, 1, 1, 0, 0, 0)

username = 'John Doe'
template1 = jinja.get_template('info/uptime')
rendered1 = template1.render(started=started)
print(rendered1)  # System uptime: 25d 4h 3m 35s.

template2 = jinja.get_template('info/newyear')
rendered2 = template2.render(newyear=newyear)
print(rendered2)  # To next year remaining 295d 10h 13m 10s!
``` 

## uchar

Simple jinja2 function to insert unicode characters
by unicode names. Very useful for inserting emoji.

#### Example:

- ./templates/info/users

```text
Welcome, {{username}} {{UN('THUMBS UP SIGN')}}!
```

```python
# main.py
from jinja2 import Environment, FileSystemLoader
from jinja2utils import uchar

jinja = Environment(loader=FileSystemLoader('./templates'))
jinja.globals['UN'] = uchar

template1 = jinja.get_template('info/users')
rendered1 = template1.render(username='John Doe')
print(rendered1)  # Welcome, John Doe 👍!
``` 

