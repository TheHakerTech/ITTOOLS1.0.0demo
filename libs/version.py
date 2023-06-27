# -*- coding: utf-8 -*-
def compareVersions(version1, version2):
    # 1.2.3 format
    version1 = version1.split(".")
    version2 = version2.split(".")
    for v1, v2 in zip(version1, version2):
        if int(v1) > int(v2):
            return 1
        elif int(v1) < int(v2):
            return -1
    return 0
