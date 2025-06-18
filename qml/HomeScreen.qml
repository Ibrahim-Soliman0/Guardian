import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Controls.Material 6.5

Rectangle {
    width: 940
    height: 670
    color: root.backgroundColor
    focus: false
    antialiasing: true
    anchors.fill: parent
    property string currentScreen: "Home"
    property int isMonitoringActive: userSettings.isMonitoringActive

    Customswitch {
        id: customswitch
        width: 150
        height: 60
        x: parent.width / 2 - customswitch.width / 2
        y: parent.height / 1.7
        checked: isMonitoringActive
        settingKey: "isMonitoringActive"
    }


    Image {
        id: shieldIconAccent
        x: parent.width / 2 - shieldIconAccent.width / 2
        y: 100
        width: 256
        height: 256
        smooth: true
        sourceSize: Qt.size(256, 256)
        source: "../icons_accent/ON_Shield.svg"
        fillMode: Image.PreserveAspectFit
        antialiasing: true
        opacity: customswitch.checked ? 1 : 0
        Behavior on opacity {
            NumberAnimation {
                duration: 200
            }
        }
    }

    Image {
        id: shieldIconBackground
        x: parent.width / 2 - shieldIconBackground.width / 2
        y: 100
        width: 256
        height: 256
        smooth: true
        sourceSize: Qt.size(256, 256)
        source: "../icons_accent/OFF_Shield.svg"
        fillMode: Image.PreserveAspectFit
        antialiasing: true
        opacity: customswitch.checked ? 0 : 1
        Behavior on opacity {
            NumberAnimation {
                duration: 100
            }
        }
    }
    Text {
        id: onOffText
        x: parent.width / 2 - 30 - onOffText.width / 2
        y: 490
        text: "Active Monitoring Is "
        font.pixelSize: 40
        color: "#ffffff"
        Behavior on color {
            ColorAnimation {
                duration: 200
            }
        }
    }
    Text {
        id: onOffPart
        x: parent.width / 2 - 30 + onOffText.width / 2
        y: 490
        text: customswitch.checked ? "ON" : "OFF"
        font.pixelSize: 40
        color: customswitch.checked ? root.accentColor : "#FF0000"
        Behavior on color {
            ColorAnimation {
                duration: 250
            }
        }
    }
}
