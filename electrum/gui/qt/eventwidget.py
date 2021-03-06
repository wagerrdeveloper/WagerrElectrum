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
POINTS_DIVISOR = 10

class EventWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0,0,0,0)
        
    def btnMoneyLineHomeClicked(self):
        print("Money Line Home button clicked for item : ",self.btnMoneyLineHome.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 1
        self.betWidget.lblTeam.setText(self.lblHomeTeam.text())
        self.betWidget.lblSelectedOddValue.setText(self.btnMoneyLineHome.text())
        self.addBetWidgetItemToList()

    def btnMoneyLineAwayClicked(self):
        print("Money Line Away button clicked for item : ",self.btnMoneyLineAway.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text()) 
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 2
        self.betWidget.lblTeam.setText(self.lblAwayTeam.text())
        self.betWidget.lblSelectedOddValue.setText(self.btnMoneyLineAway.text())
        self.addBetWidgetItemToList()

    def btnMoneyLineDrawClicked(self):
        print("Money Line Draw button clicked for item : ", self.btnMoneyLineDraw.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 3
        self.betWidget.lblTeam.setText(self.lblDraw.text())
        self.betWidget.lblSelectedOddValue.setText(self.btnMoneyLineDraw.text())
        self.addBetWidgetItemToList()

    def btnSpreadHomeClicked(self):
        print("Spread Home button clicked for item : ",self.btnSpreadHome.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 4
        self.betWidget.lblTeam.setText(self.lblHomeTeam.text())
        self.betWidget.lblSpreadOrTotal.setText("Handicap " + self.homeSpreadSign + self.spreadPoints)
        self.betWidget.lblSpreadOrTotal.show()
        self.betWidget.lblSelectedOddValue.setText(self.spreadHomeOdds)
        self.addBetWidgetItemToList()

    def btnSpreadAwayClicked(self):
        print("Spread Away button clicked for item : ",self.btnSpreadAway.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 5
        self.betWidget.lblTeam.setText(self.lblHomeTeam.text())
        self.betWidget.lblSpreadOrTotal.setText("Handicap " + self.awaySpreadSign + self.spreadPoints)
        self.betWidget.lblSpreadOrTotal.show()
        self.betWidget.lblSelectedOddValue.setText(self.spreadAwayOdds)
        self.addBetWidgetItemToList()

    def btnTotalHomeClicked(self):
        print("Total Home button clicked for item : ",self.btnTotalHome.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 6
        self.betWidget.lblTeam.setText(self.lblHomeTeam.text())
        self.betWidget.lblSpreadOrTotal.setText("Over" + self.totalPoints)
        self.betWidget.lblSpreadOrTotal.show()
        self.betWidget.lblSelectedOddValue.setText(self.totalsOverOdds)
        self.addBetWidgetItemToList()

    def btnTotalAwayClicked(self):
        print("Total Away button clicked for item : ",self.btnTotalAway.text())
        self.betWidget = BetWidget(self.parent)
        self.betWidget.lblTitle.setText(self.lblHomeTeam.text() + " vs " + self.lblAwayTeam.text())  
        self.betWidget.eventIdToBetOn = self.eventId
        self.betWidget.betOutcome = 7
        self.betWidget.lblTeam.setText(self.lblHomeTeam.text())
        self.betWidget.lblSpreadOrTotal.setText("Under" + self.totalPoints)
        self.betWidget.lblSpreadOrTotal.show()
        self.betWidget.lblSelectedOddValue.setText(self.totalsUnderOdds)
        self.addBetWidgetItemToList()

    def addBetWidgetItemToList(self):
        betQListWidgetItem = QListWidgetItem(self.parent.betQListWidget)
        betQListWidgetItem.setSizeHint(QSize(300,300))
        #betQListWidgetItem.setTextAlignment(Qt.AlignHCenter)

        self.parent.betQListWidget.addItem(betQListWidgetItem)
        self.parent.betQListWidget.setItemWidget(betQListWidgetItem, self.betWidget)

        self.parent.vbox_b.addWidget(self.parent.betQListWidget)

    def setData(self,obj):
        self.eventId = str(obj["event_id"])
        self.lblTournament = QLabel(obj["tournament"] + " " + str("(Event ID: " + str(obj["event_id"]) + ")"))
        self.lblTournament.setStyleSheet("QLabel { background-color : rgb(250, 218, 221);  }")
        self.lblTournament.setAlignment(Qt.AlignLeft)
        self.lblEventTime = QLabel(time.strftime('%A,%b %dth %I:%M%p(%z %Z)', time.localtime(obj["starting"])))
        self.lblEventTime.setAlignment(Qt.AlignRight)
        self.hbox_tournament = QHBoxLayout()
        self.hbox_tournament.addWidget(self.lblTournament)
        self.hbox_tournament.addWidget(self.lblEventTime)
        self.hbox_tournament.setSpacing(0)
        self.vbox_event = QVBoxLayout()
        self.vbox_event.addLayout(self.hbox_tournament)
        self.lblEventTime.setStyleSheet("QLabel { background-color : rgb(250, 218, 221);  }")
        
        self.lblMoneyLineHeading = QLabel("   Money Line  ")
        self.lblSpreadHeading = QLabel("Spread")
        self.lblTotalHeading = QLabel("Total")
        self.lblDraw = QLabel("Draw")

        self.btnMoneyLineHome = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlHome"]/ODDS_DIVISOR))))
        self.btnMoneyLineAway = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlAway"]/ODDS_DIVISOR))))
        self.btnMoneyLineDraw = QPushButton(str(("{0:.2f}".format(obj["odds"][0]["mlDraw"]/ODDS_DIVISOR))))

        self.btnMoneyLineHome.setFixedHeight(25)
        self.btnMoneyLineAway.setFixedHeight(25)
        self.btnMoneyLineDraw.setFixedHeight(25)

        moneyLineHomeOdds = obj["odds"][0]["mlHome"]/ODDS_DIVISOR
        moneyLineAwayOdds = obj["odds"][0]["mlAway"]/ODDS_DIVISOR
        
        self.homeSpreadSign = ""
        if moneyLineHomeOdds < moneyLineAwayOdds :
            self.homeSpreadSign = "-"
        else:
            self.homeSpreadSign = "+"

        self.awaySpreadSign = ""
        if moneyLineHomeOdds > moneyLineAwayOdds :
            self.awaySpreadSign = "-"
        else:
            self.awaySpreadSign = "+"

        self.spreadPoints = str(int(obj["odds"][1]["spreadPoints"]/POINTS_DIVISOR))
        self.spreadHomeOdds = str("{0:.2f}".format(obj["odds"][1]["spreadHome"]/ODDS_DIVISOR))
        self.spreadAwayOdds = str("{0:.2f}".format(obj["odds"][1]["spreadAway"]/ODDS_DIVISOR))
        self.btnSpreadHome = QPushButton(self.homeSpreadSign + self.spreadPoints + "    " + self.spreadHomeOdds)
        self.btnSpreadHome.setFixedHeight(25)
        self.btnSpreadAway = QPushButton(self.awaySpreadSign + self.spreadPoints + "    " + self.spreadAwayOdds)
        self.btnSpreadAway.setFixedHeight(25)

        self.totalPoints = str("{0:.1f}".format(obj["odds"][2]["totalsPoints"]/POINTS_DIVISOR))
        self.totalsOverOdds = str("{0:.2f}".format(obj["odds"][2]["totalsOver"]/ODDS_DIVISOR))
        self.totalsUnderOdds = str("{0:.2f}".format(obj["odds"][2]["totalsUnder"]/ODDS_DIVISOR))
        overTotalPointText = "(O" + self.totalPoints + ")"
        underTotalPointText = "(U" + self.totalPoints + ")"
        self.btnTotalHome = QPushButton(overTotalPointText + "    " + self.totalsOverOdds)
        self.btnTotalAway = QPushButton(underTotalPointText + "    " + self.totalsUnderOdds)
        self.btnTotalHome.setFixedHeight(25)
        self.btnTotalAway.setFixedHeight(25)

        self.lblMoneyLineHeading.setAlignment(Qt.AlignHCenter)
        self.lblHomeTeam = QLabel(obj["teams"]["home"])
        self.lblAwayTeam = QLabel(obj["teams"]["away"])
        
        self.lblHomeTeam.setAlignment(Qt.AlignLeft)
        self.lblAwayTeam.setAlignment(Qt.AlignLeft)
        self.lblDraw.setAlignment(Qt.AlignLeft)
        self.lblSpreadHeading.setAlignment(Qt.AlignHCenter)
        self.lblTotalHeading.setAlignment(Qt.AlignHCenter)

        self.grid.addWidget(self.lblMoneyLineHeading,0,1)
        self.grid.addWidget(self.lblSpreadHeading,0,2)
        self.grid.addWidget(self.lblTotalHeading,0,3)

        self.grid.addWidget(self.lblHomeTeam,1,0)
        self.grid.addWidget(self.btnMoneyLineHome,1,1,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btnSpreadHome,1,2,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btnTotalHome,1,3,alignment=Qt.AlignCenter)

        self.grid.addWidget(self.lblAwayTeam,2,0)
        self.grid.addWidget(self.btnMoneyLineAway,2,1,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btnSpreadAway,2,2,alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btnTotalAway,2,3,alignment=Qt.AlignCenter)

        self.grid.addWidget(self.lblDraw,3,0)
        self.grid.addWidget(self.btnMoneyLineDraw,3,1,alignment=Qt.AlignCenter)
        #self.grid.addWidget(self.spreaddraw,3,2,alignment=Qt.AlignCenter)
        #self.grid.addWidget(self.totaldraw,3,3,alignment=Qt.AlignCenter)

        self.btnMoneyLineHome.clicked.connect(self.btnMoneyLineHomeClicked)
        self.btnMoneyLineAway.clicked.connect(self.btnMoneyLineAwayClicked)
        self.btnMoneyLineDraw.clicked.connect(self.btnMoneyLineDrawClicked)
        
        self.btnSpreadHome.clicked.connect(self.btnSpreadHomeClicked)
        self.btnSpreadAway.clicked.connect(self.btnSpreadAwayClicked)
        
        self.btnTotalHome.clicked.connect(self.btnTotalHomeClicked)
        self.btnTotalAway.clicked.connect(self.btnTotalAwayClicked)
        self.grid.setSpacing(10);
        self.vbox_event.addLayout(self.grid)
        self.setLayout(self.vbox_event)