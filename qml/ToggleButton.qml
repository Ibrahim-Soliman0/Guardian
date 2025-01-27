import QtQuick
import QtQuick.Controls

Rectangle {
    id: toggleButton
    width: 400
    height: 150
    radius: height / 2 // Rounded corners for the button
    color: toggleState ? "#4CAF50" : "#CCC" // Background color based on state
    clip: true // Clip child elements to the parent shape

    property bool toggleState: false // Toggle state (on/off)

    // Knob for the toggle button
    Rectangle {
        id: knob
        width: parent.height - 10
        height: parent.height - 10
        radius: width / 2
        color: "white"
        anchors.verticalCenter: parent.verticalCenter
        x: toggleState ? parent.width - width - 5 : 5

        Behavior on x { // Smooth transition when toggling
            NumberAnimation {
                duration: 200
                easing.type: Easing.InOutQuad
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            toggleState = !toggleState // Toggle the state
            console.log("Toggle State:", toggleState)
            py_mainapp.foo("Test")
        }
    }
}
