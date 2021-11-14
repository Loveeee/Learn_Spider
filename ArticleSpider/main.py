from scrapy.cmdline import execute

import sys
import os

# 把当前目录添加到path中
now_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(now_path)

# execute(["scrapy", "crawl", "cnblogs"])
execute(["scrapy", "crawl", "zhihu"])
