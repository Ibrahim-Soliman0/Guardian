import QtQuick
import QtQuick.Controls.Basic

Button {
    id: firstBtn

    property color colorDefault: "#55aaff"
    property color colorMouseOver: "#cccccc"
    property color colorPressed: "#333333"

    flat: true

    signal clickedToPython // Signal to notify Python

    QtObject {
        id: internal

        property var dynamicColor: if (firstBtn.down) {
                                       firstBtn.down ? colorPressed : colorDefault
                                   } else {
                                       firstBtn.hovered ? colorMouseOver : colorDefault
                                   }

        property var dynamicSize: if (firstBtn.hovered) {
                                       firstBtn.hovered ? 15 : 10
                                   } else {
                                       10
                                   }
    }

    text: qsTr("firstBtn")
    implicitWidth: 150
    implicitHeight: 70

    background: Rectangle {
        radius: internal.dynamicSize
        color: internal.dynamicColor
    }

    contentItem: Item {
        id: item1
        Text {
            id: textBtn
            text: firstBtn.text
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#ffffff"
        }
    }

    onClicked: {
        console.log("Signal clickedToPython emitted")
        clickedToPython() // Emit signal when clicked
    }
}
