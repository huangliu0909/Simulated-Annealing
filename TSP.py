import random
import math
import time


def read_countries(filename):
    # generate a map from a file
    result = {}
    test_file = open(filename, 'r+', encoding='utf-8')
    test_list = test_file.read().splitlines()
    flag = 0
    for s in test_list:
        ss = s.split("\t")
        # print(ss)
        i = 0
        result[flag] = {}
        for num in ss:
            if len(num) > 0:
                result[flag][i] = int(num)
                i += 1
        flag += 1
    return result


def generate_countries(n):
    # generate a map randomly
    # n : the number of points
    result = {}
    for i in range(n):
        result[i] = {}
        for j in range(i, n):
            if i == j:
                result[i][j] = 0
            else:
                r = random.random()
                while r == 0:
                    r = random.random()
                result[i][j] = int(r * 100)
    for i in range(n):
        for j in range(0, i):
            result[i][j] = result[j][i]
    return result


def getNextRoute(origin_route, n):
    # update the route, basing on the current route, randomly change two points
    new_route = {}
    x1 = int(n * random.random())
    x2 = int(n * random.random())
    while (x1 == x2) | (x1 == 0) | (x2 == 0):
        if x1 == 0:
            x1 = int(n * random.random())
        else:
            x2 = int(n * random.random())
    for i in range(len(origin_route)):
        if i == x1:
            new_route[i] = origin_route[x2]
        elif i == x2:
            new_route[i] = origin_route[x1]
        else:
            new_route[i] = origin_route[i]
    return new_route


def getLength(map, origin_route):
    # get the length of a route in a certain map
    l = 0
    for i in range(len(origin_route) - 1):
        l += map[origin_route[i]][origin_route[i + 1]]
    return l


def find_min(map, origin_route, n, T_min):
    t = 0
    T = 2000
    min = getLength(map, origin_route)
    min_route = {}
    while T > T_min:
        t += 1
        T = 2000 / (1 + t)
        # print(origin_route)
        new = getNextRoute(origin_route, n)
        if min > getLength(map, origin_route):
            # update min
            min_route = origin_route
            min = getLength(map, origin_route)
            # print(min)
            # print(min_route)
        if getLength(map, origin_route) > getLength(map, new):
            # if better, update
            origin_route = new
        else:
            # accept randomly
            delta = getLength(map, new) - getLength(map, origin_route)
            p = math.exp(-delta/T)
            if random.random() < p:
                origin_route = new
    # print("finish while")
    # print(min)
    # print(min_route)
    return min, min_route


if __name__ == '__main__':

    file = "origin20.txt"
    countries = read_countries(file)
    # print(countries)
    N = 20
    # num of countries
    origin = {}
    for i in range(N):
        origin[i] = i
    print(origin)
    # countries = generate_countries(N)
    min_min = 10000000
    min_min_route = {}
    circle_times = 20
    # times to repeat
    T_m = 10
    # min value of T
    start = time.time()
    for i in range(circle_times):
        m, r = find_min(countries, origin, N, T_m)
        if m < min_min:
            min_min = m
            min_min_route = r
    end = time.time()
    print("finish Monte-carlo")
    print(min_min)
    print(min_min_route)
    print(str(end - start) + " s")

    '''
    f = open('origin5.txt', 'w', encoding='utf-8')
    for i in range(N):
        origin[i] = i
        s = ""
        for j in range(N):
            s += str(countries[i][j]) + "\t"
        f.write(s + "\n")
    print(origin)
    f.close()
    next = getNextRoute(origin, N)
    print(next)
    print(getLength(countries, origin))
    print(getLength(countries, next))
    '''

