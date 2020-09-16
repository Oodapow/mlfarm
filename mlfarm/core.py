import importlib

class ClassBuilder:
    '''The instance of this class is callable with or without arguments and the call will create an instance of the python class identifier passed to the constructor.

    Args:
        _class (str): A python class identifier, e.g. mlfarm.core.ClassBuilder
        args (dict | list | object | None): Arguments for the constructor of _class. If None, the default constructor in called.

    Returns:
        ClassBuilder: A callable object that returns the instance of the class with the arguments provided.

    As an example we will be using the following class:

    >>> class A:
    ...     def __init__(self, a):
    ...         self.a = a
    ...
    >>> a = A(1)
    >>> a.a
    1
    >>> cb = ClassBuilder("__main__.A", {"a": 2})
    >>> cb().a
    2
    >>> cb() == cb()
    False
    '''
    def __init__(self, _class, args):
        split = _class.split('.')
        mn = '.'.join(split[:-1])
        self._class = getattr(importlib.import_module(mn), split[-1])
        self.args = args
    
    def __call__(self, **args):
        if (not self.args) and args:
            self.args = args
        elif self.args and args:
            if isinstance(self.args, dict) and isinstance(args, dict):
                self.args.update(args)

        if not self.args:
            obj = self._class()
        elif isinstance(self.args, list):
            obj = self._class(*self.args)
        elif isinstance(self.args, dict):
            obj = self._class(**self.args)
        else:
            obj = self._class(self.args)
        
        return obj

class BaseVisitor:
    '''This is a fake implementation of the visitor pattern. It has the purpose of offering a way to transform nested dicts and lists. The BaseVisitor class is the Identity transform so it returs a clone of the object.
    
    >>> bv = BaseVisitor()
    >>> a = [1, {'a': 2}, 3]
    >>> b = bv.visit(a)
    >>> b
    [1, {'a': 2}, 3]
    >>> b[0] = 2
    >>> a
    [1, {'a': 2}, 3]
    '''
    def visit(self, obj):
        '''This method is to be called on the object to be transformed.

        Args:
            obj (str | object | list | dict): Object to be transformed.
        
        Returns:
            str | object | list | dict: The output of the transformation.
        '''
        if isinstance(obj, dict):
            return self.visit_dict(obj)
        elif isinstance(obj, list):
            return self.visit_list(obj)
        elif isinstance(obj, str):
            return self.visit_str(obj)
        else:
            return self.visit_obj(obj)

    def visit_obj(self, obj):
        '''This is here to be overwriten in a child class. We know the argument is not list, dict or str.

        Args:
            obj ( object ): Object to be transformed.
        
        Returns:
            str | object | list | dict: The same object.
        
        >>> class ObjVisitor(BaseVisitor):
        ...     def visit_obj(self, obj):
        ...         if obj % 2 == 0:
        ...             return obj // 2
        ...         else:
        ...             return (obj + 1) // 2
        ...
        >>> ov = ObjVisitor()
        >>> a = list(range(10))
        >>> ov.visit(a)
        [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        '''
        return obj

    def visit_str(self, obj):
        '''This is here to be overwriten in a child class. The argument is a string.

        Args:
            obj (str): Object to be transformed.
        
        Returns:
            str | object | list | dict: The same object.
        
        >>> class StrVisitor(BaseVisitor):
        ...     def visit_str(self, obj):
        ...         if obj == 'nok':
        ...             return 'error'
        ...         return obj
        ...
        >>> sv = StrVisitor()
        >>> a = [{'a': 'ok'}, {'b': 1}, {'c': 'nok'}]
        >>> sv.visit(a)
        [{'a': 'ok'}, {'b': 1}, {'c': 'error'}]
        '''
        return obj

    def visit_list(self, obj):
        '''This is here to be overwriten in a child class. The argument is a list.

        Args:
            obj (list): Object to be transformed.
        
        Returns:
            str | object | list | dict: The same object.
        
        >>> class ListVisitor(BaseVisitor):
        ...     def visit_list(self, obj):
        ...         try:
        ...             return sum(obj)
        ...         except:
        ...             return super().visit_list(obj)
        ...
        >>> lv = ListVisitor()
        >>> a = {'a': [1, 2, 3], 'b': 'ok', 'c': [1, 2, 'nok']}
        >>> lv.visit(a)
        {'a': 6, 'b': 'ok', 'c': [1, 2, 'nok']}
        '''
        return [self.visit(o) for o in obj]

    def visit_dict(self, obj):
        '''This is here to be overwriten in a child class. The argument is a dict.

        Args:
            obj (dict): Object to be transformed.
        
        Returns:
            str | object | list | dict: The same object.
        
        >>> class DictVisitor(BaseVisitor):
        ...     def visit_dict(self, obj):
        ...         try:
        ...             return { **obj, 'ab': obj['a'] + obj['b'] }
        ...         except:
        ...             return super().visit_dict(obj)
        ...
        >>> dv = DictVisitor()
        >>> a = [{'a': 'ok'}, {'b': 1}, {'a': 'o', 'b': 'k'}]
        >>> dv.visit(a)
        [{'a': 'ok'}, {'b': 1}, {'a': 'o', 'b': 'k', 'ab': 'ok'}]
        '''
        return dict([(k, self.visit(v)) for k, v in obj.items()])

