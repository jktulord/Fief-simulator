import random
exit = 0
word = ""
state = "MENU"
namelist = ["John", "Max", "Макс", "Макс_Хас", "Акакаий", "Добрыня", "Яков", "Нурберг", "Паша", "Пася", "Саша", "Сася",
            "Johnathan", "Johnson", "Joe", "Jerry", "Jackson", "Jefferson", "Jacob", "Jack", "Jokey"]
womannamelist = ["Агния","Анка","Бана","Вера","Горислава","Доля","Еля","Желана","Зара","Доля"]

plebs = []
brides = []

def clear(n):
    for i in range(n):
        print(" ")


class player(object):
    """docstring"""

    def __init__(self):
        """Constructor"""
        self.name = "nothing"
        self.money = 100
        self.house = "Big house"
        self.day = 1
        self.week = 0
        self.wheet = 20
        self.wood = 0
        self.milk = 0
        self.mushrooms = 0
        self.incomingWheet = 0
        self.incomingWood = 0
        self.incomingMilk = 0
        self.incomingMushrooms = 0

    def spending(self):
        if self.wheet > 0:
            self.wheet -= 1
        elif self.mushrooms > 0:
            self.mushrooms -= 1
        elif self.milk > 0:
            self.milk -= 1

    def dayEnding(self):
        self.day += 1
        if self.day == 8:
            self.day = 1
            self.week += 1
            self.wheet += self.incomingWheet
            self.wood += self.incomingWood
            self.milk += self.incomingMilk
            self.mushrooms += self.incomingMushrooms
            self.incomingWheet = 0
            self.incomingWood = 0
            self.incomingMilk = 0
            self.incomingMushrooms = 0

    def rounding(self):
        self.wheet = round(self.wheet, 1)
        self.wood = round(self.wood, 1)
        self.milk = round(self.milk, 1)
        self.mushrooms = round(self.mushrooms, 1)
        self.incomingWheet = round(self.incomingWheet, 1)
        self.incomingWood = round(self.incomingWood, 1)
        self.incomingMilk = round(self.incomingMilk, 1)
        self.incomingMushrooms = round(self.incomingMushrooms, 1)


pl = player()

class woman(object):
    def __init__(self,type ="none"):
        self.name = womannamelist[random.randint(0, len(womannamelist) - 1)]
        self.age = random.randint(14, 20)
        if type == "child":
            self.age = 1

    def deathcheck(self):
        Dead = False
        if random.randint(0,100)+1 <= self.age-40:
            Dead = True
        return Dead

class pleb(object):
    """docstring"""

    def __init__(self, money, type):
        """Constructor"""
        self.name = namelist[random.randint(0, len(namelist) - 1)]
        self.money = money
        self.age = random.randint(18,28)
        self.wife = "none"
        self.childs = []
        self.job = "none"
        self.house = "none"
        self.cow = 0
        if type == "HasCow":
            self.cow = 1
        if type == "HasHouse":
            self.house = "shed"
            self.wife = woman()
        if type == "Child":
            self.age = 1
        self.wheet = 5
        self.wood = 0
        self.milk = 0
        self.mushrooms = 0
        self.efficiency = 0
        self.theGoal = "none"

    def deciding(self):  # Выбор цели
        food = self.wheet + self.milk + self.mushrooms
        # Решение делать еду
        if food < 7:
            self.theGoal = "food"
        elif self.house == "none":
            self.theGoal = "shed"
        # elif self.cow == 0:
        #    self.theGoal = "cow"
        else:
            self.theGoal = "food"

    def jobbing(self):  # Выбор работы на основе цели
        if self.theGoal == "food":
            self.job = "gathering"
        elif self.theGoal == "shed":
            if self.wood > 10:
                self.job = "shed"
            else:
                self.job = "wood"


    def working(self):  # Работы
        if self.job == "gathering":
            self.mushrooms += 2 * 0.8
            pl.incomingMushrooms += 2 * 0.2
        elif self.job == "wood":
            self.wood += 1 * 0.8
            pl.incomingWood += 1 * 0.2
        elif self.job == "shed":
            self.wood -= 10
            self.house = "shed"


    def spending(self):  # Расходы и доходы у крестьян
        self.wheet -= 1 * self.cow
        self.milk += 1 * self.cow
        if self.cow > 0:
            if self.mushrooms > 0:
                self.mushrooms -= 1
            elif self.wheet > 0:
                self.wheet -= 1
            elif self.milk > 0:
                self.milk -= 1
        else:
            if self.wheet > 0:
                self.wheet -= 1
            elif self.mushrooms > 0:
                self.mushrooms -= 1
            elif self.milk > 0:
                self.milk -= 1

    def familycheck(self):
        if self.wife != "none":
            if random.randint(0, 100) + 1 >= 2:
                if random.randint(0, 100) + 1 >= 50:
                    self.childs.append(pleb(0, "Child"))
                else:
                    self.childs.append(woman())

    def yearlyfamilycheck(self):
        self.age -= 1
        self.deathcheck()
        if self.wife != "none":
            self.wife.age += 1
            if self.wife.deathcheck():
                self.wife = "none"
        for ch in self.childs:
            ch.age += 1
            if ch.age >= 14:
                if ch is woman:
                    plebs.append(ch)
                if ch is pleb:
                    plebs.append(ch)
                self.childs.remove(ch)

    def deathcheck(self):
        Dead = False
        if random.randint(0,100)+1 <= self.age-40:
            Dead = True
        return Dead


    def rounding(self):
        self.wheet = round(self.wheet, 1)
        self.wood = round(self.wood, 1)
        self.milk = round(self.milk, 1)
        self.mushrooms = round(self.mushrooms, 1)


