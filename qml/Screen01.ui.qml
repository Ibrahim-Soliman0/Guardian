import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: window
    width: 1100
    height: 700

    flags: Qt.FramelessWindowHint

    visible: true
    maximumHeight: 700
    maximumWidth: 1100
    minimumHeight: 700
    minimumWidth: 1100

    title: "Test"

    FirstBtn{
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
    }

    ImageBtn{
        width: 100
        height: 100
        anchors.verticalCenterOffset: -128
        anchors.horizontalCenterOffset: 0

    }

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 1100
        height: 130
        color: "#000000"
        opacity: 0


        DragHandler{
            onActiveChanged: if(active){
                                window.startSystemMove()
                             }
        }
    }

    TopBarButton{
        x: 389
        y: 6
        width: 50
        height: 57
    }
}