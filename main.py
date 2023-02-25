from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from pytube import *
from tkinter import filedialog
import requests
import io
import os



class Youtube_app:
    def __init__(self,root):
        self.root = root
        self.root.title("  Youtube Video Downloader ||   Techs")
        self.root.geometry("600x500+300+50")
        self.root.wm_iconbitmap("D:/Playground/Projects/Youtube downloader/ico/youtube.ico")
        self.root.resizable(False,False)
        self.root.config(bg = 'white')

        title = Label(self.root,text ="  Youtube Video Downloader ||  Techs",font = ("times new roman",10),bg = "#800000",fg = "white" ).pack(side = TOP,fill = X)

        self.var_url = StringVar()
        
        lbl_url = Label(self.root,text ="Video URL",font = ("times new roman",13),bg = "white",fg = "black" ).place(x = 5,y=40)
        txt_url = Entry(self.root,font = ("times new roman",11),bg = "lightyellow",textvariable = self.var_url, borderwidth=2, relief=RIDGE).place(x = 110,y=40,width = 467)
        
        lbl_filetype = Label(self.root,text ="File Type",font = ("times new roman",13),bg = "white",fg = "black" ).place(x = 5,y=150)
        
        self.var_fileType = StringVar()
        self.var_fileType.set('Video')
        video_radio = Radiobutton(self.root,text = 'Video',variable = self.var_fileType,value = 'Video', font = ("times new roman",12),bg = "white",activebackground = 'white').place(x= 110,y = 150)
        audio_radio = Radiobutton(self.root,text = 'Audio',variable = self.var_fileType,value = 'Audio', font = ("times new roman",12),bg = "white",activebackground = 'white').place(x= 200,y = 150)

        btn_search = Button(self.root,text = 'Search', font = ("times new roman",12,"bold"),bg = 'darkred',fg = 'white',command=self.search,width = 15).place(x = 430 , y = 150)

        self.path = Label(self.root,text ="File Loc",font = ("times new roman",13),bg = "white",fg = "black" )
        self.path.place(x = 5,y=80)
        self.path_holder = Label(self.root,text =" \t\t\t",font = ("times new roman",12),bg = "lightyellow",fg = "black", borderwidth=2, relief=RIDGE, anchor = 'w' )
        self.path_holder.place(x = 110,y=80,width = 350)
        self.path_btn= Button(self.root,width = 11, text = "Path",bg = 'darkred',fg = 'white',command = self.open_path)
        self.path_btn.place(x = 490,y = 79)
  
        
        frame1 = Frame(self.root,bd = 2 , relief = RIDGE,bg = "lightyellow")
        frame1.place(x= 10,y=190,width = 580, height = 180)
        self.video_title = Label(frame1,text ="Video Title ",font = ("times new roman",11),bg = "lightgrey",anchor ='w')
        self.video_title.place(x = 0,y=0, relwidth = 1)
        
        self.video_image = Label(frame1,text ="Video \nImage ",font = ("times new roman",15),bg = "lightgrey",bd = 2,relief = RIDGE)
        self.video_image.place(x = 5,y=27, width = 180, height = 145)
        
        lbl_desc = Label(frame1,text ="Description ",font = ("times new roman",15),bg = "lightyellow").place(x = 190,y=30)

        self.video_desc = Text(frame1,font = ("times new roman",10),bg = "lightyellow")
        self.video_desc.place(x = 190,y=60, width = 380, height = 110)

        self.lbl_size = Label(self.root,text ="Total Size : 0 MB",font = ("times new roman",11),bg = "white",fg = "black" )
        self.lbl_size.place(x = 10,y=380)
        
        self.lbl_percentage = Label(self.root,text ="Downloading: 0%",font = ("times new roman",11),bg = "white",fg = "black" )
        self.lbl_percentage.place(x = 170,y=380)

        btn_clear = Button(self.root,text = 'Clear', font = ("times new roman",12),bg = 'darkred',fg = 'white',width = 9,command = self.clear).place(x = 310 , y = 375)
        self.btn_download = Button(self.root,text = 'Download 🢃', font = ("times new roman",13,"bold"),bg = 'darkred',fg = 'white',width = 17,command = self.download,state=DISABLED)
        self.btn_download.place(x = 410 , y = 375)

        self.prog = ttk.Progressbar(self.root,orient = HORIZONTAL,length =590, mode = 'determinate')
        self.prog.place(x=10,y=420,width = 580,height = 25)

        self.lbl_message = Label(self.root,text ="",font = ("Elephant",10),bg = "white",fg = "black" )
        self.lbl_message.place(x =0,y=450,relwidth = 1)

        end_title = Label(self.root,text ="  Devoloped By Koustav Dey",font = ("times new roman",10),bg = "#800000",fg = "white" ).pack(side = BOTTOM,fill = X)
        self.direct = ""
           
    def search(self):
        self.lbl_message.config(text = "")  
        try:
            if self.var_url.get() == '':
                self.lbl_message.config(text = 'Video URL is Not Found',fg = 'darkred',font = ("times new roman",10,'bold'))
            else:

                url = self.var_url.get()
                yt = YouTube(url)
                title = yt.title
                thumbnail = yt.thumbnail_url
                response=requests.get(thumbnail) 
                img_bytes = io.BytesIO(response.content)
                self.img = Image.open(img_bytes)
                self.img=self.img.resize((180,145),Image.ANTIALIAS)
                self.img=ImageTk.PhotoImage(self.img)
                self.video_image.config(image =self.img)

                desc = yt.description[:200]
                select_file=None

                if self.var_fileType.get() == 'Video':
                    select_file = yt.streams.filter(progressive = True).first()
                if self.var_fileType.get() == 'Audio':
                    select_file=yt.streams.filter(only_audio = True).first()

                self.size_inBytes = select_file.filesize
                max_size =self. size_inBytes/1024000
                self.mb = str(round(max_size,2))+'MB'
                self.lbl_size.config(text = "Total Size: "+self.mb)

                self.video_title.config(text = title)
                self.video_desc.delete('1.0',END) 
                self.video_desc.insert(END,desc) 
                self.btn_download.config(state= NORMAL)
                self.lbl_message.config(text = "Path Not Found !", fg = "darkred")  

        except Exception as e:
                self.lbl_message.config(text = "Wrong Url", fg = "darkred")  
                pass


    def progress(self, streams,chunk,bytes_remaining):
        percentage = (float(abs(bytes_remaining-self.size_inBytes)/self.size_inBytes))*float(100)
        self.prog['value']=percentage
        self.prog.update
        self.lbl_percentage.config(text = f'Downloading: {str(round(percentage,2))}%')
        if (round(percentage,2))==100:
            self.lbl_message.config(text = 'Download Complete',fg = 'green')
            self.btn_download.config(state= DISABLED)
      

    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.btn_download.config(state= DISABLED)
        self.lbl_message.config(text='')
        self.video_title.config(text='Video Title ')
        self.video_image.config(image='')
        self.lbl_message.config(text = "")  
        self.video_desc.delete('1.0',END)
        self.lbl_size.config(text = "Total Size: 0 MB")
        self.lbl_percentage.config(text = "0%")


    def open_path(self):
        self.direct = filedialog.askdirectory()
        self.path_holder.config(text =self.direct)

    def download(self):
        
        self.lbl_message.config(text = "")  
        if os.path.exists("C:\\Users\\Darknight\\Desktop\\Download")==False:
            os.mkdir("C:\\Users\\Darknight\\Desktop\\Download")

        default_path = "C:\\Users\\Darknight\\Desktop\\Download"
        yt = YouTube(self.var_url.get(),on_progress_callback = self.progress)
       
        if self.direct == "":
            if self.var_fileType.get()=='Video':
                select_file = yt.streams.filter(progressive = True).first() 
                # print("Default")
                select_file.download(default_path)

            if self.var_fileType.get() == 'Audio':
                select_file=yt.streams.filter(only_audio = True).first()
                select_file.download(default_path)

        else:
            if self.var_fileType.get()=='Video':
                select_file = yt.streams.filter(progressive = True).first() 
                # print("User")
                select_file.download(self.direct)

            if self.var_fileType.get() == 'Audio':
                select_file=yt.streams.filter(only_audio = True).first()
                select_file.download(self.direct)


root = Tk()
obj = Youtube_app(root)
root.mainloop()