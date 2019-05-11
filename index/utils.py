"""
Copyright © 2019 Alita Index / Caeglathatur

This file is part of Alita Index.

Alita Index is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Alita Index is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Alita Index.  If not, see <https://www.gnu.org/licenses/>.
"""


def format_seconds(seconds):
    if seconds > 3600:
        # use hours
        number = '{:.0f}'.format(seconds / 3600) \
            if seconds % 3600 == 0 \
            else '{:.1f}'.format(seconds / 3600)
        unit = 'hour' if number == '1' else 'hours'
    elif seconds > 60:
        # use minutes
        number = '{:.0f}'.format(seconds / 60) \
            if seconds % 60 == 0 \
            else '~{:.0f}'.format(seconds / 60)
        unit = 'minute' if number == '1' else 'minutes'
    else:
        # use seconds
        number = '{:.0f}'.format(seconds)
        unit = 'second' if number == '1' else 'seconds'
    return '{} {}'.format(number, unit)


def format_minutes(minutes):
    if minutes > 60:
        # use hours
        number = '{:.0f}'.format(minutes / 60) \
            if minutes % 60 == 0 \
            else '{:.1f}'.format(minutes / 60)
        unit = 'hour' if number == '1' else 'hours'
    else:
        # use minutes
        number = '{:.0f}'.format(minutes)
        unit = 'minute' if number == '1' else 'minutes'
    return '{} {}'.format(number, unit)


def format_word_count(word_count):
    minutes = word_count / 200  # avg human reading wpm
    return '{} {} (~{})'.format(
        str(word_count),
        'word' if word_count == 1 else 'words',
        format_minutes(minutes),
    )
