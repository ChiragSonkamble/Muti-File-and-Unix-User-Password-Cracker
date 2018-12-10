from tkinter import *
import tkFileDialog, zipfile, rarfile, sys, fileinput,crypt,os
from subprocess import call

#Get Selected Option Of Radio Button#
def getVal():
    global val
    val = c.get()
    if val==1:
        sfrar.grid_forget()
        sfunix.grid_forget()
        sfzip.grid(row=2,column=0)    
    elif val==2:
        sfzip.grid_forget()
        sfunix.grid_forget()
        sfrar.grid(row=2,column=0)
    elif val==3:
        sfzip.grid_forget()
        sfrar.grid_forget()
        sfunix.grid(row=2,column=0)

class UNIXCracker:   
    def dict(self):
        global dictFile 
        path = Label(sfunix)
        dictFile = tkFileDialog.askopenfilename()
        #File Path#
        path.config(text=dictFile)
        path.grid(row=3,column=2,columnspan=5,padx=10,pady=10)        

    #Code for calculating SHA512 Hash Shadow
    def testPass_SHA512(self,hashValue,salt2):
        res = Label(sfunix)
        res.grid(row=7,column=3,padx=10,pady=10)
        input_salt = '$6$'+str(salt2)
        f = 0
        try:
            passwordfile = open(dictFile,'r')
            for line in passwordfile.readlines():
                line = line.split("\n")[0]
                calcHashValue = crypt.crypt(line,input_salt)
                if hashValue == calcHashValue:
                    f = 1
                    res.config(text="!!!Congrats!!!\nPassword Found\nValid Password: "+line)
                    break
            
            if f==0:
                res.config(text="Sorry!\nPassword Not Found!")
                
        except Exception as e:
            res.config(text="Sorry! Beacause of some reason..\nPassword Not Found\n"+e)

    #Code for calculating MD5 Hash Shadow
    def testPass_MD5(self,hashValue):
        res = Label(sfunix)
        res.grid(row=7,column=3,padx=10,pady=10)
        input_salt = 'X0'
        f = 0
        try:
            passwordfile = open(dictFile,'r')
            for line in passwordfile.readlines():
                line = line.split("\n")[0]
                calcHashValue = crypt.crypt(line,input_salt)
                if hashValue == calcHashValue:
                    f = 1
                    res.config(text="!!!Congrats!!!\nPassword Found!\nValid Password: "+line)
                    break			
            if f==0:
                res.config(text="Sorry!\nPassword Not Found!")
        
        except Exception as e:
            res.config(text="Sorry! Because of some reason..\nPassword Not Found\n"+e)
    
    def hashCal(self):
        path = os.getcwd()
        path1 = path.split("/")[1:]
        unix = UNIXCracker()
        path1 = "/".join(path1)
        call("unshadow /etc/passwd /etc/shadow > ~"+path1+"/fileToCrack" , shell=True)
        userfile = open(path+"/fileToCrack",'r')
        f = 0
        ip_user = enter_ip_user.get()
        for usr in userfile.readlines():
            usr = usr.split("\n")[0]
            user = usr.split(":")[0]
            if user == ip_user:
                f =1
                hashValue = usr.split(":")[1]
                if hashValue[0:2] == 'X0':
                    unix.testPass_MD5(hashValue)
                else:
                    salt2 = hashValue.split("$")[2]
                    unix.testPass_SHA512(hashValue,salt2)

        if f == 0:        
            print "User not found"

class ZIP:            
    #Browse File#
    def browse_fun_zip(self):
        global usrzipfile
        path = Label(sfzip)
        usrzipfile = tkFileDialog.askopenfilename()
        #File Path#
        path.config(text=usrzipfile)
        path.grid(row=2,column=3,columnspan=2,padx=10,pady=10)

    #Browse Dictionary#
    def browse_dict_fun_zip(self):
        global zipdictfile
        path1 = Label(sfzip)
        zipdictfile = tkFileDialog.askopenfilename()
        #Dictionary Path#
        path1.config(text=zipdictfile)
        path1.grid(row=4,column=3,columnspan=2,padx=10,pady=10)

    #ZIP Craccker#
    def zipCracker(self):
        #Result#
        res = Label(sfzip)
        res.grid(row=8,column=3,columnspan=3,padx=10,pady=10)
        
        try:
            zipF = zipfile.ZipFile(usrzipfile)
            dictPtr = open(zipdictfile,'r')
            f=0
            for d in dictPtr.readlines():
    		    val = d.strip('\n')
    		    try:
    		        zipF.extractall(pwd=val)
    		        res.config(text="!!!Congrats!!!\nPassword Found!\nValid Password: "+val)
    		        f=1
    		        break
    		    except Exception as e:
    		        pass
			
            if f==0:
    	        res.config(text="Sorry!\nPassword Not Found!")
        
        except Exception as e:
            res.config(text="Sorry! Because of some reason..\nPassword Not Found\n"+str(e))

