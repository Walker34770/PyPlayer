#   LUAN ROCKENBACH DA SILVA
#   26/09/2021
#   Importação das bibliotecas necessárias
import time
from json import JSONDecodeError

import vlc
from tkinter import *
from tkinter import filedialog
from tkinter import font
import json
import os
import time
from mutagen.mp3 import MP3
from colour import Color


#   Initial Variables
player = None
is_playing = None
user_name = os.environ.get("USERNAME")
input_tk = None
new_window = None
letter_input_tk = None
is_paused = None

#   Reading in the json file the last colors player set configurations
try:
    with open('theme.json', 'r', encoding='utf-8', errors='ignore') as jfile:

        reader = json.load(jfile)

        player_bg_color = reader.get('player_bg_color', 'white')
        playlist_viewer_color = reader.get('playlist_viewer_color', 'black')
        playlist_bar_color = reader.get('playlist_bar_color', 'white')
        letter_color = reader.get('letter_color', '#fcb505')
        select_letter_color = reader.get('select_letter_color', 'black')


except FileNotFoundError:
    #   Players colors set variables
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
        music_label.config(text='', bg=player_bg_color, fg=button_bg)
        current_time.config(text='', bg=player_bg_color, fg=button_bg)
        root.title('PyPlayer')

    song_box.delete(ANCHOR)


#   Remove all Songs of the Playlist
def remove_all_songs():
    global player

    player.stop()
    music_label.config(text='', bg=player_bg_color, fg=button_bg)
    current_time.config(text='', bg=player_bg_color, fg=button_bg)
    root.title('PyPlayer')

    song_box.delete(0, END)


#   Get the current time of the playing song
def current_song_length():

    #   Get the current song time (on ms) and convert to sec
    current = player.get_time() / 1000

    # Get the time converted to sec and put it on time format
    current_song_intime_format = time.strftime('%M:%S', time.gmtime(current))
    #   Shows the current time on time format
    current_time.config(text=current_song_intime_format, bg=button_bg)

    current_time.after(1000, current_song_length)

    #   Get the total length of the current song

    total_song_current = song_box.curselection()

    music_name = song_box.get(total_song_current)

    current_song = f'C:/Users/{user_name}/Music/{music_name}.mp3'
    current_song_mp3 = MP3(current_song)

    song_total_length = current_song_mp3.info.length

    length_converted_totime = time.strftime('%M:%S', time.gmtime(song_total_length))

    total_song_time.config(text=' - ' + length_converted_totime, bg=button_bg)


#   Stop Menu button
def stop():
    global player

    player.stop()
    music_label.config(text='', bg=button_bg)
    current_time.config(text='', bg=button_bg)
    root.title('PyPlayer')


#   Play song function
def play():
    global player
    global is_playing
    global is_paused

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

        music_label.config(text=music_name, bg=button_bg)
        is_paused = False
        root.title('PyPlayer - ' + music_name)

        current_song_length()


#   Next song button
def next_song():
    global player
    global is_playing
    global is_paused

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

    music_label.config(text=music_name, bg=button_bg)
    is_paused = False
    root.title('PyPlayer - ' + music_name)

    #   Move selection bar
    song_box.select_clear(0, END)
    song_box.activate(next)
    song_box.select_set(next, last=None)


#   Forward song button
def back_song():
    global player
    global is_playing
    global is_paused

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

    music_label.config(text=music_name, bg=button_bg)
    is_paused = False
    root.title('PyPlayer - ' + music_name)

    #   Move selection bar
    song_box.select_clear(0, END)
    song_box.activate(back)
    song_box.select_set(back, last=None)


#   Pause song function
def pause():
    global player
    global is_paused

    if is_paused is False:
        player.pause()
        is_paused = True
        pause_label.config(text='Paused', bg=button_bg)

    elif is_paused is True:
        player.pause()
        pause_label.config(text='', bg=button_bg)
        is_paused = False


#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS

#   Function to check if an color exist or not
def check_color(color):
    try:
        color = color.replace(' ', '')
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


#   Set the background player color
def bg_color_set():
    global input_tk
    global player_bg_color
    global button_bg

    #   Take the input of the color set window
    player_bg_color = input_tk.get()

    if check_color(player_bg_color) is True:

        try:

            new_window.destroy()

            #   Changing the colors
            root.config(background=player_bg_color)
            controls_frame.config(bg=player_bg_color)
            time_frame.config(bg=player_bg_color)
            volume_frame.config(bg=player_bg_color)

            if player_bg_color != 'black':
                back_btn.config(bg=player_bg_color)
                next_btn.config(bg=player_bg_color)
                pause_btn.config(bg=player_bg_color)
                play_btn.config(bg=player_bg_color)

                plus_btn.config(bg=player_bg_color)
                less_btn.config(bg=player_bg_color)

                music_label.config(bg=player_bg_color)
                pause_label.config(bg=player_bg_color)

                current_time.config(bg=player_bg_color)
                total_song_time.config(bg=player_bg_color)

            if player_bg_color != 'black':
                button_bg = player_bg_color
            else:
                button_bg = 'white'

        except:
            new_window.destroy()

    elif check_color(player_bg_color) is False:
        player_bg_color = 'white'
        new_window.destroy()


