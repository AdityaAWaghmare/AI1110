import os
import numpy as np
import tkinter as tk
import pygame

# Path to the directory containing the songs
SONGS_DIR = "songs"

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.played_songs = []
        self.current_song = None
        self.paused = False

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Create UI elements
        self.song_label = tk.Label(root, text="No song playing")
        self.song_label.pack()

        self.play_button = tk.Button(root, text="Play", command=self.play_song)
        self.play_button.pack()

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_song)
        self.pause_button.pack()

        self.resume_button = tk.Button(root, text="Resume", command=self.resume_song)
        self.resume_button.pack()

        self.shuffle_button = tk.Button(root, text="Shuffle", command=self.shuffle_songs)
        self.shuffle_button.pack()

        self.forward_button = tk.Button(root, text="Forward", command=self.play_next_song)
        self.forward_button.pack()

    def play_song(self):
        # Stop the currently playing song
        if self.current_song:
            pygame.mixer.music.stop()

        # Get a random song from the directory
        songs = os.listdir(SONGS_DIR)
        if not songs:
            self.song_label.configure(text="No songs found")
            return

        available_songs = [song for song in songs if song not in self.played_songs]

        if not available_songs:
            self.song_label.configure(text="No other songs to play")
            return

        song = np.random.choice(available_songs)
        song_path = os.path.join(SONGS_DIR, song)

        # Play the selected song
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.paused = False

        self.played_songs.append(song)
        self.current_song = song
        self.song_label.configure(text="Now playing: " + song)

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True

    def resume_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def shuffle_songs(self):
        # Stop the currently playing song
        if self.current_song:
            pygame.mixer.music.stop()

        # Shuffle the songs list
        songs = os.listdir(SONGS_DIR)
        np.random.shuffle(songs)

        if not songs:
            self.song_label.configure(text="No songs found")
            return

        self.played_songs = []
        song_path = os.path.join(SONGS_DIR, songs[0])
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.paused = False

        self.played_songs.append(songs[0])
        self.current_song = songs[0]
        self.song_label.configure(text="Now playing: " + songs[0])

    def play_next_song(self):
        if self.current_song:
            self.play_song()

# Create the main application window
root = tk.Tk()
root.title("Music Player")

# Create an instance of the MusicPlayer class
music_player = MusicPlayer(root)

# Start the main UI event loop
root.mainloop()

