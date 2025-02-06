holds = list(range(1,84))
jugs = [2, 6, 7, 9, 16, 19, 31, 37, 43, 46, 47, 49, 55, 63, 66, 68]

for hold in holds:
    count = 0
    with open ('../static/routes.csv') as f:
        for line in f:
            info = line.split(";")
            if str(hold) in info[2].split(', '):
                count += 1
            if str(hold) in info[3].split(', '):
                count += 1
    if hold in jugs:
        print ('hold',hold,'used',count,'times (jug)')
    else:
        print ('hold',hold,'used',count,'times')
