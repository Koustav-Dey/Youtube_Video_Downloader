from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from pytube import *
from pytube import YouTube
from pytube import Playlist
from PIL import ImageTk,Image
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












  ################################################################################################################################################################      


    def search_playlist(self):
        try:
            if self.var_data.get() == '':
                showinfo("Playlist      ", "Url Not Found!!")
            else:
                url = self.var_data.get()
                playlist_data = Playlist(url)
                playlist_data._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                flag = 5
                self.Scroll_Bar = Scrollbar(self.frame2,command = self.frame2.yview) 
                self.frame2.config(yscrollcommand=self.Scroll_Bar.set)
                self.Scroll_Bar.pack (side = RIGHT, fill = Y)
                # for url in playlist_data.video_urls:
                #     self.frame2.configure(scrollregion=self.frame2.bbox("all"))
                #     self.playlist_video_title = Label(self.frame2,text ="Video Title ",font = ("times new roman",8),bg = "lightgrey",anchor ='w',width = 80)
                #     self.playlist_video_title.place(x = 30,y=flag)
        
                #     self.playlist_video_image = Label(self.frame2,text ="Video \nImage ",font = ("times new roman",8),bg = "lightgrey",bd = 2,relief = RIDGE)
                #     self.playlist_video_image.place(x = 5,y=flag, width = 22, height = 22)
                #     yt = YouTube(url)
                #     title = yt.title
                #     thumbnail = yt.thumbnail_url
                #     response=requests.get(thumbnail) 
                #     img_bytes = io.BytesIO(response.content)
                #     self.img_playlist = Image.open(img_bytes)
                #     self.img_playlist=self.img_playlist.resize((22,22),Image.ANTIALIAS)
                #     self.img_playlist=ImageTk.PhotoImage(self.img_playlist)
                #     self.playlist_video_image.config(image =self.img_playlist)
                #     print(url)
                #     self.playlist_video_title.config(text = title )
                #     self.new_window.update()
                #     flag= flag + 20
                self.playlist.config(state = NORMAL)        
        except Exception as e:
            print(e)
            showinfo("Playlist      ", "  Wrong URL !!  ")  
            pass
        pass







    def playlist_data(self):
        # self.playlist.config(state = DISABLED)
        self.new_window = Toplevel(self.root)
        self.new_window.geometry("600x300+300+265")
        self.new_window.title("  Video Playlist")
        self.new_window.resizable(False,False)
        self.new_window.config(bg = 'white')
        self.new_window.wm_iconbitmap("D:/Playground/Projects/Youtube downloader/ico/youtube.ico")
        self.new_window.focus()

        title = Label(self.new_window,text ="  Youtube Video Downloader ||  Techs",font = ("times new roman",10),bg = "#800000",fg = "white" ).pack(side = TOP,fill = X)
        end_title = Label(self.new_window,text ="  Devoloped By Koustav Dey",font = ("times new roman",10),bg = "#800000",fg = "white" ).pack(side = BOTTOM,fill = X)

        lbl_url = Label(self.new_window,text ="Playlist URL - ",font = ("times new roman",11),bg = "white",fg = "black" ).place(x = 5,y=30)
        self.var_data = StringVar() 
        playlist_url = Entry(self.new_window,font = ("times new roman",11),takefocus=1,bg ="lightyellow",textvariable = self.var_data, borderwidth=2, relief=RIDGE).place(x = 110,y=30,width = 467)
        search = Button(self.new_window,text= "Search",width = 80,cursor ="hand2",command = self.search_playlist, font = ("times new roman",10,"bold"),bg = 'darkred',fg = 'white')
        search.place(x = 15,y=70)
        download_playlist_video = Button(self.new_window,text= "Download",width = 80,cursor ="hand2", font = ("times new roman",10,"bold"),bg = 'darkred',fg = 'white')
        download_playlist_video.place(x = 15,y=100)
        self.frame2 = Canvas(self.new_window,bd = 2 , relief = RIDGE,bg = "lightyellow")#,scrollregion=(0,0,1000,1000))
        self.frame2.place(x= 10,y=133,width = 580, height = 135)

        pass



#########################################################################################################################################



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
                self.lbl_size.config(text = "Total Size : "+self.mb)

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
        self.lbl_percentage.config(text = f'Downloading : {str(round(percentage,2))}%')
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
        self.lbl_size.config(text = "Total Size : 0 MB")
        self.lbl_percentage.config(text = "Downloading : 0%")
        self.box.current(4)
        self.path_holder.config(text ="")


    def open_path(self):
        self.direct = filedialog.askdirectory()
        self.path_holder.config(text =self.direct)
        self.lbl_message.config(text = "Path Found", fg = "green")

    def download(self):
        

        default_path = "C:\\Users\\Darknight\\Desktop\\Download"
        yt = YouTube(self.var_url.get(),on_progress_callback = self.progress)
       
        if self.direct == "":
            if self.var_fileType.get()=='Video':
                resolution_file = self.box.get()
               
                try:
                    if os.path.exists("C:\\Users\\Darknight\\Desktop\\Download")==False:
                        os.mkdir("C:\\Users\\Darknight\\Desktop\\Download")
                    select_file = yt.streams.filter(res=resolution_file).first() 
                    print(f"{resolution_file} Resolution Found!!")       
                    select_file.download(default_path)
                    showinfo("Youtube Downloader", "Download Complete !!")
                except Exception as e:
                    self.lbl_message.config(text = f"{resolution_file} Resolution Not Found", fg = "darkred")  
                    print(f"{resolution_file} Resolution Not Found")
                    pass

            if self.var_fileType.get() == 'Audio':
                if os.path.exists("C:\\Users\\Darknight\\Desktop\\Download")==False:
                    os.mkdir("C:\\Users\\Darknight\\Desktop\\Download")
                select_file=yt.streams.filter(only_audio = True).first()
                select_file.download(default_path)
                showinfo("Youtube Downloader", "Download Complete !!")

        else:
            if self.var_fileType.get()=='Video':
                resolution_file = self.box.get()
                try:
                    select_file = yt.streams.filter(res=resolution_file).first() 
                    print(f"{resolution_file} Resolution Found!!")
                    select_file.download(self.direct)
                    showinfo("Youtube Downloader", "Download Complete !!")
                except Exception as e:
                    self.lbl_message.config(text = f"{resolution_file} Resolution Not Found", fg = "darkred")  
                    print(f"{resolution_file} Resolution Not Found")
                    pass

            if self.var_fileType.get() == 'Audio':
                select_file=yt.streams.filter(only_audio = True).first()
                select_file.download(self.direct)
                showinfo("Youtube Downloader", "Download Complete !!")
        
root = Tk()
obj = Youtube_app(root)
root.mainloop()
sys.exit()