Replace the probuilderPath with the path to wherever you downloaded this repo.


```python
import sys
probuilderPath = '/Users/ishan/Documents/UniversityOfPennsylvania/UniversityOfPennsylvania/Spring2018/CIS660/ProBuilder'
if probuilderPath not in sys.path:
    sys.path.append(probuilderPath)

import ProBuilder
reload(ProBuilder)
```