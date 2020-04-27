#! /usr/bin/python3
import json
import ast
import collections

def def_comp(tree_1, tree_2):
    if tree_1 == tree_2:
        return 1
    else: 
        return 0

def new_comp(tree_1, tree_2):
    for keys in tree_1.keys():
        if def_comp(tree_1[keys], tree_2[keys]) == 1:
            print("equal")
        else:
            if type(tree_1[keys]) is list:
                for x in tree_1[keys]:
                    pass


def jsondiff(local,online,path='',todo=[]):
    if type(local) is list and type(online) is list:
        if len(local) != len(online):
            num_i = -1
            for i in local: # элемент в первом списке, 
                num_i += 1
                if (i not in online): # но не во втором списке
                    for x in range(0, len(online)): # пройдёмся по всем из второго
                        if (str(ast.literal_eval(str(i))) in str(ast.literal_eval(str(online[x])))) or (str(ast.literal_eval(str(online[x]))) in str(ast.literal_eval(str(i)))):
                            if (ast.literal_eval(str(i)) != ast.literal_eval(str(online[x]))):
                                for x in range(0,len(local)): # пройдёмся для минимальной длины
                                    tmp_1 = local[x]
                                    tmp_2 = online[x]
                                    if (type(local[x]) is dict) and (type(online[x]) is dict): # проверка что внутри вложены словари
                                        tmp_1 = ast.literal_eval(str(local[x]))
                                        tmp_2 = ast.literal_eval(str(online[x]))
                                    print("!")
                                    todo = todo + jsondiff(tmp_1, tmp_2, path+str(x) + ".")
                            else:
                                continue
                        else:
                            todo.append(path+str(num_i)+".")
        else:
            per_flg = 0
            for x in range(0, len(local)):
                for y in range(0, len(online)):
                    if local[x] == online[y]:
                        per_flg = 1
                        break 

            if per_flg == 1:
                for x in range(0, len(local)):
                    for y in range(0, len(online)):
                        tmp_1 = local[x]
                        tmp_2 = online[x]
                        if (type(local[x]) is dict) and (type(online[x]) is dict): # проверка что внутри вложены словари
                            tmp_1 = ast.literal_eval(str(local[x]))
                            tmp_2 = ast.literal_eval(str(online[x]))
                    todo = todo + jsondiff(tmp_1, tmp_2, path+str(x) + ".")


    if not (type(local) is dict) and not (type(online) is dict): #end of recursion
        if local != online:
            todo.append(path)
            return todo
        else:
            return []
    for key in local.keys():
        if not (key in online):
            todo.append(path+key+".")
        else:
            todo=todo+jsondiff(local[key],online[key],path+key+".")
    return todo


if __name__ == '__main__':
    t_1 = input()
    t_2 = input()

    tree_1 = ast.literal_eval(str(t_1))
    tree_2 = ast.literal_eval(str(t_2))

    print("answ")
    result = jsondiff(tree_1,tree_2)
    result = list(set(result))
    print(result)
    res = []
    for i in range(0,len(result)):
        flag = 0
        for j in range(0,len(result)):
            if (result[i] in result[j]):
                if (i == j):
                    continue
                if (("." + result[i])) in result[j]:
                    continue
                else: 
                    flag = 0
                    break
            else:
                flag = 1
        if flag == 1:
            res.append(result[i])
    print("Final", res)
