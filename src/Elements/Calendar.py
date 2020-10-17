from PyQt5.QtWidgets import QCalendarWidget


class Calendar(QCalendarWidget):
    def __init__(self):
        super(QCalendarWidget, self).__init__()

        self.setStyleSheet("#qt_calendar_navigationbar"
                           "{"
                           "   background-color : #F97170;"
                           "   min-height: 40px;"
                           "}"
                           "#qt_calendar_prevmonth:hover, #qt_calendar_nextmonth:hover, #qt_calendar_yearbutton:hover, #qt_calendar_monthbutton:hover{"
                           "   background-color: rgba(56, 90, 125, .01);"
                           "   color: white;"
                           "}"
                           "#qt_calendar_prevmonth:pressed, #qt_calendar_nextmonth:pressed, #qt_calendar_yearbutton:pressed, #qt_calendar_monthbutton:pressed  {"
                           "   background-color: rgba(56, 90, 125, 1);"
                           "   color: white;"
                           "}"
                           "#qt_calendar_prevmonth, #qt_calendar_nextmonth  {"
                           "   qproperty-icon: none;"
                           "}"
                           "#qt_calendar_prevmonth, #qt_calendar_nextmonth {"
                           "   color: white;"
                           "   font-weight: bold;"
                           "}"
                           "#qt_calendar_prevmonth  {"
                           "   qproperty-text: '<';"
                           "}"
                           "#qt_calendar_nextmonth  {"
                           "   qproperty-text: '>';"
                           "}"
                           "#qt_calendar_calendarview  {"
                           "   selection-background-color: #F97170;"
                           "}"
                           )
