# -*- coding: utf-8 -*-
import string,sys,os,time,ftplib
from Tkinter import *
import tkMessageBox

lUser = []
lData = []

cur_user = 0
cur_mon = 0
UserChangeAID = 0
DataChangeAID = 0

#Tk数据
list_user = None
list_mon = None
fm_data = None

class USER:
    def __init__(self):
        self.aid = 0
        self.name = ""
        self.wuxian = 0.00
        self.zinv = 0.00
        self.jiaoyu = 0.00
        self.dabing = 0.00
        self.daikuan = 0.00
        self.fangzu = 0.00
        self.yanglao = 0.00

class DATA:
    def __init__(self):
        self.aid = 0
        self.userid = 0
        self.date = 0
        self.jisuan = 0.00
        self.shiji = 0.00
        self.shouru = 0.00
        self.qizheng = 0.00
        self.wuxian = 0.00
        self.zinv = 0.00
        self.jiaoyu = 0.00
        self.dabing = 0.00
        self.daikuan = 0.00
        self.fangzu = 0.00
        self.yanglao = 0.00

def ReadUser():
    global lUser
    try:
        f = open("user.txt","rb")
    except:
        cuser = USER()
        lUser.append(cuser)
        return
    lines = f.readlines()
    f.close()
    del lines[0]
    for line in lines:
        if line[0] == "#":
            continue
        kw = line.strip(" \t\r\n").split("\t")
        if len(kw) != 9:
            print "ReadUser Error:"
            print line
        cuser = USER()
        cuser.aid = int(kw[0])
        cuser.name = kw[1]
        cuser.wuxian = "%.2f"%float(kw[2])
        cuser.zinv = "%.2f"%float(kw[3])
        cuser.jiaoyu = "%.2f"%float(kw[4])
        cuser.dabing = "%.2f"%float(kw[5])
        cuser.daikuan = "%.2f"%float(kw[6])
        cuser.fangzu = "%.2f"%float(kw[7])
        cuser.yanglao = "%.2f"%float(kw[8])
        lUser.append(cuser)

def SaveUser():
    global lUser
    f = open("user.txt","wb")
    f.write(("AID	姓名	五险一金	子女教育	继续教育	大病医疗	住房贷款利息	住房租金	赡养老人\r\n").decode("utf-8").encode("gb2312"))
    for cuser in lUser:
        f.write(str(cuser.aid)+'\t')
        f.write(str(cuser.name)+'\t')
        f.write(str(cuser.wuxian)+'\t')
        f.write(str(cuser.zinv)+'\t')
        f.write(str(cuser.jiaoyu)+'\t')
        f.write(str(cuser.dabing)+'\t')
        f.write(str(cuser.daikuan)+'\t')
        f.write(str(cuser.fangzu)+'\t')
        f.write(str(cuser.yanglao))
        f.write('\r\n')
    f.close()

def ReadData():
    global lData
    try:
        f = open("data.txt","rb")
    except:
        cdata = DATA()
        lData.append(cdata)
        return
    lines = f.readlines()
    f.close()
    del lines[0]
    for line in lines:
        if line[0] == "#":
            continue
        kw = line.strip(" \t\r\n").split("\t")
        if len(kw) != 14:
            print "ReadData Error:"
            print line
        cdata = DATA()
        cdata.aid = int(kw[0])
        cdata.userid = int(kw[1])
        cdata.date = int(kw[2])
        cdata.jisuan = "%.2f"%float(kw[3])
        cdata.shiji = "%.2f"%float(kw[4])
        cdata.shouru = "%.2f"%float(kw[5])
        cdata.qizheng = "%.2f"%float(kw[6])
        cdata.wuxian = "%.2f"%float(kw[7])
        cdata.zinv = "%.2f"%float(kw[8])
        cdata.jiaoyu = "%.2f"%float(kw[9])
        cdata.dabing = "%.2f"%float(kw[10])
        cdata.daikuan = "%.2f"%float(kw[11])
        cdata.fangzu = "%.2f"%float(kw[12])
        cdata.yanglao = "%.2f"%float(kw[13])
        lData.append(cdata)

def SaveData():
    global lData
    f = open("data.txt","wb")
    f.write(("AID	USERID	月份	计算纳税	实际纳税	收入	起征点	五险一金	子女教育	继续教育	大病医疗	住房贷款利息	住房租金	赡养老人\r\n").decode("utf-8").encode("gb2312"))
    for cdata in lData:
        f.write(str(cdata.aid)+"\t")
        f.write(str(cdata.userid)+"\t")
        f.write(str(cdata.date)+"\t")
        f.write(str(cdata.jisuan)+"\t")
        f.write(str(cdata.shiji)+"\t")
        f.write(str(cdata.shouru)+"\t")
        f.write(str(cdata.qizheng)+"\t")
        f.write(str(cdata.wuxian)+"\t")
        f.write(str(cdata.zinv)+"\t")
        f.write(str(cdata.jiaoyu)+"\t")
        f.write(str(cdata.dabing)+"\t")
        f.write(str(cdata.daikuan)+"\t")
        f.write(str(cdata.fangzu)+"\t")
        f.write(str(cdata.yanglao))
        f.write("\r\n")
    f.close()

