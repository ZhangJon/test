#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jon Zhang
@contact: 
@site:
@version: 1.0
@license:
@file: ATM_Shopping.py
@time: 2017/3/19 15:59
"""
#update the account file
def rewrite_account(new_account,account_file):
    with open(account_file,'w') as account_file:
        for i in range(len(new_account)):
            a,b,c,d = new_account[i]
            line = a + "\t" + b + "\t" + c + "\t"  + d + "\n"
            account_file.write(line)
def rewrite_ATM_limit(ATM_limit_info,ATM_limit_file):
    #print("ATM_limit_info1111:", ATM_limit_info)
    with open(ATM_limit_file,'w') as ATM_limit_file:
        for i in range(len(ATM_limit_info)):
            a,b = ATM_limit_info[i]
            line = a + "\t" + b + "\n"
            ATM_limit_file.write(line)
def f_register_account():
    pass
def f_unlock_account():
    pass
def f_login_account(account_file):
    account_info_f = open(account_file)
    f = account_info_f.readlines()
    list_account = [i.split() for i in f]
    print("list_account:",list_account)
    while True:
        PW_input_flag = True
        input_login_name = input("Please input your login_name:").strip()
        if len(input_login_name) == 0:
            continue
        while PW_input_flag:
            input_login_pw = input("Please input your password:").strip()
            if len(input_login_pw) != 0:
                PW_input_flag = False
        for i in range(len(list_account)):   #advice use the index, when you modify the list in the traverse the list will not go wrong
            if list_account[i][1] == input_login_name:
                if list_account[i][3] == "3":
                    print("Your account is locked!Please to unlock!")
                    rewrite_account(list_account,account_file)
                    return
                elif list_account[i][2] != input_login_pw:
                    list_account[i][3] = str(int(list_account[i][3]) + 1)
                else:
                    print("You are logining!")
                    list_account[i][3] = "0"
                    rewrite_account(list_account, account_file)
                    print(list_account[i][1])
                    return list_account[i][1]
        else:
            print("Your username or password is wrong!!You can to contact email:zj.fly100@gmail.com")
            print(list_account)
            continue
def f_login_ATM():
    ATM_account_file = r"C:\Users\P000801101\PycharmProjects\s12\day5\ATM_account_info.txt"
    return f_login_account(ATM_account_file)
def f_login_mart():
    mart_account_file = r"C:\Users\P000801101\PycharmProjects\s12\day5\mart_account_info.txt"
    return f_login_account(mart_account_file)
def f_shopping(one_person):
    dict_shopping_list = {}
    list_commodity_list = []
    commodity_list_file = r"C:\Users\P000801101\PycharmProjects\s12\day5\commodity_list.txt"
    print("-------------------------------------------------")
    print("+               +")
    print("+               +")
    print("+           hello,%s               +"%one_person)
    print("+   welcome to the ***** supermart   +")
    print("+               +")
    print("+               +")
    print("-------------------------------------------------")
    with open(commodity_list_file) as commodity_list_file_T:
        for i in commodity_list_file_T:
            if not i.startswith("#"):
                # print(type(i))
                list_commodity_list.append(i.split())
                # print("list_commodity_list:",list_commodity_list)
    while True:
        with open(commodity_list_file) as commodity_list_file_T:
            for i in commodity_list_file_T:
                print(i, end='')
        choice_id = input("Please choose one product:")
        for j in range(len(list_commodity_list)):
            if choice_id == list_commodity_list[j][0]:
                print(dict_shopping_list.keys())
                if list_commodity_list[j][0] not in dict_shopping_list.keys():
                    dict_shopping_list[list_commodity_list[j][0]] = [list_commodity_list[j][1],list_commodity_list[j][2],1]
                else:
                    dict_shopping_list[list_commodity_list[j][0]][2] += 1
                go_on_flag = input("GO ON !?(y/n)")
                if go_on_flag == 'n':
                    return dict_shopping_list
                else:
                    break
        else:
            continue
        print(dict_shopping_list)
def f_ATM_operation(ATM_limit_file,dict_shopping_list=None):
    pass
    print("""
    1、withdraw
    2、enquire
    3、deposit
    4、transfer
    5、exit
    """)
    choice_id = input("Please choose one id:")
    if choice_id == "1":

        pass
    if choice_id == "2":
        pass
    if choice_id == "3":
        pass
    if choice_id == "4":
        ATM_limit_o = open(ATM_limit_file)
        ATM_limit_info = [[i.split()[0], i.split()[1]] for i in ATM_limit_o.readlines()]
        print("ATM_limit_info", ATM_limit_info)
        while True:
            total_price = 0
            one_person = f_login_ATM()
            print("one_person_ATM:", one_person)
            print(type(one_person))
            if one_person:
                for j in dict_shopping_list.keys():
                    total_price += float(dict_shopping_list[j][1]) * dict_shopping_list[j][2]
                for i in range(len(ATM_limit_info)):
                    print('1:', type(ATM_limit_info[i][0]))
                    print('2:', ATM_limit_info[i][0])
                    if ATM_limit_info[i][0] == one_person:
                        print(type(ATM_limit_info[i][1]))
                        if float(ATM_limit_info[i][1]) >= total_price:
                            ATM_limit_info[i][1] = str(float(float(ATM_limit_info[i][1])) - total_price)
                            rewrite_ATM_limit(ATM_limit_info, ATM_limit_file)
                            print("ATM_limit_info:", ATM_limit_info)
                            return True
                        else:
                            print("You have not much money to pay for:%s" % total_price)
                            flag = input("Change one card!?(y/n)")
                            if flag == "y":
                                break
                            else:
                                return False
    if choice_id == "5":
        pass
def f_pay_bill(dict_shopping_list):
    ATM_limit_file = r"C:\Users\P000801101\PycharmProjects\s12\day5\ATM_limit_info.txt"
    return f_ATM_operation(ATM_limit_file,dict_shopping_list)
def f_mark_shopping_main():
    one_person = f_login_mart()
    print(one_person)
    if one_person:
        print("shopping")
        dict_shopping_list = f_shopping(one_person)
        if f_pay_bill(dict_shopping_list):
            print("welcome back again!")
        else:
            print("Error")
if __name__ == "__main__":
    f_mark_shopping_main()
    #f_shopping("KOKO")
