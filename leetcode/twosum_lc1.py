a = [4,2,3,5,12]
sumv = 8
h = {}
for i in a:
    k = sumv - i
    if(h.get(k,-1) == -1):
        h[i] = i
    else:
        print(i, h.get(k))
