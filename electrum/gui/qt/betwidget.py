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
        self.vbox_c = QVBoxLayout()
        self.vbox_c.setSizeConstraint(QLayout.SetMinimumSize)
        self.setFixedWidth(360)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.set_labels()

    def btnCloseClicked(self):
        self.parent.betQListWidget.takeItem(0)   

    def set_labels(self):
        self.lblTitle = QLabel("")
        self.eventIdToBetOn = ""
        self.btnBetOutcome = 0
        
        self.header_hbox = QHBoxLayout()
        self.header_hbox.setSpacing(0)
        self.btnClose = QPushButton("x")
        self.btnClose.setFixedWidth(15)
        self.btnClose.clicked.connect(self.btnCloseClicked)
        self.lblLimitError = QLabel("Incorect bet amount. Please ensure your bet is between 25-10000 WGR inclusive.")
        
        self.lblPotentialReturn = QLabel("Potential Returns:")
        self.lblPotentialReturnValue = QLabel("")
        self.frame = QFrame()
        #self.lblTitle.setStyleSheet("QLabel { background-color : rgb(250, 218, 221); }")
        self.lblTitle.setAlignment(Qt.AlignHCenter)
        self.lblPick = QLabel("Your Pick:")
        self.lblPick.setAlignment(Qt.AlignHCenter)
        self.lblTeam = QLabel("")
        self.lblTeam.setAlignment(Qt.AlignHCenter)
        font = QFont("Times", 16) 
        self.lblTeam.setFont(font)

        self.lblSpreadOrTotal = QLabel("")
        self.lblSpreadOrTotal.setAlignment(Qt.AlignHCenter)

        self.lblSelectedOddValue = QLabel("1")
        self.lblSelectedOddValue.setFixedWidth(150)
        self.lblSelectedOddValue.setAlignment(Qt.AlignHCenter)
        self.lblSelectedOddValue.setStyleSheet("background-color: grey; border:1px solid rgb(0, 0, 0); ")
        
        self.lblPotentialReturn.setAlignment(Qt.AlignHCenter)
        self.lblPotentialReturnValue.setAlignment(Qt.AlignHCenter)

        self.editBettingAmount = BTCAmountEdit(self.parent.get_decimal_point)
        self.editBettingAmount.setText("0")
        self.editBettingAmount.setValidator(QDoubleValidator(self.editBettingAmount) )
        self.editBettingAmount.setFixedWidth(180)
        self.editBettingAmount.textChanged.connect(self.betAmountChanged)

        self.fiat_c = AmountEdit(self.parent.fx.get_currency if self.parent.fx else '')
        if not self.parent.fx or not self.parent.fx.is_enabled():
            self.fiat_c.setVisible(False)

        self.editBettingAmount.frozen.connect(
            lambda: self.fiat_c.setFrozen(self.editBettingAmount.isReadOnly()))

        self.h = QHBoxLayout()
        self.btnBet = QPushButton("BET")
        self.btnBet.setFixedWidth(70)
        self.btnBet.clicked.connect(self.btnBetClicked)
        self.header_hbox.addWidget(self.lblTitle)
        self.header_hbox.addWidget(self.btnClose)
        self.vbox_c.addLayout(self.header_hbox)
        self.vbox_c.addWidget(self.lblPick)
        self.vbox_c.addWidget(self.lblTeam)
        self.vbox_c.addWidget(self.lblSpreadOrTotal)
        self.vbox_c.addWidget(self.lblSelectedOddValue,alignment=Qt.AlignCenter)
        self.h.addWidget(self.editBettingAmount)
        self.h.addWidget(self.btnBet)
        self.vbox_c.addLayout(self.h)
        self.lblLimitError.hide()
        
        self.lblLimitError.setWordWrap(True)
        self.lblLimitError.setMinimumHeight(50)
        self.vbox_c.addWidget(self.lblLimitError)
        self.vbox_c.addWidget(self.lblPotentialReturn)
        self.vbox_c.addWidget(self.lblPotentialReturnValue)
        self.setLayout(self.vbox_c)
    
    def btnBetClicked(self):
        betAmtInWgr = self.editBettingAmount.get_amount() / COIN
        print("Betting Amount : ", betAmtInWgr)
        if betAmtInWgr >= MIN_BET_AMT and betAmtInWgr <= MAX_BET_AMT:
            self.lblLimitError.hide()
            self.parent.do_bet(a = self)
            self.btnBetValue = float(self.editBettingAmount.text()) + (((float(self.editBettingAmount.text()) * (float(self.lblSelectedOddValue.text()) -1 ))) *.94 )
        else:
            self.lblLimitError.show()
        
    def betAmountChanged(self):
        bb = float(0)
        if self.editBettingAmount.text() == "":
            bb = float(0)
        else:
            bb = float(self.editBettingAmount.text())        
        self.btnBetValue = bb + (((bb * (float(self.lblSelectedOddValue.text()) -1 ))) *.94 )
        self.lblPotentialReturnValue.setText(str("{0:.2f}".format(self.btnBetValue))+ ' ' + self.parent.base_unit())