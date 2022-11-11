#!/usr/bin/env python
# coding: utf-8

import re
import yaml
from click.types import ParamType

class FieldThing(ParamType):
    name = "field=thing"
    envvar_list_splitter = r","

    def convert(self, value, param, ctx):
        if isinstance(value, dict):
            return value
        try:
            if m := re.match(r"\s*([^=]+)\s*=\s*(.+)\s*", value):
                v = yaml.safe_load(m.group(2))
                return {m.group(1): v}
            self.fail(f'unable to grok "{value}"')
        except Exception as _erp:
            self.fail(f'unable to grok "{value}": {_erp}')
