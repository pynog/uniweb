
import json
import logging
from typing import Any
from inspect import signature
import importlib

from flask import Flask, jsonify, request, make_response


class Table:

  def __init__(self, records: Any, key: str = "table1"):
    self._records = records
    self.key = key

  def toJson(self):
    return json.dumps({"column_def": [], "data": []})


def create_view_function(func, annotations: dict, method: str):
  def view_func(*args, **kwargs):
    defaults = dict(kwargs)
    if method == "GET":
      defaults.update(dict(request.args))
    else:
      defaults.update(dict(request.get_json()))
    for pmt, annotation in annotations.items():
      if annotation == 'int':
        defaults[pmt] = int(defaults[pmt])
    return func(**defaults)
  return view_func


def add_routes(app: Flask, schema: dict, verbose: bool = False):
  """

  :param app: The Flask Application to be extended
  :param schema: The API schema
  :param verbose: Flag to add log message
  """
  for path, details in schema["paths"].items():
    for method, endpoint in details.items():
      mod = importlib.import_module(endpoint["target"]["script"][:-3])
      mod_func = getattr(mod, endpoint["target"]["function"])
      if mod_func.__doc__ is not None:
        for line in mod_func.__doc__.split("\n"):
          print(line.lstrip())
      default_pmts, annotations = {}, {}
      for pmt, val in signature(mod_func).parameters.items():
        annotations[pmt] = val.annotation.__name__
        if val.default is not val.empty:
          default_pmts[pmt] = val.default
      method = method.upper()
      if verbose:
        logging.debug("")
      app.add_url_rule(rule=path, endpoint=path[1:],
                       view_func=create_view_function(mod_func, annotations, method),
                       methods=[method], defaults=default_pmts)


