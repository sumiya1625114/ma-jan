import tkinter
from functools import partial
import copy

#変数宣言
class person:
    def __init__(self):
        self.list_tehai=list()
        self.list_sutehai=list()
        self.tumohai=0

        self.nakitya=list() #暗カンの場合 自身/ 加カンの場合　ポン先の家
        self.nakihai=list() #暗カンの場合 4枚目
        self.nakimentsu=list() #要素数 pon/2 tii/2 minkan/3 ankan/3 kakan/3
        self.nakitype=list() #0pon 1tii 2minkan 3ankan 4kakan
        self.mentsu = list()
        self.sutekouho = list()
        self.matikouho = list() #二次元配列
        self.sute = 0
        self.mati = list() #待ち牌リスト
        self.yaku = list() #各待ちに役つくかの判定フラグのリスト
        self.riichi_flg = 0
        self.riichi_sengenpai = None #リーチ宣言牌の位置
        self.furiten_sute_flg = 0 #捨て牌によるフリテン
        self.furiten_minogashi_flg = 0 #見逃しによる同巡内フリテン
    
    class mentsu: #メンツ候補
        def __init__(self):
            self.syuntsu = list()
            self.kotsu = list()
            self.atama = list()
            self.uki = list()
            self.atamaflg = 0

        
player=person()
com1=person()
com2=person()
com3=person()

#cursor
yama_cur=0
rinsyan_cur=0

#山
#萬子11～19　索子21～29　筒子31～39　白発中41～43　東南西北44～47
list_yama=list()

#親 1~4
oya=1

#場風 1~4 東南西北
bakaze = 1

#fin 0=続行 1=流局 2=和了
fin = 0

#全体のカン回数
kan_cnt = 0

#表示テキスト
text = ""

#main
def main():
    main_window()
    pass


#メインウインドウ
def main_window():
    # ウィンドウの作成、Tkinterオブジェクトの取得
    global window
    window = tkinter.Tk()
    window.tk_setPalette(background="white smoke")
    window.title("ma-jan")

    # ウィンドウのサイズだけを設定
    width   = 800   # 横幅
    height  = 500   # 高さ
    window.geometry(f"{width}x{height}")

    #捨て牌選択ボタンリスト準備
    global sutebtn
    sutebtn = list()
    for i in range(14):
        sutebtn.append(tkinter.Button(window, text=i+1,width=2,command=partial(sute_player,i+1)))

    #鳴き牌選択ボタンリスト準備
    global nakichoicebtn
    nakichoicebtn = list()

    #鳴きボタン準備
    global ponbtn,tiibtn,kanbtn,riichibtn,tumobtn,ronbtn,skipbtn
    ponbtn = tkinter.Button(window)
    tiibtn = tkinter.Button(window)
    kanbtn = tkinter.Button(window)
    riichibtn = tkinter.Button(window)
    tumobtn = tkinter.Button(window)
    ronbtn = tkinter.Button(window)
    skipbtn = tkinter.Button(window)

    #text準備
    global text
    text = tkinter.Label()

    start_btn()

#startボタン
def start_btn():
    global window
    def start_click():
        btn_start.place_forget()
        reset_btn()
        taikyoku()

    btn_start = tkinter.Button(window, text="start",height=1, width=5,command=start_click)
    btn_start.place(x=0,y=0)

#resetボタン
def reset_btn():
    global window
    def reset_click():
        btn_reset.place_forget()
        reset_all()
    btn_reset = tkinter.Button(window, text="reset",height=1, width=5,command=reset_click)
    btn_reset.place(x=0,y=0)

#打牌キーの表示
def sutebtn_hyouji():
    global window
    global sutebtn

    if player.riichi_flg == 0: #通常時
        for i in range(len(player.list_tehai)):
            sutebtn[i].place(x= 25 +(50*i),y=455)

        if player.tumohai != 0:
            sutebtn[13].place(x=725,y=455)
    else:
        sutebtn[13].place(x=725,y=455) #リーチ後

#ドラ表示牌の描画
def dora_hyouji():
    global window
    global canvas_dora
    global kan_cnt
    canvas_dora = tkinter.Canvas(window, bg="white smoke", height=29, width=105)
    canvas_dora.place(x=70, y=10)
    canvas_dora.delete("all")
    canvas_dora.create_line(3,3,105,3,105,29,3,29,3,3,width=3,fill="gray70")

    global img_list_dora
    img_list_dora = list()
    d1 = list_yama[130]
    if kan_cnt == 0:
        d2 = d3 = d4 = d5 = 99
    if kan_cnt == 1:
        d2 = list_yama[128]
        d3 = d4 = d5 = 99
    if kan_cnt == 2:
        d2 = list_yama[128]
        d3 = list_yama[126]
        d4 = d5 = 99
    if kan_cnt == 3:
        d2 = list_yama[128]
        d3 = list_yama[126]
        d4 = list_yama[124]
        d5 = 99
    if kan_cnt == 4:
        d2 = list_yama[128]
        d3 = list_yama[126]
        d4 = list_yama[124]
        d5 = list_yama[122]

    img_list_dora.append(tkinter.PhotoImage(file=f".\img/sute_1/{d1}.png"))
    img_list_dora.append(tkinter.PhotoImage(file=f".\img/sute_1/{d2}.png"))
    img_list_dora.append(tkinter.PhotoImage(file=f".\img/sute_1/{d3}.png"))
    img_list_dora.append(tkinter.PhotoImage(file=f".\img/sute_1/{d4}.png"))
    img_list_dora.append(tkinter.PhotoImage(file=f".\img/sute_1/{d5}.png"))
    for i in range(5):
        canvas_dora.create_image(1 + (21 * i ), 1, image=img_list_dora[i], anchor=tkinter.NW)

