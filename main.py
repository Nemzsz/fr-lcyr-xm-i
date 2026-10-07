from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import psycopg
import requests

conn = psycopg.connect(
    host = "localhost",
    dbname  = 'Music',
    password = "972279",
    user = "postgres"
)
cursor = conn.cursor()

#with opwn("Заказчики.json", "r", encoding = "utf-8") as f:
   # data = json.load(f)

#for row in data["records"]:
   # cursor.execute("INSERT INTO customers (id, name, inn, addres, phone, type) VALUES (%s, %s, %s, %s, %s, %s)", row["id"]
    #, row["name"], row["inn"], row["addres"], row["phone"], row["type"])
#conn.commit()


window = Tk()
window.title('Главная страница')
window.geometry('1250x1250')


def AddBandsWindow():
    global NameBand, Genre
    AddWindow = Toplevel()
    AddWindow.title('Добавить группу')
    AddWindow.geometry('1250x1250')

    # Для группы
    NameBand = Entry(AddWindow, width=50)
    NameBand.place(x=250, y=250)
    AddNameBand = Label(AddWindow, text="Введите название группы")
    AddNameBand.place(x=250, y=220)

    # Для жанра
    Genre = Entry(AddWindow, width=50)
    Genre.place(x=250, y=450)
    AddGenre = Label(AddWindow, text="Введите жанр группы")
    AddGenre.place(x=250, y=420)

    # Кнопка
    AddInfoBand = Button(AddWindow, text='Добавить', command=Check)
    AddInfoBand.place(x=250, y=550)


def Check():
  CheckNameBand = NameBand.get()
  CheckGenre = Genre.get()
  if CheckNameBand == "" or CheckGenre == "":
      messagebox.showerror("пупупу","не все поля заполнены")
      return
  cursor.execute("SELECT id_band FROM Bands WHERE name_band = %s", (CheckNameBand,))
  exists_band = cursor.fetchone()
  if exists_band is not None:
      id_band = exists_band[0]
  else:
      cursor.execute("INSERT INTO Bands (name_band) VALUES (%s) RETURNING id_band", (CheckNameBand,))
      id_band = cursor.fetchone()[0]
#для жанра
  cursor.execute("SELECT id_genre FROM Genre WHERE genre_name = %s", (CheckGenre,))
  exists_genre = cursor.fetchone()
  if exists_genre is not None:
      id_genre = exists_genre[0]
  else:
      cursor.execute("INSERT INTO Genre (genre_name) VALUES (%s) RETURNING id_genre", (CheckGenre,))
      id_genre = cursor.fetchone()[0]
  cursor.execute("INSERT INTO GenreBands (id_band, id_genre) VALUES (%s, %s)", (id_band, id_genre))
  conn.commit()
  messagebox.showinfo("Супер","Все получилось")




def LearnBand():
    LearnWindow = Toplevel()
    LearnWindow.title("Узнать о группе")
    LearnWindow.geometry("1250x1250")

    # Combobox
    band_combobox = ttk.Combobox(LearnWindow, width=50)
    band_combobox.place(x=250, y=100)

    # Кнопка «Показать»
    show_button = Button(LearnWindow,
                         text='Показать',
                         command=lambda: ShowBandInfo(band_combobox, LearnWindow))
    show_button.place(x=250, y=150)

    # Загрузка групп из API
    response = requests.get("http://127.0.0.1:8000/bands")
    bands = response.json()
    band_combobox["values"] = [band["name_band"] for band in bands]
    band_combobox.band_dict = {band["name_band"]: band["id_band"] for band in bands}


def ShowBandInfo(combobox, window):
    selected_name = combobox.get()
    if selected_name == "":
        messagebox.showerror("Ошибка", "Выбери группу")
        return

    id_band = combobox.band_dict[selected_name]
    response = requests.get(f"http://127.0.0.1:8000/bands/{id_band}")
    data = response.json()
    Label(window, text=f"ID: {data['id_band']}\nНазвание: {data['name_band']}").place(x=250, y=250)

GlavText = Label(window, text='Добро пожаловать на страницу. Выберите, что вы хотите сделать:', font=("Arial", 14))
GlavText.place(x=300, y=100)

Add = Button(window, text='Добавить группу', command=AddBandsWindow)
Add.place(x=300, y=200)

learn = Button(window, text='Узнать о группе', command=LearnBand)
learn.place(x=600, y=200)

window.mainloop()