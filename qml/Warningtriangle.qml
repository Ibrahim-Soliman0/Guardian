import QtQuick 6.5
import QtQuick.Controls 6.5

Item {
    id: warningItem
    width: 300
    height: 300
    property bool animate: false

    Image {
        id: warningIcon
        anchors.centerIn: parent
        source: "../icons_accent/warning.svg"   // Update path if needed.
        fillMode: Image.PreserveAspectFit
        opacity: 1
        scale: 1.0
        rotation: 0

        ParallelAnimation {
            id: parallelAnim
            loops: Animation.Infinite
            running: warningItem.animate   // Bind running to the animate property.
            animations: [
                SequentialAnimation {
                    NumberAnimation { target: warningIcon; property: "scale"; from: 1.0; to: 1.2; duration: 600; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: warningIcon; property: "scale"; from: 1.2; to: 1.0; duration: 600; easing.type: Easing.InOutQuad }
                },
                SequentialAnimation {
                    NumberAnimation { target: warningIcon; property: "rotation"; from: 0; to: 5; duration: 300; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: warningIcon; property: "rotation"; from: 5; to: -5; duration: 600; easing.type: Easing.InOutQuad }
                    NumberAnimation { target: warningIcon; property: "rotation"; from: -5; to: 0; duration: 300; easing.type: Easing.InOutQuad }
                }
            ]
        }
    }
}
