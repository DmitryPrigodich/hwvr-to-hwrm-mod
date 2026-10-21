"""Shared review labels for the current campaign reading documents."""
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = json.loads((ROOT/'localization/reviewed_changes.json').read_text(encoding='utf8'))


def review_label(key, text):
    row = REVIEW['lines'].get(key)
    if row is None:
        return ''
    if hashlib.sha256(text.encode('utf8')).hexdigest() != row['ru_sha256']:
        return 'Текст изменён после согласования — нужна повторная сверка.'
    day=date.fromisoformat(row['reviewed_on'])
    months=('января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря')
    return f'Внесена правка пользователя · {day.day} {months[day.month-1]} {day.year}'


def review_notice(link='TRANSLATION_REVIEW.md'):
    return ('Актуальный перевод: сверка ' + REVIEW['date_label'] + '. '
            '[Что уже исправлено](' + link + '). '
            'Блоки «Старый русский» и архив RAW сохраняют исходный перевод для сравнения.')
