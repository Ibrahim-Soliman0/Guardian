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
    property string currentScreen: "" // Name of the current screen
    property string targetScreen: ""  // Associated screen name for this button

    width: 150
    height: 50

    enabled: currentScreen !== targetScreen // Disable button if already on the target screen

    background: Rectangle {
        color: if(currentScreen === targetScreen){button.textColor}else if (button.hovered) {button.textColor} else{button.bgColor}
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
            source: if(currentScreen === targetScreen){button.backgroundIcon}else if (button.hovered) {button.backgroundIcon} else{button.accentIcon}
            fillMode: Image.PreserveAspectFit
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: button.text
            font.pixelSize: 30
            font.weight: Font.Medium
            color: currentScreen === targetScreen
                   ? button.bgColor // Adjust text color when on the target screen
                   : (button.hovered ? button.bgColor : button.textColor)
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
