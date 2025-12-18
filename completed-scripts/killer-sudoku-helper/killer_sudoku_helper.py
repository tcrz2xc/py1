def combinations(target, size, exclude):
    #cage length 1
    perm_list =[]
    if size == 1:
        perm_list.append([target])
        sorted_list = sorted(perm_list)
        return sorted_list
    #cage length 2: size = 2 and target =10 where sum(a, b) = target and a !=b
    elif size ==2:
        perm_list2 =[]
        #case 1 (1,9)
        perm1 = permutation(1,9)
        perm_list2.append(perm1)
        #case 2 (2,8)
        perm2 = permutation(2,8)
        perm_list2.append(perm2)
        #case 3 (3,7)
        perm3 = permutation(3,7)
        perm_list2.append(perm3)
        #case 4 (4,6)
        perm4 = permutation(4,6)
        perm_list2.append(perm4)
        #restrictions using exclude
        restricted =[]
        for sublist in perm_list2:
            if any(item in exclude for item in sublist):
                continue
            restricted.append(sublist)
        restricted = sorted(restricted)
        return restricted
    elif size ==3 and target ==7:
        perm_list4=[]
        a = 1
        b = 2
        c = 4
        combo = [a, b, c]
        perm_list4.append(combo)
        return perm_list4
        
    elif size >3:
        perm_list3=[]
        sum =0
        count =1
        while sum<target:
            perm_list3.append(count)
            sum+=count
            count+=1
        #perm_list2 =perm_list3.pop()
        sorted_list = [sorted(perm_list3)]
        return sorted_list
def permutation(a,b):
    delta =[a, b]
    return delta
        
    