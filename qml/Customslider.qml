import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Layouts 6.5
import QtQuick.Window 6.5  // For QTimer

Item {
    id: root

    // Range properties
    property real from: 0
    property real to: 100
    property real value: 50
    property real stepSize: 1

    // New property: key in settings.json to read/update.
    property string settingKey: ""

    // Flag to avoid updating settings during initialization.
    property bool initializing: true

    width: 250
    height: 40

    // The track (background bar)
    Rectangle {
        id: track
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width * 0.8
        height: 15
        radius: 15
        color: "#2A2A2A"
    }

    // Highlight portion (from 'from' up to current value)
    Rectangle {
        id: highlight
        anchors.left: track.left
        anchors.verticalCenter: track.verticalCenter
        height: track.height
        radius: track.radius
        color: "#8698fc"
    }

    // The handle (draggable knob)
    Rectangle {
        id: handle
        anchors.verticalCenter: track.verticalCenter
        width: 35
        height: 35
        radius: width / 2
        color: "#ffffff"
        border.width: 3
        border.color: "#8698fc"
        z: 1

        // Optional: display the current value
        Text {
            anchors.centerIn: parent
            text: Math.round(root.value)
            color: "#8698fc"
            font.pointSize: 10
        }

        // MouseArea for dragging the handle
        MouseArea {
            id: sliderDragArea
            anchors.fill: parent

            onPressed: { moveHandle(mouse) }
            onPositionChanged: { moveHandle(mouse) }

            function moveHandle(mouse) {
                // Convert mouse coordinates into track coordinates
                var posOnTrack = sliderDragArea.mapToItem(track, mouse.x, mouse.y)
                var localX = posOnTrack.x

                // Clamp within the track boundaries
                localX = Math.max(0, Math.min(localX, track.width))

                // Convert to a ratio and then compute new value
                var ratio = localX / track.width
                var newVal = root.from + ratio * (root.to - root.from)

                // Snap to the specified stepSize
                newVal = Math.round(newVal / root.stepSize) * root.stepSize

                // Update slider value (this will trigger onValueChanged)
                root.value = Math.min(Math.max(newVal, root.from), root.to)
            }
        }
    }

    // MouseArea covering the track for direct clicks
    MouseArea {
        id: trackMouseArea
        anchors.fill: track
        onClicked: {
            var localX = mouse.x
            localX = Math.max(0, Math.min(localX, track.width))
            var ratio = localX / track.width
            var newVal = root.from + ratio * (root.to - root.from)
            newVal = Math.round(newVal / root.stepSize) * root.stepSize
            root.value = Math.min(Math.max(newVal, root.from), root.to)
        }
    }

    // Recalculate the handle position and highlight whenever 'from', 'to', or 'value' changes.
    onFromChanged: recalcPosition()
    onToChanged: recalcPosition()
    onValueChanged: {
        recalcPosition()
        // Only update settings if initialization is complete.
        if (!initializing && settingKey !== "" && settingsManager !== undefined) {
            settingsManager.setSetting(settingKey, value)
        }
    }

    function recalcPosition() {
        if (to === from)
            return  // avoid division by zero

        var ratio = (value - from) / (to - from)
        ratio = Math.max(0, Math.min(ratio, 1))
        highlight.width = ratio * (track.width - handle.width) + handle.width / 2
        handle.x = track.x + ratio * (track.width - handle.width)
    }

    Component.onCompleted: {
        console.debug("Component.onCompleted: settingKey=" + settingKey + ", userSettings[settingKey]=" + userSettings[settingKey])
        if (settingKey !== "" && typeof userSettings !== "undefined" && userSettings[settingKey] !== undefined) {
            root.value = Number(userSettings[settingKey])
        }
        console.debug("Initial slider value set to: " + root.value)
        recalcPosition()
        initializing = false
    }
}
