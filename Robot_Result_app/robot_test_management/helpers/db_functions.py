from django.db.models import Func


class JSONBDeleteKey(Func):
    function = '#-'
    template = '"attributes" #- ARRAY[%(key)s]'
    
    def __init__(self, key, **extra):
        key_as_array = '\'{}\''.format(key)  
        super(JSONBDeleteKey, self).__init__(key=key_as_array, **extra)

class JSONBRenameKey(Func):
    function = 'jsonb_set'
    template = "%(function)s(%(expressions)s - '%(old_key)s', '{%(new_key)s}', %(expressions)s->'%(old_key)s')"

    def __init__(self, expression, old_key, new_key, **extra):
        super(JSONBRenameKey, self).__init__(expression, old_key=old_key, new_key=new_key, **extra)


class JSONBSet(Func):
    function = 'jsonb_set'
    template = "%(function)s(%(expressions)s, '{\"%(key_name)s\"}', '\"%(default_value)s\"', true)"

    def __init__(self, expression, key_name, default_value, **extra):
        super(JSONBSet, self).__init__(expression, key_name=str(key_name), default_value=str(default_value), **extra)
