// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Window
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Window {
    id: window
    width: 1100
    height: 673

    flags: Qt.FramelessWindowHint | Qt.Window
    color: "transparent"

    visible: true
    maximumHeight: 673
    maximumWidth: 1100
    minimumHeight: 673
    minimumWidth: 1100


    title: "Test"

    Image {
        id: imageInstance

        property int radius: 20

        anchors.fill: parent

        source: "file:///C:/Users/moham/Desktop/vecteezy_black-and-gray-background-vector-illustration-lighting_6417811_943/vecteezy_black-and-gray-background-vector-illustration-lighting_6417811-1.jpg"
        fillMode: Image.PreserveAspectCrop
        layer.enabled: true
        layer.effect: OpacityMask {
            id: opacityMaskInstance
            maskSource: Rectangle {
                id: maskedRect
                width: imageInstance.width
                height: imageInstance.height
                radius: imageInstance.radius
            }
        }

    }

    ToggleButton {
        id: toggleButton
        x: 383
        y: 427
        width: 199
        height: 95
    }

    FirstBtn{
            id: bt
            objectName: "Test"
            property int che: 0
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

        onClicked: {
            if (bt.che == 0){
                bt.che = 1
            } else{
                bt.che = 0
            }

            py_mainapp.foo(bt.che)
        }
    }

    ImageBtn{
        width: 100
        height: 100
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: rectangle.right
        anchors.right: rectangle.left
        anchors.bottom: rectangle.top
        anchors.leftMargin: -600
        anchors.rightMargin: -600
        anchors.bottomMargin: -236
        anchors.horizontalCenter: rectangle.horizontalCenter
        anchors.verticalCenterOffset: -164
        anchors.horizontalCenterOffset: 0
    }

    TopBarButton{
        x: 307
        y: 179
        width: 50
        height: 57
    }

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 1100
        height: 100
        color: "#000000"
        opacity: 0


        DragHandler{
            onActiveChanged: if(active){
                                window.startSystemMove()
                            }
        }
    }

}