class ContextAwareVisitor(BaseVisitor):
    '''Extends BaseVisitor to keep the path to the current node. It is designed to be extended and/or used for debugging.
    '''
    _path = []

    def get_path(self):
        '''To be used in an child class.

        Returns:
            str: Full path to current node.
        '''
        return ''.join(self._path)

    def visit_list(self, obj):
        '''Appends "[i]" for each i index in the list before calling the child visit.
        '''
        i = 0
        res = []
        for o in obj:
            self._path.append(f'[{i}]')
            res.append(self.visit(o))
            self._path.pop()
            i+=1
        return res

    def visit_dict(self, obj):
        '''Appends ".k" for each k key in the dict before calling the child visit.
        '''
        res = {}
        for k,v in obj.items():
            self._path.append(k if len(self._path) == 0 else f'.{k}')
            res[k] = self.visit(v)
            self._path.pop()
        return res

class CompositeVisitor(BaseVisitor):
    '''The visit method of this class will chain the object trough all the visitor parameters.

    Args:
        *args: Arguments as a list, each should be an implementation of the BaseVisitor class.

    >>> class StrVisitor(BaseVisitor):
    ...     def visit_str(self, obj):
    ...         if obj == 'nok':
    ...             return 0
    ...         return obj
    ...
    >>> class ListVisitor(BaseVisitor):
    ...     def visit_list(self, obj):
    ...         try:
    ...             return sum(obj)
    ...         except:
    ...             return super().visit_list(obj)
    ...
    >>> vl = [
    ...    StrVisitor(),
    ...    ListVisitor()
    ... ]
    ...
    >>> cv = CompositeVisitor(*vl)
    >>> a = {'a': [1, 2, 3], 'b': 'ok', 'c': [1, 2, 'nok']}
    >>> bo = vl[0].visit(a)
    >>> bo
    {'a': [1, 2, 3], 'b': 'ok', 'c': [1, 2, 0]}
    >>> bo = vl[1].visit(bo)
    >>> o = cv.visit(a)
    >>> o == bo
    True
    >>> o
    {'a': 6, 'b': 'ok', 'c': 3}

    '''
    def __init__(self, *args):
        self.args = args

    def visit(self, obj):
        for visitor in self.args:
            obj = visitor.visit(obj)
        return obj

class ClassVisitor(BaseVisitor):
    '''Extends BaseVisitor and transforms dicts into objects is a specific key is present.
    '''
    def visit_dict(self, obj):
        '''If the argument has the "class" key, an instance of that class will be returned.

        Args:
            obj (dict): May have the "class" key, if not the parent visit_dict is called.
        Returns:
            dict | object | ClassBuilder: If the "builder" key is also present the backend instance of ClassBuilder is returned.
        
        >>> class A:
        ...     def __init__(self, a):
        ...         self.a = a
        ...
        >>> cv = ClassVisitor()
        >>> data = {
        ...     "class": "__main__.A",
        ...     "builder": True,
        ...     "args": {
        ...         "a": 1
        ...     }
        ... }
        ...
        >>> a = cv.visit(data)
        >>> a().a
        1
        >>> a(a=2).a
        2
        '''
        if not obj.get('class', False):
            return super().visit_dict(obj)

        builder = ClassBuilder(
            obj['class'], 
            self.visit(obj.get('args', None))
        )

        if obj.get('builder', False):
            return builder

        return builder()

if __name__ == "__main__":
    # class A is used in the tests, for some reason __main__.A is not working in the doctest context.
    class A:
        def __init__(self, a):
            self.a = a
    import doctest
    doctest.testmod()