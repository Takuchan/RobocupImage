a = [1,2,4,0,5,7,8,767]
for s in range(len(a)):
    print(a[s])
    if a[s] == 0:
        print('{}番目にきたね'.format(s))
