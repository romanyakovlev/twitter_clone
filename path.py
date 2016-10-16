import os

[x for x in os.scandir('./dea/') if x.is_dir()]
