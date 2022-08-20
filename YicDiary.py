import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors


WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']

# コンボボックスで利用するactionsの要素をkindsテーブルから取得する
host = '127.0.0.1'
user = 'root'
password = ''
db = 'apr01'
charset = 'utf8mb4'
connection = pymysql.connect(host=host,
                    user=user,
                    password=password,
                    db=db,
                    charset=charset,
                    cursorclass=pymysql.cursors.DictCursor)

connection.begin()
with connection.cursor() as cursor:

 sql = "select kind_name from kinds"
 cursor.execute(sql)
 result = cursor.fetchall()
 actions = []
 
 for i in range(len(result)):
    actions.append(result[i]["kind_name"])      #('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

connection.commit()
connection.close()


class Password:
  def __init__(self, master):
     master.title('ログイン画面')
     master.geometry('600x280')
     master.resizable(0, 0)
     master.grid_columnconfigure((0,2), weight=2)
     self.master = master
     self.widgets = []    #ウィジットを管理する
     self.create_widgets()

  #ログイン画面を表示
  #ウィジットを作成する
  def create_widgets(self):
     self.widget_destroy()

     #----------------------------------------------------------------------------------------------------
     # 苗字ラベル作成
     self.family_name = ttk.Label(self.master, text = "苗字", font = ("", 10))
     self.family_name.grid(row = 0, column = 0)
     self.widgets.append(self.family_name)
     self.family_name_entry = tk.Entry(self.master)
     self.family_name_entry.grid(row = 0, column = 1)
     self.widgets.append(self.family_name_entry)

     #-----------------------------------------------------------------------------------------------------
     # 名前ラベル作成
     self.first_name = tk.Label(self.master, text = "名前", font = ("", 10))
     self.first_name.grid(row = 1, column = 0)
     self.widgets.append(self.first_name)
     self.first_name_entry = tk.Entry(self.master)
     self.first_name_entry.grid(row = 1, column = 1)
     self.widgets.append(self.first_name_entry)

     #------------------------------------------------------------------------------------------------------
     # パスワードラベル作成
     self.password_label = tk.Label(self.master, text = "パスワード", font =("", 10))
     self.password_label.grid(row = 2, column = 0)
     self.widgets.append(self.password_label)
     self.pass_entry = tk.Entry(self.master, show = "*")
     self.pass_entry.grid(row = 2, column = 1)
     self.widgets.append(self.pass_entry)

     self.login_Button = tk.Button(self.master, text = "ログイン", command = self.Login)
     self.login_Button.grid(row = 3, column = 0, columnspan = 3)
     self.widgets.append(self.login_Button)

     self.register_Button = tk.Button(self.master, text = "登録画面へ", command = self.Register_pass)
     self.register_Button.grid(row = 4, column = 0, columnspan = 4)
     self.widgets.append(self.register_Button)

     self.master.grid_anchor(tk.CENTER)


  #----------------------------------------------------------------------------------------------------------
  # ログインボタン機能
  def Login(self):
     get_family_name = self.family_name_entry.get()
     get_first_name = self.first_name_entry.get()
     get_password = self.pass_entry.get()

    # データベースに予定の問い合わせを行う
    # データベースに接続
     host = '127.0.0.1'
     user = 'root'
     password = ''
     db = 'apr01'
     charset = 'utf8mb4'
     connection = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db,
                           charset=charset,
                           cursorclass=pymysql.cursors.DictCursor)
     try:
          connection.begin()
          with connection.cursor() as cursor:
             
             # パスワード, 苗字, 名前をmenberテーブルから抽出する
             sql1 = "select family_name, first_name, pass_word from menber"
             cursor.execute(sql1)
             results1 = cursor.fetchall()

             sql2 = "select menberID from menber"
             cursor.execute(sql2)
             results2 = cursor.fetchall()

             # 各entryに入力された文字が空白かを判定する
             if len(get_family_name) == 0:
               self.fail_pass()
      
             elif len(get_first_name) == 0:
               self.fail_pass()

             elif len(get_password) == 0:
                self.fail_pass()

             # 登録されているものと一致するかを確認
             for i in range(len(results1)):
                if results1[i]["family_name"] == get_family_name:
                   if results1[i]["first_name"] == get_first_name:
                       if results1[i]["pass_word"] == get_password:
                          next_menberID =  results2[i]["menberID"]
                          self.widget_destroy()

                          YicDiary(self.master, next_menberID, get_family_name, get_first_name)
                          self.master.mainloop()

            # 入力されてた情報が登録されていない場合
             self.fail_pass()

     except Exception as e:
          print('error:', e)
          connection.rollback()
    
     connection.close()

  #-------------------------------------------------------------------------------------------
  #ウィジットの破棄
  def widget_destroy(self):
    for widget in self.widgets:
        widget.destroy()

  #-------------------------------------------------------------------------------------------
  # ログインが失敗したとき
  def fail_pass(self):
      
      self.widget_destroy()

      self.fail_label = tk.Label(self.master, text = "ログインに失敗しました", font = ("", 30))
      self.fail_label.grid(row = 1, column = 0)
      self.widgets.append(self.fail_label)
      self.back_Button = tk.Button(self.master, text = "戻る", command = self.create_widgets)
      self.back_Button.grid(row = 2, column = 0, columnspan = 3)
      self.widgets.append(self.back_Button)
      

  #---------------------------------------------------------------------------------------------
  # 登録画面を表示する
  def Register_pass(self):
      self.widget_destroy()
      
      self.fail_label = tk.Label(self.master, text = "苗字 名前 パスワードを入力してください", font = ("", 20))
      self.fail_label.grid(row = 0, column = 1)
      self.widgets.append(self.fail_label)
     
      self.family_name = tk.Label(self.master, text = "苗字", font = ("", 10))
      self.family_name.grid(row = 1, column = 0)
      self.widgets.append(self.family_name)

      self.family_name_entry = tk.Entry(self.master)
      self.family_name_entry.grid(row = 1, column = 1)
      self.widgets.append(self.family_name_entry)

      self.first_name = tk.Label(self.master, text = "名前", font = ("", 10))
      self.first_name.grid(row = 2, column = 0)
      self.widgets.append(self.first_name)

      self.first_name_entry = tk.Entry(self.master)
      self.first_name_entry.grid(row = 2, column = 1)
      self.widgets.append(self.first_name_entry)

      self.password_label = tk.Label(self.master, text = "パスワード", font =("", 10))
      self.password_label.grid(row = 3, column = 0)
      self.widgets.append(self.password_label)

      self.pass_entry = tk.Entry(self.master, show = "*")
      self.pass_entry.grid(row = 3, column = 1)
      self.widgets.append(self.pass_entry)

      self.register_Button = tk.Button(self.master, text = "登録", command = self.Register)
      self.register_Button.grid(row = 4, column = 0, columnspan = 4)
      self.widgets.append(self.register_Button)

      self.back_Button = tk.Button(self.master, text = "戻る", command = self.create_widgets)
      self.back_Button.grid(row = 5, column = 0, columnspan = 5)
      self.widgets.append(self.back_Button)

  #------------------------------------------------------------------------------------------------     
  # 登録ボタン機能
  def Register(self):

      # 名前、苗字、パスワードを取得
      get_family_name = self.family_name_entry.get()
      get_first_name = self.first_name_entry.get() 
      get_password = self.pass_entry.get()
      

      # ウィジットの破棄
      self.widget_destroy()

      #ラベル作成      
      self.success_label = tk.Label(self.master, text = "登録が完了しました", font = ("", 20))
      self.success_label.grid(row = 0, column = 1)
      self.widgets.append(self.success_label)

      self.back_Button = tk.Button(self.master, text = "戻る", command = self.create_widgets)
      self.back_Button.grid(row = 1, column = 1, columnspan = 1)
      self.widgets.append(self.back_Button)


      print(get_family_name)
      print(get_first_name)
      print(get_password)

      # 各entryに入力された文字が空白かを判定する
      if len(get_family_name) == 0:
        self.Register_fail()
        return 
      
      elif len(get_first_name) == 0:
        self.Register_fail()
        return

      elif len(get_password) == 0:
        self.Register_fail()
        return

    
      host = '127.0.0.1'
      user = 'root'
      password = ''
      db = 'apr01'
      charset = 'utf8mb4'
      connection = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db,
                           charset=charset,
                           cursorclass=pymysql.cursors.DictCursor)
      try:
          connection.begin()
          with connection.cursor() as cursor:
               # 登録する苗字、名前、パスワードをmenberテーブルにinsertする
               sql = "insert into menber(family_name, first_name, pass_word) values('{}', '{}', '{}')".format(get_family_name, get_first_name, get_password)
               # 実行
               cursor.execute(sql)
            
          connection.commit()

      except Exception as e:
           print('error:', e)
           connection.rollback()

      finally:
           connection.close()
