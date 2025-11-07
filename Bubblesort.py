def bubblesort(array):

    length = len(array)
    print(";".join(map(str, array)))

    for i in range(length-1):
        for j in range(length-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                print(";".join(map(str, array)))
    
if __name__ == "__main__":

    array = list(map(int, input().split(";")))
    bubblesort(array)
