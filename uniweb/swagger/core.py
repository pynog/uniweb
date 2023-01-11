"""
"""

from decimal import Rounded
from enum import Enum
from pydoc import describe
from unittest.mock import CallableMixin
from xml.sax.xmlreader import Locator
from . import response
from typing import Callable, Literal, Optional


class Locations(Enum):
    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    COOKIE = "cookie"


class Route:

    def __init__(self, alias: str, method: str, description: str = "", operationId: str = None):
        """ Create the route.

        .. _a link: https://github.com/OAI/OpenAPI-Specification/blob/main/examples/v3.0/petstore-expanded.yaml

        :param alias:
        :param method: 
        :param description: 
        :param operationId: 
        """
        self.__alias = alias
        self.__dsc = description
        self._responses = {}
        self.__parameters = []

    @property
    def alias(self):
        return self.__alias
    
    @property
    def description(self):
        return self.__dsc

    @property
    def parameters(self):
        return self.__parameters

    def attach(self, py_func: Callable):
        if py_func.__doc__ is not None:
            self.__dsc = py_func.__doc__

    def add_parameter(self, name: str, in_: Literal[Locations.QUERY], description: str = "", required: bool = False, 
                      deprecated: bool = False, allowEmptyValue: bool = True,  style: str = None):
        """

        .. _a link: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md

        :param name:
        :param in_:
        :param description: A brief description of the parameter. This could contain examples of use. CommonMark syntax MAY be used for rich text representation
        :param required:
        :param deprecated:
        :param style:
        """
        if in_ == "path":
            required = True
        self.__parameters.append({"name": name, "in": in_, "description": description, "required": required})

    def get_parameter(self, name: str) -> Optional[dict]:
        """
        :param name: 
        """
        for pmt in self.__parameters:
            if pmt["name"] == name:
                return pmt

    def add_response(self, code: str, content: response.Content, description: str = ""):
        """ Add a response.

        .. _a link: https://github.com/OAI/OpenAPI-Specification/blob/main/examples/v3.0/petstore-expanded.yaml

        :param code: The HTML code status
        :param content: The content response
        :param description: The response description
        """
        resp = {"description": description, "content": response.Content()}
        self._responses[code] = resp
        return resp


class Schema:
    
    def __init__(self, type: str, format: str = None, version: str = "3.1.0"):
        self.__ctx = {"paths": []}

    def add_info(self, version: str, title: str, description: str, terms_of_service: str = None):
        ... 

    def add_contact(self, name: str, email: str, url: str):
        ...

    def add_license(self, url: str):
        ...
        
    def add_item(self, type: str):
        ...

    def add_server(self, url: str, description: str = None):
        """ Add different server configurations for the API.

        :param url:
        :param description:
        """
        if "servers" not in self.__ctx:
            self.__ctx["servers"] = []
        server_config = {"url": url}
        if description is not None:
            server_config["description"] = description
        self.__ctx["servers"].append(server_config)

    def add_path(self, alias: str, method: str, py_func = None) -> Route:
        swagger_path = Route(alias, method)
        if py_func is not None:
            swagger_path.attach(py_func)
        self.__ctx["paths"].append(swagger_path)

        return swagger_path

