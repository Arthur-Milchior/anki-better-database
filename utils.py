def commaJoin(l, f=(lambda x:x)):
    return ", ".join([f(x) for x in l])
