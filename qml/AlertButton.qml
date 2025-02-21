import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Shapes

Button {
    id: alertButton

    property color colorDefault: "#8698fc"
    property color colorMouseOver: "#cccccc"
    property color colorPressed: "#333333"
    property color textColor: "#FFFFFF"
    property color textColorMouseOver: "#FFCC00"
    property color textColorPressed: "#FF0000"

    flat: true

    signal clickedToPython

    property string ac: ""
    property var mainWindow

    QtObject {
        id: internal
        property var dynamicColor: alertButton.down ? colorPressed : (alertButton.hovered ? colorMouseOver : colorDefault)
        property var dynamicSize: alertButton.hovered ? 20 : 15
        property color dynamicTextColor: alertButton.down ? textColorPressed : (alertButton.hovered ? textColorMouseOver : textColor)
    }

    text: qsTr("firstBtn")
    implicitWidth: 150
    implicitHeight: 70

    background: Rectangle {
        id: bgRect
        anchors.fill: parent
        radius: internal.dynamicSize
        color: internal.dynamicColor
        Behavior on color {
            ColorAnimation { duration: 100 }
        }
        Behavior on radius {
            NumberAnimation { duration: 300 }
        }
    }

    contentItem: Item {
        id: item1
        anchors.centerIn: parent

        Text {
            id: textBtn
            text: alertButton.text
            font.pointSize: 17
            font.styleName: "Bold"
            color: internal.dynamicTextColor
            anchors.centerIn: parent
            Behavior on color {
                ColorAnimation { duration: 100 }
            }
        }
    }

    onClicked: {
        if (ac === "Close") {
            alert.visible = false;
        }
        else{
            alert.visible = false;
            if (mainWindow) {
                mainWindow.currentScreen = "Settings";
                mainWindow.stackview.push("SettingsScreen.qml");
                mainWindow.show();
            }
        }
    }
}
