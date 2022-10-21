from os import  sys, path
sys.path.append("..")

import os

import yaml
import re
from lib import helper

"""
Example:
    from lib import yamltools as lc

    file = "{}/{}".format( path.dirname(__file__) , "appconfig.yaml")
    yt = lc.yamlHelper()
    settings = yt.load(file)
    log.info(yt.data.password)
"""


class yamlHelper():
    """yaml config loader with secrets"""
    secrets={}
    yamldata={}
    __VERSION__ = "1.0.0"

    def __init__(self):
        """constructor for yaml helper"""
        self.yamldata = {}

    @property
    def data(self):
        """get the yaml document python object class"""
        if self.yamldata:
            return helper.dataClass(self.yamldata)
        return helper.dataClass(None)


    def loadYaml(self, file:str=None) -> dict:
        """load the yaml file and converts the yaml document to python object"""
        try:
            if os.path.isfile(file):
                with open(file, 'rb') as f:
                    # Converts yaml document to python object
                    return yaml.load(f, Loader=yaml.SafeLoader)
        except BaseException as e:
            print(f"Error {__package__}, {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
            return None


    def saveDictAsYamlFile(self, data:dict=None, filename:str=None)->bool:
        """saved the dict data as yaml to the defined file"""
        def represent_str(dumper, instance):
            """representer for yaml file formatting"""
            if "\n" in instance:
                instance = re.sub(' +\n| +$', '\n', instance)
                return dumper.represent_scalar('tag:yaml.org,2002:str',instance,style='|')
            else:
                return dumper.represent_scalar('tag:yaml.org,2002:str',instance)
        try:
            yaml.add_representer(str, represent_str)
            yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()))
            yaml.sort_base_mapping_type_on_output = False
            with open(filename, "w") as output:
                yaml.dump(data,
                        output,
                        allow_unicode=True,
                        encoding='utf-8',
                        sort_keys=False,
                        default_flow_style=False)
        except BaseException as e:
            print(f"Error {__package__}, {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
            return False
        return True


    def yaml_include(self, loader, node):
        """include another yaml file with !include tag"""
        file_name = os.path.join(os.path.dirname(loader.name), node.value)
        with open(file_name, 'rb') as f:
             return yaml.load(f, Loader=yaml.SafeLoader)

    def secrets_handler(self, loader, node):
        """Load !secrets tag"""
        key = str(loader.construct_scalar(node))
        if key in self.secrets:
            return self.secrets[key]

    def data_handler(self, loader, node):
        """Load !data tag"""
        key = str(loader.construct_scalar(node))
        if key in self.data:
            return self.data[key]

    def get_loader(self):
        """Get custom loaders."""
        loader = yaml.SafeLoader
        loader.add_constructor("!secret", self.secrets_handler)
        loader.add_constructor("!data", self.data_handler)
        loader.add_constructor("!include", self.yaml_include)
        return loader

    def load(self, yamlfile:str=None, secretsfile:str=None) -> dict:
        """load the yaml file"""
        try:
            if yamlfile and not secretsfile:
                secretsfile = "{}/secrets.yaml".format(os.path.dirname(yamlfile) )
            if yamlfile and os.path.isfile(yamlfile):
                if secretsfile and os.path.isfile(secretsfile):
                    self.secrets = self.loadYaml(secretsfile)
                    self.yamldata = yaml.load(open(yamlfile, "rb"), Loader=self.get_loader())
                else:
                    self.secrets = self.loadYaml(yamlfile)
            return self.yamldata
        except BaseException as e:
            print(f"Error {__package__}, {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
            return None