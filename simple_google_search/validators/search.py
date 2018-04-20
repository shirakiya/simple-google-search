schema = {
    'type': {
        'type': 'string',
        'required': False,
        'allowed': ['web', 'custom'],
    },
    'query': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
}