def CalcRet(sum):
#级数   全年应纳税所得额               税率（%）   速算扣除数
#1      不超过36000元的                  3              0
#2      超过36000元至144000元的部分     10           2520
#3      超过144000元至300000元的部分    20          16920
#4      超过300000元至420000元的部分    25          31920
#5      超过420000元至660000元的部分    30          52920
#6      超过660000元至960000元的部分    35          85920
#7      超过960000元的部分              45         181920
    ret = 0
    delnum = 0
    if sum <= 36000:
        ret = 0.03
        delnum = 0
    elif sum <= 144000:
        ret = 0.1
        delnum = 2520
    elif sum <= 300000:
        ret = 0.2
        delnum = 16920
    elif sum <= 420000:
        ret = 0.25
        delnum = 31920
    elif sum <= 660000:
        ret = 0.3
        delnum = 52920
    elif sum <= 960000:
        ret = 0.35
        delnum = 85920
    else:
        ret = 0.45
        delnum = 181920
    return ret,delnum

def CalcBonus(sum):
#级数     平均每月收入                税率(%)       速算扣除数
#1      不超过3,000元的部分             3           0
#2      超过3,000元至12,000元的部分     10          210
#3      超过12,000元至25,000元的部分    20          1410
#4      超过25,000元至35,000元的部分    25          2660
#5      超过35,000元至55,000元的部分    30          4410
#6      超过55,000元至80,000元的部分    35          7160
#7      超过80,000元的部分              45          15160
    ret = 0
    delnum = 0
    base = sum / 12
    if base <= 3000:
        ret = 0.03
        delnum = 0
    elif base <= 12000:
        ret = 0.1
        delnum = 210
    elif base <= 25000:
        ret = 0.2
        delnum = 1410
    elif base <= 35000:
        ret = 0.25
        delnum = 2660
    elif base <= 55000:
        ret = 0.30
        delnum = 4410
    elif base <= 80000:
        ret = 0.35
        delnum = 7160
    else:
        ret = 0.45
        delnum = 15160
    return sum*ret-delnum

def FindUserByUserid(userid):
    global lUser
    for cuser in lUser:
        if cuser.aid == userid:
            return cuser

def FindUserData(userid):
    global lData
    lUData = []
    for cdata in lData:
        if cdata.userid == userid:
            lUData.append(cdata)
    return sorted(lUData,key=lambda cdata:cdata.date)

def Calc(cdata):
    global lUser,lData
    lUData = FindUserData(cdata.userid)
    checkmon = 0
    for mcdata in lUData:
        if mcdata.date == 0:
            continue
        checkmon += 1
        if mcdata.date != checkmon:
            #print ("缺少["+str(checkmon)+"]月数据 无法计算").decode("utf-8")
            tkMessageBox.showwarning("警告", "缺少["+str(checkmon)+"]月数据 无法计算")
            return
    if cdata.date > checkmon+1:
        #print ("缺少["+str(checkmon+1)+"]月数据 无法计算").decode("utf-8")
        tkMessageBox.showwarning("警告", "缺少["+str(checkmon+1)+"]月数据 无法计算")
        return
    #if cdata.date <= checkmon:
    #    #print ("["+str(cdata.date)+"]月数据已存在").decode("utf-8")
    #    tkMessageBox.showwarning("警告", "["+str(cdata.date)+"]月数据已存在")
    #    return
    sum = 0
    for mdata in lUData:
        if mdata.date == 0:
            continue
        if mdata.date >= cdata.date:
            break
        sum += float(mdata.shouru)
        sum -= float(mdata.qizheng)
        sum -= float(mdata.wuxian)
        sum -= float(mdata.zinv)
        sum -= float(mdata.jiaoyu)
        sum -= float(mdata.dabing)
        sum -= float(mdata.daikuan)
        sum -= float(mdata.fangzu)
        sum -= float(mdata.yanglao)
    sum += float(cdata.shouru)
    sum -= float(cdata.qizheng)
    sum -= float(cdata.wuxian)
    sum -= float(cdata.zinv)
    sum -= float(cdata.jiaoyu)
    sum -= float(cdata.dabing)
    sum -= float(cdata.daikuan)
    sum -= float(cdata.fangzu)
    sum -= float(cdata.yanglao)
    
    ret,delnum = CalcRet(sum)
    result = sum*ret-delnum
    for mdata in lUData:
        if mdata.date == 0:
            continue
        if mdata.date >= cdata.date:
            break
        result -= float(mdata.shiji)
    if result < 0:
        result = 0
    result = "%.2f"%result
    cdata.jisuan = result
    #cdata.shiji = result
    return cdata

