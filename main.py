#   LUAN ROCKENBACH DA SILVA
#   26/09/2021
#   Importação das bibliotecas necessárias
import vlc
from tkinter import *
from tkinter import filedialog
from tkinter import font
import os

#   variáveis
player = None
is_playing = None
user_name = os.environ.get("USERNAME")
input_tk = None
new_window = None
letter_input_tk = None

#   Player colors set variables
player_bg_color = 'white'
playlist_viewer_color = 'black'
playlist_bar_color = 'white'
letter_color = '#fcb505'
select_letter_color = 'black'

#   Stating Tkinter window
root = Tk()
root.title("PyPlayer")
root.iconbitmap('music-notes.ico')
root.geometry('350x500')
root['bg'] = player_bg_color


#   Add song function
def add_song():
    global user_name

    song_dir = filedialog.askopenfilename(initialdir=f'C:\\Users\\{user_name}\\Music\\', title='Choose A Song')

    #   Removing file path and .mp3 from music name to show in listbox
    song = song_dir.replace(f'C:/Users/{user_name}/Music/', '')
    song = song.replace('.mp3', '')
    song_box.insert(END, song)

    #   Turning song box strings into bold
    bolded = font.Font(weight='bold', size='10')  # will use the default font
    song_box.config(font=bolded)


#   Add many songs to the playlist
def add_many_songs():
    songs_dir = filedialog.askopenfilenames(initialdir=f'C:\\Users\\{user_name}\\Music\\', title='Choose Many Songs')

    #   Loop for remove file path and .mp3 from many music names to show in listbox
    for song in songs_dir:
        song = song.replace(f'C:/Users/{user_name}/Music/', '')
        song = song.replace('.mp3', '')
        song_box.insert(END, song)


#   Remove Song Menu
def remove_song():
    global is_playing
    global player

    if is_playing == song_box.get(ACTIVE):
        player.stop()

    song_box.delete(ANCHOR)


#   Remove all Songs of the Playlist
def remove_all_songs():
    global player

    player.stop()

    song_box.delete(0, END)


#   Stop Menu button
def stop():
    global player

    player.stop()


#   Play song function
def play():
    global player
    global is_playing

    if song_box.get(ACTIVE) == is_playing:
        pass
    else:
        try:
            player.stop()
        except:
            pass
        music_name = song_box.get(ACTIVE)
        song = f'C:/Users/{user_name}/Music/{music_name}.mp3'
        player = vlc.MediaPlayer(song)
        player.play()
        is_playing = music_name


#   Next song button
def next_song():
    global player
    global is_playing

    #   Get the current song tuple number
    next = song_box.curselection()
    #   Add one to the current song
    next = next[0] + 1
    # Discover the nome of next song
    music_name = song_box.get(next)

    song = f'C:/Users/{user_name}/Music/{music_name}.mp3'
    try:
        player.stop()
    except:
        pass
    player = vlc.MediaPlayer(song)
    player.play()
    is_playing = music_name

    #   Move selection bar
    song_box.select_clear(0, END)
    song_box.activate(next)
    song_box.select_set(next, last=None)


#   Foward song button
def back_song():
    global player
    global is_playing

    #   Get the current song tuple number
    back = song_box.curselection()
    #   Add one to the current song
    back = back[0] - 1
    # Discover the nome of next song
    music_name = song_box.get(back)

    song = f'C:/Users/{user_name}/Music/{music_name}.mp3'
    try:
        player.stop()
    except:
        pass
    player = vlc.MediaPlayer(song)
    player.play()
    is_playing = music_name

    #   Move selection bar
    song_box.select_clear(0, END)
    song_box.activate(back)
    song_box.select_set(back, last=None)


#   Pause song function
def pause():
    global player

    player.pause()


#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS

#   Set the background player color
def bg_color_set():
    global input_tk
    global player_bg_color

    try:

        #   Take the input od the color set window
        player_bg_color = input_tk.get()
        new_window.destroy()

        #   Changing the colors
        root.config(background=player_bg_color)
        controls_frame.config(bg=player_bg_color)

        if player_bg_color != 'black':
            back_btn.config(bg=player_bg_color)
            next_btn.config(bg=player_bg_color)
            pause_btn.config(bg=player_bg_color)
            play_btn.config(bg=player_bg_color)

    except:
        new_window.destroy()


