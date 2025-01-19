import QtQuick
import QtQuick.Controls.Basic


Item {
    function handleButtonClick() {
        imageButton.scale = 1.5
    }

    id: imageButton
    width: 90
    height: 150
    anchors.centerIn: parent

    Image {
        id: buttonImage
        anchors.fill: parent
        source: "file:///C:/Users/moham/Desktop/pngwing.com.png" // Replace with your image file path
        opacity: mouseArea.pressed ? 0.6 : mouseArea.containsMouse ? 0.8 : 1.0
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        onClicked: {
            handleButtonClick()
        }
    }
}

