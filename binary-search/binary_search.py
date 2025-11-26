def find(search_list, value):
    try:
        #sort list first so that you can find the value 
        sorted_search_list = sorted(search_list)
        middle = len(sorted_search_list)//2
        #sorted_search_list = sorted_search_list[:middle]+sorted_search_list[middle+1:]
        #middle element is the value
        if sorted_search_list[middle] == value:
            return middle
        #middle element is smaller than the value
        elif sorted_search_list[middle]<value:
            return middle + find(sorted_search_list[middle:], value)
        else:
            return find(sorted_search_list[:middle], value)
    except:
        raise ValueError("value not in array")
            
    
