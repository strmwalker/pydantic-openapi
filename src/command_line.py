from src.openapi_generator import OpenAPIGenerator


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Turn files with pydantic models to OpenAPI JSON schema. '
                                                 'Config file have priority over arguments.')
    parser.add_argument('--config', type=str)
    parser.add_argument('--modules', nargs='+', help='files with Pydantic models',
                        type=str, metavar='module')
    parser.add_argument('--title', type=str, help='schema title')
    parser.add_argument('--indent', type=int, help='output indent', default=2)
    parser.add_argument('--prefix', type=str, help='reference prefix', default='#/components/schemas/')
    parser.add_argument('--file', type=argparse.FileType, help='description file')
    parser.add_argument('--text', type=str, help='description text')
    parser.add_argument('--output', type=str, help='output file')

    args = parser.parse_args()

    if args.config:
        from configparser import ConfigParser
        config_parser = ConfigParser(allow_no_value=True)
        config_parser.read(args.config)

        generator_options = config_parser['generator options']
        title = generator_options.get('title') or args.title
        indent = int(generator_options.get('indent') or args.indent)
        prefix = generator_options.get('prefix').strip('"') or args.prefix
        description = generator_options.get('description') or args.description
        if 'modules' in config_parser.sections():
            modules = [k for k in config_parser['modules']]
        else:
            modules = args.modules
    else:
        title = args.title
        indent = args.indent
        prefix = args.prefix
        modules = args.modules
        description = args.text
    generator = OpenAPIGenerator(title=title, indent=indent, ref_prefix=prefix,
                                 description=description)

    for module in modules:
        generator.load_module(module)

    if args.output:
        with open(args.output, 'w') as o:
            o.write(generator.render())
    else:
        print(generator.render())


if __name__ == '__main__':
    main()