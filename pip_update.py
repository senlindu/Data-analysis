# 查询所有过期库
# pip  list --outdated
# 批量升级过期库，实际上是通过循环逐个升级
import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions
for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)