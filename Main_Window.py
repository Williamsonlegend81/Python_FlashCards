from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QLineEdit, QMenu, QAction, QMessageBox, QInputDialog, QPushButton, QRadioButton, QFileDialog,QLabel
from PyQt5 import uic
from Adding_Flash import SecondUI
from Display_Deck import ThirdUI
from PyQt5.QtCore import Qt
import sys
import os

my_list = []
new_list = []
due_list = []
learn_list = []
address = str(os.getcwd())
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("main_w.ui", self)

        # Load the Widgets
        self.listwidget = self.findChild(QListWidget, "listWidget")
        self.add_flash = self.findChild(QPushButton, "pushButton_2")
        self.decks = self.findChild(QPushButton, "pushButton")
        self.stats = self.findChild(QPushButton, "pushButton_3")
        self.dark_mode = self.findChild(QRadioButton, "radioButton")
        self.deck_creation = self.findChild(QPushButton, "pushButton_4")
        self.import_file = self.findChild(QPushButton, "pushButton_5")
        self.new = self.findChild(QListWidget, "listWidget_2")
        self.learn = self.findChild(QListWidget, "listWidget_3")
        self.due = self.findChild(QListWidget, "listWidget_4")
        self.timelabel = self.findChild(QLabel,"label_5")

        # Connect the radio buttons to their edit
        self.dark_mode.toggled.connect(self.toggle_theme)
        self.add_flash.clicked.connect(self.openwindow)
        self.deck_creation.clicked.connect(self.add_item)
        self.import_file.clicked.connect(self.open_directory)
        self.decks.clicked.connect(self.opendecks)

        # Adding the Items
        for index in range(self.listwidget.count()):
            my_list.append(self.listwidget.item(index).text())

        # Connect context menu event
        self.listwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget.customContextMenuRequested.connect(self.open_menu)

        # Show the App
        self.show()

        # Message Box
        if os.path.exists("check.txt")==False:
            f = open("check.txt","w")
            f.close()
        f = open("check.txt","r")
        s = f.readline()
        # print(s)
        f.close()
        if (s!='1'):
            f = open("check.txt","w")
            f.write('1')
            f.close()
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("""Here are some new features\n
    Version 1.2.0\n
    1. Duplicate FlashCard detection in folder 
    while inserting new flashcard.\n
    2. Reversed Basic Card Insertion is also 
    possible now in the Add FlashCard Window.\n
    Last updated 07 August 2024""")
            msg_box.setWindowTitle("Updates in my project")
            msg_box.setStandardButtons(QMessageBox.Ok)
            retval = msg_box.exec_()

    def open_directory(self):
        fname = str(QFileDialog.getExistingDirectory(self,"Select Directory",""))
        if fname!="":
            folder_name = fname.split('/')[-1]
            dupli = False
            for el in my_list:
                if (el==folder_name):
                    dupli = True
            if (dupli==False):
                index = self.listwidget.currentRow()
                self.listwidget.insertItem(index,folder_name)
                counter = 0
                self.elements = len(os.listdir(f"{fname}"))
                for el in os.listdir(f"{fname}"):
                    if el.endswith(".json"):    
                        counter+=1
                self.new.insertItem(index, f"{counter}")
                self.learn.insertItem(index, "0")
                new_list.append(f"{counter}")
                learn_list.append("0")
                due_list.append("0")
                self.due.insertItem(index, "0")
                my_list.append(folder_name)
            else:
                self.show_info_box()
    def open_menu(self, position):
        menu = QMenu()

        # Create actions
        remove_action = QAction("Remove deck", self)
        up_action = QAction("Move Up", self)
        down_action = QAction("Move Down", self)
        add_action = QAction("Add deck", self)
        edit_action = QAction("Rename deck", self)

        # Connect actions to their handlers
        remove_action.triggered.connect(self.remove_item)
        up_action.triggered.connect(self.move_item_up)
        down_action.triggered.connect(self.move_item_down)
        add_action.triggered.connect(self.add_item)
        edit_action.triggered.connect(self.edit_item)

        # Add actions to the menu
        menu.addAction(remove_action)
        menu.addAction(up_action)
        menu.addAction(down_action)
        menu.addAction(add_action)
        menu.addAction(edit_action)

        # Show the context menu at the cursor position
        menu.exec_(self.listwidget.mapToGlobal(position))

    def openwindow(self):
        self.window = SecondUI(my_list)
        self.window.show()
        self.close()
    def toggle_theme(self):
        if (self.dark_mode.text()=="Dark Mode"):
            dark_style = """
                QMainWindow {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #3c3c3c;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #5c5c5c;
                    color: #ffffff;
                    border: 1px solid #3c3c3c;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton::hover {
                    background-color: #6c6c6c;
                }
                QRadioButton {
                    color: #ffffff;
                }
                """
            self.setStyleSheet(dark_style)
            self.dark_mode.setText("Light Mode")
        else:
            light_style = """
                QMainWindow {
                    background-color: #ffffff;
                    color: #000000;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000000;
                    border: 1px solid #b0b0b0;
                }
                QLabel {
                    color: #000000;
                }
                QPushButton::hover {
                    background-color: #d0d0d0;
                }
                QRadioButton {
                    color: #000000;
                }
                """
            self.setStyleSheet(light_style)
            self.dark_mode.setText("Dark Mode")
    def remove_item(self):
        currentindex = self.listwidget.currentRow()
        item = self.listwidget.item(currentindex)
        question = QMessageBox.question(self, "Remove deck", "Are you sure of deleting the item "+item.text(), QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            item = self.listwidget.takeItem(currentindex)
            my_list.remove(item.text())
            if new_list and learn_list and due_list:
                new_list.pop(currentindex)
                learn_list.pop(currentindex)
                due_list.pop(currentindex)
            item2 = self.new.takeItem(currentindex)
            item3 = self.learn.takeItem(currentindex)
            item4 = self.due.takeItem(currentindex)
            del item
            del item2
            del item3
            del item4
    def move_item_up(self):
        index = self.listwidget.currentRow()
        if index>=1:
            item = self.listwidget.takeItem(index)
            item2 = self.new.takeItem(index)
            item3 = self.learn.takeItem(index)
            item4 = self.due.takeItem(index)
            self.new.insertItem(index-1, item2)
            self.learn.insertItem(index-1, item3)
            self.due.insertItem(index-1, item4)
            self.listwidget.insertItem(index-1, item)
            self.listwidget.setCurrentItem(item)
    def move_item_down(self):
        index = self.listwidget.currentRow()
        if index<self.listwidget.count()-1:
            item = self.listwidget.takeItem(index)
            item2 = self.new.takeItem(index)
            item3 = self.learn.takeItem(index)
            item4 = self.due.takeItem(index)
            self.listwidget.insertItem(index+1, item)
            self.new.insertItem(index+1, item2)
            self.learn.insertItem(index+1, item3)
            self.due.insertItem(index+1, item4)
            self.listwidget.setCurrentItem(item)
    def add_item(self):
        index = self.listwidget.currentRow()
        text, ok = QInputDialog.getText(self, "Enter deck", "Enter deck name to insert deck")
        if text and ok is not None:
            dupli = False
            for el in os.listdir(address):
                if (el==text):
                    dupli = True
            for el in my_list:
                if (el==text):
                    dupli = True
            if (dupli==False):
                self.listwidget.insertItem(index, text)
                self.new.insertItem(index, "0")
                self.learn.insertItem(index, "0")
                self.due.insertItem(index, "0")
                my_list.append(text)
                new_list.append("0")
                learn_list.append("0")
                due_list.append("0")
            else:
                self.show_info_box()
    def opendecks(self):
        counter = 0
        ans = False
        if (self.dark_mode.text()=="Dark Mode"):
            ans = True
        else:
            ans = False
        for i in new_list:
            counter += int(i)
        self.window = ThirdUI(my_list,UIWindow,counter,ans)
        self.window.show()

        # print(counter)

        self.hide()
    def edit_item(self):
        index = self.listwidget.currentRow()
        item = self.listwidget.item(index)
        if item is not None:
            text, ok = QInputDialog.getText(self, "Rename deck", "Enter the new name for the deck", QLineEdit.Normal, item.text())
            if text and ok is not None:
                dupli = False
                for el in os.listdir(address):
                    if (el==text):
                        dupli = True
                for el in my_list:
                    if (el==text):
                        dupli = True
                if (dupli==False):
                    prev_name = item.text()
                    item.setText(text)
                    my_list[index] = text
                    present = False
                    print(os.listdir(address))
                    # print("Item text:",prev_name)
                    for el in os.listdir(address):
                        if (el==prev_name):
                            present = True
                            break
                    # print(present)
                    if present==True:
                        os.rename(f"{prev_name}",f"{text}")
                else:
                    self.show_info_box()
    def show_info_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Folder already exists in Window")
        msg.setWindowTitle("Important Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

app = QApplication(sys.argv)

UIWindow = UI()

app.exec_()