def SelectUser(*args):
    global list_user,cur_user,list_mon
    if list_user.size() == 0:
        return
    cur_user = list_user.get(list_user.curselection())
    cur_user = int(cur_user.split('.')[0])
    for i in range(list_user.size()):
        list_user.itemconfig(i,bg="#ffffff")
    list_user.itemconfig(list_user.curselection(),bg="#3399ff")
    
    list_mon.delete(0,END)
    lUData = FindUserData(cur_user)
    if len(lUData) == 0:
        AddNianzhong()
        return
    for cdata in lUData:
        if cdata.date == 0:
            list_mon.insert(END, "0 年终奖")
        else:
            list_mon.insert(END, str(cdata.date)+" 月")
    list_mon.selection_set(END)
    SelectMon(None)

def SelectMon(*args):
    global root
    global list_mon,cur_mon,cur_user,fm_data,DataChangeAID
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    if list_mon.size() == 0:
        return
    cur_mon = list_mon.get(list_mon.curselection())
    cur_mon = int(cur_mon.split(' ')[0])
    for i in range(list_mon.size()):
        list_mon.itemconfig(i,bg="#ffffff")
    list_mon.itemconfig(list_mon.curselection(),bg="#3399ff")
    
    if fm_data:
        fm_data.destroy()
    fm_data = Frame(root)
    cuser = FindUserByUserid(cur_user)
    lUData = FindUserData(cur_user)
    for cdata in lUData:
        if cdata.date == cur_mon:
            DataChangeAID = cdata.aid
            if cdata.date == 0:
                cstr = "["+cuser.name.decode("gb2312").encode("utf-8")+"]年终奖纳税信息:"
                Label(fm_data, text=cstr, font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
                Label(fm_data, text="奖金额：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
                Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
                e1 = Entry(fm_data)
                e2 = Entry(fm_data)
                e1.grid(row=1,column=1)
                e2.grid(row=2,column=1)
                e1.insert(0,cdata.shouru)
                e2.insert(0,cdata.shiji)
                e1["state"] = "readonly"
                e2["state"] = "readonly"
            else:
                cstr = "["+cuser.name.decode("gb2312").encode("utf-8")+"]"+str(cur_mon)+"月纳税信息:"
                Label(fm_data, text=cstr, font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
                Label(fm_data, text="总收入：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
                Label(fm_data, text="起征点：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
                Label(fm_data, text="五险一金：", font=("Symbol", 12), height=2).grid(row=3,sticky=E)
                Label(fm_data, text="子女教育：", font=("Symbol", 12), height=2).grid(row=4,sticky=E)
                Label(fm_data, text="继续教育：", font=("Symbol", 12), height=2).grid(row=5,sticky=E)
                Label(fm_data, text="大病医疗：", font=("Symbol", 12), height=2).grid(row=6,sticky=E)
                Label(fm_data, text="住房贷款：", font=("Symbol", 12), height=2).grid(row=7,sticky=E)
                Label(fm_data, text="住房租金：", font=("Symbol", 12), height=2).grid(row=8,sticky=E)
                Label(fm_data, text="赡养老人：", font=("Symbol", 12), height=2).grid(row=9,sticky=E)
                Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=10,sticky=E)
                e1 = Entry(fm_data)
                e2 = Entry(fm_data)
                e3 = Entry(fm_data)
                e4 = Entry(fm_data)
                e5 = Entry(fm_data)
                e6 = Entry(fm_data)
                e7 = Entry(fm_data)
                e8 = Entry(fm_data)
                e9 = Entry(fm_data)
                e10 = Entry(fm_data)
                e1.grid(row=1,column=1)
                e2.grid(row=2,column=1)
                e3.grid(row=3,column=1)
                e4.grid(row=4,column=1)
                e5.grid(row=5,column=1)
                e6.grid(row=6,column=1)
                e7.grid(row=7,column=1)
                e8.grid(row=8,column=1)
                e9.grid(row=9,column=1)
                e10.grid(row=10,column=1)
                e1.insert(0,cdata.shouru)
                e2.insert(0,cdata.qizheng)
                e3.insert(0,cdata.wuxian)
                e4.insert(0,cdata.zinv)
                e5.insert(0,cdata.jiaoyu)
                e6.insert(0,cdata.dabing)
                e7.insert(0,cdata.daikuan)
                e8.insert(0,cdata.fangzu)
                e9.insert(0,cdata.yanglao)
                e10.insert(0,cdata.shiji)
                e1["state"] = "readonly"
                e2["state"] = "readonly"
                e3["state"] = "readonly"
                e4["state"] = "readonly"
                e5["state"] = "readonly"
                e6["state"] = "readonly"
                e7["state"] = "readonly"
                e8["state"] = "readonly"
                e9["state"] = "readonly"
                e10["state"] = "readonly"
            break
    button_stat = Button(fm_data, text ="全年统计", font=("Symbol", 12), command = ButtonDataStat)
    button_stat.grid(row=11,column=1)
    fm_data.pack(side=LEFT,fill=BOTH)

def AddNianzhong():
    global root,fm_data,cur_user
    global e1,e2
    if fm_data:
        fm_data.destroy()
    fm_data = Frame(root)
    cuser = FindUserByUserid(cur_user)
    cstr = "["+cuser.name.decode("gb2312").encode("utf-8")+"]年终奖纳税信息:"
    Label(fm_data, text=cstr, font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
    Label(fm_data, text="奖金额：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
    Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
    e1 = Entry(fm_data)
    e2 = Entry(fm_data)
    e1.grid(row=1,column=1)
    e2.grid(row=2,column=1)
    e1.insert(0,"0.00")
    e2.insert(0,"0.00")
    e2["state"] = "readonly"
    button_c = Button(fm_data, text ="计算", font=("Symbol", 12), command = ButtonCalcData0)
    button_c.grid(row=3,column=0)
    button_s = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonAddData0)
    button_s.grid(row=3,column=1)
    cstr = "\n\
    年终奖纳税：\n\
    \n\
    可以选择按年度总收入申报\n\
    或者全年一次性奖金收入申报\n\
    \n\
    如果选择按总收入申报 这里填【0.00】\n\
    \n\
    如果每个月薪资都能达到起征点\n\
    建议选择全年一次性奖金收入申报\n\
    否则建议选择按年度总收入申报\n\
    "
    Label(fm_data, text=cstr, justify = 'left', font=("Symbol", 11)).grid(row=4,sticky=E,columnspan=3)
    fm_data.pack(side=LEFT,fill=BOTH)


def ButtonDataStat():
    global cur_user
    lUData = FindUserData(cur_user)
    sum_all = 0
    sum_shui = 0
    bonus = 0
    bonus_shui = 0
    for cdata in lUData:
        if cdata.date == 0:
            bonus = cdata.shouru
            bonus_shui = cdata.shiji
        sum_all += float(cdata.shouru)
        sum_shui += float(cdata.shiji)
    tkMessageBox.showinfo("统计", "总收入："+str(sum_all)+"\n总纳税："+str(sum_shui)+"\n\n年终奖："+str(bonus)+"\n年终税："+str(bonus_shui))

def ButtonUserChange():
    global root,fm_data,cur_user
    global e1,e2,e3,e4,e5,e6,e7,e8
    global UserChangeAID
    if fm_data:
        fm_data.destroy()
    cuser = FindUserByUserid(cur_user)
    UserChangeAID = cuser.aid
    fm_data = Frame(root)
    Label(fm_data, text="修改用户：", font=("Symbol", 14), height=2).grid(row=0,columnspan=2)
    Label(fm_data, text="姓名：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
    Label(fm_data, text="五险一金：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
    Label(fm_data, text="子女教育：", font=("Symbol", 12), height=2).grid(row=3,sticky=E)
    Label(fm_data, text="继续教育：", font=("Symbol", 12), height=2).grid(row=4,sticky=E)
    Label(fm_data, text="大病医疗：", font=("Symbol", 12), height=2).grid(row=5,sticky=E)
    Label(fm_data, text="住房贷款：", font=("Symbol", 12), height=2).grid(row=6,sticky=E)
    Label(fm_data, text="住房租金：", font=("Symbol", 12), height=2).grid(row=7,sticky=E)
    Label(fm_data, text="赡养老人：", font=("Symbol", 12), height=2).grid(row=8,sticky=E)
    e1 = Entry(fm_data)
    e2 = Entry(fm_data)
    e3 = Entry(fm_data)
    e4 = Entry(fm_data)
    e5 = Entry(fm_data)
    e6 = Entry(fm_data)
    e7 = Entry(fm_data)
    e8 = Entry(fm_data)
    e1.grid(row=1,column=1)
    e2.grid(row=2,column=1)
    e3.grid(row=3,column=1)
    e4.grid(row=4,column=1)
    e5.grid(row=5,column=1)
    e6.grid(row=6,column=1)
    e7.grid(row=7,column=1)
    e8.grid(row=8,column=1)
    e1.insert(0,cuser.name.decode("gb2312"))
    e2.insert(0,cuser.wuxian)
    e3.insert(0,cuser.zinv)
    e4.insert(0,cuser.jiaoyu)
    e5.insert(0,cuser.dabing)
    e6.insert(0,cuser.daikuan)
    e7.insert(0,cuser.fangzu)
    e8.insert(0,cuser.yanglao)
    button_add = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonUserChangeSave)
    button_add.grid(row=9,column=1)
    fm_data.pack(side=LEFT,fill=BOTH)

def ButtonUserChangeSave():
    global e1,e2,e3,e4,e5,e6,e7,e8
    global UserChangeAID,lUser,list_user,cur_user
    e1["state"] = "readonly"
    e2["state"] = "readonly"
    e3["state"] = "readonly"
    e4["state"] = "readonly"
    e5["state"] = "readonly"
    e6["state"] = "readonly"
    e7["state"] = "readonly"
    e8["state"] = "readonly"
    for i in range(len(lUser)):
        if lUser[i].aid == UserChangeAID:
            lUser[i].name = e1.get().strip(" \t\r\n").encode("gb2312")
            lUser[i].wuxian = e2.get().strip(" \t\r\n")
            lUser[i].zinv = e3.get().strip(" \t\r\n")
            lUser[i].jiaoyu = e4.get().strip(" \t\r\n")
            lUser[i].dabing = e5.get().strip(" \t\r\n")
            lUser[i].daikuan = e6.get().strip(" \t\r\n")
            lUser[i].fangzu = e7.get().strip(" \t\r\n")
            lUser[i].yanglao = e8.get().strip(" \t\r\n")
            break
    SaveUser()
    list_user.delete(0,END)
    for cuser in lUser:
        list_user.insert(END, str(cuser.aid)+"."+cuser.name.decode("gb2312"))
    for i in range(list_user.size()):
        if int(list_user.get(i).split('.')[0]) == cur_user:
            list_user.selection_set(i)

def ButtonUser():
    global fm_data
    global e1,e2,e3,e4,e5,e6,e7,e8
    if fm_data:
        fm_data.destroy()
    fm_data = Frame(root)
    Label(fm_data, text="新增用户：", font=("Symbol", 14), height=2).grid(row=0,columnspan=2)
    Label(fm_data, text="姓名：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
    Label(fm_data, text="五险一金：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
    Label(fm_data, text="子女教育：", font=("Symbol", 12), height=2).grid(row=3,sticky=E)
    Label(fm_data, text="继续教育：", font=("Symbol", 12), height=2).grid(row=4,sticky=E)
    Label(fm_data, text="大病医疗：", font=("Symbol", 12), height=2).grid(row=5,sticky=E)
    Label(fm_data, text="住房贷款：", font=("Symbol", 12), height=2).grid(row=6,sticky=E)
    Label(fm_data, text="住房租金：", font=("Symbol", 12), height=2).grid(row=7,sticky=E)
    Label(fm_data, text="赡养老人：", font=("Symbol", 12), height=2).grid(row=8,sticky=E)
    e1 = Entry(fm_data)
    e2 = Entry(fm_data)
    e3 = Entry(fm_data)
    e4 = Entry(fm_data)
    e5 = Entry(fm_data)
    e6 = Entry(fm_data)
    e7 = Entry(fm_data)
    e8 = Entry(fm_data)
    e1.grid(row=1,column=1)
    e2.grid(row=2,column=1)
    e3.grid(row=3,column=1)
    e4.grid(row=4,column=1)
    e5.grid(row=5,column=1)
    e6.grid(row=6,column=1)
    e7.grid(row=7,column=1)
    e8.grid(row=8,column=1)
    e1.insert(0,"")
    e2.insert(0,0)
    e3.insert(0,0)
    e4.insert(0,0)
    e5.insert(0,0)
    e6.insert(0,0)
    e7.insert(0,0)
    e8.insert(0,0)
    button_add = Button(fm_data, text ="完成", font=("Symbol", 12), command = ButtonAddUser)
    button_add.grid(row=9,column=1)
    fm_data.pack(side=LEFT,fill=BOTH)

def ButtonAddUser():
    global lUser,list_user
    global e1,e2,e3,e4,e5,e6,e7,e8
    cuser = USER()
    cuser.aid = lUser[-1].aid + 1
    cuser.name = e1.get().strip(" \t\r\n").encode("gb2312")
    cuser.wuxian = "%.2f"%float(e2.get().strip(" \t\r\n"))
    cuser.zinv = "%.2f"%float(e3.get().strip(" \t\r\n"))
    cuser.jiaoyu = "%.2f"%float(e4.get().strip(" \t\r\n"))
    cuser.dabing = "%.2f"%float(e5.get().strip(" \t\r\n"))
    cuser.daikuan = "%.2f"%float(e6.get().strip(" \t\r\n"))
    cuser.fangzu = "%.2f"%float(e7.get().strip(" \t\r\n"))
    cuser.yanglao = "%.2f"%float(e8.get().strip(" \t\r\n"))
    lUser.append(cuser)
    SaveUser()
    list_user.insert(END, str(cuser.aid)+"."+cuser.name.decode("gb2312").encode("utf-8"))
    list_user.selection_clear(0,END)
    list_user.selection_set(END)
    SelectUser(None)

def ButtonDataChange():
    global root,fm_data,cur_user
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    global DataChangeAID,lData
    if fm_data:
        fm_data.destroy()
    fm_data = Frame(root)
    for cdata in lData:
        if cdata.aid == DataChangeAID:
            if cdata.date == 0:
                Label(fm_data, text="数据修改：", font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
                Label(fm_data, text="奖金额：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
                Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
                e1 = Entry(fm_data)
                e2 = Entry(fm_data)
                e1.grid(row=1,column=1)
                e2.grid(row=2,column=1)
                e1.insert(0,cdata.shouru)
                e2.insert(0,cdata.shiji)
                button_c = Button(fm_data, text ="计算", font=("Symbol", 12), command = ButtonCalcData0)
                button_c.grid(row=11,column=0)
                button_s = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonDataChangeSave)
                button_s.grid(row=11,column=1)
            else:
                Label(fm_data, text="数据修改：", font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
                Label(fm_data, text="总收入：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
                Label(fm_data, text="起征点：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
                Label(fm_data, text="五险一金：", font=("Symbol", 12), height=2).grid(row=3,sticky=E)
                Label(fm_data, text="子女教育：", font=("Symbol", 12), height=2).grid(row=4,sticky=E)
                Label(fm_data, text="继续教育：", font=("Symbol", 12), height=2).grid(row=5,sticky=E)
                Label(fm_data, text="大病医疗：", font=("Symbol", 12), height=2).grid(row=6,sticky=E)
                Label(fm_data, text="住房贷款：", font=("Symbol", 12), height=2).grid(row=7,sticky=E)
                Label(fm_data, text="住房租金：", font=("Symbol", 12), height=2).grid(row=8,sticky=E)
                Label(fm_data, text="赡养老人：", font=("Symbol", 12), height=2).grid(row=9,sticky=E)
                Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=10,sticky=E)
                e1 = Entry(fm_data)
                e2 = Entry(fm_data)
                e3 = Entry(fm_data)
                e4 = Entry(fm_data)
                e5 = Entry(fm_data)
                e6 = Entry(fm_data)
                e7 = Entry(fm_data)
                e8 = Entry(fm_data)
                e9 = Entry(fm_data)
                e10 = Entry(fm_data)
                e1.grid(row=1,column=1)
                e2.grid(row=2,column=1)
                e3.grid(row=3,column=1)
                e4.grid(row=4,column=1)
                e5.grid(row=5,column=1)
                e6.grid(row=6,column=1)
                e7.grid(row=7,column=1)
                e8.grid(row=8,column=1)
                e9.grid(row=9,column=1)
                e10.grid(row=10,column=1)
                e1.insert(0,cdata.shouru)
                e2.insert(0,cdata.qizheng)
                e3.insert(0,cdata.wuxian)
                e4.insert(0,cdata.zinv)
                e5.insert(0,cdata.jiaoyu)
                e6.insert(0,cdata.dabing)
                e7.insert(0,cdata.daikuan)
                e8.insert(0,cdata.fangzu)
                e9.insert(0,cdata.yanglao)
                e10.insert(0,cdata.shiji)
                button_c = Button(fm_data, text ="计算", font=("Symbol", 12), command = ButtonCalcData)
                button_c.grid(row=11,column=0)
                button_s = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonDataChangeSave)
                button_s.grid(row=11,column=1)
            break
    #button_add = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonDataChangeSave)
    #button_add.grid(row=11,column=1)
    fm_data.pack(side=LEFT,fill=BOTH)

def ButtonDataChangeSave():
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    global DataChangeAID,lData
    for i in range(len(lData)):
        if lData[i].aid == DataChangeAID:
            if lData[i].date == 0:
                e1["state"] = "readonly"
                e2["state"] = "readonly"
                lData[i].shouru = e1.get().strip(" \t\r\n")
                lData[i].shiji = e2.get().strip(" \t\r\n")
            else:
                e1["state"] = "readonly"
                e2["state"] = "readonly"
                e3["state"] = "readonly"
                e4["state"] = "readonly"
                e5["state"] = "readonly"
                e6["state"] = "readonly"
                e7["state"] = "readonly"
                e8["state"] = "readonly"
                e9["state"] = "readonly"
                e10["state"] = "readonly"
                lData[i].shouru = e1.get().strip(" \t\r\n")
                lData[i].qizheng = e2.get().strip(" \t\r\n")
                lData[i].wuxian = e3.get().strip(" \t\r\n")
                lData[i].zinv = e4.get().strip(" \t\r\n")
                lData[i].jiaoyu = e5.get().strip(" \t\r\n")
                lData[i].dabing = e6.get().strip(" \t\r\n")
                lData[i].daikuan = e7.get().strip(" \t\r\n")
                lData[i].fangzu = e8.get().strip(" \t\r\n")
                lData[i].yanglao = e9.get().strip(" \t\r\n")
                lData[i].shiji = e10.get().strip(" \t\r\n")
            break
    SaveData()

def ButtonData():
    global fm_data,cur_user,cur_mon
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    if cur_user == 0:
        return
    cuser = FindUserByUserid(cur_user)
    lUData = FindUserData(cur_user)
    shouru = 0
    if len(lUData) > 1:
        cur_mon = lUData[-1].date + 1
        shouru = lUData[-1].shouru
    else:
        cur_mon = 1
        shouru = "%.2f"%(float(cuser.wuxian)/0.22)
    if cur_mon > 12:
        tkMessageBox.showwarning("警告", "已录入全年数据")
        return
    if fm_data:
        fm_data.destroy()
    fm_data = Frame(root)
    cstr = "["+cuser.name.decode("gb2312").encode("utf-8")+"]"+str(cur_mon)+"月纳税计算:"
    Label(fm_data, text=cstr, font=("Symbol", 14), height=2).grid(row=0,columnspan=3)
    Label(fm_data, text="总收入：", font=("Symbol", 12), height=2).grid(row=1,sticky=E)
    Label(fm_data, text="起征点：", font=("Symbol", 12), height=2).grid(row=2,sticky=E)
    Label(fm_data, text="五险一金：", font=("Symbol", 12), height=2).grid(row=3,sticky=E)
    Label(fm_data, text="子女教育：", font=("Symbol", 12), height=2).grid(row=4,sticky=E)
    Label(fm_data, text="继续教育：", font=("Symbol", 12), height=2).grid(row=5,sticky=E)
    Label(fm_data, text="大病医疗：", font=("Symbol", 12), height=2).grid(row=6,sticky=E)
    Label(fm_data, text="住房贷款：", font=("Symbol", 12), height=2).grid(row=7,sticky=E)
    Label(fm_data, text="住房租金：", font=("Symbol", 12), height=2).grid(row=8,sticky=E)
    Label(fm_data, text="赡养老人：", font=("Symbol", 12), height=2).grid(row=9,sticky=E)
    Label(fm_data, text="纳税额：", font=("Symbol", 12), height=2).grid(row=10,sticky=E)
    e1 = Entry(fm_data)
    e2 = Entry(fm_data)
    e3 = Entry(fm_data)
    e4 = Entry(fm_data)
    e5 = Entry(fm_data)
    e6 = Entry(fm_data)
    e7 = Entry(fm_data)
    e8 = Entry(fm_data)
    e9 = Entry(fm_data)
    e10 = Entry(fm_data)
    e1.grid(row=1,column=1)
    e2.grid(row=2,column=1)
    e3.grid(row=3,column=1)
    e4.grid(row=4,column=1)
    e5.grid(row=5,column=1)
    e6.grid(row=6,column=1)
    e7.grid(row=7,column=1)
    e8.grid(row=8,column=1)
    e9.grid(row=9,column=1)
    e10.grid(row=10,column=1)
    e1.insert(0,shouru)
    e2.insert(0,5000)
    e3.insert(0,cuser.wuxian)
    e4.insert(0,cuser.zinv)
    e5.insert(0,cuser.jiaoyu)
    e6.insert(0,cuser.dabing)
    e7.insert(0,cuser.daikuan)
    e8.insert(0,cuser.fangzu)
    e9.insert(0,cuser.yanglao)
    e10.insert(0,"")
    e10["state"] = "readonly"
    button_c = Button(fm_data, text ="计算", font=("Symbol", 12), command = ButtonCalcData)
    button_c.grid(row=11,column=0)
    button_s = Button(fm_data, text ="保存", font=("Symbol", 12), command = ButtonAddData)
    button_s.grid(row=11,column=1)
    fm_data.pack(side=LEFT,fill=BOTH)

def ButtonAddData0():
    global lData
    global cur_user,list_mon
    global e1,e2
    if e2.get().strip(" \t\r\n") == "0.00" and e1.get().strip(" \t\r\n") != "0.00":
        tkMessageBox.showwarning("警告", "先计算 再保存")
        return
    cdata = DATA()
    cdata.aid = lData[-1].aid + 1
    cdata.userid = cur_user
    cdata.date = 0
    cdata.shouru = "%.2f"%float(e1.get().strip(" \t\r\n"))
    cdata.shiji = "%.2f"%float(e2.get().strip(" \t\r\n"))
    cdata.jisuan = "%.2f"%float(e2.get().strip(" \t\r\n"))
    lData.append(cdata)
    SaveData()
    list_mon.insert(0, "0 年终奖")
    list_mon.selection_clear(0,END)
    list_mon.selection_set(END)
    SelectMon(None)

def ButtonAddData():
    global lData
    global cur_user,cur_mon,list_mon
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    if e10.get().strip(" \t\r\n") == "":
        tkMessageBox.showwarning("警告", "先计算 再保存")
        return
    cdata = DATA()
    cdata.aid = lData[-1].aid + 1
    cdata.userid = cur_user
    cdata.date = cur_mon
    cdata.shouru = "%.2f"%float(e1.get().strip(" \t\r\n"))
    cdata.qizheng = "%.2f"%float(e2.get().strip(" \t\r\n"))
    cdata.wuxian = "%.2f"%float(e3.get().strip(" \t\r\n"))
    cdata.zinv = "%.2f"%float(e4.get().strip(" \t\r\n"))
    cdata.jiaoyu = "%.2f"%float(e5.get().strip(" \t\r\n"))
    cdata.dabing = "%.2f"%float(e6.get().strip(" \t\r\n"))
    cdata.daikuan = "%.2f"%float(e7.get().strip(" \t\r\n"))
    cdata.fangzu = "%.2f"%float(e8.get().strip(" \t\r\n"))
    cdata.yanglao = "%.2f"%float(e9.get().strip(" \t\r\n"))
    cdata.shiji = "%.2f"%float(e10.get().strip(" \t\r\n"))
    cdata.jisuan = "%.2f"%float(e10.get().strip(" \t\r\n"))
    lData.append(cdata)
    SaveData()
    list_mon.insert(END, str(cdata.date)+" 月")
    list_mon.selection_clear(0,END)
    list_mon.selection_set(END)
    SelectMon(None)

def ButtonDataDel():
    global cur_user,lData
    cuser = FindUserByUserid(cur_user)
    lUData = FindUserData(cur_user)
    for i in range(len(lData)):
        if lData[i].aid == lUData[-1].aid:
            del lData[i]
            break
    SaveData()
    for i in range(list_user.size()):
        if int(list_user.get(i).split('.')[0]) == cur_user:
            list_user.selection_set(i)
    SelectUser(None)

def ButtonCalcData0():
    global e1,e2
    sum = float(e1.get().strip(" \t\r\n"))
    shui = CalcBonus(sum)
    shui = "%.2f"%float(shui)
    e2["state"] = NORMAL
    e2.delete(0,END)
    e2.insert(0,shui)
    e2["state"] = "readonly"

def ButtonCalcData():
    global cur_user,cur_mon
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10
    cdata = DATA()
    cdata.userid = cur_user
    cdata.date = cur_mon
    cdata.shouru = "%.2f"%float(e1.get().strip(" \t\r\n"))
    cdata.qizheng = "%.2f"%float(e2.get().strip(" \t\r\n"))
    cdata.wuxian = "%.2f"%float(e3.get().strip(" \t\r\n"))
    cdata.zinv = "%.2f"%float(e4.get().strip(" \t\r\n"))
    cdata.jiaoyu = "%.2f"%float(e5.get().strip(" \t\r\n"))
    cdata.dabing = "%.2f"%float(e6.get().strip(" \t\r\n"))
    cdata.daikuan = "%.2f"%float(e7.get().strip(" \t\r\n"))
    cdata.fangzu = "%.2f"%float(e8.get().strip(" \t\r\n"))
    cdata.yanglao = "%.2f"%float(e9.get().strip(" \t\r\n"))
    cdata = Calc(cdata)
    if cdata == None:
        return
    e10["state"] = NORMAL
    e10.delete(0,END)
    e10.insert(0,cdata.jisuan)
    e10["state"] = "readonly"

def TkLoop():
    global root
    global lUser,lData
    global list_user,list_mon,fm_data
    root = Tk()
    root.title("2019个税计算")
    curWidth = 800
    curHeight = 600
    scnWidth,scnHeight = root.maxsize()
    tmpcnf = "%dx%d+%d+%d"%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    root.geometry(tmpcnf)
        
    fm_user = Frame(root)
    fm_userbutton = Frame(fm_user)
    button_user = Button(fm_userbutton, text ="修改用户", font=("Symbol", 11),command = ButtonUserChange)
    button_user.pack(side=LEFT)
    button_uchange = Button(fm_userbutton, text ="新增用户", font=("Symbol", 11),command = ButtonUser)
    button_uchange.pack(side=RIGHT)
    fm_userbutton.pack()
    scrl_user = Scrollbar(fm_user)
    scrl_user.pack(side=RIGHT, fill=Y)
    var_user = StringVar()
    list_user = Listbox(fm_user, selectmode=BROWSE, listvariable = var_user, yscrollcommand = scrl_user.set)
    list_user.bind('<<ListboxSelect>>', SelectUser)
    for cuser in lUser:
        list_user.insert(END, str(cuser.aid)+"."+cuser.name.decode("gb2312").encode("utf-8"))
    list_user.pack(side=LEFT, fill=BOTH)
    scrl_user.config(command=list_user.yview)
    fm_user.pack(side=LEFT,fill=BOTH)
    
    fm_mon = Frame(root)
    fm_monbutton = Frame(fm_mon)
    button_data = Button(fm_monbutton, text ="新增数据", font=("Symbol", 11),command = ButtonData)
    button_data.pack()
    fm_monbutton.pack(side=TOP)
    fm_monlist = Frame(fm_mon)
    scrl_mon = Scrollbar(fm_monlist)
    scrl_mon.pack(side=RIGHT, fill=Y)
    var_mon = StringVar()
    list_mon = Listbox(fm_monlist, selectmode=BROWSE, listvariable = var_mon, yscrollcommand = scrl_mon.set)
    list_mon.bind('<<ListboxSelect>>', SelectMon)
    list_mon.pack(side=LEFT, fill=BOTH)
    scrl_mon.config(command=list_mon.yview)
    fm_monlist.pack(expand=1,fill=BOTH)
    fm_monbuttondown = Frame(fm_mon)
    button_datadel = Button(fm_monbuttondown, text ="删除数据", font=("Symbol", 11),command = ButtonDataDel)
    button_datadel.pack(side=LEFT)
    button_dchange = Button(fm_monbuttondown, text ="修改数据", font=("Symbol", 11),command = ButtonDataChange)
    button_dchange.pack(side=RIGHT)
    fm_monbuttondown.pack(side=BOTTOM)
    fm_mon.pack(side=LEFT,fill=BOTH)
    
    list_user.selection_set(0)
    SelectUser(None)
    
    root.mainloop()

def main():
    ReadUser()
    ReadData()
    TkLoop()

if __name__ == '__main__':
    main()

