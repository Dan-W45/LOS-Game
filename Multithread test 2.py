import time, os
from multiprocessing import Pool

cores = os.cpu_count()
print("This machine has",str(cores),"cores")
print("This program will calculate the squares of 20000 numbers")

def sum_square(number):
    s = 0
    for i in range(number):
        s += i*i
    return s

if __name__ == "__main__":
    numbers = list(range(20000))
##    print("Input:  " + str(numbers))
    stime = time.time()
    pool = Pool(cores+1)
    result = pool.map(sum_square, numbers)
##    print("Output: " + str(result))
    print("Multi-threaded time:",str(time.time()-stime)+"s")

    pool.close()
    pool.join()

    result2 = []
    stime2 = time.time()
    for number in numbers:
        result2.append(sum_square(number))

##    print("Output: " + str(result2))
    print("Single-threaded time:",str(time.time() - stime2)+"s")

    input("To exit press enter")