class RAR:
    #Browse File#
    def browse_fun_rar(self):
        self.usrrarfile = tkFileDialog.askopenfilename()
        #File Path#
        path = Label(sfrar,text=self.usrrarfile)
        path.grid(row=2,column=3,columnspan=2,padx=10,pady=10)

    #Browse Dictionary#
    def browse_dict_fun_rar(self):
	    self.rardictfile = tkFileDialog.askopenfilename()
	    #Dictonary Path#
	    path1 = Label(sfrar,text=self.rardictfile)
	    path1.grid(row=4,column=3,columnspan=2,padx=10,pady=10)
	
    #RAR Cracker#
    def rarCracker(self):
        #Result#
        res = Label(sfrar)
        res.grid(row=8,column=3,columnspan=3,padx=10,pady=10)
        try:
            p=0
            fileload = rarfile.RarFile(self.usrrarfile)
            dictionery = self.rardictfile 
            for i in fileinput.input(dictionery):
                pwd=i.strip('\n')
                try:
                    fileload.extractall('.',pwd=str(pwd))
                    res.config(text="!!!Congrats!!!\nPassword Found!\nValid Password: "+pwd)
                    p=1
                except Exception as e:
                    pass
            if p==0:
                res.config(text="Sorry!\nPassword Not Found!")
               
        except Exception as e:
            res.config(text="Sorry! Because of some reason..\nPassword Not Found\n"+str(e))

def main():
    global sfzip
    global sfrar
    global sfunix
    global c
    global enter_ip_user
    dictFile = ""
    usrzipfile = ""
    usrrarfile = ""
    rardictfile = ""
    zipdictfile = ""
    
    #GUI#
    home = Tk()
    home.title("MultiCracker")
    home.geometry("800x400")

    title = Label(home,text="MultiCracker",width=100,height=3)
    title.grid(row=0,column=0,columnspan=3)    
    
    #Radio Frame#
    rf = Frame(home)
    rf.grid(row=1,column=0,columnspan=3)

    #RadioButton#
    c = IntVar()
    c.set(1)

    r1 = Radiobutton(rf,text="ZIP",variable=c,value=1,command=getVal)
    r2 = Radiobutton(rf,text="RAR",variable=c,value=2,command=getVal)  
    r3 = Radiobutton(rf,text="Linux",variable=c,value=3,command=getVal)
    r4 = Radiobutton(rf,text="Win",variable=c,value=4,command=getVal)

    r1.grid(row=0,column=4,padx=10,pady=10)
    r2.grid(row=0,column=5,padx=10,pady=10)
    r3.grid(row=0,column=6,padx=10,pady=10)
    r4.grid(row=0,column=7,padx=10,pady=10)

    #Sub Frame Linux#
    sfunix = Frame(home,width=900)
    sfunix.grid(row=3,column=0)    
    
    #Sub Frame RAR#
    sfrar = Frame(home,width=900)
    sfrar.grid(row=3,column=0)

    #Sub Frame ZIP#
    sfzip = Frame(home,width=900)
    sfzip.grid(row=3,column=0)
   
    zipObj = ZIP()
    rarObj = RAR()
    unixObj = UNIXCracker()

    #Browse File Button#
    browse_file = Button(sfzip, text="Browse ZIP File", command=zipObj.browse_fun_zip, width=25)
    browse_file.grid(row=2,column=0,padx=10,pady=10)    

    #Browse Dictonary Button#
    browse_dict_file = Button(sfzip, text="Browse Dictonary File", command=zipObj.browse_dict_fun_zip, width=25)
    browse_dict_file.grid(row=4,column=0,padx=10,pady=10)

    #Crack Button#
    Crack = Button(sfzip, text="Crack", command=zipObj.zipCracker, width=25)
    Crack.grid(row=6,column=3,columnspan=3,sticky=W,padx=10,pady=10)

    #Browse File Button#
    browse_file = Button(sfrar, text="Browse RAR File", command=rarObj.browse_fun_rar, width=25)
    browse_file.grid(row=2,column=0,padx=10,pady=10)

    #Browse Dictonary Button#
    browse_dict_file = Button(sfrar, text="Browse Dictonary File", command=rarObj.browse_dict_fun_rar, width=25)
    browse_dict_file.grid(row=4,column=0,padx=10,pady=10)

    #Crack Button#
    Crack = Button(sfrar, text="Crack", command=rarObj.rarCracker, width=25)
    Crack.grid(row=6,column=3,columnspan=3,sticky=W,padx=10,pady=10)

    #Enter User Label#
    EnterUsr = Button(sfunix,text="Enter USER name: ",width=25)
    EnterUsr.grid(row=1,column=1,padx=10,pady=10)
    
    
    #Browse Dictonary Button#
    EnterDict = Button(sfunix, text="Enter dictionary file", command=unixObj.dict, width=25)
    EnterDict.grid(row=3,column=1,padx=10,pady=10)

    enter_ip_user = Entry(sfunix)
    enter_ip_user.grid(row=1,column=2,columnspan=5,padx=10,pady=10)
    enter_ip_user.focus_set()

    #Crack Button#
    Crack = Button(sfunix, text="Crack", command=unixObj.hashCal, width=25)
    Crack.grid(row=5,column=2,columnspan=5,sticky=W,padx=10,pady=10)

    home.mainloop()

if __name__ == '__main__':
    main()
