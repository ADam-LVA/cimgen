import os

def location(version):
     return "cimpy." + version + ".Base";

base = {
    "base_class": "Base",
    "class_location": location
}

template_files=[ { "filename": "cimpy_class_template.mustache", "ext": ".py" } ]

partials = {}

# called by chevron, text contains the label {{dataType}}, which is evaluated by the renderer (see class template)
def _set_default(text, render):
    result = render(text)

    # the field {{dataType}} either contains the multiplicity of an attribute if it is a reference or otherwise the
    # datatype of the attribute. If no datatype is set and there is also no multiplicity entry for an attribute, the
    # default value is set to None. The multiplicity is set for all attributes, but the datatype is only set for basic
    # data types. If the data type entry for an attribute is missing, the attribute contains a reference and therefore
    # the default value is either None or [] depending on the mutliplicity. See also write_python_files
    if result in ['M:1', 'M:0..1', 'M:1..1', '']:
        return 'None'
    elif result in ['M:0..n', 'M:1..n'] or 'M:' in result:
        return '"list"'

    result = result.split('#')[1]
    if result in ['integer', 'Integer']:
        return '0'
    elif result in ['String', 'DateTime', 'Date']:
        return "''"
    elif result == 'Boolean':
        return 'False'
    else:
        # everything else should be a float
        return '0.0'

def _create_init(path):
    init_file = path + "/__init__.py"
    with open(init_file, 'w'):
        pass

# creates the Base class file, all classes inherit from this class
def _create_base(path):
    base_path = path + "/Base.py"
    base = ['from enum import Enum\n\n', '\n', 'class Base():\n', '    """\n', '    Base Class for CIM\n',
            '    """\n\n',
            '    cgmesProfile = Enum("cgmesProfile", {"EQ": 0, "SSH": 1, "TP": 2, "SV": 3, "DY": 4, "GL": 5, "DI": 6})',
            '\n\n', '    def __init__(self, *args, **kw_args):\n', '        pass\n',
            '\n', '    def printxml(self, dict={}):\n', '        return dict\n']

    with open(base_path, 'w') as f:
        for line in base:
            f.write(line)

def setup(version_path):
    if not os.path.exists(version_path):
        os.makedirs(version_path)
        _create_init(version_path)
        _create_base(version_path)

