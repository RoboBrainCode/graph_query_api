import numpy as np
import json
import pickle
import os
from showheatmap import funcMain
currDirectory=os.path.dirname(os.path.realpath(__file__))
def parse(input1):
    for key,val in input1.iteritems():
        x_str=""
        # print type(val)
        if type(val)==np.ndarray:
            x_arrstr = np.char.mod('%f', val)
            x_str = ",".join(x_arrstr)
        elif type(val)==list:
            for i in range(len(val)):
                val[i]=str(val[i])
            x_str=",".join(val)
        else:
            x_str=str(val)
        input1[key]=x_str
    return input1

with open('params_task_entertainment.pik','rb') as ff:
        params = pickle.load(ff)

for key,val in params.iteritems():
    activity_name=key
    print activity_name
    val['pi']=str(val['pi'])
    param_pi="{"+'"pi":'+json.dumps(val['pi'])+"}"
    param_human=json.dumps(parse(val['human']))
    param_object=json.dumps(parse(val['object']))
    with open ("template", "r") as myfile:
        data=myfile.read()
    fname = "heatmap_activity_{0}".format(activity_name)
    pathName=currDirectory+'/heatmap/'+fname+'.png'
    newdata=data % {'activity':activity_name,'mediapath':pathName,'param_pi':param_pi,'param_human':param_human,'param_object':param_object}
    with open('json/'+activity_name+'.json','w') as f:
        f.write(newdata);
    funcMain(activity_name,'params_task_entertainment.pik',pathName)
