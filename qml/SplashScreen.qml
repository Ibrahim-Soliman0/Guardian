import QtQuick
import QtQuick.Controls

Window {
    id: splashScreen
    width: 600
    height: 400
    visible: true
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint // Frameless and always on top
    color: "transparent" // Transparent background

    Rectangle {
        anchors.fill: parent
        color: "transparent" // Transparent background
        radius: 20

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                text: "My Application"
                font.pixelSize: 24
                color: "white"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