# Change player backgroud color
def bg_color():
    global player_bg_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    new_window['bg'] = player_bg_color

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the player background color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=bg_color_set)
    button.pack()

    new_window.mainloop()


#   Set the letters colors
def letter_color_set():
    global letter_color

    try:

        #   Take the input od the color set window
        letter_color = input_tk.get()
        new_window.destroy()

        #   Changing the colors
        song_box.config(fg=letter_color)

    except:
        new_window.destroy()


#   Change the letters color
def lt_color():
    global letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    new_window['bg'] = player_bg_color

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the music name letters colors", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=letter_color_set)
    button.pack()

    new_window.mainloop()


def viewer_color_set():
    global playlist_viewer_color

    try:

        #   Take the input od the color set window
        playlist_viewer_color = input_tk.get()
        new_window.destroy()

        #   Changing the colors
        song_box.config(bg=playlist_viewer_color)

    except:
        new_window.destroy()


#   Change the letters color
def viewer_color():
    global letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    new_window['bg'] = player_bg_color

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the playlist viewer color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=viewer_color_set)
    button.pack()

    new_window.mainloop()


#   Set the color od the selection bar
def bar_color_set():
    global playlist_bar_color

    try:

        #   Take the input od the color set window
        playlist_bar_color = input_tk.get()
        new_window.destroy()

        #   Changing the colors
        song_box.config(selectbackground=playlist_bar_color)

    except:
        new_window.destroy()


#   Change the bar color
def bar_color():
    global playlist_bar_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    new_window['bg'] = player_bg_color

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the playlist bar color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=bar_color_set)
    button.pack()

    new_window.mainloop()


#   Set the color od the selection bar
def slc_ltt_color_set():
    global playlist_bar_color

    try:

        #   Take the input od the color set window
        select_letter_color = input_tk.get()
        new_window.destroy()

        #   Changing the colors
        song_box.config(selectforeground=select_letter_color)

    except:
        new_window.destroy()


#   Change the selected letter color
def slc_letter_color():
    global select_letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    new_window['bg'] = player_bg_color

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the selected letter color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=slc_ltt_color_set)
    button.pack()

    new_window.mainloop()


#   END OF THE PERSONALIZATION FUNCTIONS
#   END OF THE PERSONALIZATION FUNCTIONS
#   END OF THE PERSONALIZATION FUNCTIONS


#   Playlist box
song_box = Listbox(root, bg=playlist_viewer_color, fg=letter_color, width=61,
                   selectbackground=playlist_bar_color, selectforeground=select_letter_color)
song_box.pack()

#   Player control buttons images
back_img = PhotoImage(file='back.png')
next_img = PhotoImage(file='next.png')
pause_img = PhotoImage(file='pause.png')
play_img = PhotoImage(file='play.png')


#   Player control buttons frames
controls_frame = Frame(root, bg=player_bg_color)
controls_frame.pack(pady=120)

#   Player control buttons
back_btn = Button(controls_frame, image=back_img, borderwidth=0, command=back_song, bg=player_bg_color)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, command=pause, bg=player_bg_color)
play_btn = Button(controls_frame, image=play_img, borderwidth=0, command=play, bg=player_bg_color)
next_btn = Button(controls_frame, image=next_img, borderwidth=0, command=next_song, bg=player_bg_color)


#   Player control buttons position
back_btn.grid(row=0, column=0, padx=10)
pause_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
next_btn.grid(row=0, column=3, padx=10)


#   Player Menu
my_menu = Menu(root)
root.config(menu=my_menu)


#   Add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label='Add one song to the playlist', command=add_song)

#   Add many songs menu
add_song_menu.add_command(label='Add many songs to the playlist', command=add_many_songs)


#   Remove song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label='Remove one song to the playlist', command=remove_song)

#   Remove many songs menu
remove_song_menu.add_command(label='Remove all songs of the playlist', command=remove_all_songs)


#   Stop menu
my_menu.add_command(label='Stop', command=stop)


# Colors set menu
set_color_menu = Menu(my_menu)
my_menu.add_cascade(label='Colors', menu=set_color_menu)
set_color_menu.add_command(label='Background color', command=bg_color)
set_color_menu.add_command(label='Letters color', command=lt_color)
set_color_menu.add_command(label='Playlist Viewer color', command=viewer_color)
set_color_menu.add_command(label='Playlist Bar Color', command=bar_color)
set_color_menu.add_command(label='Selected letter color', command=slc_letter_color)

root.mainloop()
