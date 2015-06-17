import os
currDirectory=os.path.dirname(os.path.realpath(__file__))
# print os.path.abspath(os.path.join(currDirectory, os.pardir))
path=os.path.abspath(os.path.join(os.path.abspath(os.path.join(currDirectory, os.pardir)), os.pardir))+'/Frontend/app/images/planit'
print path