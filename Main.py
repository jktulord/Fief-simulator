import random
exit = 0
word = ""
state = "MENU"
namelist = ["John", "Max", "Макс", "Макс_Хас", "Акакаий", "Добрыня", "Яков", "Нурберг", "Паша", "Пася", "Саша", "Сася",
            "Johnathan", "Johnson", "Joe", "Jerry", "Jackson", "Jefferson", "Jacob", "Jack", "Jokey"]
womannamelist = ["Агния","Анка","Бана","Вера","Горислава","Доля","Еля","Желана","Зара","Доля","Дуля","Дуня","Желя","Елена",
                 "Есения","Златослава","Ирина","Искра","Иста","Каролина","Катерина","Люта","Лебедь","Маня","Милана","Мира",
                 "Негомира","Ольга","Просковья","Панислава","Раша","Рослава","Светислава","Сияна","Соня","Тайна","Тихомира"]

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
        self.house = Mansion_lv1
        self.adds = []
        self.day = 1
        self.week = 0
        self.wheet = 20
        self.wood = 300
        self.milk = 0
        self.mushrooms = 0
        self.instruments = 0
        self.cow = 0
        self.freeSpace = self.house.freeSpace
        self.capacity = self.house.capacity
        self.cowCapacity = self.house.cowCapacity
        self.incomingWheet = 0
        self.incomingWood = 0
        self.incomingMilk = 0
        self.incomingMushrooms = 0
        self.inProgress = "none"
        self.daysInProgress = 0

    def spending(self):
        foodSpending = 1
        for i in range(0,foodSpending):
            if self.wheet > 0:
                self.wheet -= 1
            elif self.mushrooms > 0:
                self.mushrooms -= 1
            elif self.milk > 0:
                self.milk -= 1
        self.wheet -= self.cow

    def profiting(self):
        self.milk += self.cow * 1.5

    def rotting(self):
        if self.capacity < self.milk+self.mushrooms+self.wood+self.wheet:
            self.milk -= (self.milk // self.capacity) * self.milk * 0.1
            self.wheet -= (self.wheet // self.capacity) * self.wheet * 0.1
            self.wood -= (self.wood // self.capacity) * self.wood * 0.1
            self.mushrooms -= (self.mushrooms // self.capacity) * self.mushrooms * 0.1

    def dayEnding(self):
        self.day += 1
        if self.inProgress != "none":
            self.progressing()
        if self.day == 8:
            self.day = 1
            self.week += 1
            self.wheet += self.incomingWheet
            self.wood += self.incomingWood
            self.milk += self.incomingMilk
            self.mushrooms += self.incomingMushrooms
            self.instruments = 0
            self.cow = 0
            self.incomingWheet = 0
            self.incomingWood = 0
            self.incomingMilk = 0
            self.incomingMushrooms = 0
            tr.generateGoods()
            for p in plebs:
                p.yearlyfamilycheck()

    def rounding(self):
        self.wheet = round(self.wheet, 1)
        if self.wheet < 0:
            self.wheet = 0
        self.wood = round(self.wood, 1)
        if self.wood < 0:
            self.wood = 0
        self.milk = round(self.milk, 1)
        if self.milk < 0:
            self.milk = 0
        self.mushrooms = round(self.mushrooms, 1)
        if self.mushrooms < 0:
            self.mushrooms = 0
        self.incomingWheet = round(self.incomingWheet, 1)
        self.incomingWood = round(self.incomingWood, 1)
        self.incomingMilk = round(self.incomingMilk, 1)
        self.incomingMushrooms = round(self.incomingMushrooms, 1)

    def build(self, Building):
        if self.inProgress == "none" and self.wood - Building.woodCost >= 0:
            if Building.type == "main" and Building.tier > self.house.tier:
                self.inProgress = Building
                self.daysInProgress = Building.buildTime
                self.wood -= Building.woodCost
            elif Building.type == "adds" and self.freespace > 1:
                self.freespace -= 1
                self.inProgress = Building
                self.daysInProgress = Building.buildTime
                self.wood -= Building.woodCost

        else:
            print("НЕКОРЕКТНО")

    def progressing(self):
        if self.inProgress != "none":
            self.daysInProgress -= 1
            if self.daysInProgress == 0:
                if self.inProgress.type == "main":
                    self.house = self.inProgress
                    self.inProgress = "none"
                    print("DONE")
                elif self.inProgress.type == "adds":
                    self.addsBuildings.append(self.inProgress)
                    self.inProgress = "none"
                    print("DOne")
                self.freespaceupdate()

    def freespaceupdate(self):
        self.freeSpace = self.house.freeSpace - len(self.adds)
        self.capacity = self.house.capacity
        self.cowCapacity = self.house.cowCapacity
        for i in self.adds:
            self.capacity += i.capacity
            self.cowCapacity += i.cowCapacity

class building(object):
    def __init__(self, name, type, wood, rooms = 0, buildTime = 0, capacity = 0, tier = 1, freeSpace = 0, cowCapacity = 0):
        self.name = name
        self.type = type # main, adds or houses
        self.tier = tier
        self.woodCost = wood
        self.rooms = rooms
        self.buildTime = buildTime
        self.capacity = capacity
        self.cowCapacity = cowCapacity
        self.freeSpace = freeSpace


Mansion_lv1 = building("Mansion_lv1", "main", wood=10, rooms=1, buildTime=3,capacity=300, freeSpace=1, tier=1)
Mansion_lv2 = building("Mansion_lv2", "main", wood=100, rooms=2, buildTime=3,capacity=500, freeSpace=2, tier=2)
Mansion_lv3 = building("Mansion_lv3", "main", wood=400, rooms=3, buildTime=7,capacity=1250, freeSpace=5, tier=3)
Mansion_lv4 = building("Mansion_lv4", "main", wood=900, rooms=4, buildTime=9,capacity=2250, freeSpace=8, tier=4)
Mansion_lv5 = building("Mansion_lv5", "main", wood=1500, rooms=5, buildTime=13,capacity=5000, freeSpace=14, tier=5)
Mansion_lv6 = building("Mansion_lv6", "main", wood=3500, rooms=5, buildTime=15,capacity=10000, freeSpace=18, tier=6)
Storage_lv1 = building("Storage_lv1", "adds", wood=100, rooms=0, buildTime=2,capacity=500, tier=1)
Storage_lv2 = building("Storage_lv2", "adds", wood=350, rooms=0, buildTime=4,capacity=1250, tier=2)
Storage_lv3 = building("Storage_lv3", "adds", wood=750, rooms=0, buildTime=5,capacity=2500, tier=3)
Barn_lv1 = building("Barn_lv1", "adds", wood=150, cowCapacity=3, buildTime=2, tier=1)
Barn_lv2 = building("Barn_lv2", "adds", wood=150, cowCapacity=3, buildTime=2, tier=2)
Dorm_lv1 = building("Dorm_lv1", "adds", wood=150, rooms=2, buildTime=2, tier=1)
Dorm_lv2 = building("Dorm_lv2", "adds", wood=150, rooms=4, buildTime=4, tier=2)

buildlist = [Mansion_lv1, Mansion_lv2, Mansion_lv3,Mansion_lv4,Mansion_lv5,Mansion_lv6,Storage_lv1,Storage_lv2,Storage_lv3,Barn_lv1,Barn_lv2,Dorm_lv1,Dorm_lv2]

pl = player()

class woman(object):
    def __init__(self,type ="none"):
        self.name = womannamelist[random.randint(0, len(womannamelist) - 1)]
        self.age = random.randint(14, 20)
        self.sex = "female"
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
        self.sex = "male"
        self.money = money
        self.age = random.randint(18,28)
        self.wife = "none"
        self.childs = []
        self.job = "none"
        self.house = "none"
        self.cow = 0
        self.cowCapacity = 99
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
        self.instruments = 0
        self.efficiency = 1
        self.theGoal = "none"
        self.requiredMoney = 0

    def deciding(self):  # Выбор цели
        food = self.wheet + self.milk + self.mushrooms
        wheet = self.wheet
        requiredfood = 1 + 0.1*len(self.childs)
        if self.wife != "none":
            requiredfood += 0.4


        if food < requiredfood * 7:  # Решение делать еду
            self.theGoal = "food"
        elif self.house == "none": #хижина
            self.theGoal = "shed"
        elif self.wife == "none":
            self.theGoal = "wife"
        elif self.instruments == 0: # Инструменты
            self.theGoal = "instruments"
        elif self.cow == 0: # Корова
            self.theGoal = "cow"
        else:
            if food < requiredfood * 14:
                self.theGoal = "food" # Просто еда
            else:
                R = random.randint(1,4)
                if R == 1:
                    self.theGoal = "instruments"
                if R == 2:
                    self.theGoal = "cow"
                if R == 3:
                    self.theGoal = "food"
        if wheet < 7 * self.cow:
            self.theGoal = "wheet"

    def jobbing(self):  # Выбор работы на основе цели
        if self.theGoal == "food":
            self.job = "gathering"
            if self.instruments > 0:
                self.job = "wheet"
        elif self.theGoal == "wheet":
            if self.instruments == 0:
                self.requiredMoney = tr.instrumentsCost
                if self.money >= self.requiredMoney:
                    self.job = "BuyingInstruments"
                self.job = "SellingCow"
            else:
                self.job = "wheet"
        elif self.theGoal == "wife":
            self.job = "wifeFinding"
        elif self.theGoal == "shed":
            if self.wood > 10:
                self.job = "BuildingShed"
            else:
                self.job = "wood"
        elif self.theGoal == "instruments":
            self.requiredMoney = tr.instrumentsCost
            if self.money >= self.requiredMoney:
                self.job = "BuyingInstruments"
            elif round(self.wood) > 0:
                self.job = "SellingWood"
            else:
                self.job = "wood"
        elif self.theGoal == "cow":
            self.requiredMoney = tr.cowCost
            if self.money >= self.requiredMoney:
                self.job = "BuyingCow"
            elif round(self.wood,1) > 0:
                self.job = "SellingWood"
            else:
                self.job = "wood"

    def working(self):  # Работы
        self.efficiency = 1
        if self.wife != "none":
            self.efficiency += 0.5
        self.efficiency += 0.1*len(self.childs)
        self.efficiency += 0.1 * self.instruments
        if self.job == "gathering":
            self.mushrooms += 2 * self.efficiency * 0.8
            pl.incomingMushrooms += 2 * self.efficiency* 0.2
        elif self.job == "wood":
            self.wood += 1 * self.efficiency * 0.8
            pl.incomingWood += 1 *self.efficiency * 0.2
        elif self.job == "wheet":
            self.wheet += 4 * self.efficiency * 0.8
            pl.incomingWheet += 4 *self.efficiency * 0.2
        elif self.job == "wifeFinding":
            self.wife = brides[random.randint(0,len(brides)-1)]
            brides.remove(self.wife)
        elif self.job == "BuildingShed":
            self.wood -= 10
            self.house = "Shed"
        elif self.job == "BuyingInstruments":
            tr.buying(self, "instruments", 1)
        elif self.job == "BuyingCow":
            tr.buying(self, "cow", 1)
        elif self.job == "SellingCow":
            tr.selling(self, "cow", 1)
        elif self.job == "SellingWood":
            tr.selling(self,"wood",round(self.wood,1))

    def spending(self):  # Расходы и доходы у крестьян
        self.wheet -= 1 * self.cow
        self.milk += 1 * self.cow * 0.8
        pl.milk += 1 * self.cow * 0.2
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
            if random.randint(0, 100) + 1 <= 5:
                if random.randint(0, 100) + 1 >= 50:
                    self.childs.append(pleb(0, "Child"))
                else:
                    self.childs.append(woman())

    def yearlyfamilycheck(self):
        self.age += 1
        self.deathcheck()
        if self.wife != "none":
            self.wife.age += 1
            if self.wife.deathcheck():
                self.wife = "none"
        for ch in self.childs:
            ch.age += 1
            if ch.age >= 14:
                if ch.sex == "female":
                    brides.append(ch)
                if ch.sex == "male":
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
        self.money = round(self.money, 1)

class trader(object):
    def __init__(self):
        self.money = 100
        self.maxcargo = 100
        self.wheet = 0
        self.wood = 0
        self.milk = 0
        self.mushrooms = 0
        self.cow = 30
        self.instruments = 30
        self.wheetCost = 1
        self.woodCost = 2
        self.milkCost = 2
        self.mushroomsCost = 1.5
        self.cowCost = 10
        self.instrumentsCost = 5

    def generateGoods(self):
        self.money += (self.wheet + self.milk + self.wood + self.mushrooms)
        number = []
        self.instruments += (random.randint(1,30))
        self.cow += (random.randint(1,31))
        freecargo = self.maxcargo
        for i in range(4):
            num = random.randint(1, self.maxcargo * 0.5) % freecargo
            number.append(num)
            freecargo -= num
        self.wheet += number[0]
        self.wood += number[1]
        self.milk += number[2]
        self.mushrooms += number[3]

    def rounding(self):
        self.wheet = round(self.wheet, 1)
        if self.wheet < 0:
            self.wheet = 0
        self.wood = round(self.wood, 1)
        if self.wood < 0:
            self.wood = 0
        self.milk = round(self.milk, 1)
        if self.milk < 0:
            self.milk = 0
        self.mushrooms = round(self.mushrooms, 1)
        if self.mushrooms < 0:
            self.mushrooms = 0
        self.money = round(self.money, 1)


    def buying(self,buyer,goods,amount):
        if len(plebs) < 100:
            print("Покупка",buyer.name,goods,amount)
        if goods == "wheet":
            if buyer.money - self.wheetCost * amount >= 0 and self.wheet - amount >= 0 :
                buyer.money -= self.wheetCost * amount
                self.money += self.wheetCost * amount
                buyer.wheet += amount
                self.wheet -= amount
        elif goods == "wood":
            if buyer.money - self.woodCost * amount >= 0 and self.wood - amount >= 0 :
                buyer.money -= self.woodCost * amount
                self.money += self.woodCost * amount
                buyer.wood += amount
                self.wood -= amount
        elif goods == "milk":
            if buyer.money - self.milkCost * amount >= 0 and self.milk - amount >= 0 :
                buyer.money -= self.milkCost * amount
                self.money += self.milkCost * amount
                buyer.milk += amount
                self.milk -= amount
        elif goods == "mushrooms":
            if buyer.money - self.mushroomsCost * amount >= 0 and self.mushrooms - amount >= 0 :
                buyer.money -= self.mushroomsCost * amount
                self.money += self.mushroomsCost * amount
                buyer.mushrooms += amount
                self.mushrooms -= amount
        elif goods == "cow":
            if buyer.money - self.cowCost * amount >= 0 and self.cow - amount >= 0 and buyer.cowCapacity >= buyer.cow + amount :
                buyer.money -= self.cowCost * amount
                self.money += self.cowCost * amount
                buyer.cow += amount
                self.cow -= amount
        elif goods == "instruments":
            if buyer.money - self.instrumentsCost * amount >= 0 and self.instruments - amount >= 0 :
                buyer.money -= self.instrumentsCost * amount
                self.money += self.instrumentsCost * amount
                buyer.instruments += amount
                self.instruments -= amount
        else:
            print("EXEPTION")

    def selling(self,seller,goods,amount):
        if len(plebs) < 100:
            print("Продажа", seller.name, goods, amount)
        if goods == "wheet":
            if self.money - self.wheetCost * amount >= 0 and seller.wheet - amount >= 0 :
                seller.money += self.wheetCost * amount
                self.money -= self.wheetCost * amount
                seller.wheet -= amount
                self.wheet += amount
        elif goods == "wood":
            if self.money - self.woodCost * amount >= 0 and seller.wood - amount >= 0 :
                seller.money += self.woodCost * amount
                self.money -= self.woodCost * amount
                seller.wood -= amount
                self.wood += amount
        elif goods == "milk":
            if self.money - self.milkCost * amount >= 0 and seller.milk - amount >= 0 :
                seller.money += self.milkCost * amount
                self.money -= self.milkCost * amount
                seller.milk -= amount
                self.milk += amount
        elif goods == "mushrooms":
            if self.money - self.mushroomsCost * amount >= 0 and seller.mushrooms - amount >= 0 :
                seller.money += self.mushroomsCost * amount
                self.money -= self.mushroomsCost * amount
                seller.mushrooms -= amount
                self.mushrooms += amount
        elif goods == "cow":
            if self.money - self.cowCost * amount >= 0 and seller.cow - amount >= 0:
                seller.money += self.cowCost * amount
                self.money -= self.cowCost * amount
                seller.cow -= amount
                self.cow += amount
        elif goods == "instruments":
            if self.money - self.instrumentsCost * amount >= 0 and seller.instruments - amount >= 0:
                seller.money += self.instrumentsCost * amount
                self.money -= self.instrumentsCost * amount
                seller.instruments -= amount
                self.instruments += amount
        else:
            print("Ошибка")

tr = trader()

while exit == 0:

    if state == "MENU":  # стейт меню
        print("-v0.1.1 - BUILDINGS Update")
        print("Симулятор Дворянина")
        print("1 - начать игру")
        print("2 - выйти")

    elif state == "MAIN":
        print("День:", pl.day, "Week:", pl.week)
        print("Состояние деревушки")
        print("Ваши деньги -", pl.money)
        print("Количество семей -", len(plebs))
        print("Дом -", pl.house.name)
        if pl.inProgress != "none":
            print("Проект:",pl.inProgress.name,"Осталось дней:",pl.daysInProgress)
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
            "№", i, "Имя:", p.name + " " * (9 - len(p.name)),"|Дом:", p.house, "Коровы:", p.cow,"Инструменты:", p.instruments,"|Гр:", p.mushrooms, "|Пш:", p.wheet, "|Млк:", p.milk, "|Др:", p.wood, "|")
            print("Возраст:",p.age,"Жена:", wife,"Дети:", len(p.childs),"Работа:", p.job, "Деньги:", p.money)
            i = i + 1
        print("---")
        print("find №# - Инфа по номеру")
        print("2 - Инфа по имени")
        print("Нажмите Enter чтобы продолжить")

    elif state == "BRIDELIST":
        i = 0
        for p in brides:
            print("№",i, "Имя:", p.name + " " * (9 - len(p.name)), "Возраст:", p.age)
            i = i + 1

    elif state == "STATUS":
        print("Ваши деньги -", pl.money)
        print("Склад (",pl.capacity,")")
        print("-|Грибы:", pl.mushrooms, "|Пшеница:", pl.wheet, "|")
        print("|Молоко:", pl.milk, "|Дрова:", pl.wood, "|")
        print("Инструменты:", pl.instruments)
        print("Коровы:",pl.cow,"/",pl.cowCapacity)
        print("Ежедневные Расходы - Еда: 1")
        print("Рассчитываемый доход за", pl.day - 1)
        print(" |Гр:", pl.incomingMushrooms, "|Пш:", pl.incomingWheet, "|Млк:",
              pl.incomingMilk, "|Др:", pl.incomingWood, "|")
        print("1 - Посмотреть доступные для строения")
        print("2 - Посмотреть Мои строения")

    elif state == "BUILDLIST":
        print("Доступные строения:")
        i = 0
        for p in buildlist:
            if p.type == "main":
                if p.tier == 1 + pl.house.tier:
                    print("Основное здание:")
                    print("№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Стоимость:", p.woodCost, "Cовбодные комнаты:", p.rooms,)
                    print("Время постройки:", p.buildTime, "Вместимость:", p.capacity,"Максимальное количество пристроек:",p.freeSpace)
                    print("Доп. здание---------------------------------------")
            elif p.type == "adds" and p.tier < pl.house.tier:
                print(
                "№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Стоимость:", p.woodCost, "Cовбодные комнаты:", p.rooms)
                print("Время постройки:", p.buildTime, "Вместимость:", p.capacity,"Места для скота:", p.cowCapacity)
                print("------------------------------------------------------")
            i = i + 1

    elif state == "BUILDINGLIST":
        print("Основное строение:")
        print("Имя:", pl.house.name + " " * (9 - len(pl.house.name)), "Стоимость:", pl.house.woodCost, "Cовбодные комнаты:",pl.house.rooms)
        print("Вместимость:", pl.house.capacity, "Сободного места для пристроек:", pl.house.freeSpace, "Уровень:", pl.house.tier )
        print("Всего места для скота:", pl.cowCapacity)
        print("Доп. здание---------------------------------------")
        for p in pl.adds:
            print("№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Стоимость:", p.woodCost, "Дополнительные комнаты:",
                p.rooms,)
            print("Дополнительная вместимость:", p.capacity, "Дополнительные места для скота:", p.cowCapacity)
            print("------------------------------------------------------")
            i = i + 1

    elif state == "CONFIRMING":
        print("Вы уверенны что хотите закончить день?(Y/N)")

    elif state == "CONFIRMING2":
        print("Вы уверенны что хотите закончить неделю?(Y/N)")

    elif state == "TRADE":
        print("Вещи торговца(",tr.money,")")
        print("|Грибы:", tr.mushrooms, "|Пшеница:", tr.wheet, "|")
        print("|Молоко:", tr.milk, "|Дрова:", tr.wood, "|")
        print("|Коровы:", tr.cow, "|Интсрументы:", tr.instrumentsCost, "|")
        print("B - Купить")
        print("S - Продать")
        print("1 - Выйти")

    elif state == "BUYLIST":
        print("Цена покупки ")
        print("|Грибы(MSH):", tr.mushroomsCost, "|Пшеница(WHT:", tr.wheetCost, "|")
        print("|Молоко(MLK):", tr.milkCost, "|Дрова(WOD):", tr.woodCost, "|")
        print("|Коровы(COW):", tr.cowCost, "|Интсрументы(INS):", tr.instrumentsCost, "|")
        print("Пример -[COW 1]")
        print("1 - Выйти")

    elif state == "SELLLIST":
        print("Цена продажи ")
        print("|Грибы(MSH):", pl.mushrooms, "|Пшеница(WHT):", pl.wheet, "|")
        print("|Молоко(MLK):", pl.milk, "|Дрова(WOD):", pl.wood, "|")
        print("|Коровы(COW):", pl.cow, "|Интсрументы(INS):", pl.instruments, "|")
        print("Пример -[MSH 1]")
        print("1 - Выйти")

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
        if word == "8":
            state = "MONTHENDING"

    elif state == "MENU":
        if word == "1":
            state = "MAIN"
            plebs = [pleb(10, "HasHouse", ), pleb(0, "HasCow", ), pleb(0, "HasNone", )]
            brides = [woman(), woman(), woman(), woman()]
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
        if word == "1":
            state = "BUILDLIST"
        elif word == "2":
            state = "BUILDINGLIST"
        else:
            state = "MAIN"

    elif state == "BUILDLIST":
        if word[0:5] == "BUILD":
            pl.build(buildlist[int(word[6:])])
        state = "MAIN"

    elif state == "BUILDINGLIST":
        state = "MAIN"

    elif state == "TRADE":
        tr.rounding()
        if word == "b":
            state = "BUYLIST"
        if word == "s":
            state = "SELLLIST"
        if word == "1":
            state = "MAIN"

    elif state == "BUYLIST":
        if word[0:3] == "MSH":
            tr.buying(pl,"mushrooms",int(word[4:]))
        elif word[0:3] == "WHT":
            tr.buying(pl,"wheet",int(word[4:]))
        elif word[0:3] == "MLK":
            tr.buying(pl,"milk",int(word[4:]))
        elif word[0:3] == "WOD":
            tr.buying(pl,"wood",int(word[4:]))
        elif word[0:3] == "COW":
            tr.buying(pl,"cow",int(word[4:]))
        elif word[0:3] == "INS":
            tr.buying(pl,"instruments",int(word[4:]))
        elif word == "1":
            state = "TRADE"
        else:
            print("Mistake")

    elif state == "SELLLIST":
        if word[0:3] == "MSH":
            tr.selling(pl,"mushrooms",int(word[4:]))
        elif word[0:3] == "WHT":
            tr.selling(pl,"wheet",int(word[4:]))
        if word[0:3] == "MLK":
            tr.selling(pl,"milk",int(word[4:]))
        elif word[0:3] == "WOD":
            tr.selling(pl,"wood",int(word[4:]))
        if word[0:3] == "COW":
            tr.selling(pl,"cow",int(word[4:]))
        elif word[0:3] == "INS":
            tr.selling(pl,"instruments",int(word[4:]))
        elif word == "1":
            state = "TRADE"

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
            i.familycheck()
        pl.spending()
        pl.profiting()
        pl.rotting()
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
                i.familycheck()
            pl.spending()
            pl.profiting()
            pl.rotting()
            pl.dayEnding()
            pl.rounding()

    elif state == "MONTHENDING":
        state = "MAIN"
        print("1")
        day = pl.day
        for j in range(0, 21):
            for i in plebs:
                i.deciding()
                i.jobbing()
                i.working()
                i.spending()
                i.rounding()
                i.familycheck()
            pl.spending()
            pl.profiting()
            pl.rotting()
            pl.dayEnding()
            pl.rounding()


    word = "none"
