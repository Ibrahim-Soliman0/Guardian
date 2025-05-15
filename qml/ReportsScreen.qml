import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

Rectangle {
    id: root
    width: 940
    height: 670
    visible: true

    property color accentColor: "#8698fc"
    property color backgroundColor: "#121212"


    Popup {
        id: pathPopup
        width: parent.width * 0.8
        height: parent.height * 0.7
        anchors.centerIn: parent
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        background: Rectangle {
            color: "#1E1E1E"
            radius: 5
            border.color: accentColor
        }

        contentItem: ScrollView {
            clip: true
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width
                spacing: 8
                anchors.margins: 10

                Repeater {
                    model: notificationList.currentItem ? notificationList.currentItem.lines : []

                    delegate: ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 8

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 2

                                Text {
                                    text: modelData.split(" - ")[0]
                                    font.pixelSize: 13
                                    color: "#DDDDDD"
                                    wrapMode: Text.Wrap
                                    Layout.fillWidth: true
                                }

                                Text {
                                    text: modelData.split(" - ").length > 1 ? modelData.split(" - ")[1] : ""
                                    font.pixelSize: 12
                                    color: accentColor
                                    wrapMode: Text.Wrap
                                    Layout.fillWidth: true
                                }
                            }

                            Item { Layout.preferredWidth: 8 }

                            Button {
                                id: locateBtn
                                text: "Locate"
                                font.pixelSize: 15
                                contentItem: Text {
                                    text: parent.text
                                    font: parent.font
                                    color: locateBtn.hovered ? backgroundColor : accentColor
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                background: Rectangle {
                                    color: locateBtn.hovered ? accentColor : backgroundColor
                                    Behavior on color {
                                        ColorAnimation {
                                            duration: 300
                                            easing.type: Easing.OutQuint
                                        }
                                    }
                                    radius: 4
                                    border.color: accentColor
                                    border.width: 1
                                }
                                onClicked: {
                                    var fullPath = modelData.split(" - ")[0].trim()
                                    var folderPath = fullPath.substring(0, fullPath.lastIndexOf("\\"))
                                    Qt.openUrlExternally("file:///" + folderPath)
                                }
                            }
                        }

                        // Separator line
                        Rectangle {
                            Layout.fillWidth: true
                            height: 1
                            color: accentColor
                            opacity: 0.4
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        color: backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                height: 60
                color: backgroundColor

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16

                    Label {
                        text: "Alert Notifications"
                        font.pixelSize: 20
                        font.bold: true
                        color: accentColor
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Label {
                        text: "| Total Alerts: " + notificationList.count
                        font.pixelSize: 20
                        color: accentColor
                    }

                    Item { Layout.fillWidth: true }

                    Button {
                        id: dismissAllButton
                        text: "Dismiss All"
                        font.pixelSize: 14
                        flat: true
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: dismissAllButton.hovered ? backgroundColor : accentColor
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle {
                            color: dismissAllButton.hovered ? accentColor : backgroundColor
                            Behavior on color {
                                ColorAnimation {
                                    duration: 300
                                    easing.type: Easing.OutQuint
                                }
                            }
                            radius: 4
                            border.color: accentColor
                            border.width: 1
                        }
                        onClicked: {
                            alertProcessor.clear_alerts()
                        }
                    }
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ListView {
                    id: notificationList
                    model: ListModel {}
                    spacing: 8
                    boundsBehavior: Flickable.StopAtBounds

                    delegate: Item {
                        width: notificationList.width
                        height: contentColumn.height + 24

                        property string paths: model.paths || ""
                        property var lines: paths
                            .split("\n")
                            .filter(function(p) { return p.trim().length > 0 })

                        Rectangle {
                            width: parent.width - 20
                            height: contentColumn.height + 24
                            color: "#1E1E1E"
                            radius: 5
                            anchors.horizontalCenter: parent.horizontalCenter

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    notificationList.currentIndex = index
                                    pathPopup.open()
                                }
                            }
                        }

                        ColumnLayout {
                            id: contentColumn
                            width: parent.width - 32
                            anchors.centerIn: parent
                            spacing: 8

                            RowLayout {
                                Layout.fillWidth: true

                                Label {
                                    text: model.process
                                    font.pixelSize: 18
                                    font.bold: true
                                    color: accentColor
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                }

                                Label {
                                    text: model.timestamp
                                    font.pixelSize: 15
                                    font.bold: true
                                    color: accentColor
                                    horizontalAlignment: Text.AlignRight
                                    Layout.alignment: Qt.AlignRight
                                }

                            }

                            RowLayout {
                                Layout.fillWidth: true

                                Label {
                                    text: lines.length + " sensitive paths detected"
                                    font.pixelSize: 15
                                    color: "#ffffff"
                                    wrapMode: Text.Wrap
                                    Layout.fillWidth: true
                                }

                                Label {
                                    text: "Detected in " + model.elapsed
                                    font.pixelSize: 15
                                    color: "#ffffff"
                                    horizontalAlignment: Text.AlignLeft
                                    Layout.leftMargin: -420
                                }

                                Button {
                                    id: dismissOne
                                    text: "Dismiss"
                                    font.pixelSize: 15
                                    flat: true
                                    contentItem: Text {
                                        text: parent.text
                                        font: parent.font
                                        color: dismissOne.hovered ? backgroundColor : accentColor
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    background: Rectangle {
                                        color: dismissOne.hovered ? accentColor : backgroundColor
                                        Behavior on color {
                                            ColorAnimation {
                                                duration: 300
                                                easing.type: Easing.OutQuint
                                            }
                                        }
                                        radius: 4
                                        border.color: accentColor
                                        border.width: 1
                                    }
                                    onClicked: {
                                        alertProcessor.clearProcess(model.process)
                                        notificationList.model.remove(index)
                                    }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                height: 1
                                color: accentColor
                            }
                        }
                    }
                }
            }
        }
    }

    onActiveFocusChanged: if (activeFocus) {
        notificationList.model.clear()
        alertProcessor.initialize()
    }

    Component.onCompleted: {
        alertProcessor.initialize()
    }

    Connections {
        target: alertProcessor

        function onNewAlert(process_name, paths, timestamp, elapsed) {
            notificationList.model.append({
                process:   process_name,
                paths:     paths || "",
                timestamp: timestamp,
                elapsed:   elapsed
            })
        }

        function onAlertsCleared() {
            notificationList.model.clear()
        }
    }
}
