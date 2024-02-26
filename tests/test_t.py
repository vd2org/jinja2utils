import os
from tempfile import TemporaryDirectory

import pytest
from jinja2 import Environment, PrefixLoader, FileSystemLoader, TemplateNotFound
from jinja2utils import t_factory

TEMPLATE_EN1 = "Welcome, {{username}}!"
TEMPLATE_EN2 = "Goodbye, {{username}}!"
TEMPLATE_RU1 = "Привет, {{username}}!"
TEMPLATE_RU2 = "Пока, {{username}}!"


def test_t():
    with TemporaryDirectory() as tmpdir:
        for lang, file_name, content in (
                ('en/home', 'welcome', TEMPLATE_EN1),
                ('en/home', 'goodbye', TEMPLATE_EN2),
                ('ru/home', 'welcome', TEMPLATE_RU1),
                ('ru/home', 'goodbye', TEMPLATE_RU2),
        ):
            a = os.makedirs(f'{tmpdir}/{lang}/', exist_ok=True)
            print()
            with open(f'{tmpdir}/{lang}/{file_name}', 'w') as f:
                f.write(content)

        loader = PrefixLoader({
            'en': FileSystemLoader(f'{tmpdir}/en'),
            'ru': FileSystemLoader(f'{tmpdir}/ru'),
        })

        jinja = Environment(loader=loader)
        get_t = t_factory(jinja)

        t_en = get_t('en')
        rendered_en1 = t_en('home/welcome', username='John Doe')
        rendered_en2 = t_en('home/goodbye', username='John Doe')

        assert rendered_en1 == "Welcome, John Doe!"
        assert rendered_en2 == "Goodbye, John Doe!"

        t_ru = get_t('ru')
        rendered_ru1 = t_ru('home/welcome', username='Иван')
        rendered_ru2 = t_ru('home/goodbye', username='Иван')

        assert rendered_ru1 == "Привет, Иван!"
        assert rendered_ru2 == "Пока, Иван!"


def test_t_not_found():
    with TemporaryDirectory() as tmpdir:
        loader = PrefixLoader({
            'en': FileSystemLoader(f'{tmpdir}/en'),
        })

        jinja = Environment(loader=loader)
        get_t = t_factory(jinja)

        t = get_t('en')

        with pytest.raises(TemplateNotFound):
            t('welcome', username='John Doe')

        with pytest.raises(TemplateNotFound):
            t('home/goodbye', username='John Doe')
