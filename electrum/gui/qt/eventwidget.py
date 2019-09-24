from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QScrollArea, QTextEdit, 
                             QFrame, QShortcut, QMainWindow, QCompleter, QInputDialog,
                             QWidget, QMenu, QSizePolicy, QStatusBar, QListView,
                             QAbstractItemView, QSpacerItem, QSizePolicy, QListWidget,
                             QListWidgetItem, QWidget, QLabel)
from PyQt5.QtCore import Qt, QRect, QStringListModel, QModelIndex, QItemSelectionModel,QSize
import time
from .betwidget import BetWidget

ODDS_DIVISOR = 10000

class EventWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.grid=QGridLayout()
        self.grid.setContentsMargins(0,0,0,0)
        
    def homeButtonClicked(self):
        print("button clicked for item : ",self.MoneyLineHomeButton.text())
        
        self.betWidget=BetWidget(self.parent)
        self.betWidget.header_label.setText(self.homelabel.text()+" vs "+self.awaylabel.text())  
        self.betWidget.event_id_bet=self.eventId
        self.betWidget.outcome_bet=1      
        self.betWidget.team_label.setText(self.homelabel.text())
        self.betWidget.selectedOddValue.setText(self.MoneyLineHomeButton.text())
        
        self.parent.betQListWidget.clear()
        betQListWidgetItem = QListWidgetItem(self.parent.betQListWidget)
        betQListWidgetItem.setSizeHint(QSize(380,300))
        betQListWidgetItem.setTextAlignment(Qt.AlignHCenter)

        self.parent.betQListWidget.addItem(betQListWidgetItem)
        self.parent.betQListWidget.setItemWidget(betQListWidgetItem, self.betWidget)

        self.parent.vbox_b.addWidget(self.parent.betQListWidget)

    def awayButtonClicked(self):
        print("button clicked for item : ",self.MoneyLinelAwayButton.text())
        self.betWidget=BetWidget(self.parent)
        self.betWidget.header_label.setText(self.homelabel.text()+" vs "+self.awaylabel.text()) 
        self.betWidget.event_id_bet=self.eventId
        self.betWidget.outcome_bet=2        
        self.betWidget.team_label.setText(self.awaylabel.text())
        self.betWidget.selectedOddValue.setText(self.MoneyLinelAwayButton.text())
        
        self.parent.betQListWidget.clear()
        betQListWidgetItem = QListWidgetItem(self.parent.betQListWidget)
        betQListWidgetItem.setSizeHint(QSize(380,300))
        betQListWidgetItem.setTextAlignment(Qt.AlignHCenter)

        self.parent.betQListWidget.addItem(betQListWidgetItem)
        self.parent.betQListWidget.setItemWidget(betQListWidgetItem, self.betWidget)
        self.parent.vbox_b.addWidget(self.parent.betQListWidget)

    def drawButtonClicked(self):
        print("button clicked for item : ",
        self.MoneyLinelDrawButton.text())
        self.betWidget=BetWidget(self.parent)
        self.betWidget.header_label.setText(self.homelabel.text()+" vs "+self.awaylabel.text())  
        self.betWidget.event_id_bet=self.eventId
        self.betWidget.outcome_bet=3      
        self.betWidget.team_label.setText(self.drawlabel.text())
        self.betWidget.selectedOddValue.setText(self.MoneyLinelDrawButton.text())
        
        self.parent.betQListWidget.clear()
        betQListWidgetItem = QListWidgetItem(self.parent.betQListWidget)
        betQListWidgetItem.setSizeHint(QSize(380,300))
        betQListWidgetItem.setTextAlignment(Qt.AlignHCenter)

        self.parent.betQListWidget.addItem(betQListWidgetItem)
        self.parent.betQListWidget.setItemWidget(betQListWidgetItem, self.betWidget)
        self.parent.vbox_b.addWidget(self.parent.betQListWidget)

    def setdata(self,obj):
        self.eventId=str(obj["event_id"])
        self.tournament=QLabel(obj["tournament"]+" "+str("(Event ID: "+str(obj["event_id"])+")"))
        self.tournament.setStyleSheet("QLabel { background-color : rgb(250, 218, 221);  }")
        self.tournament.setAlignment(Qt.AlignLeft)
        self.eventTime=QLabel(time.strftime('%A,%b %dth %I:%M%p(%z %Z)', time.localtime(obj["starting"])))
        self.eventTime.setAlignment(Qt.AlignRight)
        self.hbox_tournament=QHBoxLayout()
        self.hbox_tournament.addWidget(self.tournament)
        self.hbox_tournament.addWidget(self.eventTime)
        self.hbox_tournament.setSpacing(0)
        self.vbox_event=QVBoxLayout()
        self.vbox_event.addLayout(self.hbox_tournament)
        self.eventTime.setStyleSheet("QLabel { background-color : rgb(250, 218, 221);  }")
        self.MoneyLinelabel=QLabel("   Money Line  ")
        self.totalhome=QPushButton("-")
        self.spreadhome=QPushButton("-")
        self.spreadaway=QPushButton("-")
        self.totalaway=QPushButton("-")
        self.spreaddraw=QPushButton("-")
        self.totaldraw=QPushButton("-")
        self.totalhome.setEnabled(False)
        self.spreadhome.setEnabled(False)
        self.spreadaway.setEnabled(False)
        self.totalaway.setEnabled(False)
        self.spreaddraw.setEnabled(False)
        self.totaldraw.setEnabled(False)

        self.MoneyLinelabel.setAlignment(Qt.AlignHCenter)
        self.homelabel=QLabel(obj["teams"]["home"])
        self.awaylabel=QLabel(obj["teams"]["away"])
        self.drawlabel=QLabel("Draw")
        self.spread=QLabel("Spread")
        self.total=QLabel("Total")
        self.homelabel.setAlignment(Qt.AlignLeft)
        self.awaylabel.setAlignment(Qt.AlignLeft)
        self.drawlabel.setAlignment(Qt.AlignLeft)
        self.spread.setAlignment(Qt.AlignHCenter)
        self.total.setAlignment(Qt.AlignHCenter)

        self.MoneyLineHomeButton = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlHome"]/ODDS_DIVISOR))))        
        self.MoneyLinelAwayButton = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlAway"]/ODDS_DIVISOR))))
        self.MoneyLinelDrawButton = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlDraw"]/ODDS_DIVISOR))))

        self.grid.addWidget(self.MoneyLinelabel,0,1)
        self.grid.addWidget(self.spread,0,2)
        self.grid.addWidget(self.total,0,3)

        self.grid.addWidget(self.homelabel,1,0)
        self.grid.addWidget(self.MoneyLineHomeButton,1,1,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.spreadhome,1,2,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.totalhome,1,3,alignment=Qt.AlignCenter)

        self.grid.addWidget(self.awaylabel,2,0)
        self.grid.addWidget(self.MoneyLinelAwayButton,2,1,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.spreadaway,2,2,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.totalaway,2,3,alignment=Qt.AlignCenter)

        self.grid.addWidget(self.drawlabel,3,0)
        self.grid.addWidget(self.MoneyLinelDrawButton,3,1,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.spreaddraw,3,2,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.totaldraw,3,3,alignment=Qt.AlignCenter)

        self.MoneyLineHomeButton.clicked.connect(self.homeButtonClicked)
        self.MoneyLinelAwayButton.clicked.connect(self.awayButtonClicked)
        self.MoneyLinelDrawButton.clicked.connect(self.drawButtonClicked)
        self.vbox_event.addLayout(self.grid)
        self.setLayout(self.vbox_event)