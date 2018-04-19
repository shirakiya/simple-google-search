import cerberus
from .search import schema as search_schema


schema_mapping = {
    'search': search_schema,
}


def get_validator(endpoint):
    schema = schema_mapping.get(endpoint)

    return cerberus.Validator(schema) if schema else None
