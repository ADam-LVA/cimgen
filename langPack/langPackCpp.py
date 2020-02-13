import os
import json

def location(version):
     return "BaseClass.h";

base = {
    "base_class": "BaseClass",
    "class_location": location
}

template_files = [ { "filename": "cpp_header_template.mustache", "ext": ".hpp" },
                   { "filename": "cpp_object_template.mustache", "ext": ".cpp" } ]

partials = { 'class':          '{{#langPack.format_class}}{{range}} {{dataType}}{{/langPack.format_class}}',
             'null_init_list': '{{#attributes}} _{{label}}({{#langPack._set_default}}{{dataType}}{{/langPack._set_default}}), {{/attributes}}'
           }

def format_class(text, render):
    result = render(text)
    tokens = result.split(' ')
    if len(tokens) < 2:
        return None;
    if (tokens[0]) == '':
        val = _get_rid_of_hash(tokens[1]);
        return val
    else:
        val = _get_rid_of_hash(tokens[0]);
        return val

# Some names are encoded as #name or http://some-url#name
# This function returns the name
def _get_rid_of_hash(name):
    tokens = name.split('#')
    if len(tokens) == 1:
        return tokens[0]
    if len(tokens) > 1:
        return tokens[1]
    return name

def _create_attribute_includes(text, render):
    unique = []
    include_string = ""
    in_ = render(text)
    jsonString1 = in_.replace("'", "\"")
    jsonString = jsonString1.replace("&quot;", "\"")
    if jsonString != None and jsonString != "":
        attributes = json.loads(jsonString)
        for attribute in attributes:
            clarse = ''
            if "range" in attribute:
                clarse = _get_rid_of_hash(attribute["range"])
            elif "dataType" in attribute:
                clarse = _get_rid_of_hash(attribute["dataType"])
            if clarse not in unique:
                unique.append(clarse)
    for clarse in unique:
        if clarse != "":
            if clarse == "String":
                include_string += '\n#include "String.hpp"'
            else:
                include_string += '\nclass ' + clarse + ';'

    return include_string

def _set_default(text, render):
    result = render(text)

    # the field {{dataType}} either contains the multiplicity of an attribute if it is a reference or otherwise the
    # datatype of the attribute. If no datatype is set and there is also no multiplicity entry for an attribute, the
    # default value is set to None. The multiplicity is set for all attributes, but the datatype is only set for basic
    # data types. If the data type entry for an attribute is missing, the attribute contains a reference and therefore
    # the default value is either None or [] depending on the mutliplicity. See also write_python_files
    if result in ['M:1', 'M:0..1', 'M:1..1', 'M:0..n', 'M:1..n', ''] or 'M:' in result:
        return '0'
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

def setup(version_path):
    if not os.path.exists(version_path):
        os.makedirs(version_path)

