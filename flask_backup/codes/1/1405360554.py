#-*-coding: utf-8 -*-
import random
 
def intro():
        suggest = raw_input("가위바위보 하실래요?('응', '아니'로 답해주세요): ")
        if suggest == "아니":
                print("ㅇㅋ ㅂㅂ")
        elif suggest != "응" and suggest != "아니":
                print "뭔말인지 모르겠어요.",
                intro()
        else:
                suggest2 = int(raw_input("몇게임 하실래요?(숫자로 답해주세요): "))
                for i in range(suggest2):
                        game()
               
 
def game():
        comint = random.randint(0,2)
        if comint == 0:
                com = "가위"
        elif comint == 1:
                com = "바위"
        else:
                com = "보"
 
        user = raw_input("가위바위보: ")
        while user not in ["가위", "바위", "보"]:
                user = raw_input("게임 제대로 합시당 ㅡㅡ 다시 가위바위보: ")
        else:
                if user == "가위":
                        userint = 0
                elif user == "바위":
                        userint = 1
                else:
                        userint = 2
 
        print "컴퓨터는: "+com
        print "당신은: "+user
 
        score = {
                'tie' : 0,
                'win' : 0,
                'lose' : 0
        }
 
        if comint == userint:
                print "비겼네영"
                score["tie"] += 1
                print
        elif comint == userint+1 or comint == userint-2 :
                print "너 짐ㅋ"
                score["lose"] += 1
        else:
                print "ㅊㅋ이김"
                score["win"] += 1
 
        for key in score:
                print key,
                print score[key]
 
def closing():
        suggest = raw_input("다시 하실래요?('응', '아니'로 답해주세요): ")
        if suggest == "아니":
                print("ㅇㅋ ㅂㅂ")
        elif suggest != "응" and suggest != "아니":
                print "뭔말인지 모르겠어요",
                closing()
        else:
                intro()
 
intro()
closing()