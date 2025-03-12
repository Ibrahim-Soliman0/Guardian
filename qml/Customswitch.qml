import QtQuick 6.5
import QtQuick.Controls.Basic
import QtQuick.Controls.FluentWinUI3

Rectangle {
    id: customSwitch
    width: 100
    height: 40
    radius: height / 2
    color: checked ? root.accentColor : root.menuColor
    border.color: root.accentColor
    border.width: 2

    property bool checked: false
    property real hoverOpacity: 0

    property string settingKey: ""

    Behavior on hoverOpacity {
        NumberAnimation { duration: 300 }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: customSwitch.hoverOpacity = 0.3
        onExited: customSwitch.hoverOpacity = 0
        onClicked: {
            customSwitch.checked = !customSwitch.checked
            if (settingKey !== "" && typeof settingsManager !== "undefined") {
                settingsManager.setSetting(settingKey, customSwitch.checked)
            }
        }
    }

    // Darkening overlay for hover effect
    Rectangle {
        anchors.fill: parent
        color: "grey"
        opacity: customSwitch.hoverOpacity
        radius: parent.radius
    }

    // The switch handle that moves on click
    Rectangle {
        id: handle
        width: parent.height - 8
        height: width
        radius: width / 2
        color: root.textColor
        anchors.verticalCenter: parent.verticalCenter
        x: customSwitch.checked ? parent.width - width - 3 : 3

        Behavior on x {
            NumberAnimation {
                duration: 300
                easing.type: Easing.OutCubic
            }
        }
    }
}