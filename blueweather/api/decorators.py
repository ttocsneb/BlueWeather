"""
Api Decorators
"""

from typing import Type, Optional


class Api:
    """
    Api Handler

    :param func: api function
    :param method: allowed request method types
    :param schema: result schema
    :param args_schema: request schema
    """
    def __init__(self, **kwargs):
        self.func: callable = kwargs.pop('func')
        self.method: Optional[str] = kwargs.pop('method')
        self.args_schema: Optional[Type[Schema]] = kwargs.pop('args_schema')
        self.schema: Optional[Type[Schema]] = kwargs.pop('schema')
