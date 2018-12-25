from functools import wraps, partial
import inflection as inflection


_camelize = partial(inflection.camelize, uppercase_first_letter=False)


def _camelize_ref(ref):
    name = ref.rpartition('/')[2]
    camel_name = _camelize(name)
    return ref[:ref.rfind('/') + 1] + camel_name


def _camelize_prop(prop):
    if 'title' in prop:
        prop['title'] = _camelize(prop['title'])
    if '$ref' in prop:
        prop['$ref'] = _camelize_ref(prop['$ref'])
    if 'items' in prop and '$ref' in prop['items']:
        prop['items']['$ref'] = _camelize_ref(prop['items']['$ref'])
    return prop


def camelize(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        schema: dict = f(*args, **kwargs)
        definitions = schema.pop('definitions')
        schema['definitions'] = {}

        for k in definitions:
            definition = definitions[k]
            camel_k = _camelize(k)
            camel_title = _camelize(definition['title'])
            properties = definition.pop('properties')
            camel_properties = {
                _camelize(p): _camelize_prop(prop)
                for p, prop in properties.items()
            }
            definition['title'] = camel_title
            definition['properties'] = camel_properties
            if 'required' in definition:
                definition['required'] = [_camelize(req) for req in definition['required']]
            schema['definitions'][camel_k] = definition
        return schema

    return wrapper