#--------------------------------------------------------------------------------------------------------
#　登録に失敗したとき
  def Register_fail(self):
      
      self.widget_destroy()

      #ラベル作成      
      self.success_label = tk.Label(self.master, text = "登録に失敗しました", font = ("", 20))
      self.success_label.grid(row = 0, column = 1)
      self.widgets.append(self.success_label)

      self.back_Button = tk.Button(self.master, text = "戻る", command = self.Register_pass)
      self.back_Button.grid(row = 1, column = 1, columnspan = 1)
      self.widgets.append(self.back_Button)

#-------------------------------------------------------------------------------------------------------------------------

class YicDiary:
  def __init__(self, master, next_menberID, get_family_name, get_first_name):
    
    master.title("予定管理アプリ   " + get_family_name + get_first_name + "でログイン中")
    
    self.sub_win = None
    

    self.menberID = next_menberID

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(master)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    self.rightFrame = tk.Frame(master)
    self.rightFrame.grid(row=0, column=1)
    self.rightBuild(self.rightFrame)

  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)
    
  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)
 
    self.schedules()
    
  
  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedules(self): 
     #ウィジットを廃棄
     for widget2 in self.r2_frame.winfo_children():
         widget2.destroy()
     
     

  # データベースに予定の問い合わせを行う
  # データベースに接続
     host = '127.0.0.1'
     user = 'root'
     password = ''
     db = 'apr01'
     charset = 'utf8mb4'
     connection = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db,
                           charset=charset,
                           cursorclass=pymysql.cursors.DictCursor)

     try:
         connection.begin()
         with connection.cursor() as cursor:

            # schedules表とcalender表をscheduleIDで内部結合する
            # 日付が同じ間
             sql1 = "select menberID from menber"
             cursor.execute(sql1)
             results1 = cursor.fetchall()
             print(len(results1))
             
             for i in range(len(results1)):

              n_menberID = results1[i]["menberID"]
              #print(n_menberID)
                 
              sql1 = "select family_name from menber where menberID = {}".format(n_menberID)
                 
              cursor.execute(sql1)
              family_names = cursor.fetchone()
              #print(family_names)
              self.family_name = family_names["family_name"]
                  
              sql2 = "select first_name from menber where menberID = {}".format(n_menberID)
                  
              cursor.execute(sql2)
              first_names = cursor.fetchone()
              #print(first_names)
              self.first_name = first_names["first_name"]
              #self.combobox()
              
              sql3 = "select kindID from schedules inner join calender on schedules.scheduleID = calender.scheduleID where days = '{}-{}-{}' and menberID = {}".format(self.year, self.mon, self.today, n_menberID)
              cursor.execute(sql3)
              print(f"\n{sql3}\n")
              KINDs = cursor.fetchone()
              print(KINDs, 'a')
              if KINDs != None:
                kindIDs = KINDs["kindID"]
                print(kindIDs, 's')
            
                sql4 = "select Kind_name from kinds where kindID = {}".format(kindIDs)
                cursor.execute(sql4)
                result = cursor.fetchone()
                kind_names = result['Kind_name']
              
              
                sql5 = "select schedules.schedule_name from schedules inner join calender on schedules.scheduleID = calender.scheduleID where days = '{}-{}-{}' and menberID = {}".format(self.year, self.mon, self.today, n_menberID)
                cursor.execute(sql5)
                results2 = cursor.fetchall()
              
                print(results2)
                frame = tk.Frame(self.r2_frame)
                frame.grid(row = i, column = 0)
                for j, row in enumerate(results2):
                      schedule_names = row["schedule_name"]
                      x = len(schedule_names)
                      if x > 10:
                        for i in range(0, x, 10):
                          schedule_names = schedule_names[:10 + i] + "\n" + schedule_names[10 + i:]
                      textlist = ("{}{} (予定){} (内容){}\n".format(self.family_name, self.first_name, kind_names, schedule_names))
                      label = tk.Label(frame, text = textlist, font = ("",10))
                      label.grid(row=j, column=0)
                      
     #except Exception as e:
         #print('error:', e)
         #connection.rollback()

     finally:
         connection.close()

  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(days)

    # 種別
    kind_name = self.combo.get()
    print(kind_name)

    # 別表にしている人は、外部キーとして呼び出す値を得る
    # getKey() メソッド (または関数)は自作すること
    def getKey(kind_name):
        if kind_name == '学校':
            return 1

        elif kind_name == '試験':
            return 2
      
        elif kind_name == '課題':
            return 3

        elif kind_name == '行事':
            return 4

        elif kind_name == '就活':
            return 5

        elif kind_name == 'アルバイト':
            return 6

        elif kind_name == '旅行':
            return 7

    kindID = getKey(kind_name)

    # 予定
    schedule_name = self.text.get("1.0", "end") # 文字を最初から最後まで取得するという意味
    print(schedule_name)

    # データベースに接続する
    host = '127.0.0.1'
    user = 'root'
    password = ''
    db = 'apr01'
    charset = 'utf8mb4'
    connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset=charset,
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        # トランザクション開始
        connection.begin()
        with connection.cursor() as cursor:

            # sqlの作成・定義
            # 参照される側のデータを挿入
            sql = "insert into schedules(kindID, schedule_name, menberID) values({}, '{}', {})".format(kindID, schedule_name, self.menberID)
            # デバック
            #print(sql)

            # sqlの実行
            cursor.execute(sql)

            #上の操作で挿入されたデータの主キーの値を取得
            sql = "select max(scheduleID) from schedules"


            # sqlの実行
            cursor.execute(sql)
            results = cursor.fetchone() # 更新

            next_scheduleID = results["max(scheduleID)"]

            sql = "insert into calender(days, scheduleID) values('{}', {})".format(days, next_scheduleID)
            cursor.execute(sql)
            
            
            
        connection.commit()

    except Exception as e:
         print('error:', e)
         connection.rollback()

    finally:
         connection.close()
    # この行に制御が移った時点で、DBとの接続は切れている

    self.sub_win.destroy()

  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day

    self.schedules()
    

def Main():
  master = tk.Tk()
  Password(master)
  master.mainloop()

if __name__ == '__main__':
  Main()