#手牌の描画
def tehai_hyouji():
    global window
    global canvas_tehai1,canvas_tehai2,canvas_tehai3,canvas_tehai4,canvas_tehai5,canvas_tehai6,canvas_tehai7
    global canvas_tehai8,canvas_tehai9,canvas_tehai10,canvas_tehai11,canvas_tehai12,canvas_tehai13,canvas_tehai14
    global canvas_naki
    # キャンバス作成
    canvas_tehai1 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai2 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai3 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai4 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai5 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai6 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai7 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai8 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai9 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai10 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai11 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai12 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai13 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)
    canvas_tehai14 = tkinter.Canvas(window, bg="white smoke", height=70, width=50)

    canvas_naki = tkinter.Canvas(window, bg="white smoke", height=165, width=90) #鳴き牌キャンバス

    # キャンバス表示
    canvas_tehai1.place(x=10, y=380)
    canvas_tehai2.place(x=60, y=380)
    canvas_tehai3.place(x=110, y=380)
    canvas_tehai4.place(x=160, y=380)
    canvas_tehai5.place(x=210, y=380)
    canvas_tehai6.place(x=260, y=380)
    canvas_tehai7.place(x=310, y=380)
    canvas_tehai8.place(x=360, y=380)
    canvas_tehai9.place(x=410, y=380)
    canvas_tehai10.place(x=460, y=380)
    canvas_tehai11.place(x=510, y=380)
    canvas_tehai12.place(x=560, y=380)
    canvas_tehai13.place(x=610, y=380)
    canvas_tehai14.place(x=710, y=380)
    
    canvas_naki.place(x=650,y=205) #鳴き牌　表示位置

    canvas_tehai1.delete("all")
    canvas_tehai2.delete("all")
    canvas_tehai3.delete("all")
    canvas_tehai4.delete("all")
    canvas_tehai5.delete("all")
    canvas_tehai6.delete("all")
    canvas_tehai7.delete("all")
    canvas_tehai8.delete("all")
    canvas_tehai9.delete("all")
    canvas_tehai10.delete("all")
    canvas_tehai11.delete("all")
    canvas_tehai12.delete("all")

    canvas_naki.delete("all")

    global img_list_player_tehai
    global img_player_tumohai
    global img_list_naki

    img_list_player_tehai = list()
    img_player_tumohai = ""
    img_list_naki = list()

    #イメージ作成
    for i in range(len(player.list_tehai)):
        x=player.list_tehai[i]
        img_list_player_tehai.append(tkinter.PhotoImage(file=f".\img/tehai/{x}.gif", width=50, height=70)  )     
        #キャンバスにイメージを表示
        code = "canvas_tehai{}.create_image(30, 40, image=img_list_player_tehai[{}], anchor=tkinter.CENTER)".format(i+1,i)
        exec(code)

    #鳴き牌 イメージ表示
    cur = 0
    cnt = 0
    for i in range(len(player.nakimentsu)):
        if player.nakitype[i] <= 1: #pon/tii
            x1 = player.nakimentsu[i][0]
            x2 = player.nakimentsu[i][1]
            y  = player.nakihai[i]
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x1}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x2}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_2/{y}.png"))
            if player.nakitya[i] == com1: #下家
                canvas_naki.create_image(23, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(63, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 3
            if player.nakitya[i] == com2: #対面
                canvas_naki.create_image(23, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 3
            if player.nakitya[i] == com3: #上家
                canvas_naki.create_image(23, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(50, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 3
                pass
        if player.nakitype[i] == 2: #minkan
            x1 = player.nakimentsu[i][0]
            x2 = player.nakimentsu[i][1]
            x3 = player.nakimentsu[i][2]
            y  = player.nakihai[i]
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x1}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x2}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x3}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_2/{y}.png"))
            if player.nakitya[i] == com1: #下家
                canvas_naki.create_image(3 , 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(23, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 139 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(63, 146 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4
            if player.nakitya[i] == com2: #対面
                canvas_naki.create_image(3 , 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(23, 146 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(50, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4
            if player.nakitya[i] == com3: #上家
                canvas_naki.create_image(3 , 146 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(30, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(50, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4
            pass
        if player.nakitype[i] == 3: #ankan
            x1 = player.nakimentsu[i][0]
            x2 = player.nakimentsu[i][1]
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/99.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x1}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x2}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/99.png"))
            
            canvas_naki.create_image(10, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
            canvas_naki.create_image(30, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
            canvas_naki.create_image(50, 139 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
            canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
            cnt += 1
            cur += 4
            pass
        if player.nakitype[i] == 4: #kakan
            x1 = player.nakimentsu[i][0]
            x2 = player.nakimentsu[i][1]
            y1 = player.nakimentsu[i][2]
            y2  = player.nakihai[i]
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x1}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_1/{x2}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_2/{y1}.png"))
            img_list_naki.append(tkinter.PhotoImage(file=f".\img/sute_2/{y2}.png"))
            if player.nakitya[i] == com1: #下家
                canvas_naki.create_image(23, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(63, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(63, 126 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4
            if player.nakitya[i] == com2: #対面
                canvas_naki.create_image(23, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(43, 126 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4
            if player.nakitya[i] == com3: #上家
                canvas_naki.create_image(23, 146 - (41*cnt), image=img_list_naki[2 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(23, 126 - (41*cnt), image=img_list_naki[3 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(50, 139 - (41*cnt), image=img_list_naki[0 + cur], anchor=tkinter.NW)
                canvas_naki.create_image(70, 139 - (41*cnt), image=img_list_naki[1 + cur], anchor=tkinter.NW)
                cnt += 1
                cur += 4   
            pass

        pass

    
    if player.tumohai != 0:
        y = player.tumohai
        img_player_tumohai = tkinter.PhotoImage(file=f".\img/tehai/{y}.gif", width=50, height=70)
        canvas_tehai14.create_image(30, 40, image=img_player_tumohai, anchor=tkinter.CENTER)

#河の描画
def kawa_hyouji():
    global window
    global canvas_center
    global canvas_com1_tehai,canvas_com2_tehai,canvas_com3_tehai
    global img_com1_tehai,img_com2_tehai,img_com3_tehai
    global canvas_kawa_player_1,canvas_kawa_player_2,canvas_kawa_player_3,canvas_kawa_player_4
    global canvas_kawa_com1_1,canvas_kawa_com1_2,canvas_kawa_com1_3,canvas_kawa_com1_4
    global canvas_kawa_com2_1,canvas_kawa_com2_2,canvas_kawa_com2_3,canvas_kawa_com2_4
    global canvas_kawa_com3_1,canvas_kawa_com3_2,canvas_kawa_com3_3,canvas_kawa_com3_4
    #真ん中
    canvas_center = tkinter.Canvas(window, bg="white smoke", height=100, width=100)    
    canvas_center.place(x=350, y=165)
    canvas_center.delete("all")
    canvas_center.create_line(0,0,100,0,width=10,fill="gray70")
    canvas_center.create_line(0,0,0,100,width=10,fill="gray70")
    canvas_center.create_line(0,100,100,100,width=4,fill="gray70")
    canvas_center.create_line(100,100,100,0,width=6,fill="gray70")
    #comの手牌
    canvas_com1_tehai = tkinter.Canvas(window, bg="white smoke", height=215, width=20)  
    canvas_com2_tehai = tkinter.Canvas(window, bg="white smoke", height=20, width=215) 
    canvas_com3_tehai = tkinter.Canvas(window, bg="white smoke", height=215, width=20) 
    canvas_com1_tehai.place(x=750, y=100)
    canvas_com2_tehai.place(x=290, y=30)
    canvas_com3_tehai.place(x=30, y=100)
    canvas_com1_tehai.delete("all")
    canvas_com2_tehai.delete("all")
    canvas_com3_tehai.delete("all")
    img_com1_tehai = tkinter.PhotoImage(file="./img/tehai_com/2.png")
    img_com2_tehai = tkinter.PhotoImage(file="./img/tehai_com/3.png")
    img_com3_tehai = tkinter.PhotoImage(file="./img/tehai_com/4.png")
    canvas_com1_tehai.create_image(5,5,image=img_com1_tehai,anchor=tkinter.NW)
    canvas_com2_tehai.create_image(5,5,image=img_com2_tehai,anchor=tkinter.NW)
    canvas_com3_tehai.create_image(5,5,image=img_com3_tehai,anchor=tkinter.NW)
    
    #河
    canvas_kawa_player_1 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_player_1.place(x=350, y=268)
    canvas_kawa_player_1.delete("all")
    canvas_kawa_player_2 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_player_2.place(x=350, y=296)
    canvas_kawa_player_2.delete("all")
    canvas_kawa_player_3 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_player_3.place(x=350, y=324)
    canvas_kawa_player_3.delete("all")
    canvas_kawa_player_4 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_player_4.place(x=350, y=352)
    canvas_kawa_player_4.delete("all")

    canvas_kawa_com1_1 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com1_1.place(x=450, y=135)
    canvas_kawa_com1_1.delete("all")
    canvas_kawa_com1_2 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com1_2.place(x=478, y=135)
    canvas_kawa_com1_2.delete("all")
    canvas_kawa_com1_3 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com1_3.place(x=506, y=135)
    canvas_kawa_com1_3.delete("all")
    canvas_kawa_com1_4 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com1_4.place(x=534, y=135)
    canvas_kawa_com1_4.delete("all")

    canvas_kawa_com2_4 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_com2_4.place(x=318, y=51)
    canvas_kawa_com2_4.delete("all")
    canvas_kawa_com2_3 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_com2_3.place(x=318, y=79)
    canvas_kawa_com2_3.delete("all")
    canvas_kawa_com2_2 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_com2_2.place(x=318, y=107)
    canvas_kawa_com2_2.delete("all")
    canvas_kawa_com2_1 = tkinter.Canvas(window, bg="white smoke", height=27, width=130)    
    canvas_kawa_com2_1.place(x=318, y=135)
    canvas_kawa_com2_1.delete("all")

    canvas_kawa_com3_4 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com3_4.place(x=236, y=165)
    canvas_kawa_com3_4.delete("all")
    canvas_kawa_com3_3 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com3_3.place(x=264, y=165)
    canvas_kawa_com3_3.delete("all")
    canvas_kawa_com3_2 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com3_2.place(x=292, y=165)
    canvas_kawa_com3_2.delete("all")
    canvas_kawa_com3_1 = tkinter.Canvas(window, bg="white smoke", height=130, width=27)    
    canvas_kawa_com3_1.place(x=320, y=165)
    canvas_kawa_com3_1.delete("all")

    #親表示
    global img_oya1,img_oya2,img_oya3,img_oya4
    global oya
    img_oya1 = tkinter.PhotoImage(file="./img/sonota/o1.png")
    img_oya2 = tkinter.PhotoImage(file="./img/sonota/o2.png")
    img_oya3 = tkinter.PhotoImage(file="./img/sonota/o3.png")
    img_oya4 = tkinter.PhotoImage(file="./img/sonota/o4.png")
    if oya == 1:
        canvas_center.create_image(10,70,image=img_oya1,anchor=tkinter.NW) #p1
    if oya == 2:    
        canvas_center.create_image(70,55,image=img_oya2,anchor=tkinter.NW) #p2
    if oya == 3:  
        canvas_center.create_image(55,10,image=img_oya3,anchor=tkinter.NW) #p3
    if oya == 4:  
        canvas_center.create_image(10,10,image=img_oya4,anchor=tkinter.NW) #p4
    #リー棒表示
    global img_r1,img_r2
    img_r1 = tkinter.PhotoImage(file="./img/sonota/r1.png")
    img_r2 = tkinter.PhotoImage(file="./img/sonota/r2.png")
    if player.riichi_flg == 1:
        canvas_center.create_image(15,95,image=img_r2,anchor=tkinter.NW) #p1
    if com1.riichi_flg == 1:
        canvas_center.create_image(93,15,image=img_r1,anchor=tkinter.NW) #p2
    if com2.riichi_flg == 1:
        canvas_center.create_image(15,3,image=img_r2,anchor=tkinter.NW) #p3
    if com3.riichi_flg == 1:
        canvas_center.create_image(3,15,image=img_r1,anchor=tkinter.NW) #p4
    #捨て牌表示
    global img_list_player_kawa
    img_list_player_kawa = list()
    x=1
    for i in range(len(player.list_sutehai)):
        a=player.list_sutehai[i]
        if player.riichi_sengenpai != i: #通常時
            img_list_player_kawa.append(tkinter.PhotoImage(file=f".\img/sute_1/{a}.png", width=50, height=70))
        else: #リーチ宣言牌
            img_list_player_kawa.append(tkinter.PhotoImage(file=f".\img/sute_2/{a}.png", width=50, height=70))
        #1行目
        if (i+1) <= 6:
            if player.riichi_sengenpai != i:
                code = "canvas_kawa_player_1.create_image({}, 1, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 19
            else:
                code = "canvas_kawa_player_1.create_image({}, 7, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 26
        #2行目
        if 6 < (i+1) <= 12:
            if (i+1) == 7:
                x = 0 #先頭の場合は1にリセット
            if player.riichi_sengenpai != i:
                code = "canvas_kawa_player_2.create_image({}, 1, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 19
            else:
                code = "canvas_kawa_player_2.create_image({}, 7, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 26
        #3行目
        if 12 < (i+1) <= 18:
            if (i+1) == 13:
                x = 0
            if player.riichi_sengenpai != i:
                code = "canvas_kawa_player_3.create_image({}, 1, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 19
            else:
                code = "canvas_kawa_player_3.create_image({}, 7, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 26
        #4行目
        if 18 < (i+1):
            if (i+1) == 19:
                x = 0
            if player.riichi_sengenpai != i:
                code = "canvas_kawa_player_4.create_image({}, 1, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 19
            else:
                code = "canvas_kawa_player_4.create_image({}, 7, image=img_list_player_kawa[{}], anchor=tkinter.NW)".format(x,i)
                exec(code)
                x += 26
    #捨て牌表示 com1
    global img_list_com1_kawa
    img_list_com1_kawa = list()
    x=112
    #1行目
    for i in range(len(com1.list_sutehai)):
        a=com1.list_sutehai[i]
        img_list_com1_kawa.append(tkinter.PhotoImage(file=f".\img/sute_2/{a}.png", width=50, height=70)  )     
        if (i+1) <= 6:
            code = "canvas_kawa_com1_1.create_image(1, {}, image=img_list_com1_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #2行目
        if 6 < (i+1) <= 12:
            if (i+1) == 7:
                x=112
            code = "canvas_kawa_com1_2.create_image(1, {}, image=img_list_com1_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #3行目
        if 12 < (i+1) <= 18:
            if (i+1) == 13:
                x=112
            code = "canvas_kawa_com1_3.create_image(1, {}, image=img_list_com1_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #4行目
        if 18 < (i+1):
            if (i+1) == 19:
                x=112
            code = "canvas_kawa_com1_4.create_image(1, {}, image=img_list_com1_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
    #捨て牌表示 com2
    global img_list_com2_kawa
    img_list_com2_kawa = list()
    x=112
    #1行目
    for i in range(len(com2.list_sutehai)):
        a=com2.list_sutehai[i]
        img_list_com2_kawa.append(tkinter.PhotoImage(file=f".\img/sute_3/{a}.png", width=50, height=70)  )     
        if (i+1) <= 6:
            code = "canvas_kawa_com2_1.create_image({}, 1, image=img_list_com2_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #2行目
        if 6 < (i+1) <= 12:
            if (i+1) == 7:
                x=112
            code = "canvas_kawa_com2_2.create_image({}, 1, image=img_list_com2_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #3行目
        if 12 < (i+1) <= 18:
            if (i+1) == 13:
                x=112
            code = "canvas_kawa_com2_3.create_image({}, 1, image=img_list_com2_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
        #4行目
        if 18 < (i+1):
            if (i+1) == 19:
                x=112
            code = "canvas_kawa_com2_4.create_image({}, 1, image=img_list_com2_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x -= 19
    #捨て牌表示 com3
    global img_list_com3_kawa
    img_list_com3_kawa = list()
    x=1
    #1行目
    for i in range(len(com3.list_sutehai)):
        a=com3.list_sutehai[i]
        img_list_com3_kawa.append(tkinter.PhotoImage(file=f".\img/sute_4/{a}.png", width=50, height=70)  )     
        if (i+1) <= 6:
            code = "canvas_kawa_com3_1.create_image(1, {}, image=img_list_com3_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x += 19
        #2行目
        if 6 < (i+1) <= 12:
            if (i+1) == 7:
                x=1
            code = "canvas_kawa_com3_2.create_image(1, {}, image=img_list_com3_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x += 19
        #3行目
        if 12 < (i+1) <= 18:
            if (i+1) == 13:
                x=1
            code = "canvas_kawa_com3_3.create_image(1, {}, image=img_list_com3_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x += 19
        #4行目
        if 18 < (i+1):
            if (i+1) == 19:
                x=1
            code = "canvas_kawa_com3_4.create_image(1, {}, image=img_list_com3_kawa[{}], anchor=tkinter.NW)".format(x,i)
            exec(code)
            x += 19
    
#洗牌
def sipai():
    #kazu
    for k in range(3):
        for j in range(9):
            for i in range(4):
                list_yama.append((k+1)*10 + j+1)
    #jihai
    for j in range(7):
        for i in range(4):
            list_yama.append(4*10 + j+1)

#山を混ぜる
def mazeru():
    import random
    random.shuffle(list_yama) 

#親決め
def oyakime():
    import random
    global oya
    oya = random.randint(1,4)

#配牌
def haipai(name):
    global yama_cur
    for i in range(13):
        x=list_yama[yama_cur]
        name.list_tehai.append(x)
        yama_cur += 1

#理牌
def ripai(name):
    name.list_tehai.sort()

#ツモ処理
def tumo(name):
    global yama_cur
    x=list_yama[yama_cur]
    name.tumohai=x
    yama_cur += 1
    name.furiten_minogashi_flg = 0 #同順内見逃しフリテンフラグのリセット

    tehai_hyouji()
    tenpai_check(name) #テンパイの確認

    if name == player:
        k = ankan_check(name) #playerが暗カン加カンできるか確認
        flg = k[0]
        result_ankan = k[1]
        result_kakan = k[2]

        nakip_btn(name,result_ankan,result_kakan) #鳴きボタンplayerを呼び出す
        sute(name)        
    else:
        sute(name) #suteを呼び出す

#嶺上ツモ処理
def rinsyan_tumo(name):
    global rinsyan_cur,kan_cnt
    name.furiten_minogashi_flg = 0 #同順内見逃しフリテンフラグのリセット

    if rinsyan_cur <= 1:
        x=list_yama[134 + rinsyan_cur]
    else:
        x=list_yama[132 + rinsyan_cur - 2]
    name.tumohai=x
    rinsyan_cur += 1
    kan_cnt += 1

    tehai_hyouji()
    dora_hyouji()
    tenpai_check(name) #テンパイの確認

    if name == player:
        k = ankan_check(name) #playerが追加で暗カン加カンできるか確認
        flg = k[0]
        result_ankan = k[1]
        result_kakan = k[2]

        nakip_btn(name,result_ankan,result_kakan) #鳴きボタンplayerを呼び出す
        sute(name)
        pass
    else:
        sute(name) #suteを呼び出す
    
#親名を返す関数
def oya_who():
    global oya

    if oya == 1:
        return player
    if oya == 2:
        return com1
    if oya == 3:
        return com2
    if oya == 4:
        return com3  

#捨て牌処理
def sute(name):
    #ツモ切り
    if name != player:
        name.list_sutehai.append(name.tumohai)
        name.tumohai = 0
        ripai(name)
        kawa_hyouji()
        furiten_check(name)

        n = naki_check(player,name) #playerが鳴くか確認 (鳴く人,捨てた人)
        nflg = n[0]
        result_pon = n[1]
        result_tii = n[2]
        result_kan = n[3]

        if player.riichi_flg == 1: #リーチ後は鳴けない
            nflg = 0        
            
        naki_btn(name,nflg,result_pon,result_tii,result_kan) #鳴き選択ボタンの表示
        pass           

    else:
        sutebtn_hyouji()

        
#捨て処理（プレイヤー）
def sute_player(input):
    nakibtn_del()
    sutebtn_del()

    #各候補を実際の捨て牌/待ち牌に格納
    tehai = list()
    tehai = player.list_tehai.copy()
    tflg = 0

    for i in range(len(player.sutekouho)): #捨て候補にあるか確認
        if input == 14:
            if player.tumohai == player.sutekouho[i]:
                tflg = 1
        else:
            if tehai[input-1] == player.sutekouho[i]:
                tflg = 1
    
    if tflg == 1:
        if input == 14:
            player.sute = player.tumohai
        else:
            player.sute = tehai[input-1]

        for i in range(len(player.sutekouho)):
            if player.sutekouho[i] == player.sute:
                cur = i
        player.mati = copy.deepcopy(player.matikouho[cur])

    #鳴き後の処理かツモ後か判断
    if player.tumohai != 0: #ツモ後
        if input == 14:
            player.list_sutehai.append(player.tumohai)
            player.tumohai = 0
            ripai(player)
            tehai_hyouji()
            kawa_hyouji()
            furiten_check(player)
            turnp(nextp(player))
        else:
            player.list_sutehai.append(player.list_tehai[input - 1])
            player.list_tehai[input - 1] = player.tumohai
            player.tumohai = 0
            ripai(player)
            tehai_hyouji()
            kawa_hyouji()
            furiten_check(player)
            turnp(nextp(player))
    else: #鳴き後
        player.list_sutehai.append(player.list_tehai[input - 1])
        del player.list_tehai[input - 1] #切った牌を手牌から削除
        ripai(player)
        tehai_hyouji()
        kawa_hyouji()
        furiten_check(player)
        turnp(nextp(player))

#次のプレイヤー
def nextp(name):
    #次のプレイヤーを返す
    if name == player:
        return com1
    if name == com1:
        return com2
    if name == com2:
        return com3
    if name == com3:
        return player
    pass
    

#ツモ順のプレイヤーターン処理
def turnp(name):
    global fin
    check_ryu()
    if fin == 0:
        tumo(name)
    elif fin == 1:
        ryukyoku()
    pass

#流局のチェック
def check_ryu():
    global yama_cur
    global kan_cnt,fin
    if yama_cur == (122 - kan_cnt):
        fin = 1

#流局処理
def ryukyoku():
    messege(1)

#メッセージの描画
def messege(type):
    global text
    
    if type == 1: #流局
        text = tkinter.Label(text="流局",font=("Helvetica",15))
        text.place(x=70,y=45)
    elif type == 2: #和了
        text = tkinter.Label(text="和了",font=("Helvetica",15))
        text.place(x=70,y=45)
    else:
        pass

#reset
def reset():
    global yama_cur,fin,kan_cnt,list_yama,rinsyan_cur
    player.__init__()
    com1.__init__()
    com2.__init__()
    com3.__init__()
    yama_cur=0
    rinsyan_cur=0
    fin=0
    kan_cnt=0
    list_yama=list()

    sutebtn_del()
    nakibtn_del()
    nakichoicebtn_del()
    canv_del()

    pass

#reset_all
def reset_all():
    reset()
    start_btn()
    pass

#sutebtn_del
def sutebtn_del():
    global sutebtn
    for i in range(14):
        sutebtn[i].place_forget()
        pass

#nakibtn_del
def nakibtn_del():
    global ponbtn,tiibtn,kanbtn,riichibtn,tumobtn,ronbtn,skipbtn
    ponbtn.place_forget()
    tiibtn.place_forget()
    kanbtn.place_forget()
    riichibtn.place_forget()
    tumobtn.place_forget()
    ronbtn.place_forget()
    skipbtn.place_forget()
    pass

#nakichoicebtn_del
def nakichoicebtn_del():
    global nakichoicebtn
    for i in range(len(nakichoicebtn)):
        nakichoicebtn[i].place_forget()
        pass

#canv_del
def canv_del():
    global canvas_tehai1,canvas_tehai2,canvas_tehai3,canvas_tehai4,canvas_tehai5,canvas_tehai6,canvas_tehai7
    global canvas_tehai8,canvas_tehai9,canvas_tehai10,canvas_tehai11,canvas_tehai12,canvas_tehai13,canvas_tehai14
    canvas_tehai1.destroy()
    canvas_tehai2.destroy()
    canvas_tehai3.destroy()
    canvas_tehai4.destroy()
    canvas_tehai5.destroy()
    canvas_tehai6.destroy()
    canvas_tehai7.destroy()
    canvas_tehai8.destroy()
    canvas_tehai9.destroy()
    canvas_tehai10.destroy()
    canvas_tehai11.destroy()
    canvas_tehai12.destroy()
    canvas_tehai13.destroy()
    canvas_tehai14.destroy()

    global canvas_center,canvas_dora
    global canvas_kawa_player_1,canvas_kawa_player_2,canvas_kawa_player_3,canvas_kawa_player_4
    global canvas_kawa_com1_1,canvas_kawa_com1_2,canvas_kawa_com1_3,canvas_kawa_com1_4
    global canvas_kawa_com2_1,canvas_kawa_com2_2,canvas_kawa_com2_3,canvas_kawa_com2_4
    global canvas_kawa_com3_1,canvas_kawa_com3_2,canvas_kawa_com3_3,canvas_kawa_com3_4
    global canvas_naki

    canvas_center.delete("all")
    canvas_naki.delete("all")
    canvas_dora.delete("all")
    canvas_kawa_player_1.destroy()
    canvas_kawa_player_2.destroy()
    canvas_kawa_player_3.destroy()
    canvas_kawa_player_4.destroy()
    canvas_kawa_com1_1.destroy()
    canvas_kawa_com1_2.destroy()
    canvas_kawa_com1_3.destroy()
    canvas_kawa_com1_4.destroy()
    canvas_kawa_com2_1.destroy()
    canvas_kawa_com2_2.destroy()
    canvas_kawa_com2_3.destroy()
    canvas_kawa_com2_4.destroy()
    canvas_kawa_com3_1.destroy()
    canvas_kawa_com3_2.destroy()
    canvas_kawa_com3_3.destroy()
    canvas_kawa_com3_4.destroy()

    global canvas_com1_tehai,canvas_com2_tehai,canvas_com3_tehai
    canvas_com1_tehai.destroy()
    canvas_com2_tehai.destroy()
    canvas_com3_tehai.destroy()

    global text
    text.place_forget()
    text.destroy()

#naki_check 戻り値 (flg,result_pon,result_tii,result_kan)
def naki_check(n_name,s_name): #鳴く人,捨てた人
    pai = s_name.list_sutehai[-1]
    tehai = n_name.list_tehai.copy()
    result_pon = list()
    result_tii = list()
    result_kan = list()
    flg = 0
    temppon = list()
    tempkan = list()

    #ハイテイは鳴けない
    if yama_cur == (122 - kan_cnt):
        return flg,result_pon,result_tii,result_kan

    #pon
    if n_name == player:
        for i in range(len(player.list_tehai)):
            if pai == tehai[i]:
                temppon.append(i)

        if len(temppon) >= 2:
            result_pon.append(temppon[0])
            result_pon.append(temppon[1])
            flg = 1
            
        else:
            pass
    
    #tii
    if  n_name == player and s_name == com3: #プレイヤーかつ上家の捨て牌
        for i in range(len(player.list_tehai)):
            if pai//10 != 4:
                if pai - 2 == tehai[i] : #末尾に付ける場合
                    temp1 = i
                    for j in range(i+1,len(player.list_tehai)):
                        if pai - 1 == tehai[j]:
                            temp2 = j
                            result_tii.append([temp1,temp2])
                            flg = 1
                if pai - 1 == tehai[i] : #真ん中に付ける場合
                    temp3 = i
                    for k in range(i+1,len(player.list_tehai)):
                        if pai + 1 == tehai[k] :
                            temp4 = k
                            result_tii.append([temp3,temp4])
                            flg = 1
                if pai + 1 == tehai[i] : #先頭に付ける場合
                    temp5 = i
                    for l in range(i+1,len(player.list_tehai)):
                        if pai + 2 == tehai[l] :
                            temp6 = l
                            result_tii.append([temp5,temp6])
                            flg = 1
    #kan
    if n_name == player:
        for i in range(len(player.list_tehai)):
            if pai == tehai[i]:
                tempkan.append(i)

        if len(tempkan) >= 3:
            result_kan = tempkan.copy()
            flg = 1
            
        else:
            pass

    return flg,result_pon,result_tii,result_kan

#ankan_check
def ankan_check(name):
    result_ankan = list()
    result_kakan = list()
    tehai = list()
    flg = 0

    tehai = name.list_tehai.copy()
    tehai.append(name.tumohai) #ツモ含めた手牌
    t = len(tehai) - 1 #最後の牌（ツモ牌）の位置

    if yama_cur == (122 - kan_cnt): #ハイテイは鳴けない
        return flg,result_ankan,result_kakan

    for i in range(len(tehai)): #暗槓の確認
        #4つ同じ牌を探す
        for j in range(i+1,len(tehai)):
            if tehai[i] == tehai[j]:
                for k in range(j+1,len(tehai)):
                    if tehai[i] == tehai[k]:
                        for l in range(k+1,len(tehai)):
                            if tehai[i] == tehai[l]:
                                if l == t: #ツモ牌なら13に変換
                                    a = 13
                                else:
                                    a = l
                                result_ankan.append([i,j,k,a])
                                flg += 1
    
    plist = list()

    for i in range(len(name.nakitype)): #加カンの確認
        if name.nakitype[i] == 0:
            plist.append(i) #ponのみリスト化
    for i in range(len(plist)): #同じ牌を探索
        for j in range(len(tehai)):
            if tehai[j] == name.nakihai[plist[i]]: #pon牌と同じ
                if j == t: #ツモ牌なら13に変換
                    a = 13
                else:
                    a = j
                result_kakan.append(a)
                flg += 1
    return flg,result_ankan,result_kakan

#naki_btn　#プレイヤー以外のツモ番
def naki_btn(name,nflg,result_pon,result_tii,result_kan):
    rflg = 0 #ロンフラグ

    if (atarihai_check(player,name.list_sutehai[-1]) == 2 and
        player.furiten_sute_flg == 0 and player.furiten_minogashi_flg == 0):
        rflg = 1

    if nflg == 1:
        if len(result_pon) > 0:
            ponbtn_hyouji(name,result_pon)
        if len(result_tii) > 0:
            tiibtn_hyouji(name,result_tii)
        if len(result_kan) > 0:
            kanbtn_hyouji(name,result_kan)
        if rflg == 1:
            ronbtn_hyouji(name) #name:捨てた人
        skipbtn_hyouji(name)
    elif rflg == 1:
        ronbtn_hyouji(name)
        skipbtn_hyouji(name)
    else:
        turnp(nextp(name))
    pass

#nakip_btn #プレイヤーのツモ番
def nakip_btn(name,result_ankan,result_kakan):
    if len(result_ankan) + len(result_kakan) > 0 and name.riichi_flg == 0: #カン/カン候補あるか(and リーチ後不可)
        ankanbtn_hyouji(name,result_ankan,result_kakan)
    if atarihai_check(name,name.tumohai) >= 1: #ツモ/あたり牌か
        if atarihai_check(name,name.tumohai) == 2 or menzen_check(name) == 1: #役なしかつ鳴いてたら不可
            tumobtn_hyouji(name)
    if menzen_check(name) == 1 and len(name.sutekouho) > 0 and name.riichi_flg == 0: #リーチ/面前かつ捨て候補がある(and リーチ後不可)
        riichibtn_hyouji(name)
    pass

#atarihai_check
def atarihai_check(name,pai): #0:なし 1:役なしあたり 2:役ありあたり
    atari_flg = 0
    for i in range(len(name.mati)):
        if name.mati[i] == pai:
            atari_flg = 2
    return atari_flg

#menzen_check
def menzen_check(name): #面前なら1
    menzen_flg = 1
    for i in range(len(name.nakitype)):
        if name.nakitype[i] != 3: #nakitype3は暗カン
            menzen_flg = 0
    return menzen_flg

#ponbtn_hyouji
def ponbtn_hyouji(name,result_pon):
    global window,ponbtn
    def pon_click():
        nakibtn_del()
        pon_main(name,result_pon)

    ponbtn = tkinter.Button(window, text="ポン",height=1, width=5,command=pon_click)
    ponbtn.place(x=550,y=280)
    #色つけ
    l = len(name.list_sutehai) #捨て牌の数
    a = (l + 6 -1)//6 #切り上げ(a+b-1)//b 何個目の河か
    b = l - (6 * (a - 1)) #何個目の牌か
    
    if name == com1:
        code = "canvas_kawa_com1_{}.create_line(0,130 -(20*{}),27,130 -(20*{}),width=3,fill='red')".format(a,b,b)
    if name == com2:
        code = "canvas_kawa_com2_{}.create_line(130 -(20*{}),0,130 -(20*{}),27,width=3,fill='red')".format(a,b,b)
    if name == com3:
        code = "canvas_kawa_com3_{}.create_line(0,1 +(20*{}),27,1 +(20*{}),width=3,fill='red')".format(a,b,b)
    exec(code)
    pass

#tiibtn_hyouji
def tiibtn_hyouji(name,result_tii):
    global window,tiibtn
    def tii_click():
        nakibtn_del()
        if len(result_tii) == 1: #一個だけなら飛ばす
            result = result_tii[0] #一次元配列に変換して渡す
            tii_main(name,result)
        else:
            tii_select(name,result_tii)
        
    tiibtn = tkinter.Button(window, text="チー",height=1, width=5,command=tii_click)
    tiibtn.place(x=550,y=310)

    #色つけ
    l = len(name.list_sutehai) #捨て牌の数
    a = (l + 6 -1)//6 #切り上げ(a+b-1)//b 何個目の河か
    b = l - (6 * (a - 1)) #何個目の牌か
    
    if name == com1:
        code = "canvas_kawa_com1_{}.create_line(0,130 -(20*{}),27,130 -(20*{}),width=3,fill='red')".format(a,b,b)
    if name == com2:
        code = "canvas_kawa_com2_{}.create_line(130 -(20*{}),0,130 -(20*{}),27,width=3,fill='red')".format(a,b,b)
    if name == com3:
        code = "canvas_kawa_com3_{}.create_line(0,1 +(20*{}),27,1 +(20*{}),width=3,fill='red')".format(a,b,b)
    exec(code)

    pass

#kanbtn_hyouji
def kanbtn_hyouji(name,result_kan):
    global window,kanbtn
    def kan_click():
        nakibtn_del()
        kan_main(name,2,result_kan) #2 minkan
        
    kanbtn = tkinter.Button(window, text="カン",height=1, width=5,command=kan_click)
    kanbtn.place(x=550,y=340)

    #色つけ
    l = len(name.list_sutehai) #捨て牌の数
    a = (l + 6 -1)//6 #切り上げ(a+b-1)//b 何個目の河か
    b = l - (6 * (a - 1)) #何個目の牌か
    
    if name == com1:
        code = "canvas_kawa_com1_{}.create_line(0,130 -(20*{}),27,130 -(20*{}),width=3,fill='red')".format(a,b,b)
    if name == com2:
        code = "canvas_kawa_com2_{}.create_line(130 -(20*{}),0,130 -(20*{}),27,width=3,fill='red')".format(a,b,b)
    if name == com3:
        code = "canvas_kawa_com3_{}.create_line(0,1 +(20*{}),27,1 +(20*{}),width=3,fill='red')".format(a,b,b)
    exec(code)
    pass

#ankanbtn_hyouji
def ankanbtn_hyouji(name,result_ankan,result_kakan):
    global window,kanbtn
    def kan_click():
        sutebtn_del() #捨てボタンも消す
        nakibtn_del()
        if len(result_ankan) + len(result_kakan) == 1:
            if len(result_ankan) == 1:
                result = result_ankan[0] #一次元配列に変換して渡す
                kan_main(name,3,result) #3 ankan
            else:
                result = result_kakan #一次元配列のまま渡す
                kan_main(name,4,result) #4 kakan
        else:
            ankan_select(name,result_ankan,result_kakan)
        
    kanbtn = tkinter.Button(window, text="カン",height=1, width=5,command=kan_click)
    kanbtn.place(x=550,y=340)
    pass

#riichibtn_hyouji
def riichibtn_hyouji(name):
    global window,riichibtn
    def riichi_click():
        sutebtn_del() #捨てボタンも消す
        nakibtn_del()
        riichi_select(name)
        
    riichibtn = tkinter.Button(window, text="リーチ",height=1, width=5,command=riichi_click)
    riichibtn.place(x=600,y=250)
    pass

#tumobtn_hyouji
def tumobtn_hyouji(name):
    global window,tumobtn
    def tumo_click():
        sutebtn_del() #捨てボタンも消す
        nakibtn_del()
        messege(2) #とりあえず和了表示
        
    tumobtn = tkinter.Button(window, text="ツモ",height=1, width=5,command=tumo_click)
    tumobtn.place(x=600,y=280)
    pass

#ronbtn_hyouji
def ronbtn_hyouji(name):
    global window,ronbtn
    player.furiten_minogashi_flg = 1 #見逃しフラグ

    def ron_click():
        nakibtn_del()
        messege(2) #とりあえず和了表示

    #色つけ
    l = len(name.list_sutehai) #捨て牌の数
    a = (l + 6 -1)//6 #切り上げ(a+b-1)//b 何個目の河か
    b = l - (6 * (a - 1)) #何個目の牌か
    
    if name == com1:
        code = "canvas_kawa_com1_{}.create_line(0,130 -(20*{}),27,130 -(20*{}),width=3,fill='red')".format(a,b,b)
    if name == com2:
        code = "canvas_kawa_com2_{}.create_line(130 -(20*{}),0,130 -(20*{}),27,width=3,fill='red')".format(a,b,b)
    if name == com3:
        code = "canvas_kawa_com3_{}.create_line(0,1 +(20*{}),27,1 +(20*{}),width=3,fill='red')".format(a,b,b)
    exec(code)
        
    ronbtn = tkinter.Button(window, text="ロン",height=1, width=5,command=ron_click)
    ronbtn.place(x=600,y=310)
    pass

#skipbtn_hyouji
def skipbtn_hyouji(name):
    global window,skipbtn
    def skip_click():
        nakibtn_del()
        kawa_hyouji()
        turnp(nextp(name))
        
    skipbtn = tkinter.Button(window, text="skip",height=1, width=5,command=skip_click)
    skipbtn.place(x=600,y=340)
    pass

#pon_main
def pon_main(name,result_pon):
    player.furiten_minogashi_flg = 0 #見逃しフラグリセット

    #鳴き用手牌に格納
    player.nakitya.append(name)
    player.nakihai.append(name.list_sutehai[-1])
    t1 = result_pon[0]
    t2 = result_pon[1]
    player.nakimentsu.append([player.list_tehai[t1],player.list_tehai[t2]])
    player.nakitype.append(0) #0pon 1tii 2minkan 3ankan 4kakan

    #削除
    del name.list_sutehai[-1]
    del player.list_tehai[t1 : t1 + 2]

    tenpai_check(player) #テンパイの確認
    
    #表示更新
    tehai_hyouji()
    kawa_hyouji()

    #suteへ移動
    sute(player)
    pass

#tii_select
def tii_select(name,result_tii):
    global window
    global nakichoicebtn
    nakichoicebtn.clear()

    #結果を使いやすく組み替える
    xlist = list()
    for i in range(len(result_tii)):
        xlist.append(result_tii[i][0])
        xlist.append(result_tii[i][1])
        pass

    xset = set(xlist) #重複削除した集合
    unique_list = list(xset) #一意のリスト
    unique_list.sort()

    global nakichoice_flg,nakichoice_select1,nakichoice_select2,nakichoice_name
    nakichoice_flg = 0
    nakichoice_select1 = 0
    nakichoice_select2 = 0
    nakichoice_name = name
    

    def nakichoice_click(input): 
        global nakichoice_flg,nakichoice_select1,nakichoice_select2
        if nakichoice_flg == 0: #選択一回目
            nakichoicebtn_del()
            nakichoice_select1 = input
            tmplist = list()
            

            for i in range(len(result_tii)):
                if input == result_tii[i][0]:
                    tmplist.append(result_tii[i][1])
                if input == result_tii[i][1]:
                    tmplist.append(result_tii[i][0])
            
            tmplist.sort()
            
            #色付け
            code1 = "canvas_tehai{}.create_line(0,0,50,0,width=5,fill='red')".format(input +1)
            code2 = "canvas_tehai{}.create_line(0,0,0,70,width=5,fill='red')".format(input +1)
            code3 = "canvas_tehai{}.create_line(0,70,50,70,width=5,fill='red')".format(input +1)
            code4 = "canvas_tehai{}.create_line(50,70,50,0,width=5,fill='red')".format(input +1)
            exec(code1)
            exec(code2)
            exec(code3)
            exec(code4)

            for i in range(len(tmplist)): #二次ボタン配置
                nakichoicebtn[tmplist[i]].place(x= 25 +(50 * tmplist[i]),y=455)

        if nakichoice_flg == 1: #選択二回目
            nakichoicebtn_del()
            nakichoice_select2 = input

            #色消し
            code = "canvas_tehai{}.delete('all')".format(nakichoice_select1 +1)
            exec(code)

            result = list()
            result.append(nakichoice_select1)
            result.append(nakichoice_select2)
            result.sort()

            tii_main(nakichoice_name,result) #tii_main　呼び出し
            
        nakichoice_flg = 1 #選択回数

        pass

    for i in range(14): #ボタン作成
        nakichoicebtn.append(tkinter.Button(window, text=i+1,width=2,command=partial(nakichoice_click,i)))

    for i in range(len(unique_list)): #一次ボタン配置
        nakichoicebtn[unique_list[i]].place(x= 25 +(50 * unique_list[i]),y=455)

#ankan_select
def ankan_select(name,result_ankan,result_kakan):
    global window
    global nakichoicebtn
    nakichoicebtn.clear()
    unique_list = list()

    for i in range(len(result_ankan)): #ulist作成
        unique_list.append(result_ankan[i][0])
    for i in range(len(result_kakan)):
        unique_list.append(result_kakan[i])

    def nakichoice_click(input):
        nakichoicebtn_del()
        result = list()
        kflg = 0

        for i in range(len(result_ankan)): #選択がankanか確認
            if result_ankan[i][0] == input:
                kflg = 3
                result = (result_ankan[i][0],result_ankan[i][1],result_ankan[i][2],result_ankan[i][3]) 
        
        for i in range(len(result_kakan)): #選択がkakanか確認
            if result_kakan[i] == input:
                kflg = 4
                result.append(result_kakan[i])


        kan_main(name,kflg,result) #kflg 3ankan 4kakan

        pass


    for i in range(14): #ボタン作成
        nakichoicebtn.append(tkinter.Button(window, text=i+1,width=2,command=partial(nakichoice_click,i)))

    for i in range(len(unique_list)): #ボタン配置
        if unique_list[i] != 13:
            nakichoicebtn[unique_list[i]].place(x= 25 +(50 * unique_list[i]),y=455)
        else:
            nakichoicebtn[13].place(x=725,y=455)
    pass

#riichi_select
def riichi_select(name):
    global window
    global nakichoicebtn
    nakichoicebtn.clear()

    tehai = list()
    tehai = copy.deepcopy(name.list_tehai)
    tehai += [name.tumohai]
    posl = list()

    for i in range(len(tehai)): #捨て候補を位置poslに変換
        for j in range(len(name.sutekouho)):
            if tehai[i] == name.sutekouho[j]:
                posl.append(i)
        pass

    def nakichoice_click(input):
        nakichoicebtn_del()

        #各候補を実際の捨て牌/待ち牌に格納
        name.sute = tehai[input]
        for i in range(len(name.sutekouho)):
            if name.sutekouho[i] == name.sute:
                cur = i
        name.mati = copy.deepcopy(name.matikouho[cur])
        
        #捨て処理
        if input == 13:
            name.list_sutehai.append(name.tumohai)
            name.tumohai = 0 
        else:
            name.list_sutehai.append(name.list_tehai[input])
            name.list_tehai[input] = name.tumohai
            name.tumohai = 0            

        #各フラグ更新処理
        name.riichi_flg = 1
        name.riichi_sengenpai = len(name.list_sutehai)-1
        furiten_check(name)        

        #次のプレイヤーへ
        ripai(name)
        tehai_hyouji()
        kawa_hyouji()
        turnp(nextp(name))
        pass

    for i in range(14): #ボタン作成
        nakichoicebtn.append(tkinter.Button(window, text=i+1,width=2,command=partial(nakichoice_click,i)))

    for i in range(len(posl)): #ボタン配置
        if posl[i] != 13:
            nakichoicebtn[posl[i]].place(x= 25 +(50 * posl[i]),y=455)
            pass
        else:
            nakichoicebtn[13].place(x=725,y=455)
    pass

#furiten_check
def furiten_check(name):
    for i in range(len(name.mati)):
        for j in range(len(name.list_sutehai)):
            if name.mati[i] == name.list_sutehai[j]:
                name.furiten_sute_flg = 1

#tii_main
def tii_main(name,result_tii):
    player.furiten_minogashi_flg = 0 #見逃しフラグリセット

    #鳴き用手牌に格納
    player.nakitya.append(name)
    player.nakihai.append(name.list_sutehai[-1])
    t1 = result_tii[0]
    t2 = result_tii[1]
    player.nakimentsu.append([player.list_tehai[t1],player.list_tehai[t2]])
    player.nakitype.append(1) #0pon 1tii 2minkan 3ankan 4kakan

    #削除
    del name.list_sutehai[-1]
    del player.list_tehai[t1]
    del player.list_tehai[t2 - 1] #直前の削除でずれるから一個まえ

    tenpai_check(player) #テンパイの確認
    
    #表示更新
    tehai_hyouji()
    kawa_hyouji()

    #suteへ移動
    sute(player)
    pass

#kan_main
def kan_main(name,kflg,result_kan): #kflg 2minkan 3ankan 4kakan
    p = 0
    if kflg == 2: #minkan
        #鳴き用手牌に格納
        player.nakitya.append(name)
        player.nakihai.append(name.list_sutehai[-1])
        t1 = result_kan[0]
        t2 = result_kan[1]
        t3 = result_kan[2]
        player.nakimentsu.append([player.list_tehai[t1],player.list_tehai[t2],player.list_tehai[t3]])
        player.nakitype.append(kflg) #0pon 1tii 2minkan 3ankan 4kakan

        #削除
        del name.list_sutehai[-1]
        del player.list_tehai[t1 : t1 + 3]

    if kflg == 3: #ankan
        #鳴き用手牌に格納
        t1 = result_kan[0]
        t2 = result_kan[1]
        t3 = result_kan[2]
        t4 = result_kan[3]
        player.nakitya.append(name)
        p = name.list_tehai[t1] #鳴き牌

        if t4 == 13: #ツモ牌を含むか
            player.nakihai.append(name.tumohai)
        else:
            player.nakihai.append(name.list_tehai[t4])

        player.nakimentsu.append([player.list_tehai[t1],player.list_tehai[t2],player.list_tehai[t3]])
        player.nakitype.append(kflg) #0pon 1tii 2minkan 3ankan 4kakan

        #削除
        if t4 == 13:
            name.tumohai = 0
            del player.list_tehai[t1 : t1 + 3]
        else:
            del player.list_tehai[t1 : t1 + 4]
            player.list_tehai.append(player.tumohai)
            name.tumohai = 0
    
    if kflg == 4: #kakan
        #鳴き用手牌に格納
        t = result_kan[0]

        if t == 13: #ツモ牌を含むか
            p = name.tumohai #鳴き牌
        else:
            p = name.list_tehai[t]

        for i in range(len(name.nakihai)):
            if p == name.nakihai[i]:
                n = i
        
        name.nakimentsu[n].append(p)
        name.nakitype[n] = kflg

        #削除
        if t == 13:
            name.tumohai = 0
        else:
            del name.list_tehai[t]
            name.list_tehai.append(name.tumohai)
            name.tumohai = 0
    
    #各候補を実際の捨て牌/待ち牌に格納
    tflg = 0
    for i in range(len(player.sutekouho)): #捨て候補にあるか確認
        if p == player.sutekouho[i]:
            tflg = 1
    
    if tflg == 1 and (kflg == 3 or kflg == 4):
        player.sute = p
        for i in range(len(player.sutekouho)):
            if player.sutekouho[i] == player.sute:
                cur = i
        player.mati = copy.deepcopy(player.matikouho[cur])    

    #表示更新
    ripai(name)
    tehai_hyouji()
    kawa_hyouji()

    #嶺上ツモへ移動
    rinsyan_tumo(player)
    pass

#tenpai_check
def tenpai_check(name):
    name.mentsu = list() #メンツ候補の初期化
    name.sutekouho = list()
    name.matikouho = list()

    tehai = list()
    tehai = name.list_tehai.copy()
    tehai.extend([name.tumohai])    
    tehai.sort()

    tempatama = list()
    temptehai = list()
    tempsyuntsu = list()
    tempkotsu = list()
    tempuki = list()
    m_cur = 0 #メンツ配列格納時のカーソル
    onaji = 0
    
    #頭候補検索
    for i in range(len(tehai)): 
        for j in range(i+1,len(tehai)):
            if tehai[i] == tehai[j] and tehai[i] != onaji : #同じ組み合わせは入れない
                tempatama.append([tehai[i],tehai[j]]) #頭をtempに追加
                onaji = tehai[i]
                tlist = list()
                for k in range(len(tehai)):
                    if k != i and k != j:
                        tlist.append(tehai[k])
                temptehai.append(tlist) #頭抜きの手牌をtempに追加
    
    #頭あり順子優先検索
    for i in range(len(temptehai)): 
        sr = syu_serch(temptehai[i])
        kr = ko_serch(sr[1])
        tempsyuntsu = sr[0]
        tempkotsu = kr[0]
        tempuki = kr[1]

        name.mentsu.append(person.mentsu()) #構造体配列 列の追加
        name.mentsu[m_cur].atama = tempatama[i].copy()
        name.mentsu[m_cur].syuntsu = copy.deepcopy(tempsyuntsu)
        name.mentsu[m_cur].kotsu = copy.deepcopy(tempkotsu)
        name.mentsu[m_cur].uki = tempuki.copy()
        name.mentsu[m_cur].atamaflg = 1
        m_cur += 1
    
    #頭あり刻子優先検索
    for i in range(len(temptehai)): 
        kr = ko_serch(temptehai[i])
        sr = syu_serch(kr[1])
        tempsyuntsu = sr[0]
        tempkotsu = kr[0]
        tempuki = sr[1]

        name.mentsu.append(person.mentsu()) #構造体配列 列の追加
        name.mentsu[m_cur].atama = tempatama[i].copy()
        name.mentsu[m_cur].syuntsu = copy.deepcopy(tempsyuntsu)
        name.mentsu[m_cur].kotsu = copy.deepcopy(tempkotsu)
        name.mentsu[m_cur].uki = tempuki.copy()
        name.mentsu[m_cur].atamaflg = 1
        m_cur += 1
    
    #頭なし順子優先検索
    sr = syu_serch(tehai)
    kr = ko_serch(sr[1])
    tempsyuntsu = sr[0]
    tempkotsu = kr[0]
    tempuki = kr[1]

    name.mentsu.append(person.mentsu()) #構造体配列 列の追加
    name.mentsu[m_cur].atama = [] #空
    name.mentsu[m_cur].syuntsu = copy.deepcopy(tempsyuntsu)
    name.mentsu[m_cur].kotsu = copy.deepcopy(tempkotsu)
    name.mentsu[m_cur].uki = tempuki.copy()
    name.mentsu[m_cur].atamaflg = 0
    m_cur += 1

    #頭なし刻子優先検索
    kr = ko_serch(tehai)
    sr = syu_serch(kr[1])
    tempsyuntsu = sr[0]
    tempkotsu = kr[0]
    tempuki = sr[1]

    name.mentsu.append(person.mentsu()) #構造体配列 列の追加
    name.mentsu[m_cur].atama = [] #空
    name.mentsu[m_cur].syuntsu = copy.deepcopy(tempsyuntsu)
    name.mentsu[m_cur].kotsu = copy.deepcopy(tempkotsu)
    name.mentsu[m_cur].uki = tempuki.copy()
    name.mentsu[m_cur].atamaflg = 0
    m_cur += 1

    #ノーテンのメンツ候補をおおまかに削除
    for i in range(len(name.mentsu)-1,-1,-1): #逆順
        if name.mentsu[i].atamaflg == 1: 
            if len(name.mentsu[i].uki) >= 4: #頭ありならuki4以上でノーテン
                del name.mentsu[i]
            else:
                pass
        else: 
            if len(name.mentsu[i].uki) >= 3: #頭なしならuki3以上でノーテン
                del name.mentsu[i]
            else:
                pass  
    
    sutelist = list()
    matilist = list()
    
    #待ちをすべて抽出
    for i in range(len(name.mentsu)): #通常パターン
        if len(name.mentsu[i].uki) != 0:
            r = mati_serch(name.mentsu[i].uki,name.mentsu[i].syuntsu,name.mentsu[i].atamaflg)
            sutelist += (r[0])
            matilist += (r[1])
        else: #浮き0パターン
            for j in range(len(name.mentsu[i].syuntsu)): #順子処理
                uki = name.mentsu[i].syuntsu[j] #j番目を浮きとして格納
                exsyuntsu = list()

                for k in range(len(name.mentsu[i].syuntsu)): #j番目以外を順子として格納
                    if j != k: 
                        exsyuntsu.append(name.mentsu[i].syuntsu[k])
                
                r = mati_serch_ukinasi(uki,exsyuntsu,name.mentsu[i].atamaflg)
                sutelist += (r[0])
                matilist += (r[1])

            for j in range(len(name.mentsu[i].kotsu)): #刻子処理
                uki = name.mentsu[i].kotsu[j] #j番目を浮きとして格納
                r = mati_serch_ukinasi(uki,name.mentsu[i].syuntsu,name.mentsu[i].atamaflg)
                sutelist += (r[0])
                matilist += (r[1])

    #特殊役の処理
    #チートイツ    
    if len(name.nakimentsu) == 0: #チートイは鳴きなし
        tir = mati_serch_titoi(tehai)
        if len(tir) == 2: #テンパイ
            sutelist += [tir[0]]
            sutelist += [tir[1]]
            matilist += [[tir[1]]]
            matilist += [[tir[0]]]

    #国士無双
    if len(name.nakimentsu) == 0: #国士は鳴きなし
        kor = mati_serch_kokushi(tehai)
        if kor:
            sutelist += kor[0]
            matilist += kor[1]

    su = list()
    ma = list()

    #重複削除
    for i in range(len(sutelist)): #sute重複削除
        if i == 0:
            sold = copy.deepcopy(sutelist)
            mold = copy.deepcopy(matilist)
            su.append(sold[0])
            ma.append(mold[0])
        else:
            flg = 0
            for j in range(len(su)):
                if sutelist[i] == su[j]:
                    ma[j] += matilist[i]
                    flg = 1

            if flg == 0:
                sold = copy.deepcopy(sutelist)
                mold = copy.deepcopy(matilist)
                su.append(sold[i])
                ma.append(mold[i])
    pass

    for i in range(len(ma)): #mati重複削除
        xset = set(ma[i]) 
        ma[i] = list(xset) 
        ma[i].sort()

    #結果があればクラスに格納して終了
    if len(su) != 0 and len(ma) != 0:
        name.sutekouho = copy.deepcopy(su)
        name.matikouho = copy.deepcopy(ma)

    pass

#syu_serch
def syu_serch(tlist): #順子検索
    hailist = tlist.copy()
    tempr = list()
    flg = 0
    while flg == 0:
        flg = 1
        for i in range(len(hailist)):
            if hailist[i] // 10 == 4: #字牌は除く
                continue
            for j in range(i+1,len(hailist)):
                if hailist[i] + 1 == hailist[j]:
                    for k in range(j+1,len(hailist)):
                        if hailist[j] + 1 == hailist[k]:
                            tempr.append([hailist[i],hailist[j],hailist[k]])
                            del hailist[i]
                            del hailist[j-1]
                            del hailist[k-2]
                            flg = 0
                            break
                    else:
                        continue
                    break
            else:
                continue
            break
    result = tempr
    amari = hailist
    return result,amari #result:二次元配列 amari:一次元配列

#ko_serch
def ko_serch(tlist): #刻子検索
    hailist = tlist.copy()
    tempr = list()
    flg = 0
    while flg == 0:
        flg = 1
        for i in range(len(hailist)):
            for j in range(i+1,len(hailist)):
                if hailist[i] == hailist[j]:
                    for k in range(j+1,len(hailist)):
                        if hailist[j] == hailist[k]:
                            tempr.append([hailist[i],hailist[j],hailist[k]])
                            del hailist[i]
                            del hailist[j-1]
                            del hailist[k-2]
                            flg = 0
                            break
                    else:
                        continue
                    break
            else:
                continue
            break
    result = tempr
    amari = hailist
    return result,amari

#syu_serch_rev
def syu_serch_rev(tlist): #順子検索(逆順)
    hailist = tlist.copy()
    tempr = list()
    flg = 0
    while flg == 0:
        flg = 1
        for i in range(len(hailist)-1,-1,-1):
            if hailist[i] // 10 == 4: #字牌は除く
                continue
            for j in range(i-1,-1,-1):
                if hailist[i] - 1 == hailist[j]:
                    for k in range(j-1,-1,-1):
                        if hailist[j] - 1 == hailist[k]:
                            tempr.append([hailist[k],hailist[j],hailist[i]])
                            del hailist[i]
                            del hailist[j]
                            del hailist[k]
                            flg = 0
                            break
                    else:
                        continue
                    break
            else:
                continue
            break
    result = tempr
    amari = hailist
    return result,amari #result:二次元配列 amari:一次元配列

#mati_serch
def mati_serch(uki,syuntsu,atamaflg): #待ち検索 uki:一次元 syuntsu:二次元
    olist = list()
    gara = list()

    for i in range(len(uki)): #浮き牌の全ての柄を取り出す
        gara.append(uki[i] // 10)

    xset = set(gara) #重複削除した集合
    gara = list(xset) #一意のリスト
    gara.sort()

    for i in range(len(gara)): #柄の数反復
        for j in range(len(syuntsu)): #順子のメンツ数反復
            if gara[i] == syuntsu[j][0] // 10 : #柄が同じ順子を格納
                olist += syuntsu[j]
    
    olist += uki #最後に浮き牌も格納
    olist.sort()

    mati = list() #二次元配列
    sute = list()

    for i in range(len(olist)-1): #グループ分け
        alist = list()
        blist = list()

        alist = olist[0:i+1]
        blist = olist[i+1:]

        r1 = syu_serch(alist)
        r2 = syu_serch(blist)

        amari = r1[1] + r2[1] #amariをマージ
        amari.sort()

        if atamaflg == 1 and len(amari) == 3: #頭あり
            if amari[0] == amari[1]:
                mati.append([amari[0]])
                sute.append(amari[2])
            if amari[1] == amari[2]:
                mati.append([amari[1]])
                sute.append(amari[0])
            if amari[0] + 1 == amari[1] and amari[0]//10 != 4 and amari[0]//10==amari[1]//10: 
                if amari[0]%10 != 1 and amari[1]%10 != 9: #両面
                    mati.append([amari[0]-1,amari[1]+1])
                    sute.append(amari[2])
                elif amari[0]%10 != 1: #辺張
                    mati.append([amari[0]-1])
                    sute.append(amari[2])
                elif amari[1]%10 != 9: #辺張
                    mati.append([amari[1]+1])
                    sute.append(amari[2])
            if amari[1] + 1 == amari[2] and amari[0]//10 != 4 and amari[1]//10==amari[2]//10:
                if amari[1]%10 != 1 and amari[2]%10 != 9: #両面
                    mati.append([amari[1]-1,amari[2]+1])
                    sute.append(amari[0])
                elif amari[1]%10 != 1: #辺張
                    mati.append([amari[1]-1])
                    sute.append(amari[0])
                elif amari[2]%10 != 9: #辺張
                    mati.append([amari[2]+1])
                    sute.append(amari[0])
            if amari[0] + 2 == amari[1] and amari[0]//10 != 4 and amari[0]//10==amari[1]//10: 
                mati.append([amari[0]+1])
                sute.append(amari[2])
            if amari[1] + 2 == amari[2] and amari[1]//10 != 4 and amari[1]//10==amari[2]//10: 
                mati.append([amari[1]+1])
                sute.append(amari[0])
        elif atamaflg == 0 and len(amari) == 2: #頭なし
            mati.append([amari[0]])
            sute.append(amari[1])
            mati.append([amari[1]])
            sute.append(amari[0])
    
    return sute,mati #mati:二次元

#mati_serch_ukinasi
def mati_serch_ukinasi(uki,syuntsu,atamaflg): #待ち検索(浮きなし/あがり形) uki:一次元 syuntsu:二次元
        
    olist = list()
    gara = list()

    for i in range(len(uki)): #浮き牌の全ての柄を取り出す
        gara.append(uki[i] // 10)

    xset = set(gara) #重複削除した集合
    gara = list(xset) #一意のリスト
    gara.sort()

    for i in range(len(gara)): #柄の数反復
        for j in range(len(syuntsu)): #順子のメンツ数反復
            if gara[i] == syuntsu[j][0] // 10 : #柄が同じ順子を格納
                olist += syuntsu[j]
    
    olist += uki #最後に浮き牌も格納
    olist.sort()

    mati = list() #二次元配列
    sute = list()

    for i in range(len(olist)-1): #グループ分け
        for time in range(3): #3通り反復(順順/順逆/逆逆)
            alist = list()
            blist = list()

            alist = olist[0:i+1]
            blist = olist[i+1:]

            if time == 0:
                r1 = syu_serch(alist)
                r2 = syu_serch(blist)
            elif time == 1:
                r1 = syu_serch(alist)
                r2 = syu_serch_rev(blist)
            elif time == 2:
                r1 = syu_serch_rev(alist)
                r2 = syu_serch_rev(blist)

            amari = r1[1] + r2[1] #amariをマージ
            amari.sort()

            if atamaflg == 1 and len(amari) == 3: #頭あり
                if amari[0] == amari[1]:
                    mati.append([amari[0]])
                    sute.append(amari[2])
                if amari[1] == amari[2]:
                    mati.append([amari[1]])
                    sute.append(amari[0])
                if amari[0] + 1 == amari[1] and amari[0]//10 != 4 and amari[0]//10==amari[1]//10:
                    if amari[0]%10 != 1 and amari[1]%10 != 9: #両面
                        mati.append([amari[0]-1,amari[1]+1])
                        sute.append(amari[2])
                    elif amari[0]%10 != 1: #辺張
                        mati.append([amari[0]-1])
                        sute.append(amari[2])
                    elif amari[1]%10 != 9: #辺張
                        mati.append([amari[1]+1])
                        sute.append(amari[2])
                if amari[1] + 1 == amari[2] and amari[0]//10 != 4 and amari[1]//10==amari[2]//10:
                    if amari[1]%10 != 1 and amari[2]%10 != 9: #両面
                        mati.append([amari[1]-1,amari[2]+1])
                        sute.append(amari[0])
                    elif amari[1]%10 != 1: #辺張
                        mati.append([amari[1]-1])
                        sute.append(amari[0])
                    elif amari[2]%10 != 9: #辺張
                        mati.append([amari[2]+1])
                        sute.append(amari[0])
                if amari[0] + 2 == amari[1] and amari[0]//10 != 4 and amari[0]//10==amari[1]//10: #間張
                    mati.append([amari[0]+1])
                    sute.append(amari[2])
                if amari[1] + 2 == amari[2] and amari[1]//10 != 4 and amari[1]//10==amari[2]//10: #間張
                    mati.append([amari[1]+1])
                    sute.append(amari[0])
                if amari[0] + 2 == amari[2] and amari[0]//10 != 4 and amari[0]//10==amari[2]//10: #間張
                    mati.append([amari[0]+1])
                    sute.append(amari[1])
            elif atamaflg == 0 and len(amari) == 2: #頭なし
                mati.append([amari[0]])
                sute.append(amari[1])
                mati.append([amari[1]])
                sute.append(amari[0])
    
    return sute,mati #mati:二次元

#mati_serch_titoi
def mati_serch_titoi(titehai):

    templ = list()
    templ = copy.deepcopy(titehai)

    flg = 0
    while flg == 0:
        flg = 1
        for i in range(len(templ)-1):
            if templ[i] == templ[i+1]:
                del templ[i+1]
                del templ[i]
                flg = 0
                break
    return templ

#mati_serch_kokushi
def mati_serch_kokushi(kotehai):
    templ = list()
    templ = copy.deepcopy(kotehai)
    yaol = list() #ヤオチュウ牌
    yaol = [11,19,21,29,31,39,41,42,43,44,45,46,47]
    sute = list()
    mati = list()

    for i in range(len(templ)-1,-1,-1):
        for j in range(len(yaol)-1,-1,-1):
            if templ[i] == yaol[j]:
                del templ[i]
                del yaol[j]
                break
    
    if len(templ) == 2 and len(yaol) == 1: #テンパイ
        for i in range(len(templ)):
            if (templ[i]==11 or templ[i]==19 or templ[i]==21 or templ[i]==29 or
                templ[i]==31 or templ[i]==39 or templ[i]//10 == 4):
                if i == 0:
                    sute.append(templ[1])
                    mati.append([yaol[0]])
                elif i == 1:
                    sute.append(templ[0])
                    mati.append([yaol[0]])
    elif len(yaol) == 0 and len(templ) ==1: #13面待ち
        sute.append(templ[0])
        mati.append([11,19,21,29,31,39,41,42,43,44,45,46,47])

        if (templ[0]==11 or templ[0]==19 or templ[0]==21 or templ[0]==29 or
            templ[0]==31 or templ[0]==39 or templ[0]//10 == 4): #あがり形
            sute += [11,19,21,29,31,39,41,42,43,44,45,46,47]
            mati += [[11],[19],[21],[29],[31],[39],[41],[42],[43],[44],[45],[46],[47]]
    
    return sute,mati

#tenpai_check_syokai
def tenpai_check_syokai(name): #初回のみ配牌時点でのテンパイ確認

    #ツモを99とし、その99を切ったものとして待ちを抽出する
    name.tumohai = 99
    tenpai_check(player)
    name.tumohai = 0

    #各候補を実際の捨て牌/待ち牌に格納
    tflg = 0
    for i in range(len(player.sutekouho)): #捨て候補にあるか確認
        if 99 == player.sutekouho[i]:
            tflg = 1
    
    if tflg == 1:
        player.sute = 99
        for i in range(len(player.sutekouho)):
            if player.sutekouho[i] == player.sute:
                cur = i
        player.mati = copy.deepcopy(player.matikouho[cur])

#対局の一連の処理
def taikyoku():
    global yama_cur
    global oya
    yama_cur = 0

    sipai()
    mazeru()
    oyakime()

    haipai(player)
    haipai(com1)
    haipai(com2)
    haipai(com3)

    #テスト用　任意の牌を事前に格納
    #player.list_tehai = list()
    #player.list_tehai = [15,16,17,19,19,19,27,27,27,28,41,41,41]

    #global list_yama
    #list_yama = list()
    #for i in range(137):
    #    list_yama.append(26)

    ripai(player)
    ripai(com1)
    ripai(com2)
    ripai(com3)

    tenpai_check_syokai(player)

    tehai_hyouji()
    kawa_hyouji()
    dora_hyouji()

    #親からツモ
    turnp(oya_who())
    
if __name__ == "__main__":
    main()

# ウィンドウのループ処理
window.mainloop()