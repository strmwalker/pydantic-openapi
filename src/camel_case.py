from functools import wraps, partial
import inflection as inflection


_camelize = partial(inflection.camelize, uppercase_first_letter=False)


def _camelize_ref(prop):
    ref = prop['$ref']
    name = ref.rpartition('/')[2]
    camel_name = _camelize(name)
    prop['$ref'] = ref[:ref.rfind('/') + 1] + camel_name
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
            camel_properties = {}
            for p in properties:
                camel_p = _camelize(p)
                prop = properties[p]
                if 'title' in prop:
                    prop['title'] = _camelize(prop['title'])
                if '$ref' in prop:
                    prop = _camelize_ref(prop)
                if 'items' in prop and '$ref' in prop['items']:
                    prop['items'] = _camelize_ref(prop['items'])
                camel_properties[camel_p] = prop

            definition['title'] = camel_title
            definition['properties'] = camel_properties
            schema['definitions'][camel_k] = definition
        return schema

    return wrapper
