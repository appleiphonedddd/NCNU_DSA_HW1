def selectsort(array):
    length = len(array)
    
    print(";".join(map(str, array)))
    
    # Selection sort
    for i in range(length - 1):
        min_index = i
        for j in range(i + 1, length):
            if array[j] < array[min_index]:
                min_index = j
        
        if min_index != i:
            array[i], array[min_index] = array[min_index], array[i]
            print(",".join(map(str, array)))

if __name__ == "__main__":
    array = list(map(int, input("").split(",")))
    selectsort(array)
