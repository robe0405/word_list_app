import tkinter as tk
import tkinter.font as tkFont
import pandas as pd
import sys
import random
import requests
from bs4 import BeautifulSoup

class Application:
    def __init__(self):
        # tkinter(bace)
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("English_word")

        #pandas()
        global df_My,df_toeic
        df_My = pd.read_csv("/Users/tanakaroberuto/desktop/English_word.csv")
        df_toeic = pd.read_csv("/Users/tanakaroberuto/desktop/toeic_word.csv")

        # Font
        self.font_title = tkFont.Font(family="Arial", size=50, weight="bold", slant="italic")
        self.font_word = tkFont.Font(family="Arial", size=50, slant="italic")
        self.font_mean = tkFont.Font(family="Arial", size=20)

        # first_page
        self.label_title = tk.Label(self.window, text="English_word", fg="blue4", font=self.font_title)
        self.label_title.pack(side="top", pady=100)
        self.button_Toeic = tk.Button(self.window, text="toeic_word", height=2, width=12, fg="grey26")
        self.button_Toeic.config(command=lambda : self.second_page())
        self.button_Toeic.place(x=180, y=340)
        self.button_My = tk.Button(self.window, text="My_word", height=2, width=12, fg="grey26")
        self.button_My.config(command=lambda : self.go(0))
        self.button_My.place(x=320, y=340)

        # toeicのデータ(スクレイピング用)
        load_url = "https://toiguru.jp/toeic-vocabulary-list"
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")
        level = soup.find_all("tbody")
        global Eng_1,Eng_2,Eng_3,Eng_4,Eng_5
        Eng_1 = level[0]
        Eng_2 = level[1]
        Eng_3 = level[2]
        Eng_4 = level[3]
        Eng_5 = level[4]

        self.num = 0
        self.button_num = 1

    # second_page
    def second_page(self):
        self.label_title.destroy()
        self.button_My.destroy()
        self.button_Toeic.destroy()

        self.label_se_title = tk.Label(self.window, fg="red", font=self.font_title)
        self.label_se_title.config(text="Level")
        self.label_se_title.pack(side="top", pady=60)

        self.button1 = tk.Button(self.window, fg="grey26", text="level_1", height=3, width=18, command=lambda : self.go(1))
        self.button1.pack(side="top")
        self.button2 = tk.Button(self.window, fg="grey26", text="level_2", height=3, width=18, command=lambda : self.go(2))
        self.button2.pack(side="top")
        self.button3 = tk.Button(self.window, fg="grey26", text="level_3", height=3, width=18, command=lambda : self.go(3))
        self.button3.pack(side="top")
        self.button4 = tk.Button(self.window, fg="grey26", text="level_4", height=3, width=18, command=lambda : self.go(4))
        self.button4.pack(side="top")
        self.button5 = tk.Button(self.window, fg="grey26", text="level_5", height=3, width=18, command=lambda : self.go(5))
        self.button5.pack(side="top")
        self.button_num = self.button_num * -1

    # スクレイピング
    def data(self, eng):
        alf = "abcdefghijklmnopqrstuvwxyz"
        word_list = []
        mean_list = []
        for i in eng.find_all("td"):
            list_alf = []
            list_ja = []
            for l in i.text:
                if l in alf:
                    list_alf.append(l)
                else:
                    list_ja.append(l)
            num = len(list_alf) - 1
            alf_changed = "".join(list_alf)
            ja_changed = "".join(list_ja)
            word_list.append(alf_changed)
            mean_list.append(ja_changed)
        df = pd.DataFrame({"英単語":word_list, "意味":mean_list}).set_index("英単語")
        df.to_csv("/Users/tanakaroberuto/Desktop/toeic_word.csv")

    # pandas
    def pandas(self, df):
        # データの読み込み
        global eng_word
        eng_word = df.iloc[:, 0]
        eng_mean = df.iloc[:, 1]
        # データを辞書型にしシャッフル
        self.dict = dict(zip(eng_word, eng_mean))
        self.keys = list(self.dict.keys())
        random.shuffle(self.keys)

    # 英単語とボタンを表示
    def word_page(self, key):
        self.label_word = tk.Label(self.window, fg="grey26", font=self.font_word)
        self.label_word.config(text=key)
        self.label_word.pack(side="top", pady=60)
        self.button_mean(key)
        self.button_word()

    # Nextボタン
    def button_word(self):
        self.buttonword = tk.Button(self.window, text="Next")
        self.buttonword.config(height=2, width=17)
        self.buttonword.config(command=lambda : self.back())
        self.buttonword.place(x=220, y=340)

    # meanボタン
    def button_mean(self, key):
        self.buttonmean = tk.Button(self.window, text="mean", fg="red")
        self.buttonmean.config(height=2, width=17)
        self.buttonmean.config(command=lambda : self.mean_page(key))
        self.buttonmean.place(x=220, y=300)

    # 英単語・意味・Nextボタンを表示
    def mean_page(self, key):
        self.buttonmean.destroy()
        # label_mean
        self.label_mean = tk.Label(self.window, fg="grey38", font=self.font_mean)
        self.label_mean.config(text=self.dict[key])
        self.label_mean.pack(side="top")

        self.button_num = self.button_num * -1

    def go(self, request):
        if self.button_num == -1:
            self.label_se_title.destroy()
            self.button1.destroy()
            self.button2.destroy()
            self.button3.destroy()
            self.button4.destroy()
            self.button5.destroy()
            self.button_num = self.button_num * -1
            if request == 1:
                self.data(Eng_1)
                self.pandas(df_toeic)
            elif request == 2:
                self.data(Eng_2)
                self.pandas(df_toeic)
            elif request == 2:
                self.data(Eng_3)
                self.pandas(df_toeic)
            elif request == 2:
                self.data(Eng_4)
                self.pandas(df_toeic)
            else:
                self.data(Eng_5)
                self.pandas(df_toeic)
            self.main()
        else:
            self.pandas(df_My)
            self.main()

    def back(self):
        self.label_word.destroy()
        self.buttonword.destroy()
        self.buttonmean.destroy()
        if self.button_num == -1:
            self.label_mean.destroy()
            self.button_num = self.button_num * -1
        self.num += 1
        self.main()

    def main(self):
        self.label_title.destroy()
        self.button_Toeic.destroy()
        self.button_My.destroy()

        for num, key in zip(range(len(eng_word)), self.keys):
            if self.num == num:
                self.word_page(key)
        if len(eng_word) == self.num:
            sys.exit()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
