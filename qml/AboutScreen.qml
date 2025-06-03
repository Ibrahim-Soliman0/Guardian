import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects

Rectangle {
    id: aboutScreen
    width: 940
    height: 670
    color: root.backgroundColor
    focus: false
    antialiasing: true
    anchors.fill: parent

    property color accentColor: "#8698fc"
    property string versionNumber: "1.0.0" // Placeholder version number

    Image {
        id: logoPlaceholder
        width: 150
        height: 150
        source: "../icons_accent/StaticLogo.png"
        anchors.horizontalCenterOffset: 0
        fillMode: Image.PreserveAspectFit
        anchors.horizontalCenter: parent.horizontalCenter
        y: 16  // Start at top
    }

    Text {
        id: titleText
        text: "GUARDIAN"
        font.letterSpacing: 4
        font.pixelSize: 40
        font.bold: true
        color: accentColor
        anchors.horizontalCenter: parent.horizontalCenter
        y: logoPlaceholder.y + logoPlaceholder.height + 8

        DropShadow {
            horizontalOffset: 0
            verticalOffset: 0
            radius: 15.0 // Increased radius for more diffuse glow
            samples: 24  // Increased samples for smoother glow
            color: "#8698fc"
            spread: 0.2 // Added spread for slight intensity boost near text
        }
    }

    Text {
        id: versionText
        text: "Version: " + aboutScreen.versionNumber
        color: "#aaaaaa"
        font.pixelSize: 20
        anchors.horizontalCenter: parent.horizontalCenter
        y: titleText.y + titleText.implicitHeight + 10
    }

    Text {
        id: descriptionText
        text: "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Segoe UI'; font-size:9.75pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700; color:#8698fc;\">Guardian</span><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700;\"> protects your system from </span><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700; color:#8698fc;\">Information Stealers</span><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700;\"> and </span><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700; color:#8698fc;\">Ransomwares</span><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700;\">.</span></p>\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Arial'; font-size:16pt;\"><br /></p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Arial'; font-size:16pt; font-weight:700;\">It employs a behavior-based approach, intercepting potentially harmful file operations performed by processes using Windows API hooking techniques.</span></p></body></html>"
        color: "#ffffff"
        wrapMode: Text.WordWrap
        textFormat: Text.RichText
        font.family: "Arial"
        width: aboutScreen.width * 0.7
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenter: parent.horizontalCenter
        y: versionText.y + versionText.implicitHeight + 20
    }



    Rectangle {
        id: aboutText
        width: aboutScreen.width * 0.4
        height: 1
        color: "#444444"
        anchors.horizontalCenter: parent.horizontalCenter
        y: descriptionText.y + descriptionText.implicitHeight + 20
    }

    Text {
        id: creatorsTitle
        text: "Creators:-"
        font.pixelSize: 25
        font.family: "Arial"
        font.bold: true
        color: "#8698fc"
        anchors.horizontalCenter: parent.horizontalCenter
        y: aboutText.y + aboutText.implicitHeight + 20
    }

        Column {
            id: creatorsList
            spacing: 5
            anchors.horizontalCenter: parent.horizontalCenter
            y: creatorsTitle.y + creatorsTitle.implicitHeight + 10
            Text { text: "- Mohamed Elmasry"; color: "#ffffff"; font.pixelSize: 23; font.family: "Arial"; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter }
            Text { text: "- Ibrahim Soliman"; color: "#ffffff"; font.pixelSize: 23; font.family: "Arial"; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter }
            Text { text: "- Ahmed Abdallah"; color: "#ffffff"; font.pixelSize: 23; font.family: "Arial"; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter }
            Text { text: "- Omar Tamer"; color: "#ffffff"; font.pixelSize: 23; font.family: "Arial"; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter }
        }
}

