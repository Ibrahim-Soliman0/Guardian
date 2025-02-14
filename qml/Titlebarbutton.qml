import QtQuick 6.5
import QtQuick.Controls.Basic
import QtQuick.Shapes

Button {
    id: button
    // Custom properties
    property string accentIcon: "" // Default image
    property string backgroundIcon: "" // Image to show on hover
    property color bgColor: root.menuColor
    property color textColor: root.accentColor
    property string ac: ""

    width: 150
    height: 50
    background: Rectangle {
        color: button.hovered ? button.textColor : button.bgColor
        Behavior on color {
            ColorAnimation {
                duration: 300
            }
        }
    }

    contentItem: Row {
        id: row
        anchors.centerIn: parent

        Image {
            id: buttonIcon
            anchors.centerIn: parent
            width: 24
            height: 24
            source: button.hovered ? button.backgroundIcon : button.accentIcon
            fillMode: Image.PreserveAspectFit
        }
    }

    onClicked: if(ac === "Exit"){root.close()} else{root.hide()}
}
