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
        self.cow = 0
        self.food = 0
        self.Resources = setResources(wheet = 20,wood = 300)
        self.ResourceIncoming = setResources()
        self.freeSpace = self.house.freeSpace
        self.capacity = self.house.capacity
        self.cowCapacity = self.house.cowCapacity
        self.inProgress = "none"
        self.daysInProgress = 0

    def foodCounting(self):
        self.food = 0
        for key in self.Resources:
            if self.Resources[key].type == "food":
                self.food += self.Resources[key].amount

    def spending(self):
        foodSpending = 1
        for i in range(0,foodSpending):
            for key in self.Resources:
                if self.Resources[key].amount >= 1 and self.Resources[key].type == "food":
                    self.Resources[key].amount -= 1
                    break
        self.Resources["wheet"].amount -= self.cow

    def profiting(self):
        self.Resources["milk"].amount += self.cow * 1.5

    def rotting(self):
        if self.capacity < self.food:
            for key in self.Resources:
                self.Resources[key] -= (self.Resources[key] // self.capacity) * (self.capacity - self.Resources[key]) * 0.1
                print("Гниение", key, (self.Resources[key] // self.capacity) * (self.capacity - self.Resources[key]) * 0.1)

    def dayEnding(self):
        self.day += 1
        if self.inProgress != "none":
            self.progressing()
        if self.day == 8:
            self.day = 1
            self.week += 1
            for key in self.Resources:
                self.Resources[key].amount += self.ResourceIncoming[key].amount
                self.ResourceIncoming[key].amount = 0
            for key in self.Resources:
                self.Resources[key].amount += self.ResourceIncoming[key].amount
                self.ResourceIncoming[key].amount = 0
            self.cow = 0
            tr.generateGoods()
            for p in plebs:
                p.yearlyfamilycheck()

    def rounding(self):
        for key in self.Resources:
            self.Resources[key].rounding()
        for key in self.ResourceIncoming:
            self.ResourceIncoming[key].rounding()

    def build(self, Building):
        if self.inProgress == "none" and self.buildCostCheck(Building.RequiredResources):
            if Building.type == "main" and Building.tier > self.house.tier:
                self.inProgress = Building
                self.daysInProgress = Building.buildTime
                self.buildCostSubstraction(Building.RequiredResources)
            elif Building.type == "adds" and self.freespace > 1:
                self.freespace -= 1
                self.inProgress = Building
                self.daysInProgress = Building.buildTime
                self.buildCostSubstraction(Building.RequiredResources)
        else:
            print("НЕКОРЕКТНО")

    def buildCostCheck(self,RequiredResources):
        Check = False
        for key in RequiredResources:
            if RequiredResources[key].amount <= self.Resources[key].amount:
                Check = True
                break
        return Check

    def buildCostSubstraction(self,RequiredResources):
        for key in RequiredResources:
            self.Resources[key].amount -= RequiredResources[key].amount

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

class resource(object):
    def __init__(self, name, type, keyword, tier, amount = 0, baseCost = 0):
        self.name = name
        self.type = type
        self.keyword = keyword
        self.tier = tier
        self.amount = amount
        self.baseCost = baseCost

    def amountChange(self,amount):
        Kek = self
        Kek.amount = amount
        return Kek

    def rounding(self):
        self.amount = round(self.amount,1)
        if self.amount < 0:
            self.amount = 0

def setResources(wheet = 0,berries = 0,mushrooms = 0,milk = 0,wood = 0,instruments = 0):
    Resources = {"wheet": resource("wheet","food", "WHT",baseCost = 1, tier = 1,amount = wheet),
                "mushrooms": resource("mushrooms","food", "MSH", baseCost = 1.3, tier = 1,amount = mushrooms),
                "berries": resource("berries","food", "BRY",baseCost = 1.2, tier = 1,amount = berries),
                "milk": resource("milk","food", "MLK",baseCost = 2.5, tier = 2,amount = milk),
                "wood": resource("wood","building material","WOD", baseCost = 2, tier = 1,amount = wood),
                "instruments": resource("instruments", "craftable", "INS",baseCost = 5, tier = 2,amount = instruments)}
    return Resources

def setRequiredResources(wood = 0,instruments = 0):
    Resource = {"wood": resource("wood", "building material", "WOD", baseCost=2, tier=1, amount=wood),
                "instruments": resource("instruments", "craftable", "INS", baseCost=5, tier=2, amount=instruments)}
    return Resource

class building(object):
    def __init__(self, name, type, RequiredResources, rooms = 0, buildTime = 0, capacity = 0, tier = 1, freeSpace = 0, cowCapacity = 0):
        self.name = name
        self.type = type # main, adds or houses
        self.tier = tier
        self.RequiredResources = RequiredResources
        self.rooms = rooms
        self.buildTime = buildTime
        self.capacity = capacity
        self.cowCapacity = cowCapacity
        self.freeSpace = freeSpace


Mansion_lv1 = building("Mansion_lv1", "main", RequiredResources=setRequiredResources(wood=10), rooms=1, buildTime=3, capacity=300, freeSpace=1, tier=1)
Mansion_lv2 = building("Mansion_lv2", "main", RequiredResources=setRequiredResources(wood=100), rooms=2, buildTime=3, capacity=500, freeSpace=2, tier=2)
Mansion_lv3 = building("Mansion_lv3", "main", RequiredResources=setRequiredResources(wood=350,instruments=1), rooms=3, buildTime=7, capacity=1250, freeSpace=5, tier=3)
Mansion_lv4 = building("Mansion_lv4", "main", RequiredResources=setRequiredResources(wood=900,instruments=3), rooms=4, buildTime=9, capacity=2250, freeSpace=8, tier=4)
Mansion_lv5 = building("Mansion_lv5", "main", RequiredResources=setRequiredResources(wood=1350,instruments=5), rooms=5, buildTime=13, capacity=5000, freeSpace=14, tier=5)
Storage_lv1 = building("Storage_lv1", "adds", RequiredResources=setRequiredResources(wood=100,instruments=1), rooms=0, buildTime=2, capacity=500, tier=1)
Storage_lv2 = building("Storage_lv2", "adds", RequiredResources=setRequiredResources(wood=300,instruments=2), rooms=0, buildTime=2, capacity=1250, tier=1)
Barn_lv1 = building("Barn_lv1", "adds", RequiredResources=setRequiredResources(wood=100,instruments=1), cowCapacity=3, buildTime=2, tier=1)
Dorm_lv1 = building("Dorm_lv1", "adds", RequiredResources=setRequiredResources(wood=100,instruments=1), rooms=2, buildTime=2, tier=1)

buildlist = [Mansion_lv1, Mansion_lv2, Mansion_lv3,Mansion_lv4,Mansion_lv5,Storage_lv1,Storage_lv2,Barn_lv1,Dorm_lv1]

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
        self.Resources = setResources(wheet = 10)
        self.efficiency = 1
        self.theGoal = "none"
        self.requiredMoney = 0
        self.food = 0
        self.foodCounting()

    def foodCounting(self):
        self.food = 0
        for key in self.Resources:
            if self.Resources[key].type == "food":
                self.food += self.Resources[key].amount

    def requiredfoodCounting(self):
        self.requiredfood = 1 + 0.1 * len(self.childs)
        if self.wife != "none":
            self.requiredfood += 0.4

    def deciding(self):  # Выбор цели
        self.foodCounting()
        wheet = self.Resources["wheet"].amount
        self.requiredfoodCounting()


        if self.food < self.requiredfood * 7:  # Решение делать еду
            self.theGoal = "food"
        elif self.house == "none": #хижина
            self.theGoal = "shed"
        elif self.wife == "none":
            self.theGoal = "wife"
        elif self.Resources["instruments"].amount == 0: # Инструменты
            self.theGoal = "instruments"
        elif self.cow == 0: # Корова
            self.theGoal = "cow"
        else:
            if self.food < self.requiredfood * 14:
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
            if self.Resources["instruments"].amount > 0:
                self.job = "wheet"
        elif self.theGoal == "wheet":
            if self.Resources["instruments"].amount == 0:
                self.requiredMoney = self.Resources["instruments"].baseCost
                if self.money >= self.requiredMoney:
                    self.job = "BuyingInstruments"
                self.job = "SellingCow"
            else:
                self.job = "wheet"
        elif self.theGoal == "wife":
            self.job = "wifeFinding"
        elif self.theGoal == "shed":
            if self.Resources["wood"].amount > 10:
                self.job = "BuildingShed"
            else:
                self.job = "wood"
        elif self.theGoal == "instruments":
            self.requiredMoney = self.Resources["instruments"].baseCost
            if self.money >= self.requiredMoney:
                self.job = "BuyingInstruments"
            elif round(self.Resources["wood"].amount) > 0:
                self.job = "SellingWood"
            else:
                self.job = "wood"
        elif self.theGoal == "cow":
            self.requiredMoney = tr.cowCost
            if self.money >= self.requiredMoney:
                self.job = "BuyingCow"
            elif round(self.Resources["wood"].amount, 1) > 0:
                self.job = "SellingWood"
            else:
                self.job = "wood"

    def efficiencyCalculating(self):
        self.efficiency = 1
        if self.wife != "none":
            self.efficiency += 0.5
        self.efficiency += 0.1 * len(self.childs)
        self.efficiency += 0.1 * self.Resources["instruments"].amount

    def working(self):  # Работы
        self.efficiencyCalculating()
        if self.job == "gathering":
            a = random.randint(5,15)
            b = random.randint(5,15)
            self.Resources["mushrooms"].amount += b * 0.1 * self.efficiency * 0.8
            pl.ResourceIncoming["mushrooms"].amount += b * 0.1 * self.efficiency * 0.2
            self.Resources["berries"].amount += a * 0.1 * self.efficiency * 0.8
            pl.ResourceIncoming["berries"].amount += a * 0.1 * self.efficiency * 0.2
        elif self.job == "wood":
            self.Resources["wood"].amount += 1 * self.efficiency * 0.8
            pl.ResourceIncoming["wood"].amount += 1 * self.efficiency * 0.2
        elif self.job == "wheet":
            self.Resources["wheet"].amount += 4 * self.efficiency * 0.8
            pl.ResourceIncoming["wheet"].amount += 4 * self.efficiency * 0.2
        elif self.job == "wifeFinding":
            self.wife = brides[random.randint(0, len(brides)-1)]
            brides.remove(self.wife)
        elif self.job == "BuildingShed":
            self.Resources["wood"].amount -= 10
            self.house = "Shed"
        elif self.job == "BuyingInstruments":
            tr.buying(self, self.Resources["instruments"].name, 1)
        elif self.job == "BuyingCow":
            tr.buying(self, "cow", 1)
        elif self.job == "SellingCow":
            tr.selling(self, "cow", 1)
        elif self.job == "SellingWood":
            tr.selling(self, self.Resources["wood"].name, round(self.Resources["wood"].amount, 1))

    def spending(self):  # Расходы и доходы у крестьян
        self.Resources["wheet"].amount -= 1 * self.cow
        self.Resources["milk"].amount += 1 * self.cow * 0.8
        pl.Resources["milk"].amount += 1 * self.cow * 0.2
        if self.cow > 0:
            if self.Resources["berries"].amount > 0:
                self.Resources["berries"].amount -= 1
            elif self.Resources["mushrooms"].amount > 0:
                self.Resources["mushrooms"].amount -= 1
            elif self.Resources["wheet"].amount > 0:
                self.Resources["wheet"].amount -= 1
            elif self.Resources["milk"].amount > 0:
                self.Resources["milk"].amount -= 1
        else:
            if self.Resources["wheet"].amount > 0:
                self.Resources["wheet"].amount -= 1
            elif self.Resources["berries"].amount > 0:
                self.Resources["berries"].amount -= 1
            elif self.Resources["mushrooms"].amount > 0:
                self.Resources["mushrooms"].amount -= 1
            elif self.Resources["milk"].amount > 0:
                self.Resources["milk"].amount -= 1

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
        for key in self.Resources:
            self.Resources[key].rounding()
        for key in self.Resources:
            self.Resources[key].rounding()
        self.money = round(self.money,1)


class trader(object):
    def __init__(self):
        self.money = 100
        self.maxcargo = 100
        self.Resources = setResources(instruments=30000000000)
        self.cow = 30
        self.cowCost = 10

    def generateGoods(self):
        self.money += 100
        number = []
        self.cow += (random.randint(1,31))
        self.Resources["instruments"].amount += (random.randint(1, 31))
        freecargo = self.maxcargo
        for i in range(3):
            num = random.randint(1, self.maxcargo * 0.5) % freecargo
            number.append(num)
            freecargo -= num
        self.Resources["wheet"].amount += number[0]
        self.Resources["wood"].amount += number[1]
        self.Resources["instruments"].amount += number[2]

    def rounding(self):
        for key in self.Resources:
            self.Resources[key].rounding()
        self.money = round(self.money, 1)


    def buying(self,buyer,goods,amount):

        if goods == "cow":
            if buyer.money - self.cowCost * amount >= 0 and self.cow - amount >= 0 and buyer.cowCapacity >= buyer.cow + amount :
                if len(plebs) < 100:
                    print("Покупка", buyer.name, goods, amount)
                buyer.money -= self.cowCost * amount
                self.money += self.cowCost * amount
                buyer.cow += amount
                self.cow -= amount
        elif buyer.money - self.Resources[goods].baseCost * amount >= 0 and self.Resources[goods].amount - amount >= 0:
            if len(plebs) < 100:
                print("Покупка", buyer.name, goods, amount)
            buyer.money -= self.Resources[goods].baseCost * amount
            self.money += self.Resources[goods].baseCost * amount
            buyer.Resources[goods].amount += amount
            self.Resources[goods].amount -= amount
        else:
            print("Неудачная транзакция",goods)


    def selling(self,seller,goods,amount):
        if goods == "cow":
            if self.money - self.cowCost * amount >= 0 and seller.cow - amount >= 0:
                if len(plebs) < 100:
                    print("Продажа", seller.name, goods, amount)
                seller.money += self.cowCost * amount
                self.money -= self.cowCost * amount
                seller.cow -= amount
                self.cow += amount
        elif self.money - self.Resources[goods].baseCost * amount >= 0 and seller.Resources[goods].amount - amount >= 0:
            if len(plebs) < 100:
                print("Продажа", seller.name, goods, amount)
            seller.money += self.Resources[goods].baseCost * amount
            self.money -= self.Resources[goods].baseCost * amount
            seller.Resources[goods].amount -= amount
            self.Resources[goods].amount += amount
        else:
            print("Неудачная транзакция")


def showResourcesAmount(Dict, name):
    i = 0
    line = "|"
    print(name + ':')
    for key in Dict:
        i += 1
        line += Dict[key].name +": "+ str(Dict[key].amount)+"|"
        if i == 3:
            print(line)
            line = "|"
            i = 0
    if i > 0:
        print(line)


def showResourcesPrice(Dict, name):
    i = 0
    line = "|"
    print(name + ':')
    for key in Dict:
        i += 1
        line += Dict[key].name, ": " + str(Dict[key].baseCost + "|")
        if i == 3:
            print(line)
            line = "|"
            i = 0
    if i > 0:
        print(line)

def KeywordSearch(Dict, keyword):
    ret = "None"
    for i in Dict:
        if Dict[i].keyword == keyword:
            ret = i
    return i

tr = trader()

while exit == 0:

    if state == "MENU":  # стейт меню
        print("-v0.1.9 - TRAITS prepatch")
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
            "№", i, "Имя:", p.name + " " * (9 - len(p.name)),"|Дом:", p.house, "Коровы:", p.cow,"Инструменты:", p.Resources["instruments"].amount,"|Еда:",p.food,"|")
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
        showResourcesAmount(pl.Resources, "Рессурсы")
        print("Коровы:",pl.cow,"/",pl.cowCapacity)
        print("Ежедневные Расходы - Еда: 1")
        #print("Рассчитываемый доход за", pl.day - 1)
        #print(" |Гр:", pl.incomingMushrooms, "|Пш:", pl.incomingWheet, "|Млк:",
        #      pl.incomingMilk, "|Др:", pl.incomingWood, "|")
        print("1 - Посмотреть доступные для строения")
        print("2 - Посмотреть Мои строения")
        print("3 - Посмотреть доход")


    elif state == "BUILDLIST":
        print("Доступные строения:")
        i = 0
        for p in buildlist:
            if p.type == "main":
                if p.tier == 1 + pl.house.tier:
                    print("Основное здание:")
                    print("№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Cовбодные комнаты:", p.rooms,)
                    showResourcesAmount(p.RequiredResources, "Требуемые рессурсы")
                    print("Время постройки:", p.buildTime, "Вместимость:", p.capacity)
                    print("Доп. здание---------------------------------------")
            elif p.type == "adds":
                print(
                "№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Cовбодные комнаты:", p.rooms)
                showResourcesAmount(p.RequiredResources, "Требуемые рессурсы")
                print("Время постройки:", p.buildTime, "Вместимость:", p.capacity,"Места для скота:", p.cowCapacity)
                print("------------------------------------------------------")
            i = i + 1

    elif state == "BUILDINGLIST":
        print("Основное строение:")
        print("Имя:", pl.house.name + " " * (9 - len(pl.house.name)),"Cовбодные комнаты:",pl.house.rooms)
        print("Вместимость:", pl.house.capacity, "Сободного места для пристроек:", pl.house.freeSpace, "Уровень:", pl.house.tier )
        print("Всего места для скота:", pl.cowCapacity)
        print("Доп. здание---------------------------------------")
        for p in pl.adds:
            print("№", i, "Имя:", p.name + " " * (9 - len(p.name)), "Дополнительные комнаты:",
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
        showResourcesAmount(tr.Resources, "Рессурсы")
        print("B - Купить")
        print("S - Продать")
        print("1 - Выйти")

    elif state == "BUYLIST":
        showResourcesPrice(tr.Resources, "Цена покупки")
        print("Пример -[COW 1]")
        print("1 - Выйти")

    elif state == "SELLLIST":
        showResourcesAmount(pl.Resources, "Ваши ресурсы")
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
        if word[0:3] == "COW":
            tr.buying(pl,"cow",int(word[4:]))
        elif word == "1":
            state = "TRADE"
        else:
            try:
                tr.buying(pl,KeywordSearch(pl.Resources,word[0:3]),int(word[4:]))
            except:
                print("Mistake")

    elif state == "SELLLIST":
        if word[0:3] == "COW":
            tr.selling(pl, "cow", int(word[4:]))
        elif word == "1":
            state = "TRADE"
        else:
            try:
                tr.selling(pl, KeywordSearch(pl.Resources), int(word[4:]))
            except:
                print("Mistake")

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
