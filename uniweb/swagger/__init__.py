""" Generate the OpenAPIv3 swagger file.
File should be based on the following standards: https://swagger.io/
"""

import sys
import importlib

from typing import Union
from ..api import parse_schema
from . import core


def build(schema: Union[str, dict], output: str = None):
  """
  description:
  content:
            application/json:

  """
  if not isinstance(schema, dict):
    schema = parse_schema(schema)
  for path, details in schema["paths"].items():
    for method, endpoint in details.items():
        if endpoint["target"].get("package", {}).get("path") is not None:
            sys.path.append(endpoint["target"]["package"]["path"])
        if endpoint["target"].get("package", {}).get("name") is not None:
            mod = importlib.import_module("%s.%s" % (endpoint["target"]["package"]["name"], endpoint["target"]["script"][:-3]))
        else:
            mod = importlib.import_module(endpoint["target"]["script"][:-3])
        mod_func = getattr(mod, endpoint["target"]["function"])
        core.Route(path, method)

