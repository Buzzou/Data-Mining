import numpy as np
import pandas as pd
from numpy import log2 as log

eps = np.finfo(float).eps
# epsilon is the smallest representable number, to avoid going to use the log(0) or 0 may got in the denominator

# ---------------------------------------------------Dataset---------------------------------------------------------- #

# an attribute 2 test(internal node) = its value (branch)
outlook = 'overcast,overcast,overcast,overcast,rainy,rainy,rainy,rainy,rainy,sunny,sunny,sunny,sunny,sunny'.split(',')
temp = 'hot,cool,mild,hot,mild,cool,cool,mild,mild,hot,hot,mild,cool,mild'.split(',')
humidity = 'high,normal,high,normal,high,normal,normal,normal,high,high,high,high,normal,normal'.split(',')
windy = 'FALSE,TRUE,TRUE,FALSE,FALSE,FALSE,TRUE,FALSE,TRUE,FALSE,TRUE,FALSE,FALSE,TRUE'.split(',')
# leaf node 'play' assigns a classification: Y/N
play = 'yes,yes,yes,yes,yes,yes,no,yes,no,no,no,no,yes,yes'.split(',')

# Create pandas dataframe
dataset = {'outlook': outlook, 'temp': temp, 'humidity': humidity, 'windy': windy, 'play': play}
df = pd.DataFrame(dataset, columns=['outlook', 'temp', 'humidity', 'windy', 'play'])
print(df)
print()


# ---------------------------------------------------Step 1----------------------------------------------------------- #
# compute entropy for the whole data-set

def find_entropy(df):
    desired_class = df.keys()[-1]  # 'play'

    entropy_whole = 0
    values = df[desired_class].unique()  # 'Yes', 'No'
    for value in values:
        fraction = df[desired_class].value_counts()[value] / len(df[desired_class])
        entropy_whole += -fraction * np.log2(fraction)
    return entropy_whole


# ---------------------------------------------------Step 2----------------------------------------------------------- #
# Step 2a) calculate entropy of each attribute

def find_entropy_attribute(df, attribute):  # function to calculate entropy of each attribute
    Class = df.keys()[-1]  # 'play'
    target_variables = df[Class].unique()  # 'Yes', 'No'
    variables = df[attribute].unique()  # 'FALSE', 'TRUE', different values of that attribute

    entropy_attribute = 0
    for variable in variables:
        entropy_each_value = 0
        for target_variable in target_variables:
            num = len(df[attribute][df[attribute] == variable][df[Class] == target_variable])  # numerator: 6 or 2
            den = len(df[attribute][df[attribute] == variable])  # denominator: 8 or 6
            fraction = num / (den + eps)  # pi
            entropy_each_value += -fraction * log(fraction + eps)  # calculate entropy for one value like 'TRUE'
        fraction2 = den / len(df)
        entropy_attribute += -fraction2 * entropy_each_value  # Sums up all the entropy of windy

    return abs(entropy_attribute)


# Step 2b) calculate Info gain of each attribute

def ig(df):  # function to calculate IG, pick the highest info gain attribute
    IG = []
    for key in df.keys()[:-1]:
        IG.append(find_entropy(df) - find_entropy_attribute(df, key))
    return df.keys()[:-1][np.argmax(IG)]


# ---------------------------------------------------Build Tree------------------------------------------------------- #
def get_subtable(df, node, attValue):
    return df[df[node] == attValue].reset_index(drop=True)


def buildTree(df, tree=None):
    node = ig(df)  # Get attribute with maximum information gain, 'outlook'
    print('node is: ', node)
    print()
    # 取决策节点的分支
    attValues = np.unique(df[node])  # 'sunny, overcast, rainy'， 当前node的那一列中的各种取值情况
    # df[node] 是被选中的node的那一列
    # Create an empty dictionary to create tree
    if tree is None:
        tree = {}
        tree[node] = {}

    for attValue in attValues:
        subtable = get_subtable(df, node, attValue)

        print('df[node] is: ', '\n', df[node])
        print()
        print('attValue is: ', attValue)
        print()
        print(subtable)
        print()
        col_play_value, counts = np.unique(subtable['play'], return_counts=True)
        print('col_play_value is: ', col_play_value)
        print()
        print('counts is: ', counts)
        print()

        if len(counts) == 1:  # only one possibility
            tree[node][attValue] = col_play_value[0]  # let the name = this column value
        else:
            tree[node][attValue] = buildTree(subtable)  # Calling the function recursively

    return tree


# -------------------------------------------------------------------------------------------------------------------- #

t = buildTree(df)
import pprint

pprint.pprint(t)
