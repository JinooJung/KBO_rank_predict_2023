import itertools
import tqdm
import pandas as pd
import random

player_predict = {
    "희도":"두롯삼한에케엘키엔기",
    "지환":"두삼엔키에케엘롯기한",
    "진우":"롯삼한두엘케에키엔기",
    "재홍":"키엘케에삼한기롯두엔",
    "지훈":"에키엘케기엔삼롯두한",
    "와지":"에케롯삼엘두키엔한기",
    "종윤":"에키케두롯한엘삼엔기",
    "동욱":"키케에삼기엘두롯한엔",
    "동건":"키에케삼롯엘두엔한기",
    "다윤":"엘에롯키케두삼엔기한"
}


result = {
    4:["롯에엘엔두기삼키케한",[0,1,2,3,4.5,4.5,6,7,8,9]],
    4.5:["에롯엘엔두삼기키한케",[0,1,2,3,4,5,6,7,8,9]],
    5:["엘에롯두엔기삼키한케",[0,1,2,3,4.5,4.5,6,7,8,9]],
    5.5:["엘에엔롯두기키삼한케",[0,1,2,3,4,5,6,7,8,9]],
    6:["엘에엔롯키두케한기삼",[0,1,2,3,4,5,6,7,8,9]],
    6.5:["엘에두엔롯기케한키삼",[0,1,2,3,4,5,6,7,8,9]],
    7:["엘에두엔케기롯한키삼",[0,1,2,3.5,3.5,5,6,7,8,9]],
    7.5:["엘에케엔두기롯한삼키",[0,1,2,3,4,5,6,7,8,9]],
    8:["엘케에엔기두롯삼한키",[0,1,2,3,4,5,6,7,8,9]],
    8.5:["엘케엔에기두롯한삼키",[0,1,2,3,4,5,6,7,8,9]],
    9:["엘케엔두에기롯삼한키",[0,1,2,3,4,5,6,7,8,9]],
    9.5:["엘케에엔두기롯삼한키",[0,1,2,3,4,5,6,7,8,9]],
}

def score(pred, ans):
    score = 100
    for i, p in enumerate(pred):
        j = ans[1][ans[0].index(p)]
        score -= abs(i-j)
    return score

def mse_score(pred, ans):
    score = 0
    for i, p in enumerate(pred):
        j = ans[1][ans[0].index(p)]
        score += (i-j)**2
    return (score/10)**0.5

player_score = {}

for p in player_predict.keys():
    player_score[p] = {}

for p in player_predict.keys():
    for m in result.keys(): 
        player_score[p][m] = (score(player_predict[p], result[m])) 

def baseline(m):
    candidate = itertools.permutations(range(10),10)
    candidate = list(candidate)

    scores = [sum([abs(result[m][1][i]-c[i]) for i in range(10)]) for c in tqdm.tqdm(candidate)]
    
    # scores = [(sum([(c[i]-i)**2 for i in range(10)])/10)**0.5 for c in tqdm.tqdm(candidate)]
    scores = pd.Series(scores)
    return scores.mean(), scores.quantile(0.25), scores.quantile(0.75), scores.std()

def print_monthly_score(month, verbose=True):
    monthly_score = []
    for p in player_score.keys():
        monthly_score.append([p, player_score[p][month]])

    if(verbose):
        mean, Q3, Q1, std = baseline(month)

    monthly_score.sort(key=lambda x:-x[1])

    before_rank = 0
    before_score = 0
    if(verbose):
        if(type(month) == int):
            print(f" -- 2023년 {month}월 최종 순위!")
        else:
            print(f" -- 2023년 {int(month+0.5)}월 중간 순위!")
        print(f"If choose randomly .... E(scores) = {mean}점, std(scores) = {round(std,3)}, Q1 = {Q1}점, Q3 = {Q3}점")
    for i, ms in enumerate(monthly_score):
        rank = i+1
        if(before_score==ms[1]):
            rank = before_rank
        else:
            before_rank = rank
            before_score = ms[1]
        if(verbose):
            print(f"{rank}등 - {ms[0]} {ms[1]}점")
    
    return monthly_score

def show_graph():
    import matplotlib.pyplot as plt
    from matplotlib import rc
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    score_per_player = {}
    month = list(result.keys())
    month.sort()

    total_result = {}
    for m in month:
        total_result[m] = print_monthly_score(m, verbose=False)

    check_empty = [[] for _ in range(20)]

    for i, p in enumerate(player_score.keys()):
        score_per_player[p] = []
        for m in month:
            for ts in total_result[m]:
                if(ts[0]==p):
                    while(ts[1] in check_empty[len(score_per_player[p])]):
                        ts[1]+=0.1
                    check_empty[len(score_per_player[p])].append(ts[1])
                    score_per_player[p].append(ts[1])
                    break
            

    for p in player_score.keys():
        plt.plot(month, score_per_player[p], label=p)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.show()

def find_winner_case():
    winner_case = {}
    for p in player_predict.keys():
        winner_case[p] = 0
    candidate = itertools.permutations("두롯삼한에케엘키엔기",10)
    for c in tqdm.tqdm(candidate):
        ans = [c, [0,1,2,3,4.5,4.5,6,7,8,9]]
        score_c = {}
        for p in player_predict.keys():
            score_c[p] = score(player_predict[p], ans)
        win_score = min(score_c.values())
        num_winner = 0
        for p in player_predict.keys():
            if(score_c[p]==win_score):
                num_winner += 1
        for p in player_predict.keys():
            if(score_c[p]==win_score):
                winner_case[p] += 1/num_winner
    return winner_case


    

print_monthly_score(9.5) 
show_graph()

print(find_winner_case())