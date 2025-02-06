data = []

with open ('../static/routes.csv') as f:
    for row in f:
        info = row.split(';')
        data.append(info[2])
        data.append(info[3])
        
jugs = [2,6,9,16,19,7,43,55,46,47,31,49,63,66,37,68]
jugs.sort()

for hold in jugs:
    count = 0
    for entry in data:
        if str(hold) in entry.split(', '):
            count += 1
    hold_nr = str(hold)
    print ('hold ' + hold_nr + 'used' + str(count) + 'times')

with open ('../static/routes.csv') as f:
    for line in f:
        info = line.split(";")
        for hold in jugs:
            if str(hold) in info[2].split(', ') or str(hold) in info[3].split(', '):
                print('hold', hold, 'used in route', info[0])
