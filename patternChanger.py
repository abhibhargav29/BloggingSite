import re

#Input
n = int(input())

str_list=[]
for i in range(n):
    str_list.append(input())

#Pattern Changing
new_list=[]
pat1 = re.compile(r'(?<= )&&(?= )')
pat2 = re.compile(r'(?<= )\|\|(?= )')
for i in range(n):
    str_list[i]=re.sub(pat1, "and" ,str_list[i])
    str_list[i]=re.sub(pat2, "or" ,str_list[i])

#Output
for string in str_list:
    print(string)
