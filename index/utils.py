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
