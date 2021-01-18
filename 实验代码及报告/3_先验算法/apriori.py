import pandas as pd
import itertools

# 准备数据
data = pd.read_csv('GroceryStoreDataSet.csv')

minimum_support_count = 2
records = []
for i in range(0, 20):
    records.append([str(data.values[i, j]) for j in range(0, 4)])
print("records: ", records)

items = sorted([item for sublist in records for item in sublist if item != 'nan'])


# 算候选1-项集c1和频繁1-项集l1
def stage_1(items, minimum_support_count):
    c1 = {i: items.count(i) for i in items}
    l1 = {}
    for key, value in c1.items():
        if value >= minimum_support_count:
            l1[key] = value

    return c1, l1


# 算c2和l2
def stage_2(l1, records, minimum_support_count):
    l1 = sorted(list(l1.keys()))
    L1 = list(itertools.combinations(l1, 2))
    print("L1: ", L1)
    c2 = {}
    l2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in records:
            if sublist(iter1, iter2):
                count += 1
        c2[iter1] = count
    for key, value in c2.items():
        if value >= minimum_support_count:
            if check_subset_frequency(key, l1, 1):
                l2[key] = value

    return c2, l2


# 子项集
def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)


# 测试子项集是否频繁
def check_subset_frequency(itemset, l, n):
    if n > 1:
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


# 算c3,l3
def stage_3(l2, records, minimum_support_count):
    l2 = list(l2.keys())
    L2 = sorted(list(set([item for t in l2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    c3 = {}
    l3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in records:
            if sublist(iter1, iter2):
                count += 1
        c3[iter1] = count
    for key, value in c3.items():
        if value >= minimum_support_count:
            if check_subset_frequency(key, l2, 2):
                l3[key] = value

    return c3, l3


# 算c4,l4
def stage_4(l3, records, minimum_support_count):
    l3 = list(l3.keys())
    L3 = sorted(list(set([item for t in l3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    c4 = {}
    l4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in records:
            if sublist(iter1, iter2):
                count += 1
        c4[iter1] = count
    for key, value in c4.items():
        if value >= minimum_support_count:
            if check_subset_frequency(key, l3, 3):
                l4[key] = value

    return c4, l4


c1, l1 = stage_1(items, minimum_support_count)
c2, l2 = stage_2(l1, records, minimum_support_count)
c3, l3 = stage_3(l2, records, minimum_support_count)
c4, l4 = stage_4(l3, records, minimum_support_count)
print("c1 => ", c1)
print("c2 => ", c2)
print("l1 => ", l1)
print("l2 => ", l2)
print("l3 => ", l3)
print("l4 => ", l4)


sets = []
for iter1 in list(l3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

itemlist = {**l1, **l2, **l3, **l4}


def support_count(itemset, itemlist):
    return itemlist[itemset]


list_l3 = list(l3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist) / support_count(iter1, itemlist)) * 100
        print("Confidence{}->{} = ".format(a, b), confidence)
