
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def proverit_dlitelnost(dlitelnost_str):
    try:
        dlitelnost = float(dlitelnost_str)
        if dlitelnost > 0:
            return True, dlitelnost
        else:
            messagebox.showerror("Ошибка", "Длительность должна быть больше 0")
            return False, 0
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число в поле 'Длительность'")
        return False, 0

def proverit_datu(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2024-12-25)")
        return False

def sohranit_v_json(trenirovki):
    try:
        with open("trainings.json", "w", encoding="utf-8") as file:
            json.dump(trenirovki, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
        return False

def zagruzit_iz_json():
    try:
        with open("trainings.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
        return []

def otfiltrovat(trenirovki, tip, data):
    result = trenirovki.copy()

    if tip != "Все":
        result = [t for t in result if t["type"] == tip]
    
    if data:
        result = [t for t in result if t["date"] == data]
    
    return result

def obnovit_tablicu(tree, trenirovki):
    """Обновление таблицы"""
    for item in tree.get_children():
        tree.delete(item)
 
    for i, trenirovka in enumerate(trenirovki, start=1):
        tree.insert("", "end", values=(trenirovka["date"], trenirovka["type"], trenirovka["duration"]))

def dobavit_trenirovku():
    data = polya["data"].get()
    tip = polya["tip"].get()
    dlitelnost_str = polya["dlitelnost"].get()

    if not proverit_datu(data):
        return

    dlitelnost_valid, dlitelnost = proverit_dlitelnost(dlitelnost_str)
    if not dlitelnost_valid:
        return

    novaya_trenirovka = {
        "date": data,
        "type": tip,
        "duration": dlitelnost
    }
 
    trenirovki.append(novaya_trenirovka)

    sohranit_v_json(trenirovki)

    obnovit_tablicu(polya["tree"], trenirovki)

    polya["data"].delete(0, tk.END)
    polya["data"].insert(0, datetime.now().strftime("%Y-%m-%d"))
    polya["dlitelnost"].delete(0, tk.END)
    
    messagebox.showinfo("Успех", "Тренировка добавлена!")

def primenit_filtr():
    tip = polya["filter_tip"].get()
    data = polya["filter_data"].get()
    
    if data:
        if not proverit_datu(data):
            return
    
    otfiltrovannye = otfiltrovat(trenirovki, tip, data)
    obnovit_tablicu(polya["tree"], otfiltrovannye)
    
    if len(otfiltrovannye) == 0:
        messagebox.showinfo("Инфо", "Нет тренировок, соответствующих фильтру")

def sbroshit_filtr():
    polya["filter_tip"].set("Все")
    polya["filter_data"].delete(0, tk.END)
    obnovit_tablicu(polya["tree"], trenirovki)

def sozdat_okno():
    global trenirovki, polya

    trenirovki = zagruzit_iz_json()

    root = tk.Tk()
    root.title("Training Planner - План тренировок")
    root.geometry("900x500")
    
    polya = {}
    
    ramka_dobavleniya = tk.LabelFrame(root, text="Добавить тренировку", padx=10, pady=10)
    ramka_dobavleniya.pack(pady=10, padx=10, fill="x")
    
    tk.Label(ramka_dobavleniya, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
    polya["data"] = tk.Entry(ramka_dobavleniya, width=15)
    polya["data"].grid(row=0, column=1, padx=5, pady=5)
    polya["data"].insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    tk.Label(ramka_dobavleniya, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5)
    polya["tip"] = tk.StringVar()
    spisok_tipov = ["Бег", "Плавание", "Велосипед", "Силовая", "Йога", "Растяжка", "Другое"]
    vybor_tipa = ttk.Combobox(ramka_dobavleniya, textvariable=polya["tip"], values=spisok_tipov, width=15)
    vybor_tipa.grid(row=0, column=3, padx=5, pady=5)
    vybor_tipa.set("Бег")
    
    tk.Label(ramka_dobavleniya, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5)
    polya["dlitelnost"] = tk.Entry(ramka_dobavleniya, width=15)
    polya["dlitelnost"].grid(row=0, column=5, padx=5, pady=5)
    
    knopka_dobavit = tk.Button(ramka_dobavleniya, text="Добавить тренировку", command=dobavit_trenirovku, bg="lightgreen")
    knopka_dobavit.grid(row=0, column=6, padx=10, pady=5)
    
    ramka_filtrov = tk.LabelFrame(root, text="Фильтры", padx=10, pady=10)
    ramka_filtrov.pack(pady=10, padx=10, fill="x")
    
    tk.Label(ramka_filtrov, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
    polya["filter_tip"] = tk.StringVar()
    vybor_filter_tipa = ttk.Combobox(ramka_filtrov, textvariable=polya["filter_tip"], 
                                      values=["Все"] + spisok_tipov, width=15)
    vybor_filter_tipa.grid(row=0, column=1, padx=5, pady=5)
    vybor_filter_tipa.set("Все")
    
    tk.Label(ramka_filtrov, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
    polya["filter_data"] = tk.Entry(ramka_filtrov, width=15)
    polya["filter_data"].grid(row=0, column=3, padx=5, pady=5)
    
    knopka_filtr = tk.Button(ramka_filtrov, text="Применить фильтр", command=primenit_filtr)
    knopka_filtr.grid(row=0, column=4, padx=5, pady=5)
    
    knopka_sbros = tk.Button(ramka_filtrov, text="Сбросить фильтр", command=sbroshit_filtr)
    knopka_sbros.grid(row=0, column=5, padx=5, pady=5)
    
    ramka_tablicy = tk.Frame(root)
    ramka_tablicy.pack(fill="both", expand=True, padx=10, pady=10)
    
    polya["tree"] = ttk.Treeview(ramka_tablicy, columns=("Дата", "Тип", "Длительность"), show="headings")
    
    polya["tree"].heading("Дата", text="Дата")
    polya["tree"].heading("Тип", text="Тип тренировки")
    polya["tree"].heading("Длительность", text="Длительность (мин)")
    
    polya["tree"].column("Дата", width=150)
    polya["tree"].column("Тип", width=200)
    polya["tree"].column("Длительность", width=150)
    
    polzunok = ttk.Scrollbar(ramka_tablicy, orient="vertical", command=polya["tree"].yview)
    polya["tree"].configure(yscrollcommand=polzunok.set)
    
    polya["tree"].pack(side="left", fill="both", expand=True)
    polzunok.pack(side="right", fill="y")
    
    obnovit_tablicu(polya["tree"], trenirovki)
    
    return root

if __name__ == "__main__":
    trenirovki = []
    polya = {}
    
    okno = sozdat_okno()
    okno.mainloop()
