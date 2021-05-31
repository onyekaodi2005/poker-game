from copy import deepcopy
import traceback
import csv

playerData = {'player1': 0, 'player2': 0}
numberStack = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
reversedNumberStack = ['6','7','8','9','T','J','Q','K','A','2','3','4','5']
cardValues = {'T':10, 'J':11, 'Q':12, 'K':13,'A':14}
babycardValues = {'T':10, 'J':11, 'Q':12, 'K':13,'A':1}

def findWinner(player1, player2):
    oneFound = False
    twoFound = False
    oneFound = 10 if royalFlush(player1) else False
    twoFound = 10 if royalFlush(player2) else False
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Royal Flush')

    oneFound,twoFound = straightFlush([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Straight Flush')
    
    oneFound,twoFound = fourOfAKind([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Four Of a Kind')
    
    oneFound,twoFound = fullHouse([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Full House')
    
    oneFound,twoFound = flush([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Flush')
    
    oneFound,twoFound = straight([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Straight')
    
    oneFound,twoFound = threeOfAKind([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Three Of A Kind')
    
    oneFound,twoFound = twoPairs([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'Two Pairs')
    
    oneFound,twoFound = onePair([player1,player2])
    if oneFound or twoFound:
        return returnWinner(oneFound, twoFound, 'One Pair')
    
    oneFound,twoFound = highCard([player1,player2])
    return returnWinner(oneFound, twoFound, 'High Card')
        

def returnWinner(one,two,type=''):
    if int(one) > int(two):
        return [1,0,type]
    elif int(one) < int(two):
        return [0,1,type]
    elif one and two and int(one) == int(two):
        return [1,1,type]
    else:
        return [0,0,type]

def checkWinner(d):
    p1 = d['1'][0] if (int(d['1'][0]) > int(d['2'][0]) and d['1'][1]) or (int(d['1'][0]) == int(d['2'][0]) and d['1'][1]) else False 
    if not p1:
        p2 = d['2'][0] if (int(d['2'][0]) > int(d['1'][0]) and d['2'][1]) or (int(d['2'][0]) == int(d['1'][0]) and d['2'][1]) else False
    else:
        p2 = False
    return [p1,p2]

def royalFlush(dataList=[]):
    data = ['T','J','Q','K','A']
    suits = [i[1] for i in dataList]
    if suits.count(suits[0]) != 5:
        return False
    for i in dataList:
        if i[0] not in data: 
            return False
        else:
            x = data.index(i[0]) 
            del data[x]
    return True

def straightFlush(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        d.update({f'{count}': [0,True]})
        nums, suits = [i[0] for i in dataList], [i[1] for i in dataList]
        if suits.count(suits[0]) < 5:
            d.update({f'{count}': [0,False]})
            continue
        else:
            nums.sort()
            charList,num,check = [i[0] for i in nums if not i.isnumeric()],[i[0] for i in nums if i.isnumeric()],''
            num.sort()
            valid,reverse = True,True
            if '2' in num:
                index = reversedNumberStack.index('2')
                for i in reversed(reversedNumberStack[index-(len(num)+1):index]):
                    if i in charList:
                        num.insert(0,i)
                    else:
                        valid = False
                        break
            elif '9' in num and charList:
                try:
                    index,reverse = numberStack.index(num[-1]), False
                except:
                    print(numberStack)
                for i in numberStack[index+1:][:5-len(num)]:
                    if i in charList:
                        num+=i
                    else:
                        valid = False
                        break
            if not valid:
                d.update({f'{count}': [0,False]})
                continue
            if reverse:
                index = reversedNumberStack.index(num[-1])
                for i in reversedNumberStack[:index+1][-5:]:
                    if i in num:
                        d[f'{count}'][0] += int(i) if i.isnumeric() else babycardValues[i]
                    else:
                        valid = False
                        break
            else:
                index = numberStack.index(num[0])
                for i in numberStack[index:index+5]:
                    if i in num:
                        d[f'{count}'][0] += int(i) if i.isnumeric() else babycardValues[i]
                    else:
                        valid = False
                        break
            if not valid:
                d.update({f'{count}': [0,False]})
    return checkWinner(d)

def fourOfAKind(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        nums = [i[0] for i in dataList]
        nums.sort()
        if nums.count(nums[0]) >= 4 or nums.count(nums[-1]) >= 4:
            d.update({f'{count}': [nums[0] if nums.count(nums[0]) >= 4 else nums[-1], True]})
        else:
            d.update({f'{count}': [0, False]})
    return checkWinner(d)

def fullHouse(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        nums = [i[0] for i in dataList]
        nums.sort()
        if nums.count(nums[0]) == 3 and nums.count(nums[-1]) == 2:
            d.update({f'{count}': [nums[0] if nums[0].isnumeric() else cardValues[nums[0]], True]})
        elif nums.count(nums[-1]) == 3 and nums.count(nums[0]) == 2:
            d.update({f'{count}': [nums[-1] if nums[-1].isnumeric() else cardValues[nums[-1]], True]})
        else:
            d.update({f'{count}': [0, False]})
    return checkWinner(d)

def flush(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        suits = [i[1] for i in dataList]
        if suits.count(suits[0]) == 5:
            d.update({f'{count}': [0, True]})
            for i in dataList:
                if i[0].isnumeric():
                    d[f'{count}'][0] += int(i[0])
                else:
                    d[f'{count}'][0] += cardValues[i[0]]
        else:
            d.update({f'{count}': [0, False]})
    return checkWinner(d)

def straight(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        charList, num = [], []
        for i in dataList:
            if i[0].isnumeric():
                num += i[0]
            else:
                charList += i[0]
        num.sort()
        valid = True
        if num and num[0] == '2' and len(num) < 5:
            for i in reversed(numberStack[len(num)-5:]):
                if i in charList:
                    num.insert(0,i)
                else:
                    valid = False
                    break
        elif not num or num[-1] == '9' and len(num) < 5:
            index = numberStack.index('T')
            for i in numberStack[index: index+(5-len(num))]:
                if i in charList:
                        num.append(i)
                else:
                    valid = False
        if not valid:
            d.update({f'{count}': [0, False]})
            continue
        
        d.update({f'{count}': [0, True]})
        if '2' in num:
            index = reversedNumberStack.index(num[0])
            for i in reversedNumberStack[index:index+5]:
                if i not in num:
                    d.update({f'{count}': [0, False]})
                    break
                if i[0].isnumeric():
                    d[f'{count}'][0] += int(i[0])
                else:
                    d[f'{count}'][0] += babycardValues[i[0]]
        else:
            index = numberStack.index(num[0])
            for i in numberStack[index:index+5]:
                if i not in num:
                    d.update({f'{count}': [0, False]})
                    break
                if i[0].isnumeric():
                    d[f'{count}'][0] += int(i[0])
                else:
                    d[f'{count}'][0] += cardValues[i[0]]

    return checkWinner(d)

def threeOfAKind(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        d.update({f'{count}': [0, True]})
        nums, check, found = [i[0] for i in dataList], 1, False
        for i in nums:
            if nums.count(i) >= 3 and not found:
                found = True
            if i[0].isnumeric():
                d[f'{count}'][0] += int(i[0])
            else:
                d[f'{count}'][0] += cardValues[i[0]]
            if check > 3 and not found:
                d.update({f'{count}': [0, False]})
                break
            check += 1
    return checkWinner(d)

def twoPairs(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        d.update({f'{count}': [0, True]})
        nums, found = deepcopy(dataList), []
        for i in dataList:
            index = nums.index(i)
            nums.pop(index)
            for q in nums:
                if i[0] == q[0] and q[0] not in found:
                    found += i[0]
                    break
            if i[0].isnumeric():
                d[f'{count}'][0] += int(i[0])
            else:
                d[f'{count}'][0] += cardValues[i[0]]
        if len(found) < 2:
            d.update({f'{count}': [0, False]})
    return checkWinner(d)

def onePair(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        d.update({f'{count}': [0, False]})
        nums, found = deepcopy(dataList), False
        for i in dataList:
            if not found:
                index = nums.index(i)
                nums.pop(index)
                for q in nums:
                    if i[0] == q[0]:
                        found = True
                        d[f'{count}'][1] = True
                        break
            if i[0].isnumeric():
                d[f'{count}'][0] += int(i[0])
            else:
                d[f'{count}'][0] += cardValues[i[0]]
        if not found:
            d.update({f'{count}': [0, False]})
    return checkWinner(d)

def highCard(dataLists=[]):
    d, count = {},0
    for dataList in dataLists:
        count+=1
        d.update({f'{count}': [0, True]})
        nums = [i[0] for i in dataList]
        for i in nums:
            if i[0].isnumeric():
                d[f'{count}'][0] += int(i[0])
            else:
                d[f'{count}'][0] += cardValues[i[0]]
    return checkWinner(d)


if __name__ == '__main__':
    try:
        fp = open('./poker.txt', 'r')
        createLog = input('Generate Data File y/n - ') 
        if createLog.upper() == 'Y':
            qt = open('./poker.csv','w')
            csvWrite = csv.writer(qt)
            csvWrite.writerow(['PLAYER ONE', 'PLAYER TWO', 'PLAY', 'PLAYER ONE CARD', 'PLAYER TWO CARD'])
            generateFile = True
        else:
            generateFile = False

        line = 1
        for z in fp.readlines():
            player1, player2, card = findWinner(z.split()[0:5], z.split()[5:]) 
            if generateFile:
                x = ['***WINNER***' if player1 else 'LOSER','***WINNER***' if player2 else 'LOSER',card,z[0:14],z[15:]]
                csvWrite.writerow(x)
            
            playerData['player1'] += player1
            playerData['player2'] += player2
            print(f"PLAYER 1 - {'***WINNER***' if player1 else 'LOSER'}, PLAYER 2 - {'***WINNER***' if player2 else 'LOSER'}\t\t{card}\t\tLINE#: {line}\n") 
            line +=1
        x = 'FINAL SCORES: '   
        print("\u0332".join(x))
        print(f"PLAYER ONE TOTAL WINS = {playerData['player1']}")
        print(f"PLAYER TWO TOTAL WINS = {playerData['player2']}")
        if generateFile:
            fp.close()
            qt.close()
            print('Poker File Result Generated Successfully!!!')
    except Exception as ex:
        traceback.print_exc()
        print(ex)



