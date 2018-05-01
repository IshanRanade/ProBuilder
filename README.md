To run the program, open up Maya 2017, open up the Script Editor, and paste the following Python code and run.
Replace the Probuilder path with the path to wherever you downloaded this repo.

```python
import maya.cmds as cmds

cmds.unloadPlugin('ProBuilder')
cmds.loadPlugin('/Users/ishan/Documents/UniversityOfPennsylvania/UniversityOfPennsylvania/Spring2018/CIS660/ProBuilder/ProBuilder.py')

```