import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Window
import Qt5Compat.GraphicalEffects

Window {
    id: alert
    visible: false
    flags: Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
    modality: Qt.ApplicationModal
    color: "transparent"
    width: 750
    height: 550

    property var mainWindow


    property var dragStart: Qt.point(0, 0)

    function openAlert() {
        visible = true
        forceActiveFocus()
        raise()
    }

    function closeAlert() {
        visible = false
    }

    Connections {
        target: alertHandler
        onShowAlert: {
            alert.openAlert();
        }
    }

    MouseArea {
        id: dragArea
        anchors.fill: parent
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        acceptedButtons: Qt.LeftButton
        onPressed: {
            alert.dragStart = Qt.point(mouse.x, mouse.y)
        }
        onPositionChanged: {
            alert.x += mouse.x - alert.dragStart.x;
            alert.y += mouse.y - alert.dragStart.y;
        }
    }

    Item {
        id: alertContainer
        width: 750
        height: 550
        anchors.centerIn: parent

        Rectangle {
            id: alertBox
            anchors.centerIn: parent
            width: parent.width
            height: parent.height
            radius: 15
            color: "#1e1e1e"
            border.color: "#8698fc"
            border.width: 2

            AlertTitleBarButton {
                id: exitbutton
                x: 670
                y: 21
                width: 40
                height: 52
                textColor: "#8698fc"
                bgColor: "#1e1e1e"
                accentIcon: "../icons_accent/exit.png"
                backgroundIcon: "../icons_background/exit.png"
                ac: "Exit"
            }

            Warningtriangle {
                id: warningItem
                x: 38
                y: 180
                width: 121
                height: 132
            }

            Text {
                id: warningLabel
                x: 216
                y: 28
                color: "#FF0000"
                text: "Critical Warning!"
                font.pixelSize: 40
                verticalAlignment: Text.AlignVCenter
                font.styleName: "Bold"
                font.family: "Arial"
            }

            Text {
                id: warningText
                x: 194
                y: 171
                width: 486
                height: 208
                textFormat: Text.RichText
                color: "#ffffff"
                text: "Suspicious activity detected!<br><br>Your device may be compromised by<br>a data-stealing malware.<br><br> The attack has been halted and<br>removed upon detection.<br><br>Tap <span style='color:#8698fc;'>Report</span> for more details."
                font.pixelSize: 27
                verticalAlignment: Text.AlignVCenter
                font.styleName: "Bold"
                font.family: "Arial"
            }

            AlertButton {
                id: repButton
                width: 131
                height: 70
                anchors.centerIn: parent
                text: "Report"
                colorDefault: "#8698fc"
                textColor: "#ffffff"
                textColorPressed: "#ffffff"
                colorPressed: "#8698fc"
                textColorMouseOver: "#8698fc"
                ac: "root"
                mainWindow: alert.mainWindow
                anchors.verticalCenterOffset: 212
                anchors.horizontalCenterOffset: 270
            }

            AlertButton {
                id: cancleButton
                width: 131
                height: 70
                anchors.centerIn: parent
                text: "Cancel"
                textColorPressed: "#ffffff"
                colorPressed: "#ff0000"
                colorDefault: "#0f0f0f"
                textColor: "#ff0000"
                ac: "Close"
                textColorMouseOver: "#ff0000"
                anchors.verticalCenterOffset: 212
                anchors.horizontalCenterOffset: -260
            }
        }
    }
}
