from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QScrollArea, QTextEdit, 
                             QFrame, QShortcut, QMainWindow, QCompleter, QInputDialog,
                             QWidget, QMenu, QSizePolicy, QStatusBar, QListView,
                             QAbstractItemView, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem, QWidget, QLabel, QLayout)
from PyQt5.QtCore import Qt, QRect, QStringListModel, QModelIndex, QItemSelectionModel,QSize
from PyQt5.QtGui import QFont, QDoubleValidator
from .amountedit import AmountEdit, BTCAmountEdit
from electrum.bitcoin import COIN, is_address, TYPE_ADDRESS

MIN_BET_AMT  = 25 #WGR
MAX_BET_AMT  = 10000 #WGR

class BetWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.vbox_c=QVBoxLayout()
        self.vbox_c.setSizeConstraint(QLayout.SetMinimumSize)
        self.setFixedWidth(360)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.set_labels()

    def closeButtonClicked(self):
        self.parent.betQListWidget.takeItem(0)   

    def set_labels(self):
        self.header_label=QLabel("")
        self.event_id_bet=""
        self.outcome_bet=0
        
        self.header_hbox=QHBoxLayout()
        self.header_hbox.setSpacing(0)
        self.close_button=QPushButton("x")
        self.close_button.setFixedWidth(15)
        self.close_button.clicked.connect(self.closeButtonClicked)
        self.limit_label=QLabel("Incorect bet amount. Please ensure your bet is between 25-10000 tWGR inclusive.")
        
        self.potential_label=QLabel("Potential Returns:")
        self.potential_returns_value_label=QLabel("")
        self.frame=QFrame()
        #self.header_label.setStyleSheet("QLabel { background-color : rgb(250, 218, 221); }")
        self.header_label.setAlignment(Qt.AlignHCenter)
        self.yourpick=QLabel("Your Pick:")
        self.yourpick.setAlignment(Qt.AlignHCenter)
        self.team_label=QLabel("")
        self.team_label.setAlignment(Qt.AlignHCenter)
        newfont = QFont("Times", 16) 
        self.team_label.setFont(newfont)
        self.selectedOddValue=QLabel("1")
        self.selectedOddValue.setFixedWidth(150)
        self.selectedOddValue.setAlignment(Qt.AlignHCenter)
        self.selectedOddValue.setStyleSheet("background-color: grey; border:1px solid rgb(0, 0, 0); ")
        
        self.potential_label.setAlignment(Qt.AlignHCenter)
        self.potential_returns_value_label.setAlignment(Qt.AlignHCenter)

        self.betting_amount_c = BTCAmountEdit(self.parent.get_decimal_point)
        self.betting_amount_c.setText("0")
        self.betting_amount_c.setValidator(QDoubleValidator(self.betting_amount_c) )
        self.betting_amount_c.setFixedWidth(180)
        self.betting_amount_c.textChanged.connect(self.betValueChanged)

        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.betting_amount_c.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.betting_amount_c.isReadOnly()))

        self.h=QHBoxLayout()
        self.bet=QPushButton("BET")
        self.bet.setFixedWidth(70)
        self.bet.clicked.connect(self.betButtonClicked)
        self.header_hbox.addWidget(self.header_label)
        self.header_hbox.addWidget(self.close_button)
        self.vbox_c.addLayout(self.header_hbox)
        self.vbox_c.addWidget(self.yourpick)
        self.vbox_c.addWidget(self.team_label)
        self.vbox_c.addWidget(self.selectedOddValue,alignment=Qt.AlignCenter)
        self.h.addWidget(self.betting_amount_c)
        self.h.addWidget(self.bet)
        self.vbox_c.addLayout(self.h)
        self.limit_label.hide()
        
        self.limit_label.setWordWrap(True)
        self.limit_label.setMinimumHeight(50)
        self.vbox_c.addWidget(self.limit_label)
        self.vbox_c.addWidget(self.potential_label)
        self.vbox_c.addWidget(self.potential_returns_value_label)
        self.setLayout(self.vbox_c)
    
    def betButtonClicked(self):
        betAmtInWgr = self.betting_amount_c.get_amount() / COIN
        print("Betting Amount : ",betAmtInWgr)
        if betAmtInWgr>=MIN_BET_AMT and betAmtInWgr<=MAX_BET_AMT:
            self.limit_label.hide()
            self.parent.do_bet(a=self)
            self.betValue=float(self.betting_amount_c.text()) + (((float(self.betting_amount_c.text()) * (float(self.selectedOddValue.text()) -1 ))) *.94 )
        else:
            self.limit_label.show()
        
    def betValueChanged(self):
        bb=float(0)
        if self.betting_amount_c.text()=="":
            bb=float(0)
        else:
            bb=float(self.betting_amount_c.text())        
        self.betValue=bb + (((bb * (float(self.selectedOddValue.text()) -1 ))) *.94 )
        self.potential_returns_value_label.setText(str("{0:.2f}".format(self.betValue))+ ' ' + self.parent.base_unit())