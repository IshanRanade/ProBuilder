To run the program, open up Maya 2017, open up the Script Editor, and paste the following Python code and run.
Replace the probuilderPath with the path to wherever you downloaded this repo.

The following code will first delete all geometry in the scene and then run the ProBuilder program.


```python
import maya.cmds
import maya.mel
import sys

probuilderPath = '/Users/ishan/Documents/UniversityOfPennsylvania/UniversityOfPennsylvania/Spring2018/CIS660/ProBuilder'
if probuilderPath not in sys.path:
    sys.path.append(probuilderPath)
    
if globals().has_key('init_modules'):
	for m in [x for x in sys.modules.keys() if x not in init_modules]:
		del(sys.modules[m]) 
else:
	init_modules = sys.modules.keys()


import ProBuilder

```