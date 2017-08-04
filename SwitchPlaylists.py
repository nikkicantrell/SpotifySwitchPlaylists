import sys
import spotipy
import spotipy.util as util
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.username = '22wgdlnq7jvwbtjn2k5d6upcy'
        self.client_id = '8c0cea4a5b4046f0a063fbcaf5d83df7'
        self.client_secret = 'aa425627988a4ea0ab6b79b1aef5f4e6'
        self.redirect_url = 'https://github.com/nikkicantrell/SpotifySwitchPlaylists'
        self.openWindow()
        self.trackBox = None
        self.scroll = None
        self.displaySongs()
    def openWindow(self):
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(self.username, scope, self.client_id, self.client_secret, self.redirect_url)
        if token == None:
            pass
            #TODO user auth failed
        print ('worked')
        self.user = spotipy.Spotify(auth=token)
        self.playlists = self.user.current_user_playlists()
        self.fromRadioButtons = []
        self.toRadioButtons = []
        playlists = self.playlists
        self.layout = QGridLayout()
        self.toBox = QGroupBox("To: ")
        self.fromBox = QGroupBox("From: ")
        self.layout.addWidget(self.toBox, 0, 1)
        self.layout.addWidget(self.fromBox, 0, 0)
        toBoxLay = QVBoxLayout()
        fromBoxLay = QVBoxLayout()
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                toRadio = QRadioButton(playlist['name'])
                toBoxLay.addWidget(toRadio)
                self.toRadioButtons.append([toRadio, playlist['id']])
                fromRadio = QRadioButton(playlist['name'])
                fromRadio.toggled.connect(lambda: self.displaySongs())
                fromBoxLay.addWidget(fromRadio)
                self.fromRadioButtons.append([fromRadio, playlist['id']])
            if playlists['next']:
                playlists = self.user.next(playlists)
            else:
                playlists = None
        self.toBox.setLayout(toBoxLay)
        self.fromBox.setLayout(fromBoxLay)
        self.setWindowTitle("Spotify Switch Playists App")
        self.setLayout(self.layout)
    def displaySongs(self):
        if self.trackBox:
            self.layout.removeWidget(self.trackBox)
            self.trackBox.setParent(None)
        if self.scroll:
            self.layout.removeWidget(self.scroll)
            self.scroll.setParent(None)
        self.trackBox = QGroupBox("Songs: ")
        self.layout.addWidget(self.trackBox, 1, 0)
        trackBoxLay = QVBoxLayout()
        fromId = None
        toId = None
        songs = False
        for butt in self.fromRadioButtons:
            if butt[0].isChecked():
                fromId = butt[1]
                break
        for butt in self.toRadioButtons:
            if butt[0].isChecked():
                toId = butt[1]
                break
        tracks = self.user.user_playlist(self.username, fromId)['tracks']
        self.trackRadioButtons = []
        while tracks:
            for i, item in enumerate(tracks['items']):
                songs = True
                track = item['track']
                trackRadio = QRadioButton(track['name'] + ' by ' + track['artists'][0]['name'])
                trackBoxLay.addWidget(trackRadio)
                self.trackRadioButtons.append([trackRadio, track['id']])
            if tracks['next']:
                tracks = self.user.next(tracks)
            else:
                tracks = None
        self.trackBox.setLayout(trackBoxLay)
        if songs:
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.trackBox)
            self.layout.addWidget(self.scroll)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())
