import json, sys
import numpy as np
from veusz.plugins import *

class ImportJSON(ImportPlugin):
    """
    Read data from JSON file
    """

    name = "LoadJSON"
    author = "Brunetto Ziosi <brunetto.ziosi@gmail.com>"
    description = "Reads data form a JSON file"

    # Uncomment this line for the plugin to get its own tab
    promote_tab='LoadJSON'

    file_extensions = set(['.json'])
    
    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            ImportFieldText("name", descr="Dataset name", default="name"),
            ]

    def doImport(self, params):
        """Actually import data
        params is a ImportPluginParams object.
        Return a list of ImportDataset1D, ImportDataset2D objects
        """
        f = params.openFileWithEncoding()
        data = []
        errbar = None
        tmp = json.load(f)
        #for name, value in iter(sorted(tmp.iteritems())):
        # This is to be compatible with both python 2 and 3 
        # and run with both veusz qt4 and qt5s
        for name, value in iter(sorted(((key,tmp[key]) for key in tmp))):
            if name.endswith("errbar"):
                errbar=value
                data.append(ImportDataset1D(name=name, data=value))
                continue
            elif name.endswith("-witherr"):
                data.append(ImportDataset1D(name=name, data=value, serr=errbar))
                errbar=None
                continue
            else:
                #print(value)
                #print(type(value[0]))
                # This is to be compatible with both python 2 and 3 
                # and run with both veusz qt4 and qt5s
                if sys.version < '3':
                    str_types = [str, unicode]
                else:
                    str_types = [str, bytes]
                try:
                    if type(value[0]) in str_types:
                        data.append(ImportDatasetText(name, value))
                    else:
                        data.append(ImportDataset1D(name, value))
                except:
					continue
        return data

# add the class to the registry. An instance also works, but is deprecated
importpluginregistry.append(ImportJSON)
