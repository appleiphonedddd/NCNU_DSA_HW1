def insertionsort(array):
    length = len(array)

    print(",".join(array))

    for i in range(1, length):
        key = array[i]
        j = i - 1

        key_class = key[0]
        key_num = int(key[1:])

        while j >= 0:
            j_class = array[j][0]
            j_num = int(array[j][1:])

            if (j_class > key_class) or (j_class == key_class and j_num < key_num):
                array[j + 1] = array[j]
                j -= 1
            else:
                break

        array[j + 1] = key

        if j + 1 != i:
            print(",".join(array))

if __name__ == "__main__":
    array = input().split(",")
    insertionsort(array)
