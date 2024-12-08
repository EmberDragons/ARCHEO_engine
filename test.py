def function(c):
    d={}
    l=c.split(' ')
    for mot in l:
        d[mot] = len(mot)
            
    return d


print(function("the cat was eating the mouse and time flying by like krazy"))