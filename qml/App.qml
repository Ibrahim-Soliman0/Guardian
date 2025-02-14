import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Window

Window {
    id: root
    visible: true
    width: 1000
    height: 700
    title: "My App"
    flags: Qt.FramelessWindowHint | Qt.Window
    color: "transparent"

    property color backgroundColor: "#121212"
    property color menuColor: "#1E1E1E"
    property color accentColor: "#8698fc"
    property color textColor: "#dcd7d5"
    property string currentScreen: "Home"
    property bool collapsed: homebutton.hovered || reportsbutton.hovered || settingsbutton.hovered || aboutbutton.hovered

    // Sidebar layout
    Rectangle {
        id: sidebar
        width: collapsed ? 200 : 60
        Behavior on width { NumberAnimation { duration: 200 } }
        color: menuColor
        anchors.left: parent.left
        anchors.top: titlebar.bottom
        anchors.bottom: parent.bottom

        // Render sidebar as its own layer so it stays visible during transitions.
        layer.enabled: true
        layer.smooth: true
        z: 2

        Column {
            anchors.fill: parent

            Custombutton {
                id: homebutton
                width: parent.width
                height: 70
                text: " Home"
                accentIcon: "../icons_accent/home.png"
                backgroundIcon: "../icons_background/home.png"
                currentScreen: root.currentScreen
                targetScreen: "Home"
                onClicked: {
                    root.currentScreen = "Home";
                    stackview.push("HomeScreen.qml")
                }
            }

            Custombutton {
                id: reportsbutton
                width: parent.width
                height: 70
                text: " Reports"
                accentIcon: "../icons_accent/report.png"
                backgroundIcon: "../icons_background/report.png"
                currentScreen: root.currentScreen
                targetScreen: "Reports"
                onClicked: {
                    root.currentScreen = "Reports";
                    stackview.push("ReportsScreen.qml")
                }
            }

            Custombutton {
                id: settingsbutton
                width: parent.width
                height: 70
                text: " Settings"
                accentIcon: "../icons_accent/setting.png"
                backgroundIcon: "../icons_background/setting.png"
                currentScreen: root.currentScreen
                targetScreen: "Settings"
                onClicked: {
                    root.currentScreen = "Settings";
                    stackview.push("SettingsScreen.qml")
                }
            }

            Custombutton {
                id: aboutbutton
                width: parent.width
                height: 70
                text: " About"
                accentIcon: "../icons_accent/about.png"
                backgroundIcon: "../icons_background/about.png"
                currentScreen: root.currentScreen
                targetScreen: "About"
                onClicked: {
                    root.currentScreen = "About";
                    stackview.push("AboutScreen.qml")
                }
            }
        }
    }

    // Main Content Area
    StackView {
        id: stackview
        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.top: titlebar.bottom
        anchors.bottom: parent.bottom
        initialItem: "HomeScreen.qml"
    }

    // Title bar area
    Rectangle {
        id: titlebar
        width: 1000
        height: 30
        color: menuColor
        z: 2

        Row {
            anchors.fill: parent

            Titlebarbutton {
                id: exitbutton
                width: 40
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                accentIcon: "../icons_accent/exit.png"
                backgroundIcon: "../icons_background/exit.png"
                ac: "Exit"
            }

            Titlebarbutton {
                id: minimizebutton
                width: 40
                anchors.right: exitbutton.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                accentIcon: "../icons_accent/minimize.png"
                backgroundIcon: "../icons_background/minimize.png"
                ac: "Minimize"
            }

            // MouseArea for dragging the window
            MouseArea {
                id: dragArea
                width: parent.width - 80
                height: parent.height
                property point dragStartPosition: Qt.point(0, 0)
                onPressed: {
                    dragStartPosition = Qt.point(mouse.x, mouse.y)
                }
                onPositionChanged: {
                    root.x += mouse.x - dragStartPosition.x
                    root.y += mouse.y - dragStartPosition.y
                }
            }
        }
    }
}
