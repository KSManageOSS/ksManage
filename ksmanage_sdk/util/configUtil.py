# -*- coding:utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import copy
import os
import yaml
import sys

modelRoute = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                          "route", "modelRoute.yml")
interfaceRoute = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                              "route", "interfaceRoute.yml")


# get yaml config util,singleton type
class configUtil():
    def __init__(self):
        pass

    # sinlge
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            if sys.version_info < (3, 0):
                cls._instance = super(configUtil, cls).__new__(cls, *args, **kwargs)
            else:
                cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def getRouteOption(self, productName, bmcVersion=None, ipmi_mode=None):
        # if True:
        try:
            with open(modelRoute, "r") as file:
                modeldict = yaml.safe_load(file)

            with open(interfaceRoute, "r") as file:
                interfacedict = yaml.safe_load(file)
            content = {}
            for key, value in modeldict.items():
                for productname in value:
                    content[productname.upper()] = interfacedict.get(key)

            if content.get(productName.upper(), None):
                model_info = content.get(productName.upper())
                model_keysV = copy.deepcopy(list(model_info.keys()))
                if model_info.get("platform") == "M7":
                    if ipmi_mode == "M7_redfish":
                        model_info = interfacedict.get("OpenBmcE2")
                        model_keysV = copy.deepcopy(list(model_info.keys()))
                platform = model_info["platform"]
                model_keysV.remove("platform")
                model_keysV.remove('common')
                model_keys = []
                for model_key in model_keysV:
                    model_keys.append(model_key.replace("V", ""))
                if (bmcVersion is None or len(model_keys) == 0) and model_info.get('common'):
                    return model_info.get("common"), platform
                elif len(model_keys) >= 1:
                    model_keys.sort()

                    if float(bmcVersion) < float(model_keys[0]):
                        return model_info.get("common")
                    if len(model_keys) > 1:
                        for i in range(len(model_keys) - 1):
                            if float(bmcVersion) >= float(model_keys[i]) and float(bmcVersion) < float(
                                    model_keys[i + 1]):
                                return model_info.get("V" + str(model_keys[i])), platform
                    return model_info.get("V" + str(model_keys[len(model_keys) - 1])), platform
                else:
                    return "Error: Not find interface of {0}".format(productName), None
            return "Error: sdk does not support {0} at present.".format(productName), None
        except Exception as e:
            return "Error: " + str(e), None

    def get_platform(self, pn):
        hosttype = ""
        with open(modelRoute, "r") as file:
            modeldict = yaml.safe_load(file)

        with open(interfaceRoute, "r") as file:
            interfacedict = yaml.safe_load(file)

        for key, value in modeldict.items():
            if pn in value:
                return interfacedict.get(key).get("platform")
        return hosttype

    def getModelSupport(self, model="KR"):
        # try:
        yaml1 = open(modelRoute)
        content = yaml.load(yaml1, Loader=yaml.BaseLoader)
        yaml1.close()
        ks_list = []
        nf_list = []
        for key in content.keys():
            values = content.get(key)
            for value in values:
                if "KR" in value and model=="KR":
                    ks_list.append(value)
                elif "KR" not in value and model=="NF":
                    nf_list.append(value)
        if model=="KR":
            return list(ks_list)
        else:
            return list(nf_list)
        

if __name__ == '__main__':
    fruclass = configUtil()
    abc = fruclass.getRouteOption("NF5280M7", "5.3.0")
    print(abc)