# Change player background color
def bg_color():
    global player_bg_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the player background color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'type the color or RGB code Here ')

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
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the music name letters colors", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'type the color or RGB code Here ')

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
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

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
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

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
    global select_letter_color

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
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

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


#   Plus volume function
def plus_volume():
    global player

    current_vol = player.audio_get_volume()
    new_vol = current_vol + 10
    if new_vol <= 100:
        player.audio_set_volume(new_vol)


#   Less volume function
def less_volume():
    global player

    current_vol = player.audio_get_volume()
    new_vol = current_vol - 10

    player.audio_set_volume(new_vol)


#   Buttons background color variable control
if player_bg_color != 'black':
    button_bg = player_bg_color
else:
    button_bg = 'white'

#   Playlist box
song_box = Listbox(root, bg=playlist_viewer_color, fg=letter_color, width=61,
                   selectbackground=playlist_bar_color, selectforeground=select_letter_color)
song_box.pack()

#   Music name label
music_label = Label(root, text='', bg=player_bg_color)
music_label.pack()


#   Song length label
time_frame = LabelFrame(root, bg=player_bg_color, borderwidth=0)
time_frame.pack()

current_time = Label(time_frame, text='', bg=button_bg, borderwidth=0)
total_song_time = Label(time_frame, text='', bg=button_bg, borderwidth=0)

current_time.grid(row=0, column=1, pady=10)
total_song_time.grid(row=0, column=2, pady=10)


#   Pause label
pause_label = Label(root, text='', bg=player_bg_color)
pause_label.pack()


#   Player control buttons images
back_img = PhotoImage(file='back.png')
next_img = PhotoImage(file='next.png')
pause_img = PhotoImage(file='pause.png')
play_img = PhotoImage(file='play.png')

plus_vol = PhotoImage(file='plus.png')
less_vol = PhotoImage(file='subtraction.png')


#   Player control buttons frames
controls_frame = Frame(root, bg=player_bg_color)
controls_frame.pack()

#   Player control buttons
back_btn = Button(controls_frame, image=back_img, borderwidth=0, command=back_song, bg=button_bg)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, command=pause, bg=button_bg)
play_btn = Button(controls_frame, image=play_img, borderwidth=0, command=play, bg=button_bg)
next_btn = Button(controls_frame, image=next_img, borderwidth=0, command=next_song, bg=button_bg)

#   Player control buttons position
back_btn.grid(row=0, column=0, padx=10)
pause_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
next_btn.grid(row=0, column=3, padx=10)


#   Player volume buttons frames
volume_frame = Frame(root, bg=player_bg_color)
volume_frame.pack()

#   Player volume buttons
plus_btn = Button(volume_frame, image=plus_vol, borderwidth=0, bg=button_bg, command=plus_volume)
less_btn = Button(volume_frame, image=less_vol, borderwidth=0, bg=button_bg, command=less_volume)

#   Player volume buttons position
less_btn.grid(row=0, column=1, pady=30, padx=8)
plus_btn.grid(row=0, column=2, pady=30, padx=8)


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


#   Saving color configurations
with open('theme.json', 'w', encoding='utf-8', errors='ignore') as theme_file:
    theme = {}

    #   Giant block of code to verify if the color tha will be save exist
    #   SORRY, I TRY USE AN "FOR" BUT DOESN'T WORK

    if check_color(player_bg_color) is True:
        theme['player_bg_color'] = player_bg_color
    else:
        theme['player_bg_color'] = 'white'

    if check_color(playlist_viewer_color) is True:
        theme['playlist_viewer_color'] = playlist_viewer_color
    else:
        theme['playlist_viewer_color'] = 'black'

    if check_color(playlist_bar_color) is True:
        theme['playlist_bar_color'] = playlist_bar_color
    else:
        theme['playlist_bar_color'] = 'white'

    if check_color(letter_color) is True:
        theme['letter_color'] = letter_color
    else:
        theme['letter_color'] = '#fcb505'

    if check_color(select_letter_color) is True:
        theme['select_letter_color'] = select_letter_color
    else:
        theme['select_letter_color'] = 'black'

    json.dump(theme, theme_file)
