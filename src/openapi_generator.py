import textwrap
from importlib.util import spec_from_file_location, module_from_spec
from typing import Dict, Union

from pydantic import BaseModel
from pydantic.fields import Field


class OpenAPIGenerator:
    TYPE_MAPPING = {
        'int': 'integer',
        'float': 'number',
        'str': 'string',
        'bool': 'boolean',
        'list': 'array',
        'object': 'object'
    }

    def __init__(self):
        self.ref_cache: Dict[str, str] = {}
        self.specs = {}

    def load_file(self, module_path: str):
        module_name = module_path.rstrip('.py').replace('/', '.')
        spec = spec_from_file_location(module_name, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        for model_name in module.__all__:
            model = getattr(module, model_name)
            swagger = self.model_to_swagger(model, model_name)
            self.specs[model_name] = swagger

    TYPE = 'type: {type}'
    TITLE = 'title: {title}'
    REF = '{name}:' \
          '  $ref: {ref}'

    def model_to_swagger(self, model: Union[BaseModel, Field], model_name: str, indent: int=2) -> str:
        schema = model.schema()
        required = []
        properties = []
        ref = self.ref_cache.get(model_name)
        # enable recursive calls
        if schema['type'] == 'object':
            for key, prop in schema['properties'].items():
                if prop.get('required'):
                    required.append(key)
                prop_obj = model.__fields__[key]
                prop_swagger = self.model_to_swagger(prop_obj, key, indent)
                prop_swagger = textwrap.indent(prop_swagger, ' ' * indent)
                properties.append(prop_swagger)

        lines = [
            model_name + ':',
            self.TITLE.format(title=schema['title']),
            self.TYPE.format(type=self.TYPE_MAPPING[schema['type']]),
        ]

        if properties:
            properties = '\n'.join(properties)
            lines.append(properties)
        if required:
            required = '\n'.join(['  - ' + item for item in required])
            lines.append(required)

        return '\n'.join(lines)


