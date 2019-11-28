import platform

# print(platform.system())

def osDetect():
    pf = platform.system()

    if pf=='Windows':
        return('W')
    elif pf=='Linux':
        return('L')
    else:
        return('M')