class trader(object):
    def __init__(self):
        money = 30
        self.maxcargo = 10
        self.wheet = 0
        self.wood = 0
        self.milk = 0
        self.mushrooms = 0
        self.cow = 5
        self.wheetCost = 1
        self.woodCost = 2
        self.milkCost = 2
        self.mushroomsCost = 1.5
        self.cowCost = 10

    def generateGoods(self):
        number = []
        freecargo = self.maxcargo
        for i in range(4):
            num = random.randint(1, self.maxcargo * 0.5) % freecargo
            print(freecargo)
            number.append(num)
            print(num)
            freecargo -= num
        self.wheet += number[0]
        self.wood += number[1]
        self.milk += number[2]
        self.mushrooms += number[3]

    def buying(self,buyer,goods,amount):
        if goods == "cow":
            if buyer.money - self.cowCost * amount >= 0 and self.cow - amount >= 0 :
                buyer.money -= self.cowCost * amount
                self.money += self.cowCost * amount
                bueyr.cow += amount
                self.cow -= amount



tr = trader()

while exit == 0:

    if state == "MENU":  # стейт меню
        print("-v0.0.5")
        print("Симулятор Дворянина")
        print("1 - начать игру")
        print("2 - выйти")

    elif state == "MAIN":
        print("День:", pl.day, "Week:", pl.week)
        print("Состояние деревушки")
        print("Ваши деньги -", pl.money)
        print("Количество семей -", len(plebs))
        print("Количество Домов -", pl.house)
        print("1 - Посмотреть лист жителей")
        print("2 - Журнал продаж")
        print("3 - Осмотр хозяйства")
        print("4 - Встретить торговца")
        print("6 - Закончить день")
        print("7 - Закончить неделю")

    elif state == "LIST":
        print("Количество семей:(", len(plebs), ")")
        i = 0
        for p in plebs:
            wife = "none"
            if p.wife != "none":
                wife = p.wife.name
            print(
            "№", i, "Имя:", p.name + " " * (9 - len(p.name)),"Возраст:",p.age, "Жена:", wife,"Работа:", p.job, "Деньги:", p.money)
            print("Дом:", p.house, "Коровы:", p.cow, "|Гр:", p.mushrooms, "|Пш:", p.wheet, "|Млк:", p.milk, "|Др:", p.wood, "|")
            i = i + 1
        print("---")
        print("find №# - Инфа по номеру")
        print("2 - Инфа по имени")
        print("Нажмите Enter чтобы продолжить")

    elif state == "BRIDELIST":
        i = 0
        for p in brides:
            print("№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Возраст:", p.age)
            i = i + 1

    elif state == "STATUS":
        print("Ваши деньги -", pl.money)
        print("Склад -|Грибы:", pl.mushrooms, "|Пшеница:", pl.wheet, "|")
        print("|Молоко:", pl.milk, "|Дрова:", pl.wood, "|")
        print("Ежедневные Расходы - Еда: 1")
        print("Рассчитываемый доход за", pl.day - 1, " |Гр:", pl.incomingMushrooms, "|Пш:", pl.incomingWheet, "|Млк:",
              pl.incomingMilk, "|Др:", pl.incomingWood, "|")

    elif state == "CONFIRMING":
        print("Вы уверенны что хотите закончить день?(Y/N)")

    elif state == "CONFIRMING2":
        print("Вы уверенны что хотите закончить неделю?(Y/N)")

    elif state == "TRADE":
        tr.generateGoods()
        print("Вещи торговца -|Грибы:", tr.mushrooms, "|Пшеница:", tr.wheet, "|")
        print("|Молоко:", tr.milk, "|Дрова:", tr.wood, "|")
        print("1 - Купить корову")
    word = input()

    clear(20)

    if state == "LIST":
        if word[0:5] == "find ":
            state = "SEARCHNUMBER"
        else:
            state = "MAIN"

    elif state == "MAIN":
        if word == "1":
            state = "LIST"
        if word == "2":
            state = "MAIN"
        if word == "3":
            state = "STATUS"
        if word == "4":
            state = "TRADE"
        if word == "5":
            state = "BRIDELIST"
        if word == "6":
            state = "DAYENDING"
        if word == "7":
            state = "WEEKENDING"

    elif state == "MENU":
        if word == "1":
            state = "MAIN"
            plebs = [pleb(10, "HasHouse", ), pleb(0, "HasCow", ), pleb(0, "HasNone", )]
            brides = [woman(),woman(),woman(),woman()]
        if word == "2":
            exit = 1

    elif state == "CONFIRMING":
        if word == "y" or word == "Y":
            state = "DAYENDING"
        elif word == "n" or word == "N":
            state = "MAIN"

    elif state == "CONFIRMING2":
        if word == "y" or word == "Y":
            state = "WEEKENDING"
        elif word == "n" or word == "N":
            state = "MAIN"

    elif state == "STATUS":
        state = "MAIN"

    elif state == "TRADE":
        state = "MAIN"

    elif state == "BRIDELIST":
        state = "MAIN"

    if state == "DAYENDING":
        state = "MAIN"
        for i in plebs:
            i.deciding()
            i.jobbing()
            i.working()
            i.spending()
            i.rounding()
        pl.spending()
        pl.dayEnding()
        pl.rounding()

    elif state == "WEEKENDING":
        state = "MAIN"
        print("1")
        day = pl.day
        for j in range(day, 7):
            for i in plebs:
                i.deciding()
                i.jobbing()
                i.working()
                i.spending()
                i.rounding()
            pl.spending()
            pl.dayEnding()
            pl.rounding()

    word = "none"
