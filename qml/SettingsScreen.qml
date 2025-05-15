import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Controls.Material 6.5

Rectangle {
    width: 940
    height: 670
    color: root.backgroundColor
    focus: false
    antialiasing: true
    anchors.fill: parent

    property int isActiveAutoStart: userSettings.isActiveAutoStart
    property int isActiveMinimizedInSystemTray: userSettings.isActiveMinimizedInSystemTray
    property int isActiveSendData: userSettings.isActiveSendData
    property int maximumLogFileSize: userSettings.MaximumLogFileSize
    property int ransomInterval: userSettings.RansomInterval
    property int infoInterval: userSettings.InfoInterval

    Flickable {
        id: flickable
        anchors.fill: parent
        contentHeight: settingsColumn.height
        flickableDirection: Flickable.Vertical
        clip: true

        Column {
            id: settingsColumn
            width: flickable.width
            spacing: 15
            Item { width: 1; height: 5 } // Acts as top padding

            // Auto start block
            Rectangle {
                width: parent.width - 30
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10


                    Text {
                        text: " Auto start on system boot"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - autoStartSwitch.height /2
                    }

                    Customswitch {
                        id: autoStartSwitch
                        height: 35
                        width: 70
                        checked: isActiveAutoStart
                        settingKey: "isActiveAutoStart"
                        x: parent.width - autoStartSwitch.width - 90
                        y: parent.height/2 - autoStartSwitch.height /2
                        }
                }
            } // Auto start block end

            // Start minimized block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Start minimized in system tray"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - startMinimizedSwitch.height /2
                    }

                    Customswitch {
                        id: startMinimizedSwitch
                        height: 35
                        width: 70
                        checked: isActiveMinimizedInSystemTray
                        settingKey: "isActiveMinimizedInSystemTray"
                        x: parent.width - startMinimizedSwitch.width - 90
                        y: parent.height/2 - startMinimizedSwitch.height /2
                    }
                }
            } // Start minimized block end

            // Start send data block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Send logs to the server"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - startMinimizedSwitch.height /2
                    }

                    Customswitch {
                        id: sendData
                        height: 35
                        width: 70
                        checked: isActiveSendData
                        settingKey: "isActiveSendData"
                        x: parent.width - sendData.width - 90
                        y: parent.height/2 - sendData.height /2
                    }
                }
            } // End Start send data

            // Start send data block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Auto update the application"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - startMinimizedSwitch.height /2
                    }

                    Customswitch {
                        id: autoUpdate
                        height: 35
                        width: 70
                        checked: isActiveSendData
                        settingKey: "AutoUpdate"
                        x: parent.width - autoUpdate.width - 90
                        y: parent.height/2 - autoUpdate.height /2
                    }
                }
            } // End Start send data

            // Start storage slider block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Maximum log file size (in MB)"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - storageSlider.height /2
                    }

                    Customslider{
                        id: storageSlider
                        from: 0
                        to: 50
                        value: 0
                        stepSize: 1
                        x: parent.width - storageSlider.width
                        y: parent.height/2 - storageSlider.height /2
                        settingKey: "MaximumLogFileSize"
                    }
                }
            } // End storage slider

            // Start ransom slider block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Interval between each ransomware check"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - ransomSlider.height /2
                    }

                    Customslider{
                        id: ransomSlider
                        from: 0
                        to: 50
                        value: 0
                        stepSize: 1
                        x: parent.width - ransomSlider.width
                        y: parent.height/2 - ransomSlider.height /2
                        settingKey: "RansomInterval"
                    }
                }
            } // End ransom slider

            // Start info slider block
            Rectangle {
                width: parent.width - 30  // Reduce width for left/right padding
                height: 50
                radius: 10
                color: root.menuColor
                anchors.horizontalCenter: parent.horizontalCenter

                Row {
                    width: parent.width
                    anchors.fill: parent
                    spacing: 10

                    Text {
                        text: " Interval between each info stealer check"
                        font.pixelSize: 25
                        color: root.textColor
                        y: parent.height/2 - infoSlider.height /2
                    }

                    Customslider{
                        id: infoSlider
                        from: 0
                        to: 50
                        value: 0
                        stepSize: 1
                        x: parent.width - infoSlider.width
                        y: parent.height/2 - infoSlider.height /2
                        settingKey: "InfoInterval"
                    }
                }
            } // End info slider

            // Add bottom padding using an Item
            Item { width: 1; height: 5 }
        }
    }
}
