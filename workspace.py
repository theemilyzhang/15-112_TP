import math

def updateBRange(brange, restriction):
    if brange == []:
        if restriction[1] > restriction[0]:
            r1 = (0, restriction[0])
            r2 = (restriction[1], 2*math.pi)
            brange.append(r1)
            brange.append(r2)
        else:
            brange.append((restriction[1], restriction[0]))
    else:
        index = 0
        while index < len(brange):
            curTuple = brange[index] #copy, not a reference
            #if both ends of restriction w/in curTuple, create 2 new restriction tuples
            if (curTuple[0] < restriction[0] < curTuple[1] and
                    curTuple[0] < restriction[1] < curTuple[1]):
                brange[index] = (curTuple[0], restriction[0])
                newTuple = (restriction[1], curTuple[1])
                brange.insert(index+1, newTuple)
                index += 2
            elif (curTuple[0] < restriction[0] < curTuple[1]):
                brange[index] = (curTuple[0], restriction[0])
                index += 1
            elif (curTuple[0] < restriction[1] < curTuple[1]):
                brange[index] = (restriction[1], curTuple[1])
                index += 1
            else:
                index += 1

brange = []

updateBRange(brange, (340*math.pi/180, 20*math.pi/180))
print (brange)
updateBRange(brange, (90*math.pi/180, 180*math.pi/180))
print (brange)
updateBRange(brange, (330*math.pi/180, 350*math.pi/180))
print (brange)
updateBRange(brange, (340*math.pi/180, 20*math.pi/180))
print (brange)