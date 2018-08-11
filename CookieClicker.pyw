from __future__ import division
import Tkinter as tk
import calendar, time, tkMessageBox, tkSimpleDialog, ctypes
from PIL import Image, ImageTk


class Cookies:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1053x555+100+100")
        self.root.resizable(width="false", height="false")
        self.root.configure(background="#347ba0")
        self.root.title("Cookie Clicker")
        self.root.iconbitmap("CookieIcon.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.save)

        self.cookie = Image.open("PerfectCookie.png")
        self.cookie = ImageTk.PhotoImage(self.cookie)
        self.cookieButton = tk.Button(self.root, width=250, height=250, image=self.cookie, relief="flat", bd=0, bg="#347ba0", activebackground="#347ba0", command=self.click)
        self.cookieButton.place(x=18, y=160)
        
        self.cookies, self.count, self.CPS, self.notify, self.bakeryName, self.auto = 0, 1, 0, 0, "", False
        self.buildings = {
        "Clicker" : 0,
        "Grandma" : 0,
        "Farm" : 0,
        "Mine" : 0,
        "Factory" : 0,
        "Bank" : 0,
        "Temple" : 0,
        "Wizard Tower" : 0,
        "Shipment" : 0,
        "Alchemy Lab" : 0,
        "Portal" : 0,
        "Time Machine" : 0,
        "Antimatter Condenser" : 0,
        "Prism" : 0,
        }

        self.upgrades = {
        "Clicker" : 0,
        "Grandma" : 0,
        "Farm" : 0,
        "Mine" : 0,
        "Factory" : 0,
        "Bank" : 0,
        "Temple" : 0,
        "Wizard Tower" : 0,
        "Shipment" : 0,
        "Alchemy Lab" : 0,
        "Portal" : 0,
        "Time Machine" : 0,
        "Antimatter Condenser" : 0,
        "Prism" : 0,
        }
        
        self.cookieCount = tk.Label(self.root, font=("Merriweather",18), text=self.formatStr(self.cookies)+"\nCookies", width=20, justify="center")
        self.cookieCount.place(x=0, y=80)

        self.CPScount = tk.Label(self.root, font=("Merriweather",18), text=self.formatStr(self.CPS)+"\nCookies Per Second", width=20, justify="center")
        self.CPScount.place(x=0, y=430)

        self.Buildings = tk.LabelFrame(self.root, text="Buildings", padx=10, pady=10, width=376, height=540, bg="#347ba0", fg="white", bd=5, relief="raised")
        self.Buildings.place(x=291, y=5)

        self.counter = tk.Button(self.root, text="Count : 1", command=self.changeCount)
        self.counter.place(x=114, y=495)

        self.notifier = tk.Button(self.root, text="Notify Me", command=self.notifyMe)
        self.notifier.place(x=63, y=525)

        self.Upgrades = tk.LabelFrame(self.root, text="Upgrades", padx=10, pady=10, width=376, height=540, bg="#347ba0", fg="white", bd=5, relief="raised")
        self.Upgrades.place(x=672, y=5)

        self.bakery = tk.Button(self.root, text="'s Bakery", relief="flat", font=("Merriweather",16), command=self.updateBakeryName, width=23, justify="center")
        self.bakery.place(x=0, y=20)

        self.toggleAuto = tk.Button(self.root, text="Toggle Auto (off)", command=self.autoToggle, justify="center")
        self.toggleAuto.place(x=138, y=525)

        images1 = []
        self.buttons1 = []
        self.CPSbuildings = [0,1,8,47,260,1400,7800,44000,260000,1600000,10000000,65000000,430000000,2900000000]
        self.bPrices = [15,100,1100,12000,130000,1400000,20000000,330000000,5100000000,75000000000,1000000000000,14000000000000,170000000000000,2100000000000000]
        for i, j in zip(["Clicker","Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard Tower", "Shipment", "Alchemy Lab", "Portal", "Time Machine",
                         "Antimatter Condenser", "Prism"], range(0,14)):
            images1.append(Image.open("Buildings\\"+"".join(i.split(" "))+".png"))
            images1[j] = ImageTk.PhotoImage(images1[j])
            self.buttons1.append(tk.Button(self.Buildings, width=341, height=32, image=images1[j], relief="flat", bd=0, bg="white", activebackground="#ffdf00", command=lambda x=i, y=j: self.build(x,y), wraplength=309,
                                 compound="left", text=i+" : "+self.formatStr(self.buildings[i])+"   Price : "+self.formatStr(int(sum([round(self.bPrices[j]*(1.15**(self.buildings[i]+l)),0) for l in range(0,self.count)])))))
            self.buttons1[j].pack()

        images2 = []
        self.buttons2 = []
        self.oPrices = [100,1000,11000,120000,1300000,14000000,200000000,3300000000,51000000000,750000000000,10000000000000,140000000000000,1700000000000000,21000000000000000]
        for i, j in zip(["Clicker","Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard Tower", "Shipment", "Alchemy Lab", "Portal", "Time Machine",
                         "Antimatter Condenser", "Prism"], range(0,14)):
            images2.append(Image.open("Upgrades\\"+"".join(i.split(" "))+".png"))
            images2[j] = ImageTk.PhotoImage(images2[j])
            self.buttons2.append(tk.Button(self.Upgrades, width=341, height=32, image=images2[j], relief="flat", bd=0, bg="white", activebackground="#ffdf00", command=lambda x=i, y=j: self.upgrade(x,y), wraplength=309,
                                 compound="left", text="Upgrade "+i+" : "+self.formatStr(self.upgrades[i])+"   Price : "+self.formatStr(int(sum([round(self.oPrices[j]*(2.5**(self.upgrades[i]+l)),0) for l in range(0,self.count)])))))
            self.buttons2[j].pack()

        try:
            execfile("cookieSaveData.txt")
            self.bakery.config(text=self.bakeryName+"'s Bakery")
            self.CPS = 0
            for i, j in zip(["Clicker","Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard Tower", "Shipment", "Alchemy Lab", "Portal", "Time Machine",
                             "Antimatter Condenser", "Prism"], range(0,14)):
                self.CPS+=self.CPSbuildings[j]*(self.upgrades[i]+1)*self.buildings[i]
            newTime = calendar.timegm(time.gmtime())-self.Time
            self.cookies+=int(newTime*self.CPS*0.1)
            tkMessageBox.showinfo("Cookies Earned", "Cookies earnced since last time (at 90% reduction): "+str(int(newTime*self.CPS*0.1)))
            self.update()
        except Exception as e: print e
        
        self.root.after(1000, self.addCookies)
        self.root.mainloop()

    def build(self, building, index, noupdate=False):
        if sum([round(self.bPrices[index]*(1.15**(self.buildings[building]+l)),0) for l in range(0,self.count)])<=self.cookies:
            self.cookies-=int(sum([round(self.bPrices[index]*(1.15**(self.buildings[building]+l)),0) for l in range(0,self.count)]))
            self.buildings[building] = self.buildings[building]+self.count
        if not noupdate:
            self.update()

    def upgrade(self, building, index, noupdate=False):
        if sum([round(self.oPrices[index]*(2.5**(self.upgrades[building]+l)),0) for l in range(0,self.count)])<=self.cookies:
            self.cookies-=int(sum([round(self.oPrices[index]*(2**(self.upgrades[building]+l)),0) for l in range(0,self.count)]))
            self.upgrades[building] = self.upgrades[building]+self.count
        if not noupdate:
            self.update()

    def click(self):
        self.cookies+=(self.buildings["Clicker"]+1)*(self.upgrades["Clicker"]+1)
        self.update()

    def formatStr(self, num):
        divs = {
        3:"Thousand",
        6:"Million",
        9:"Billion",
        12:"Trillion",
        15:"Quadrillion",
        18:"Quintillion",
        21:"Sextillion",
        24:"Septillion",
        27:"Octillion",
        30:"Nonillion",
        33:"Decillion",
        36:"Undecillion",
        39:"Duodecillion",
        42:"Tredicillion",
        45:"Quattuordecillion",
        48:"Quindecillion",
        51:"Sexdecillion",
        54:"Septendicillion",
        57:"Octodecillion",
        60:"Novemdecillion",
        63:"Vigintillion",
        66:"Infinity",
        303:"An Ungodly Number of"
        }
        for i in sorted(divs.keys(), reverse=True):
            if num//(10**i):
                if i not in [66,303]:
                    return str(round(num/(10**i),3))+" "+divs[i]
                else:
                    return str(divs[i])
        else:
            return str(num)

    def update(self):
        self.cookieCount.config(text=self.formatStr(self.cookies)+"\nCookies")
        priceList = []
        for i, j, k, m in zip(self.buttons1,["Clicker","Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard Tower", "Shipment", "Alchemy Lab", "Portal", "Time Machine",
                         "Antimatter Condenser", "Prism"], range(0,14), self.buttons2):
            i.config(text=j+" : "+self.formatStr(self.buildings[j])+"   Price : "+
                     self.formatStr(int(sum([round(self.bPrices[k]*(1.15**(self.buildings[j]+l)),0) for l in range(0,self.count)]))))
            priceList.append((int(sum([round(self.bPrices[k]*(1.15**(self.buildings[j]+l)),0) for l in range(0,self.count)])), "Build "+j+" "+str(k)))
            m.config(text="Upgrade "+j+" : "+self.formatStr(self.upgrades[j])+"   Price : "+
                     self.formatStr(int(sum([round(self.oPrices[k]*(2.5**(self.upgrades[j]+l)),0) for l in range(0,self.count)]))))
            priceList.append((int(sum([round(self.oPrices[k]*(2.5**(self.upgrades[j]+l)),0) for l in range(0,self.count)])), "Upgrade "+j+" "+str(k)))
        self.CPS = 0
        for i, j in zip(["Clicker","Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard Tower", "Shipment", "Alchemy Lab", "Portal", "Time Machine",
                         "Antimatter Condenser", "Prism"], range(0,14)):
            self.CPS+=self.CPSbuildings[j]*(self.upgrades[i]+1)*self.buildings[i]
        self.CPScount.config(text=self.formatStr(self.CPS)+"\nCookies Per Second")
        if self.notify and self.cookies>=self.notify:
            tkMessageBox.showinfo("Notification", "You have reached "+self.formatStr(self.notify)+" cookies")
            self.notify = 0

        if self.auto:
            leastExpensive = min(priceList, key=lambda x: x[0])[1].split(" ")
            if leastExpensive[0]=="Build":
                self.build(leastExpensive[1], int(leastExpensive[2]), noupdate=True)
            else:
                self.upgrade(leastExpensive[1], int(leastExpensive[2]), noupdate=True)

    def changeCount(self):
        self.counter.place_forget()
        if self.count==1:
            self.count = 10
            self.counter.place(x=111, y=495)
        elif self.count==10:
            self.count = 100
            self.counter.place(x=108, y=495)
        elif self.count==100:
            self.count = 1
            self.counter.place(x=114, y=495)
        self.counter.config(text="Count : "+str(self.count))
        self.update()

    def addCookies(self):
        self.cookies+=self.CPS
        self.update()
        self.root.after(1000, self.addCookies)

    def save(self, _=None):
        save = open("cookieSaveData.txt", "w")
        save.write("self.cookies = "+str(self.cookies)+"\nself.buildings = "+str(self.buildings)+"\nself.upgrades = "+str(self.upgrades)+
                   "\nself.Time = "+str(calendar.timegm(time.gmtime()))+"\nself.bakeryName = \""+self.bakeryName+"\"")
        save.close()
        self.root.destroy()

    def notifyMe(self):
        self.notify = tkSimpleDialog.askinteger("Notification", "Input the number of cookies you would like to be notified on")

    def autoToggle(self):
        self.auto = not self.auto
        self.toggleAuto.config(text="Toggle Auto ({})".format("on" if self.auto else "off"))

    def updateBakeryName(self):
        before = str(self.bakeryName)
        self.bakeryName = tkSimpleDialog.askstring("Bakery Name", "Enter your bakery name", initialvalue="Hello")
        if self.bakeryName == None:
            self.bakeryName = before
            return
        while len(self.bakeryName)>14:
            self.bakeryName = tkSimpleDialog.askstring("Bakery Name", "Enter your name")
        self.bakery.config(text=self.bakeryName+"'s Bakery")

if __name__ == "__main__":
    myappid = "Joshua Duncan.Cookie Clicker.Cookie Clicker Game.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    c = Cookies()
