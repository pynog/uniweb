""" Generic entry point to extend an existing application with routes based on an existing Python package and following
a predefined schema.

"""

import yaml
from typing import Any, Union
from . import flask


def parse_schema(schema: str) -> dict:
  """

  :param schema:
  :return:
  """
  with open(schema) as fp:
    content = yaml.safe_load(fp)
  return content


def add_routes(app: Any, schema: Union[str, dict]):
  """

  :param app: The Web application to be extended with the routes
  :param schema: The schema definition for the extension
  """
  if not isinstance(schema, dict):
    schema = parse_schema(schema)
  if type(app).__name__ == "Flask":
    flask.add_routes(app, schema)
