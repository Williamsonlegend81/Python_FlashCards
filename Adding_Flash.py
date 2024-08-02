from PyQt5.QtWidgets import QMainWindow,QComboBox,QPushButton,QTextEdit,QLabel,QColorDialog,QFontDialog,QFileDialog
from PyQt5 import uic
import json
import os
from PyQt5.QtGui import QFont,QColor,QTextListFormat,QTextImageFormat
from PyQt5.QtCore import Qt

save = False
adds = ""
class SecondUI(QMainWindow):
    def __init__(self,my_list):
        super(SecondUI,self).__init__()

        # Load UI file
        uic.loadUi("add_flash.ui",self)

        # Load the widgets
        self.cardtype = self.findChild(QComboBox,"comboBox")
        self.cards = self.findChild(QComboBox,"comboBox_2")
        self.settings = self.findChild(QPushButton,"pushButton")
        self.bold = self.findChild(QPushButton,"pushButton_2")
        self.italic = self.findChild(QPushButton,"pushButton_3")
        self.underline = self.findChild(QPushButton,"pushButton_4")
        self.texteffects = self.findChild(QPushButton,"pushButton_5")
        self.highlight = self.findChild(QPushButton,"pushButton_6")
        self.bullets = self.findChild(QPushButton,"pushButton_9")
        self.numbering = self.findChild(QPushButton,"pushButton_8")
        self.leftalign = self.findChild(QPushButton,"pushButton_7")
        self.centeralign = self.findChild(QPushButton,"pushButton_11")
        self.rightalign = self.findChild(QPushButton,"pushButton_10")
        self.attachment = self.findChild(QPushButton,"pushButton_14")
        self.fontstyle = self.findChild(QPushButton,"pushButton_15")
        self.front = self.findChild(QTextEdit,"textEdit")
        self.back = self.findChild(QTextEdit,"textEdit_2")
        self.add = self.findChild(QPushButton,"pushButton_12")
        self.closing = self.findChild(QPushButton,"pushButton_13")
        self.flashcardtype = self.findChild(QLabel,"label")
        self.decks = self.findChild(QLabel,"label_2")
        self.frontlab = self.findChild(QLabel,"label_3")
        self.rearlab = self.findChild(QLabel,"label_4")

        self.cardtype.addItem("Basic")

        self.bold.clicked.connect(self.toggle_bold)
        self.italic.clicked.connect(self.toggle_italic)
        self.underline.clicked.connect(self.toggle_underline)
        self.centeralign.clicked.connect(self.set_center)
        self.rightalign.clicked.connect(self.set_right)
        self.leftalign.clicked.connect(self.set_left)
        self.closing.clicked.connect(self.close_it)
        self.highlight.clicked.connect(self.highlight_text)
        self.bullets.clicked.connect(self.add_bullets)
        self.numbering.clicked.connect(self.add_numbering)
        self.texteffects.clicked.connect(self.color_dialog)
        self.fontstyle.clicked.connect(self.font_dialog)
        self.attachment.clicked.connect(self.insert_image)
        self.add.clicked.connect(self.add_to_json)
        self.settings.clicked.connect(self.edit_json_file)

        for item in my_list:
            directory = f"{item}"
            parent_dir = str(os.getcwd())
            path = os.path.join(parent_dir,directory)
            try:
                os.mkdir(path)
            except OSError as error:
                print(error)
            self.cards.addItem(item)

        self.show()
    def insert_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "PNG Files(*.png);;JPEG Files(*.jpeg);;JPG Files(*.jpg)", options=options)
        if file_path:
            self.insert_image_into_text_edit(file_path)
    def insert_image_into_text_edit(self, file_path):
        if self.front.textCursor():
            cursor = self.front.textCursor()
            image_format = QTextImageFormat()
            image_format.setName(file_path)
            cursor.insertImage(image_format)
            self.front.setTextCursor(cursor)

        if self.back.textCursor():
            cursor = self.back.textCursor()
            image_format = QTextImageFormat()
            image_format.setName(file_path)
            cursor.insertImage(image_format)
            self.back.setTextCursor(cursor)      
    def toggle_bold(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
            cursor.mergeCharFormat(fmt)
        else:
            current_font = self.front.currentFont()
            is_bold = current_font.bold()
            current_font.setBold(not is_bold)
            self.front.setCurrentFont(current_font)

        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
            cursor.mergeCharFormat(fmt)
        else:
            current_font = self.back.currentFont()
            is_bold = current_font.bold()
            current_font.setBold(not is_bold)
            self.back.setCurrentFont(current_font)
    def toggle_italic(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            cursor.mergeCharFormat(fmt)
            self.front.setCurrentCharFormat(fmt)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            cursor.mergeCharFormat(fmt)
            self.back.setCurrentCharFormat(fmt)
    def add_bullets(self):
        cursor = self.front.textCursor()
        cursor.beginEditBlock()

        block_format = cursor.blockFormat()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)
        cursor.createList(list_format)

        cursor.endEditBlock()

        cursor = self.back.textCursor()
        cursor.beginEditBlock()

        block_format = cursor.blockFormat()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)
        cursor.createList(list_format)

        cursor.endEditBlock()
    def add_numbering(self):
        cursor = self.front.textCursor()
        cursor.beginEditBlock()

        block_format = cursor.blockFormat()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDecimal)
        cursor.createList(list_format)

        cursor.endEditBlock()

        cursor = self.back.textCursor()
        cursor.beginEditBlock()

        block_format = cursor.blockFormat()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDecimal)
        cursor.createList(list_format)

        cursor.endEditBlock()
    def font_dialog(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.change_font_style(font)
    def color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.change_font_color(color)
    def change_font_style(self,font):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFont(font)
            cursor.mergeCharFormat(fmt)
        else:
            self.front.setFont(font)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFont(font)
            cursor.mergeCharFormat(fmt)
        else:
            self.back.setFont(font)
    def change_font_color(self,color):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)
        else:
            self.front.setTextColor(color)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)
        else:
            self.back.setTextColor(color)
    def highlight_text(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setBackground(QColor(Qt.yellow) if fmt.background()!=QColor(Qt.yellow) else QColor(Qt.transparent))
            cursor.mergeCharFormat(fmt)
            self.front.setTextCursor(cursor)
        
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setBackground(QColor(Qt.yellow) if fmt.background() != QColor(Qt.yellow) else QColor(Qt.transparent))
            cursor.mergeCharFormat(fmt)
            self.back.setTextCursor(cursor)

    def toggle_underline(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            cursor.mergeCharFormat(fmt)
            self.front.setCurrentCharFormat(fmt)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            cursor.mergeCharFormat(fmt)
            self.back.setCurrentCharFormat(fmt)
    def close_it(self):
        self.close()
    def set_left(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            self.front.setAlignment(Qt.AlignLeft)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            self.back.setAlignment(Qt.AlignLeft)
    def set_center(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            self.front.setAlignment(Qt.AlignHCenter)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            self.back.setAlignment(Qt.AlignHCenter)
    def set_right(self):
        cursor = self.front.textCursor()
        if cursor.hasSelection():
            self.front.setAlignment(Qt.AlignRight)
        cursor = self.back.textCursor()
        if cursor.hasSelection():
            self.back.setAlignment(Qt.AlignRight)
    def edit_json_file(self):
        fname = QFileDialog.Options()
        fname |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getOpenFileName(self, "Open JSON File", f"{os.getcwd()}\\{self.cards.currentText()}", "JSON Files(*.json)")
        global save
        save = True
        global adds
        adds = str(filepath).split('/')[-1]
        # print(adds)
        if filepath!="":
            self.load_from_json(filepath)
    def add_to_json(self):
        if adds=="" and save==False:
            data = {
                "deck": self.cards.currentText(),
                "cardtype": self.cardtype.currentText(),
                "front": self.front.toHtml(),
                "back": self.back.toHtml()
            }
            with open(f"{self.cards.currentText()}\\card_{len(os.listdir(f"{self.cards.currentText()}"))+1}.json", "a") as f:
                json.dump(data, f, indent=4)
                f.write('\n')
        else:
            os.remove(f"{self.cards.currentText()}\\{adds}")
            data = {
                "deck": self.cards.currentText(),
                "cardtype": self.cardtype.currentText(),
                "front": self.front.toHtml(),
                "back": self.back.toHtml()
            }
            with open(f"{self.cards.currentText()}\\{adds}","a") as f:
                json.dump(data,f,indent=4)
                f.write('\n')

    def load_from_json(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            self.cards.setCurrentText(data["deck"])
            self.cardtype.setCurrentText(data["cardtype"])
            self.front.setHtml(data["front"])
            self.back.setHtml(data["back"])

        
