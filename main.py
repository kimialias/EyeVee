import datetime
#For data
#----------------------------------------------------------------------------------------
from playsound import playsound
#playsound
#----------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
#from data import blink_data_today, blink_data_weekly, blink_data_monthly, blink_data_yearly
from blink_data import blink_data_today, blink_data_weekly, blink_data_monthly, blink_data_yearly
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#matplotlib
#----------------------------------------------------------------------------------------
from tkinter import messagebox
#----------------------------------------------------------------------------------------
#for eye blink function
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
#----------------------------------------------------------------------------------------
#for browser
import webbrowser
#----------------------------------------------------------------------------------------
#for 20-20-20 Rule
import threading
from winotify import Notification, audio
import time
#----------------------------------------------------------------------------------------
from ctypes import windll, byref, Structure, WinError, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HMONITOR, HDC, RECT, LPARAM, DWORD, BYTE, WCHAR, HANDLE
import sys
import getopt
from enum import IntFlag
# MONITOR SETTINGS
#----------------------------------------------------------------------------------------
import ctypes

from PIL import Image
import customtkinter
import os
#----------------------------------------------------------------------------------------

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #for taskbar icon
        myappid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.title("EyeVee")
        self.iconbitmap('C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\eye-logo2.ico')
        self.geometry(f"{1440}x{820}")
        self.minsize(1200,600)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------
        # IMAGES

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

        #self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "eye-logo1.png")), size=(50, 26))

        self.logo_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "eye-logo1.png")),
                                                   dark_image=Image.open(os.path.join(image_path, "eye-logo1.png")),
                                                   size=(50, 26))

        self.eyevee_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "blinklul.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "blinklul.png")), size=(20, 20))
        self.twentyrule_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "20_logo.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "20_logo.png")),
                                                 size=(20, 20))
        self.stats_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "stats.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "stats.png")), size=(20, 20))
        self.info_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "i_logo.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "i_logo.png")), size=(20, 20))
        self.dots_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "..._logo.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "..._logo.png")), size=(20, 20))
        self.wheel_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "wheel.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "wheel.png")), size=(20, 20))

        # eyevee page
        self.header_eyevee_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_eyevee_image.png")),
                                                       size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        # 20-20-20 rule page
        self.header_20rule_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_20rule_image.png")),
                                                       size=(500, 150))

        # Blink rate stats page
        self.header_stats_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_stats_image.png")),
                                                        size=(500, 150))

        # info page
        self.header_info_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_info_image.png")),
                                                       size=(500, 150))

        # additional page
        self.header_additional_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_additional_image.png")),
                                                       size=(500, 150))
        self.share_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "share_icon.png")),
                                                        size=(20, 20))
        self.feedback_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "feedback_icon.png")),
                                                        size=(20, 20))

        # Settings page Header
        self.header_settings_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_settings_image.png")),
                                                       size=(500, 150))

        # Monitor Settings page
        self.monitorSettings_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "monitorblank.png")),
                                                       size=(20, 20))

        # Monitor Settings page Header
        self.header_monitorSettings_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_monitorSettings_image.png")),
                                                        size=(500, 150))

        self.header_EyeVee_Settings = customtkinter.CTkImage(Image.open(os.path.join(image_path, "header_EyeVee_Settings.png")),
                                                        size=(333, 100))

        # IMAGES
        #-----------------------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------------------
        # NAVIGATION FRAME ON THE LEFT CORNER

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1) #spacing

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  EyeVee",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="EyeVee",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.eyevee_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="20-20-20 Rule",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.twentyrule_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Blink Rate",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.stats_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_7_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Monitor Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.monitorSettings_icon, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=4, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="More Info",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.info_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=5, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Additional",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.dots_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=6, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.wheel_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=7, column=0, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(self.navigation_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.navigation_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

        # NAVIGATION FRAME ON THE LEFT CORNER
        # -----------------------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------------------
        # MAIN FRAME CONTENT

        # 1st create home frame (EyeVee)
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(5, weight=1)


        self.home_frame_header_eyevee_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.header_eyevee_image)
        self.home_frame_header_eyevee_image_label.grid(row=0, column=0, padx=20, pady=10)
        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.home_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame, text="Turn on the EyeVee system:", font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")

        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame, corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.eyeVee_start_button = customtkinter.CTkButton(self.switch_frame2, text="Start",
                                                               fg_color="green",
                                                               hover_color="#006400",
                                                               compound="left",
                                                               #command=lambda: [self.start_countdown()],
                                                               font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: [threading.Thread(target = self.eyeblink_window, daemon=True).start(), self.change_start_eyevee()])
        self.eyeVee_start_button.grid(row=3, column=0, padx=20, pady=10)

        self.eyeVee_stop_button = customtkinter.CTkButton(self.switch_frame2, text="Stop",
                                                              fg_color="red",
                                                              hover_color="#8B0000",
                                                              compound="left",
                                                              #command=lambda: self.stop_countdown(),
                                                              font=customtkinter.CTkFont(size=15, weight="bold"),
                                                          command=lambda: [threading.Thread(target =self.stop_EyeVee_system).start(), self.change_stop_eyevee()])
        self.eyeVee_stop_button.grid(row=3, column=1, padx=20, pady=10)

        self.eyeVee_label = customtkinter.CTkLabel(master=self.switch_frame,
                                                  text="Click 'Start' to begin",
                                                  font=customtkinter.CTkFont(size=20))
        self.eyeVee_label.grid(row=5, column=0, columnspan=1, padx=10, pady=10, sticky="")

        self.switch_frame3 = customtkinter.CTkFrame(self.home_frame)
        self.switch_frame3.grid(row=6, column=0, padx=(20, 20), pady=(20, 0), sticky="nsw")
        self.switch_frame3.grid_rowconfigure(6, weight=1)

        self.switch_frame3_header_EyeVee_Settings = customtkinter.CTkLabel(self.switch_frame3, text="",
                                                                           image=self.header_EyeVee_Settings)
        self.switch_frame3_header_EyeVee_Settings.grid(row=7, column=0, padx=20, pady=10, sticky="n")

        self.switch_frame5 = customtkinter.CTkFrame(self.switch_frame3, corner_radius=0, fg_color="transparent")
        self.switch_frame5.grid(row=8, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.switch_frame5.grid_rowconfigure(0, weight=1)

        self.every_minutes_label = customtkinter.CTkLabel(self.switch_frame5, text="Notify every __ minutes.")
        self.every_minutes_label.grid(row=8, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["1", "2", "3", "4", "5"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_1.grid(row=8, column=1, padx=20, pady=(20, 10))

        self.notify_when_label = customtkinter.CTkLabel(self.switch_frame5, text="Notify when blink rate is low than __ per minute.")
        self.notify_when_label.grid(row=9, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["10", "11", "12", "13", "14", "15"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_2.grid(row=9, column=1, padx=20, pady=(20, 10))

        self.ratio_eye_label = customtkinter.CTkLabel(self.switch_frame5,
                                                        text="Eye Aspect Ratio(To detect the eyeblink)")
        self.ratio_eye_label.grid(row=10, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["32", "33", "34", "35", "36", "37"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_3.grid(row=10, column=1, padx=20, pady=(20, 10))

        self.eyeVee_apply_button = customtkinter.CTkButton(self.switch_frame3, text="Apply",
                                                          compound="left",
                                                          command=lambda: self.eyeveePage_popup_apply(),
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.eyeVee_apply_button.grid(row=11, column=0, padx=20, pady=10, sticky="s")

        self.switch_frame4 = customtkinter.CTkFrame(self.home_frame)
        self.switch_frame4.grid(row=6, column=0, padx=(20, 20), pady=(20, 0), sticky="se")
        self.switch_frame4.grid_rowconfigure(9, weight=1)

        self.apply_label = customtkinter.CTkLabel(self.switch_frame4, text="Test your camera",
                                                            font=customtkinter.CTkFont(size=20))
        self.apply_label.grid(row=9, column=1, padx=20, pady=10, sticky="e")

        self.eyeVee_apply_button = customtkinter.CTkButton(master=self.switch_frame4, text="Test (demo)",
                                                           compound="left",
                                                           # command=lambda: self.stop_countdown(),
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: threading.Thread(target=self.eyeblink_window_test, daemon=True).start())
        self.eyeVee_apply_button.grid(row=10, column=1, padx=20, pady=10, sticky="e")

        #settings default values
        self.optionmenu_1.set("1")
        self.optionmenu_2.set("12")
        self.optionmenu_3.set("35")

        # ---------------------------------------------------------------------------------------------------------------------------

        # 2nd Frame Content
        # create second frame (20-20-20 Rule)
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                     image=self.header_20rule_image)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.second_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame,
                                                         text="Every 20 minute,\nShift your eyes to look at an object at least 20 feet away,\nFor at least 20 seconds.",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")

        '''self.rule20_switch = customtkinter.CTkSwitch(master=self.switch_frame, font=customtkinter.CTkFont(size=15, weight="bold"),
                                                     command=lambda: self.after(1, self.twentyRule_notify()),progress_color="green", border_width=0.1)
        self.rule20_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")'''

        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame, corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.twentyRule_start_button = customtkinter.CTkButton(self.switch_frame2, text="Start",
                                                               fg_color="green",
                                                               hover_color="#006400",
                                                               compound="left",
                                                               command=lambda: [self.start_countdown()],
                                                               font=customtkinter.CTkFont(size=15, weight="bold"))
        self.twentyRule_start_button.grid(row=3, column=0, padx=20, pady=10)

        self.twentyRule_stop_button = customtkinter.CTkButton(self.switch_frame2, text="Stop",
                                                              fg_color="red",
                                                              hover_color="#8B0000",
                                                              compound="left",
                                                              command=lambda: self.stop_countdown(),
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.twentyRule_stop_button.grid(row=3, column=1, padx=20, pady=10)

        self.timer_label = customtkinter.CTkLabel(master=self.switch_frame,
                                                  text="Click 'Start' to begin countdown",
                                                  font=customtkinter.CTkFont(size=20))
        self.timer_label.grid(row=4, column=0, columnspan=1, padx=10, pady=10, sticky="")

        # 2nd Frame Content
        # ---------------------------------------------------------------------------------------------------------------------------

        # 3rd Frame Content (blink rate stats)
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.header_stats_image)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.third_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame, text="Click one of the time periods below to review your blink rate statistics.\n"
                                                                                        "You should aim to blink at least 12 times per minute.",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        '''
        self.rule20_switch = customtkinter.CTkSwitch(master=self.switch_frame, text="On/Off Switch")
        self.rule20_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        '''

        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame,corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        # Creating 4 buttons
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  EyeVee", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))

        self.third_frame_button_1 = customtkinter.CTkButton(self.switch_frame2, text="Today", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: self.widgets_today())
        self.third_frame_button_1.grid(row=4, column=0, padx=20, pady=10)
        self.third_frame_button_2 = customtkinter.CTkButton(self.switch_frame2, text="Weekly", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: self.widgets_weekly())
        self.third_frame_button_2.grid(row=4, column=1, padx=20, pady=10)
        self.third_frame_button_3 = customtkinter.CTkButton(self.switch_frame2, text="Monthly", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: self.widgets_monthly())
        self.third_frame_button_3.grid(row=4, column=2, padx=20, pady=10)
        self.third_frame_button_4 = customtkinter.CTkButton(self.switch_frame2, text="Yearly", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command=lambda: self.widgets_yearly())
        self.third_frame_button_4.grid(row=4, column=3, padx=20, pady=10)
        '''self.third_frame_button_5 = customtkinter.CTkButton(self.switch_frame2, text="All-Time", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.third_frame_button_5.grid(row=4, column=4, padx=20, pady=10)'''

        # 3th
# ---------------------------------------------------------------------------------------------------------------------------
        # 7th create seventh frame (Monitor Settings)
        self.seventh_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.seventh_frame.grid_columnconfigure(0, weight=1)

        self.seventh_frame_large_image_label = customtkinter.CTkLabel(self.seventh_frame, text="", image=self.header_monitorSettings_image)
        self.seventh_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        # create switch frame1
        self.switch_frame = customtkinter.CTkFrame(self.seventh_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame,
                                                         text="Adjust Brightness",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        # create switch frame1
        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame, corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        # Slider Brightness
        self.label_brightness = customtkinter.CTkLabel(self.switch_frame2, text="Brightness: ",
                                               font=("Helvetica", 18))
        self.label_brightness.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # SLIDER
        self.my_slider = customtkinter.CTkSlider(self.switch_frame2,
                                                 from_=0, to=100,
                                                 command=self.sliding_Brightness,
                                                 progress_color="yellow",
                                                 )
        self.my_slider.grid(row=4, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
        # Define starting point
        self.my_slider.set(20)
        #Label Slider
        self.my_label = customtkinter.CTkLabel(self.switch_frame2, text=self.my_slider.get(),
                                               font=("Helvetica", 18))
        self.my_label.grid(row=4, column=2, padx=(20, 10), pady=(10, 10), sticky="ew")
        # Slider Contrast
        self.label2_contrast = customtkinter.CTkLabel(self.switch_frame2, text="Contrast: ",
                                                       font=("Helvetica", 18))
        self.label2_contrast.grid(row=5, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # Slider
        self.my_slider2 = customtkinter.CTkSlider(self.switch_frame2,
                                                 from_=0, to=100,
                                                 command=self.sliding_Contrast,
                                                 progress_color="red",
                                                 )
        self.my_slider2.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
        # Define starting point
        self.my_slider2.set(50)
        # Label Slider
        self.my_label2 = customtkinter.CTkLabel(self.switch_frame2, text=self.my_slider2.get(),
                                               font=("Helvetica", 18))
        self.my_label2.grid(row=5, column=2, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.third_frame_button_1 = customtkinter.CTkButton(self.switch_frame, text="Apply",
                                                             compound="left", command= lambda: self.change_monitor_settings(),
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.third_frame_button_1.grid(row=6, column=0, padx=20, pady=10)
        # 7th frame
        # ---------------------------------------------------------------------------------------------------------------------------
        # 4th Frame Content (info)
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(0, weight=1)

        self.fourth_frame_large_image_label = customtkinter.CTkLabel(self.fourth_frame, text="", image=self.header_info_image)
        self.fourth_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.fourth_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame, text="Here, under the 'Information' tab, we provide a link to articles that we believe will help you\navoid eye strain and maintain the health of your eyes when using the computer.",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        '''
        self.rule20_switch = customtkinter.CTkSwitch(master=self.switch_frame, text="On/Off Switch")
        self.rule20_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        '''

        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame,corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        # Creating 4 buttons

        self.fourth_frame_button_1 = customtkinter.CTkButton(self.switch_frame2, text="Eye Monitor Height/Distance",
                                                             image=self.feedback_icon, compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             command= lambda: self.eye_monitor_setup())
        self.fourth_frame_button_1.grid(row=3, column=0, padx=20, pady=10)
        self.fourth_frame_button_2 = customtkinter.CTkButton(self.switch_frame2, text="Eye Exercises",
                                                             image=self.feedback_icon, compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             command= lambda: self.eye_exercises())
        self.fourth_frame_button_2.grid(row=4, column=1, padx=20, pady=10)
        self.fourth_frame_button_3 = customtkinter.CTkButton(self.switch_frame2, text="Proper Lighting",
                                                             image=self.feedback_icon, compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             command= lambda: self.eye_proper_lighting())
        self.fourth_frame_button_3.grid(row=3, column=2, padx=20, pady=10)
        self.fourth_frame_button_4 = customtkinter.CTkButton(self.switch_frame2, text="Do Blue-Light Glasses Help with Eyestrain?",
                                                             image=self.feedback_icon, compound="left",
                                                             command=lambda: self.blue_light_glasses_article(),
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.fourth_frame_button_4.grid(row=4, column=3, padx=20, pady=10)

        # ---------------------------------------------------------------------------------------------------------------------------

        # 5th Frame Content (Additional)
        self.fifth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fifth_frame.grid_columnconfigure(0, weight=1)

        self.fifth_frame_large_image_label = customtkinter.CTkLabel(self.fifth_frame, text="",  image=self.header_additional_image)
        self.fifth_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.fifth_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame, text="Here, under the 'Additional' tab, we would be very grateful\nfor your support to share and send us your feedback.\nThank You!!",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        '''
        self.rule20_switch = customtkinter.CTkSwitch(master=self.switch_frame, text="On/Off Switch")
        self.rule20_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        '''
        # Creating 4 buttons
        self.fifth_frame_button_1 = customtkinter.CTkButton(self.switch_frame, text="Share this Software", image=self.share_icon, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command= lambda: self.share_link())
        self.fifth_frame_button_1.grid(row=3, column=0, padx=20, pady=10)
        self.fifth_frame_button_2 = customtkinter.CTkButton(self.switch_frame, text="Send your Feedback", image=self.feedback_icon, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                            command= lambda: self.feedback_link())
        self.fifth_frame_button_2.grid(row=4, column=0, padx=20, pady=10)

        # ---------------------------------------------------------------------------------------------------------------------------

        # 6th create sixth frame (settings)
        self.sixth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sixth_frame.grid_columnconfigure(0, weight=1)
        self.sixth_frame.grid_rowconfigure(5, weight=1)

        self.sixth_frame_large_image_label = customtkinter.CTkLabel(self.sixth_frame, text="", image=self.header_settings_image)
        self.sixth_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create switch button frame
        self.switch_frame = customtkinter.CTkFrame(self.sixth_frame)
        self.switch_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.switch_frame2 = customtkinter.CTkFrame(self.switch_frame, corner_radius=0, fg_color="transparent")
        self.switch_frame2.grid(row=6, column=0, padx=(20, 20), pady=(20, 0), sticky="nsw")
        self.switch_frame2.grid_rowconfigure(6, weight=1)

        # words at the top (just in case)
        '''self.switch_frame_group = customtkinter.CTkLabel(master=self.switch_frame, text="Settings lul",
                                                         font=customtkinter.CTkFont(size=15))
        self.switch_frame_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")'''

        # ---------------------------------------------------------------------------------------------------------------------------
        # settings

        self.reminder_ringtone_label = customtkinter.CTkLabel(self.switch_frame2, text="Reminder ringtone")
        self.reminder_ringtone_label.grid(row=8, column=0, padx=20, pady=10, sticky="sw")

        self.settings_optionmenu_1 = customtkinter.CTkOptionMenu(self.switch_frame2, dynamic_resizing=False,
                                                        values=["Default", "SMS", "Mail", "LoopingAlarm2"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.settings_optionmenu_1.grid(row=8, column=1, padx=20, pady=(20, 10))

        self.play_sound_only_label = customtkinter.CTkLabel(self.switch_frame2,
                                                        text="Play sound only (recommended for gaming)")
        self.play_sound_only_label.grid(row=9, column=0, padx=20, pady=10, sticky="sw")

        self.settings_optionmenu_2 = customtkinter.CTkOptionMenu(self.switch_frame2, dynamic_resizing=False,
                                                        values=["Enable", "Disable"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.settings_optionmenu_2.grid(row=9, column=1, padx=20, pady=(20, 10))

        self.only_notify_label = customtkinter.CTkLabel(self.switch_frame2,
                                                      text="Only notify if blink rate is low (please enable if play sound only is enabled)")
        self.only_notify_label.grid(row=10, column=0, padx=20, pady=10, sticky="sw")

        self.settings_optionmenu_3 = customtkinter.CTkOptionMenu(self.switch_frame2, dynamic_resizing=False,
                                                        values=["Enable", "Disable"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.settings_optionmenu_3.grid(row=10, column=1, padx=20, pady=(20, 10))

        self.settings_apply_button = customtkinter.CTkButton(self.switch_frame, text="Apply",
                                                           compound="left",
                                                           command=lambda: self.settingsPage_popup_apply(),
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        self.settings_apply_button.grid(row=11, column=0, padx=20, pady=10, sticky="s")

        self.settings_optionmenu_1.set("Default")
        self.settings_optionmenu_2.set("Disable")
        self.settings_optionmenu_3.set("Enable")

        # settings
        # ---------------------------------------------------------------------------------------------------------------------------
        # EyeVee settings

        '''self.switch_frame3 = customtkinter.CTkFrame(self.sixth_frame)
        self.switch_frame3.grid(row=6, column=0, padx=(20, 20), pady=(20, 0), sticky="nsw")
        self.switch_frame3.grid_rowconfigure(6, weight=1)

        self.switch_frame3_header_EyeVee_Settings = customtkinter.CTkLabel(self.switch_frame3, text="",
                                                                           image=self.header_EyeVee_Settings)
        self.switch_frame3_header_EyeVee_Settings.grid(row=7, column=0, padx=20, pady=10, sticky="n")

        self.switch_frame5 = customtkinter.CTkFrame(self.switch_frame3, corner_radius=0, fg_color="transparent")
        self.switch_frame5.grid(row=8, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.switch_frame5.grid_rowconfigure(0, weight=1)

        self.every_minutes_label = customtkinter.CTkLabel(self.switch_frame5, text="Notify every __ minutes")
        self.every_minutes_label.grid(row=8, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["1", "2", "3", "4", "5"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_1.grid(row=8, column=1, padx=20, pady=(20, 10))

        self.notify_when_label = customtkinter.CTkLabel(self.switch_frame5,
                                                        text="Notify when blink rate is low than __ per minute")
        self.notify_when_label.grid(row=9, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["10", "11", "12", "13", "14", "15"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_2.grid(row=9, column=1, padx=20, pady=(20, 10))

        self.ratio_eye_label = customtkinter.CTkLabel(self.switch_frame5,
                                                      text="Eye Aspect Ratio(To detect the eyeblink)")
        self.ratio_eye_label.grid(row=10, column=0, padx=20, pady=10, sticky="sw")

        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.switch_frame5, dynamic_resizing=False,
                                                        values=["32", "33", "34", "35", "36", "37"],
                                                        button_color="darkgray",
                                                        fg_color="gray",
                                                        button_hover_color="black")
        self.optionmenu_3.grid(row=10, column=1, padx=20, pady=(20, 10))

        self.eyeVee_apply_button = customtkinter.CTkButton(self.switch_frame3, text="Apply",
                                                           compound="left",
                                                           command=lambda: self.window_popup_apply(),
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        self.eyeVee_apply_button.grid(row=11, column=0, padx=20, pady=10, sticky="s")

        # settings default values
        self.optionmenu_1.set("1")
        self.optionmenu_2.set("12")
        self.optionmenu_3.set("35")'''

        # MAIN FRAME CONTENT
        # ---------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------------------

        # set default frame (EyeVee)
        self.select_frame_by_name("home")
        # set default values for scaling
        self.scaling_optionemenu.set("100%")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")
        self.frame_7_button.configure(fg_color=("gray75", "gray25") if name == "frame_7" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()
        if name == "frame_6":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()
        if name == "frame_7":
            self.seventh_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.seventh_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")

    def frame_6_button_event(self):
        self.select_frame_by_name("frame_6")

    def frame_7_button_event(self):
        self.select_frame_by_name("frame_7")
    # change appearance mode function
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

     #change the scaling function
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # ------------------------------------------------------------------------------------------------------------------------
    # EyeVee page Apply button
    def eyeveePage_popup_apply(self):
        self.optionmenu_1.set(self.optionmenu_1.get())
        self.optionmenu_2.set(self.optionmenu_2.get())
        self.optionmenu_3.set(self.optionmenu_3.get())
        self.popup = messagebox.showinfo("EyeVee", "New settings has been applied")

    # ------------------------------------------------------------------------------------------------------------------------
    # Settings page Apply button
    def settingsPage_popup_apply(self):
        self.settings_optionmenu_1.set(self.settings_optionmenu_1.get())
        self.settings_optionmenu_2.set(self.settings_optionmenu_2.get())
        self.settings_optionmenu_3.set(self.settings_optionmenu_3.get())
        self.popup = messagebox.showinfo("EyeVee", "New settings has been applied")
    # ------------------------------------------------------------------------------------------------------------------------
    # Monitor settings

    # change the Switch from ON/OFF
    def switches1(self):
        self.switch_var1.get()

    # change the Switch from ON/OFF
    def switches2(self):
        self.switch_var2.get()

    # For getting Slider value
    def sliding_Brightness(self, value):
        self.my_label.configure(text=int(value))

    # For getting Slider value
    def sliding_Contrast(self, value):
        self.my_label2.configure(text=int(value))

    #Run MonitorSettings.py
    def change_monitor_settings(self):
        monitor_settings = main(self, brightness=self.my_label.cget("text"), contrast=self.my_label2.cget("text"))

    #Monitor settings
    #------------------------------------------------------------------------------------------------------------------------
    # Countdown methods
    def countdown(self):
        global running
        while running:
            for i in range(1200, 0, -1):
                if not running:
                    break
                minutes, seconds = divmod(i, 60)
                self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                #self.timer_label.configure(text=f"Time left: {i} seconds")
                time.sleep(1)
            if running:
                self.timer_label.configure(text="Time's Up!\nRest for 20 seconds")
                toast = Notification(app_id="EyeVee",
                                     title="20-20-20 Rule",
                                     msg="20 minutes has passed, \nPlease look at an object 20 feet away(6 meters) for 20 seconds.",
                                     duration= "long",
                                     icon="C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\20_logo2.png")
                toast.set_audio(audio.LoopingAlarm2, loop=False)
                toast.add_actions(label="Got it")
                toast.show()
                time.sleep(20)

    def start_countdown(self):
        global running, timer_thread
        running = False
        timer_thread = None
        if not running:
            running = True
            timer_thread = threading.Thread(target=self.countdown)
            timer_thread.start()

    def stop_countdown(self):
        global running, timer_thread
        running = False
        timer_thread = None
        running = False
        self.timer_label.configure(text="Timer Stopped")

    def on_closing(self):
        if running:
            self.stop_countdown()
        self.destroy()
    # Countdown methods
    # ------------------------------------------------------------------------------------------------------------------------
    # Change label for EyeVee system
    def change_start_eyevee(self):
        self.eyeVee_label.configure(text="EyeVee system started")

    def change_stop_eyevee(self):
        self.eyeVee_label.configure(text="EyeVee system stopped")
    # Change label for EyeVee system
    # ------------------------------------------------------------------------------------------------------------------------
    # links

    def eye_monitor_setup(self):
        webbrowser.open("https://www.urmc.rochester.edu/encyclopedia/content.aspx?contenttypeid=85&contentid=P00516")

    def eye_exercises(self):
        webbrowser.open("https://www.webmd.com/eye-health/best-exercises-eye-strain")

    def eye_proper_lighting(self):
        webbrowser.open("https://www.benq.com/en-us/knowledge-center/knowledge/shedding-light-on-eye-strain--10-expert-tips-to-perfect-your-hom.html")

    def blue_light_glasses_article(self):
        webbrowser.open("https://axonoptics.com/blogs/post/do-blue-light-glasses-work-a-science-based-analysis")

    def share_link(self):
        self.popup = messagebox.showerror(title="Coming Soon", message="EyeVee will be available in the near future")

    def feedback_link(self):
        webbrowser.open("https://forms.gle/hWKiL39SBhFc3RJz8")
    # links

    #for graph
    def widgets_today(self):
        self.fig1, self.ax1 = plt.subplots(dpi=100, facecolor = '#2b2b2b')
        self.ax1.set_facecolor('#2b2b2b')
        self.line, = self.ax1.plot(list(blink_data_today.keys()), list(blink_data_today.values()), 'aqua', marker = 'o', linewidth = 2)

        self.ax1.grid(alpha = 0.2)
        self.ax1.set_title("Today's Blink Rate Statistics", color='white', size=15, weight="bold")
        self.ax1.set_xlabel('Minutes', color='white', size=15)
        self.ax1.set_ylabel('Blink Rate', color='white', size=15)
        self.ax1.tick_params(color = 'white', labelcolor = 'white', length = 6, width = 2)
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['left'].set_color('white')

        FigureCanvasTkAgg(self.fig1, master= self.third_frame).get_tk_widget().grid(row = 5, column = 0, padx = 0, pady = 20)

# ------------------------------------------------------------------------------------------------------------------------

    def widgets_weekly(self):
        self.fig1, self.ax1 = plt.subplots(dpi=100, facecolor = '#2b2b2b')
        self.ax1.set_facecolor('#2b2b2b')
        self.line, = self.ax1.plot(list(blink_data_weekly.keys()), list(blink_data_weekly.values()), 'aqua', marker = 'o', linewidth = 2)

        self.ax1.grid(alpha = 0.2)
        self.ax1.set_title("Weekly Blink Rate Statistics", color='white', size=15, weight="bold")
        self.ax1.set_xlabel('Day', color='white', size=15)
        self.ax1.set_ylabel('Average Blink Rate', color='white', size=15)
        self.ax1.tick_params(color = 'white', labelcolor = 'white', length = 6, width = 2)
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['left'].set_color('white')

        FigureCanvasTkAgg(self.fig1, master= self.third_frame).get_tk_widget().grid(row = 5, column = 0, padx = 0, pady = 20)

    def widgets_monthly(self):
        self.fig1, self.ax1 = plt.subplots(dpi=100, facecolor = '#2b2b2b')
        self.ax1.set_facecolor('#2b2b2b')
        self.line, = self.ax1.plot(list(blink_data_monthly.keys()), list(blink_data_monthly.values()), 'aqua', marker = 'o', linewidth = 2)

        self.ax1.grid(alpha = 0.2)
        self.ax1.set_title("Monthly Blink Rate Statistics", color='white', size=15, weight="bold")
        self.ax1.set_xlabel('Day', color='white', size=15)
        self.ax1.set_ylabel('Average Blink Rate', color='white', size=15)
        self.ax1.tick_params(color = 'white', labelcolor = 'white', length=6, width=2)
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['left'].set_color('white')

        FigureCanvasTkAgg(self.fig1, master= self.third_frame).get_tk_widget().grid(row = 5, column = 0, padx = 0, pady = 20)

    def widgets_yearly(self):
        self.fig1, self.ax1 = plt.subplots(dpi=100, facecolor = '#2b2b2b')
        self.ax1.set_facecolor('#2b2b2b')
        self.line, = self.ax1.plot(list(blink_data_yearly.keys()), list(blink_data_yearly.values()), 'aqua', marker = 'o', linewidth = 2)

        self.ax1.grid(alpha = 0.2)
        self.ax1.set_title("Yearly Blink Rate Statistics", color='white', size=15, weight="bold")
        self.ax1.set_xlabel('Month', color='white', size=15)
        self.ax1.set_ylabel('Average Blink Rate', color='white', size=15)
        self.ax1.tick_params(color = 'white', labelcolor = 'white', length=6, width=2)
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['left'].set_color('white')

        FigureCanvasTkAgg(self.fig1, master= self.third_frame).get_tk_widget().grid(row = 5, column = 0, padx = 0, pady = 20)
# Graph
# ------------------------------------------------------------------------------------------------------------------------

    #to stop the EyeVee system
    def stop_EyeVee_system(self):
        cv2.destroyAllWindows()

    # ------------------------------------------------------------------------------------------------------------------------
    # EyeVee Window
    def eyeblink_window(self):

        cap = cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1)
        plotY = LivePlot(640, 360, [20, 50], invert=True)

        idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        ratioList = []
        counter = 0
        blinkCounter = 0

        minutesSetup = int(self.optionmenu_1.get())
        blinkSetup = int(self.optionmenu_2.get())
        eyeAspectRatio = int(self.optionmenu_3.get())
        ringtoneSettings = self.settings_optionmenu_1.get()
        playSoundOnlySettings = self.settings_optionmenu_2.get()
        onlyNotifyifLow = self.settings_optionmenu_3.get()

        totalminutestoday = 0
        day = ""

        color = (255, 0, 255)

        starting_time = time.time()
        maximum_time = minutesSetup * 10  # Change the value to 60 after finished prototyping

        # File path for storing the data
        file_path = "blink_data.py"

        # Function to read data from the .py file
        def read_data(file_path):
            import blink_data
            return {
                "blink_data_today": blink_data.blink_data_today,
                "blink_data_weekly": blink_data.blink_data_weekly,
                "blink_data_monthly": blink_data.blink_data_monthly,
                "blink_data_yearly": blink_data.blink_data_yearly
            }

        # Function to write data to the .py file
        def write_data(file_path, data):
            with open(file_path, "w") as file:
                file.write("blink_data_today = " + str(data["blink_data_today"]) + "\n\n")
                file.write("blink_data_weekly = " + str(data["blink_data_weekly"]) + "\n\n")
                file.write("blink_data_monthly = " + str(data["blink_data_monthly"]) + "\n\n")
                file.write("blink_data_yearly = " + str(data["blink_data_yearly"]) + "\n")

        def getalldata():
            # Update the blink_data_today
            data["blink_data_today"].update({totalminutestoday: blinkCounter})
            '''new_blink_data_today = {totalminutestoday: blinkCounter}
            data["blink_data_today"] = new_blink_data_today'''

            # Getting average blink rate per month
            average_blink_today = sum(data["blink_data_today"].values()) / len(data["blink_data_today"])
            # Update the blink_data_weekly
            data["blink_data_weekly"].update({current_day: average_blink_today})

            # Update the blink_data_monthly
            current_day_of_month = datetime.datetime.now().strftime("%d").lstrip('0')
            data["blink_data_monthly"].update({current_day_of_month: average_blink_today})

        # Read the existing data
        data = read_data(file_path)

        def defaultsound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\Defaultaudio.mp3")

        def smssound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\SMS.mp3")

        def mailsound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\Mail.mp3")

        def loopingalarm2sound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\LoopingAlarm2.mp3")

        def windowsnotificationKeepitup():
            if (playSoundOnlySettings == "Disable"):
                average_blink = blinkCounter // minutesSetup
                toast = Notification(app_id="EyeVee",
                                     title="Keep it up!",
                                     msg=f"Your blink rate per minute is {average_blink}!\nTarget blink rate per minute => {blinkSetup}.",
                                     duration="long",
                                     icon="C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\eyeblink.gif")
                # Condition for ringtone Settings
                if (ringtoneSettings == "Default"):
                    toast.set_audio(audio.Default, loop=False)
                elif (ringtoneSettings == "SMS"):
                    toast.set_audio(audio.SMS, loop=False)
                elif (ringtoneSettings == "Mail"):
                    toast.set_audio(audio.Mail, loop=False)
                elif (ringtoneSettings == "LoopingAlarm2"):
                    toast.set_audio(audio.LoopingAlarm2, loop=False)
                toast.show()
            else:
                if (ringtoneSettings == "Default"):
                    threading.Thread(target=defaultsound, daemon=True).start()
                elif (ringtoneSettings == "SMS"):
                    threading.Thread(target=smssound, daemon=True).start()
                elif (ringtoneSettings == "Mail"):
                    threading.Thread(target=mailsound, daemon=True).start()
                elif (ringtoneSettings == "LoopingAlarm2"):
                    threading.Thread(target=loopingalarm2sound, daemon=True).start()

        def windowsnotification():
            if (playSoundOnlySettings == "Disable"):
                average_blink = blinkCounter // minutesSetup
                self.timer_label.configure(text="Time's Up!\nRest for 20 seconds")
                toast = Notification(app_id="EyeVee",
                                     title="Blink More!",
                                     msg=f"Your blink rate per minute is {average_blink}!\nTarget blink rate per minute => {blinkSetup}.",
                                     duration="long",
                                     icon="C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\eyeblink.gif")
                # Condition for ringtone Settings
                if (ringtoneSettings == "Default"):
                    toast.set_audio(audio.Default, loop=False)
                elif (ringtoneSettings == "SMS"):
                    toast.set_audio(audio.SMS, loop=False)
                elif (ringtoneSettings == "Mail"):
                    toast.set_audio(audio.Mail, loop=False)
                elif (ringtoneSettings == "LoopingAlarm2"):
                    toast.set_audio(audio.LoopingAlarm2, loop=False)
                toast.show()
            else:
                if (ringtoneSettings == "Default"):
                    threading.Thread(target=defaultsound, daemon=True).start()
                elif (ringtoneSettings == "SMS"):
                    threading.Thread(target=smssound, daemon=True).start()
                elif (ringtoneSettings == "Mail"):
                    threading.Thread(target=mailsound, daemon=True).start()
                elif (ringtoneSettings == "LoopingAlarm2"):
                    threading.Thread(target=loopingalarm2sound, daemon=True).start()

        def putText():
            cvzone.putTextRect(imgPlot, f'Blink Counter: {blinkCounter}',
                               (60, 50),
                               2, 2,
                               colorR=color)

            # print("Elapsed time: {}".format(elapsed_time))
            cvzone.putTextRect(imgPlot, "{} seconds".format(elapsed_time), (60, 330), cv2.FONT_HERSHEY_PLAIN,
                               2, 2,
                               colorR=(250, 250, 250))

            cvzone.putTextRect(img, f'Press "z" and the close button to exit',
                               (20, 450),
                               1, 1,
                               colorR=(0, 0, 0))

        def stop_camera():
            cap.release()  # Release the camera
            cv2.destroyAllWindows()

        while True:

            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            key = cv2.waitKey(1)
            if key == ord('z'):
                break

            success, img = cap.read()
            img, faces = detector.findFaceMesh(img, draw=False)

            if faces:
                face = faces[0]
                for id in idList:
                    cv2.circle(img, face[id], 2, color, cv2.FILLED)

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]
                lenghtVer, _ = detector.findDistance(leftUp, leftDown)
                lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

                cv2.line(img, leftUp, leftDown, (0, 200, 0), 1)
                cv2.line(img, leftLeft, leftRight, (0, 200, 0), 1)

                # Calculate the EAR and append it to the list
                ratio = int((lenghtVer / lenghtHor) * 100)
                ratioList.append(ratio)

                # time operations
                elapsed_time = int(time.time() - starting_time)

                # Check if the time has elapsed the maximum time set
                if elapsed_time > maximum_time:
                    current_day = datetime.datetime.now().strftime("%A")

                    # Check if the current day is the same as the variable day
                    if (day == current_day):
                        totalminutestoday += 1
                        getalldata()
                    else:
                        data["blink_data_today"].clear()
                        day = current_day
                        totalminutestoday = 1
                        new_blink_data_today = {totalminutestoday: blinkCounter}
                        data["blink_data_today"] = new_blink_data_today

                    # Check the blink counter more than or less than the target blink rate, (notification always on)
                    if (blinkCounter >= blinkSetup * minutesSetup and onlyNotifyifLow == "Disable"):  # notify if blink rate is normal and enable notification
                        windowsnotificationKeepitup()
                    elif (blinkCounter < blinkSetup * minutesSetup and onlyNotifyifLow == "Disable"):  # notify if blink rate is lower and enable notification
                        windowsnotification()

                    # Check the blink counter more than target blink rate, (notification disable if the blink rate is normal)
                    elif (blinkCounter >= blinkSetup * minutesSetup and onlyNotifyifLow == "Enable"):  # if blink rate is normal and disable notification (if blink rate is normal)
                        pass
                    else:
                        windowsnotification()

                    #Reset all the blinkCounter and starting_time, Write data to blink_data.py
                    starting_time = time.time()
                    blinkCounter = 0
                    write_data(file_path, data)

                # Checking the length of ratioList
                if len(ratioList) > 3:
                    ratioList.pop(0)
                # Calculating the average
                ratioAvg = int(sum(ratioList) / len(ratioList))

                # Check if the ratioAvg is greater than EAR that has been set, counter is for changing the color
                if ratioAvg < eyeAspectRatio and counter == 0:
                    blinkCounter += 1
                    color = (0, 0, 200)
                    counter = 1
                if counter != 0:
                    counter += 1
                    if counter > 10:
                        counter = 0
                        color = (300, 0, 0)

                imgPlot = plotY.update(ratioAvg, color)

                putText()

                img = cv2.resize(img, (640, 360))
                imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
            else:
                img = cv2.resize(img, (640, 360))
                cvzone.putTextRect(img,
                                   f'No Camera/Face found',
                                   (10, 50))
                print("No Camera/Face found")
                imgStack = cvzone.stackImages([img], 2, 1)

            #cv2.imshow("EyeVee", imgStack)
            cv2.waitKey(25)

    # EyeBlink Window
    # ------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------
#EyeVee Window for testing
    def eyeblink_window_test(self):

        cap = cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1)
        plotY = LivePlot(640, 360, [20, 50], invert=True)

        idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        ratioList = []
        counter = 0
        blinkCounter = 0

        minutesSetup = int(self.optionmenu_1.get())
        blinkSetup = int(self.optionmenu_2.get())
        eyeAspectRatio = int(self.optionmenu_3.get())
        ringtoneSettings = self.settings_optionmenu_1.get()
        playSoundOnlySettings = self.settings_optionmenu_2.get()
        onlyNotifyifLow = self.settings_optionmenu_3.get()

        totalminutestoday = 0
        day = ""

        color = (255, 0, 255)

        starting_time = time.time()
        maximum_time = minutesSetup * 10  # Change the value to 60 after finished prototyping

        # File path for storing the data
        file_path = "blink_data.py"

        # Function to read data from the .py file
        def read_data(file_path):
            import blink_data
            return {
                "blink_data_today": blink_data.blink_data_today,
                "blink_data_weekly": blink_data.blink_data_weekly,
                "blink_data_monthly": blink_data.blink_data_monthly,
                "blink_data_yearly": blink_data.blink_data_yearly
            }

        # Function to write data to the .py file
        def write_data(file_path, data):
            with open(file_path, "w") as file:
                file.write("blink_data_today = " + str(data["blink_data_today"]) + "\n\n")
                file.write("blink_data_weekly = " + str(data["blink_data_weekly"]) + "\n\n")
                file.write("blink_data_monthly = " + str(data["blink_data_monthly"]) + "\n\n")
                file.write("blink_data_yearly = " + str(data["blink_data_yearly"]) + "\n")

        def getalldata():
            # Update the blink_data_today
            data["blink_data_today"].update({totalminutestoday: blinkCounter})
            '''new_blink_data_today = {totalminutestoday: blinkCounter}
            data["blink_data_today"] = new_blink_data_today'''

            # Getting average blink rate per month
            average_blink_today = sum(data["blink_data_today"].values()) / len(data["blink_data_today"])
            # Update the blink_data_weekly
            data["blink_data_weekly"].update({current_day: average_blink_today})

            # Update the blink_data_monthly
            current_day_of_month = datetime.datetime.now().strftime("%d").lstrip('0')
            data["blink_data_monthly"].update({current_day_of_month: average_blink_today})

        # Read the existing data
        data = read_data(file_path)

        def defaultsound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\Defaultaudio.mp3")

        def smssound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\SMS.mp3")

        def mailsound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\Mail.mp3")

        def loopingalarm2sound():
            playsound("C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\audio_notification\\LoopingAlarm2.mp3")

        def windowsnotificationKeepitup():
            if (playSoundOnlySettings == "Disable"):
                average_blink = blinkCounter // minutesSetup
                toast = Notification(app_id="EyeVee",
                                     title="Keep it up!",
                                     msg=f"Your blink rate per minute is {average_blink}!\nTarget blink rate per minute => {blinkSetup}.",
                                     duration="long",
                                     icon="C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\eyeblink.gif")
                # Condition for ringtone Settings
                if (ringtoneSettings == "Default"):
                    toast.set_audio(audio.Default, loop=False)
                elif (ringtoneSettings == "SMS"):
                    toast.set_audio(audio.SMS, loop=False)
                elif (ringtoneSettings == "Mail"):
                    toast.set_audio(audio.Mail, loop=False)
                elif (ringtoneSettings == "LoopingAlarm2"):
                    toast.set_audio(audio.LoopingAlarm2, loop=False)
                toast.show()
            else:
                if (ringtoneSettings == "Default"):
                    threading.Thread(target=defaultsound, daemon=True).start()
                elif (ringtoneSettings == "SMS"):
                    threading.Thread(target=smssound, daemon=True).start()
                elif (ringtoneSettings == "Mail"):
                    threading.Thread(target=mailsound, daemon=True).start()
                elif (ringtoneSettings == "LoopingAlarm2"):
                    threading.Thread(target=loopingalarm2sound, daemon=True).start()

        def windowsnotification():
            if (playSoundOnlySettings == "Disable"):
                average_blink = blinkCounter // minutesSetup
                self.timer_label.configure(text="Time's Up!\nRest for 20 seconds")
                toast = Notification(app_id="EyeVee",
                                     title="Blink More!",
                                     msg=f"Your blink rate per minute is {average_blink}!\nTarget blink rate per minute => {blinkSetup}.",
                                     duration="long",
                                     icon="C:\\Users\\User\\PycharmProjects\\BlinkCounter2\\test_images\\eyeblink.gif")
                # Condition for ringtone Settings
                if (ringtoneSettings == "Default"):
                    toast.set_audio(audio.Default, loop=False)
                elif (ringtoneSettings == "SMS"):
                    toast.set_audio(audio.SMS, loop=False)
                elif (ringtoneSettings == "Mail"):
                    toast.set_audio(audio.Mail, loop=False)
                elif (ringtoneSettings == "LoopingAlarm2"):
                    toast.set_audio(audio.LoopingAlarm2, loop=False)
                toast.show()
            else:
                if (ringtoneSettings == "Default"):
                    threading.Thread(target=defaultsound, daemon=True).start()
                elif (ringtoneSettings == "SMS"):
                    threading.Thread(target=smssound, daemon=True).start()
                elif (ringtoneSettings == "Mail"):
                    threading.Thread(target=mailsound, daemon=True).start()
                elif (ringtoneSettings == "LoopingAlarm2"):
                    threading.Thread(target=loopingalarm2sound, daemon=True).start()

        def putText():
            cvzone.putTextRect(imgPlot, f'Blink Counter: {blinkCounter}',
                               (60, 50),
                               2, 2,
                               colorR=color)

            # print("Elapsed time: {}".format(elapsed_time))
            cvzone.putTextRect(imgPlot, "{} seconds".format(elapsed_time), (60, 330), cv2.FONT_HERSHEY_PLAIN,
                               2, 2,
                               colorR=(250, 250, 250))

            cvzone.putTextRect(img, f'Press "z" and the close button to exit',
                               (20, 450),
                               1, 1,
                               colorR=(0, 0, 0))

        def stop_camera():
            cap.release()  # Release the camera
            cv2.destroyAllWindows()

        while True:

            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            success, img = cap.read()
            img, faces = detector.findFaceMesh(img, draw=False)

            key = cv2.waitKey(1)
            if key == ord('z'):
                break

            if faces:
                face = faces[0]
                for id in idList:
                    cv2.circle(img, face[id], 2, color, cv2.FILLED)

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]
                lenghtVer, _ = detector.findDistance(leftUp, leftDown)
                lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

                cv2.line(img, leftUp, leftDown, (0, 200, 0), 1)
                cv2.line(img, leftLeft, leftRight, (0, 200, 0), 1)

                # Calculate the EAR and append it to the list
                ratio = int((lenghtVer / lenghtHor) * 100)
                ratioList.append(ratio)

                # time operations
                elapsed_time = int(time.time() - starting_time)

                # Check if the time has elapsed the maximum time set
                if elapsed_time > maximum_time:
                    current_day = datetime.datetime.now().strftime("%A")

                    # Check if the current day is the same as the variable day
                    if (day == current_day):
                        totalminutestoday += 1
                        getalldata()
                    else:
                        data["blink_data_today"].clear()
                        day = current_day
                        totalminutestoday = 1
                        new_blink_data_today = {totalminutestoday: blinkCounter}
                        data["blink_data_today"] = new_blink_data_today

                    # Check the blink counter more than or less than the target blink rate, (notification always on)
                    if (
                            blinkCounter >= blinkSetup * minutesSetup and onlyNotifyifLow == "Disable"):  # notify if blink rate is normal and enable notification
                        windowsnotificationKeepitup()
                    elif (
                            blinkCounter < blinkSetup * minutesSetup and onlyNotifyifLow == "Disable"):  # notify if blink rate is lower and enable notification
                        windowsnotification()

                    # Check the blink counter more than target blink rate, (notification disable if the blink rate is normal)
                    elif (
                            blinkCounter >= blinkSetup * minutesSetup and onlyNotifyifLow == "Enable"):  # if blink rate is normal and disable notification (if blink rate is normal)
                        pass
                    else:
                        windowsnotification()

                    # Reset all the blinkCounter and starting_time, Write data to blink_data.py
                    starting_time = time.time()
                    blinkCounter = 0
                    write_data(file_path, data)

                # Checking the length of ratioList
                if len(ratioList) > 3:
                    ratioList.pop(0)
                # Calculating the average
                ratioAvg = int(sum(ratioList) / len(ratioList))

                # Check if the ratioAvg is greater than EAR that has been set, counter is for changing the color
                if ratioAvg < eyeAspectRatio and counter == 0:
                    blinkCounter += 1
                    color = (0, 0, 200)
                    counter = 1
                if counter != 0:
                    counter += 1
                    if counter > 10:
                        counter = 0
                        color = (300, 0, 0)

                imgPlot = plotY.update(ratioAvg, color)

                putText()

                img = cv2.resize(img, (640, 360))
                imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
            else:
                img = cv2.resize(img, (640, 360))
                cvzone.putTextRect(img,
                                   f'No Camera/Face found',
                                   (10, 50))
                print("No Camera/Face found")
                imgStack = cvzone.stackImages([img], 2, 1)

            cv2.imshow("EyeVee", imgStack)
            cv2.waitKey(25)


    # EyeBlink Window for testing
    # ------------------------------------------------------------------------------------------------------------------------


_MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)

'''DEFAULT_PARAMETERS = {
    "brightness": 100,
    "contrast": 100,
    "color_preset": 9300, # 0x05: 6500K, 0x06: 7500K, 0x08: 9300K, 0x0B: user
    #"factory_color_preset": 1,
}'''

class Commands(IntFlag):
    FACTORY_RESET = 0x04
    RESET_BRIGHTNESS_CONTRAST = 0x05
    FACTORY_RESET_GEOMETRY = 0x06
    FACTORY_RESET_COLOR = 0x08
    BRIGHTNESS = 0x10 # 0-100
    CONTRAST = 0x12 # 0-100
    INPUT_SOURCE_SELECT = 0x60
    AUDIO_SPEAKER_VOLUME = 0x62
    SETTINGS = 0xb0
    OSD = 0xca
    OSD_LANG = 0xcc
    COLOR_PRESET = 0xe0 # 0x05: 6500K, 0x06: 7500K, 0x08: 9300K, 0x0B: user
    POWER_CONTROL = 0xe1

class PhysicalMonitor(Structure):
    _fields_ = [
        ('handle', HANDLE),
        ('description', WCHAR * 128)
    ]

    def __repr__(self) -> str:
        return self.description


def list_monitors():
    monitors = []

    def callback(hmonitor, hdc, lprect, lparam):
        monitors.append(HMONITOR(hmonitor))
        return True

    if not windll.user32.EnumDisplayMonitors(None, None, _MONITORENUMPROC(callback), None):
        raise WinError('EnumDisplayMonitors failed')

    physical_devices = []
    for monitor in monitors:
        # Get physical monitor count
        count = DWORD()
        if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(monitor, byref(count)):
            raise WinError()

        # Get physical monitor handles
        physical_array = (PhysicalMonitor * count.value)()
        if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(monitor, count.value, physical_array):
            raise WinError()

        physical_devices.extend(physical_array)

    return physical_devices

def close_handle(handle):
    if not windll.dxva2.DestroyPhysicalMonitor(handle):
        raise WinError()

def set_vcp_feature(monitor, code, value):
    """Sends a DDC command to the specified monitor."""
    if not windll.dxva2.SetVCPFeature(HANDLE(monitor), BYTE(code), DWORD(value)):
        raise WinError()

def parse_args(argv):
    args_dict = {}

    def _print_help_and_exit(exit_code=0):
        print("bc.py -b <brightness>")
        sys.exit(exit_code)

    try:
        opts, args = getopt.getopt(argv, "hb:", ["brightness="])
    except getopt.GetoptError:
        _print_help_and_exit(1)

    for opt, arg in opts:
        if opt == '-h':
            _print_help_and_exit()

        if opt in ("-b", "--brightness"):
            args_dict["brightness"] = int(arg)

    return args_dict

def main(argv, brightness, contrast):
    #parsed = parse_args(argv)
    #args = {**DEFAULT_PARAMETERS, **parsed}

    monitors = list_monitors()

    for monitor in monitors:
        handle = monitor.handle
        set_vcp_feature(handle, Commands.BRIGHTNESS, brightness)
        set_vcp_feature(handle, Commands.CONTRAST, contrast)
        #set_vcp_feature(handle, Commands.COLOR_PRESET, args["color_preset"])
        close_handle(handle)


if __name__ == "__main__":
    app = App()
    app.mainloop()