import requests
import io
import os
import sys
import re



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
        
        
        lbl_filetype = Label(self.root,text ="File Type",font = ("times new roman",13),bg = "white",fg = "black" ).place(x = 5,y=160)
        
        self.var_fileType = StringVar()
        self.var_fileType.set('Video')
        video_radio = Radiobutton(self.root,text = 'Video',cursor ="hand2",variable = self.var_fileType,value = 'Video', font = ("times new roman",12),bg = "white",activebackground = 'white').place(x= 110,y = 160)
        audio_radio = Radiobutton(self.root,text = 'Audio',cursor ="hand2",variable = self.var_fileType,value = 'Audio', font = ("times new roman",12),bg = "white",activebackground = 'white').place(x= 200,y = 160)

        self.btn_search = Button(self.root,text = 'Search',state=NORMAL,cursor ="hand2", font = ("times new roman",12,"bold"),bg = 'darkred',fg = 'white',command=self.search,width = 15,height =1)
        self.btn_search.place(x = 430 , y = 120)

        self.path = Label(self.root,text ="File Loc",font = ("times new roman",13),bg = "white",fg = "black" )
        self.path.place(x = 5,y=80)
        self.path_holder = Label(self.root,text =" \t\t\t",font = ("times new roman",12),bg = "lightyellow",fg = "black", borderwidth=2, relief=RIDGE, anchor = 'w' )
        self.path_holder.place(x = 110,y=80,width = 350)
        self.path_btn= Button(self.root,width = 11,state=NORMAL,cursor ="hand2", text = "Path",bg = 'darkred',fg = 'white',command = self.open_path)
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
        
        self.lbl_percentage = Label(self.root,text ="Downloading : 0%",font = ("times new roman",11),bg = "white",fg = "black" )
        self.lbl_percentage.place(x = 170,y=380)

        self.btn_clear = Button(self.root,text = 'Clear',state=NORMAL, font = ("times new roman",12),bg = 'darkred',cursor ="hand2",fg = 'white',width = 9,command = self.clear)
        self.btn_clear.place(x = 310 , y = 375)
        self.btn_download = Button(self.root,text = 'Download 🢃',cursor ="hand2", font = ("times new roman",13,"bold"),bg = 'darkred',fg = 'white',width = 17,command = self.download,state=DISABLED)
        self.btn_download.place(x = 410 , y = 375)

        self.prog = ttk.Progressbar(self.root,orient = HORIZONTAL,length =590, mode = 'determinate')
        self.prog.place(x=10,y=420,width = 580,height = 25)

        self.lbl_message = Label(self.root,text ="",font = ("Elephant",10),bg = "white",fg = "black" )
        self.lbl_message.place(x =0,y=450,relwidth = 1)

        end_title = Label(self.root,text ="  Devoloped By Koustav Dey",font = ("times new roman",10),bg = "#800000",fg = "white" ).pack(side = BOTTOM,fill = X)


        self.options=["144p","240p","360p","480p","720p","1080p"]
        self.path = Label(self.root,text ="File Quality",font = ("times new roman",13),bg = "white",fg = "black" )
        self.path.place(x = 5,y=125)
        self.box = ttk.Combobox(self.root, width = 40,font = ("times new roman",11),values = self.options)
        self.box.place(x = 110, y = 125)
        self.box.current(4)
        self.playlist = Button(self.root,text = "Playlist",width = 30,command = self.playlist_data,cursor ="hand2", font = ("times new roman",10,"bold"),bg = 'darkred',fg = 'white')
        self.playlist.place(x = 354,y=160)

        self.direct = ""

    def playlist_data(self):