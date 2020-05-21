#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
import threading
import requests

from data_providers import *

class LibraryWidget(Gtk.FlowBox):
    def __init__(self):
        Gtk.FlowBox.__init__(self)
        self.set_homogeneous(True)
        self.set_row_spacing(10)
        self.set_valign(Gtk.Align.START)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_max_children_per_line(100)

class MovieWidget(Gtk.Box):
    def __init__(self, title, year, poster):
        Gtk.EventBox.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.set_halign(Gtk.Align.CENTER)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(poster, 150, 200, True)
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)

        if len(title) > 20:
            title = title[:20] + '..'

        self.title_label = Gtk.Label(label=title)
        self.year_label = Gtk.Label(label=str(year))
        self.year_label.get_style_context().add_class('grey')

        self.title_label.set_halign(Gtk.Align.START)
        self.year_label.set_halign(Gtk.Align.START)
        self.image.set_halign(Gtk.Align.CENTER)

        self.pack_start(self.image, False, False, 0)
        self.pack_start(self.title_label, False, False, 0)
        self.pack_start(self.year_label, False, False, 0)
        self.set_can_focus(False)
        self.show()

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="moviemate")
        self.set_default_size(1000, 600)
        self.connect("destroy", Gtk.main_quit)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.notebook.append_page(Gtk.Label(label='hey'),
                                  Gtk.Label(label="Library"))

        self.add(self.notebook)

        self.init_discover_widget()

        self.move(10, 10)
        Window._style()
        self.show_all()

    def init_discover_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui_data/discover_widget.glade")
        builder.add_from_file("ui_data/movies_widget.glade")
        discover_search = builder.get_object('discover_search')
        discover_search.connect('search-changed', self.discover_search)
        self.discover_movies_widget = builder.get_object('movies_widget')
        movies_widget_viewport = builder.get_object('movies_widget_viewport')
        movies_widget_viewport.add(self.discover_movies_widget)
        self.notebook.append_page(builder.get_object('discover_widget'),
                                  Gtk.Label(label='Discover'))

    def discover_search(self, search_entry):
        text = search_entry.get_text()
        if text == '':
            return
        self.async_add_movies_from_search(text, self.discover_movies_widget)

    def async_add_movies_from_search(self, query, movies_widget):
        thread = threading.Thread(target=self.add_movies_from_search, args=(query,
                                                                            movies_widget))
        thread.start()

    def add_movies_from_search(self, query, movies_widget):
        for movie_widget in movies_widget.get_children():
            self.movies_widget.remove(movie_widget)
        c = OMDbClient()
        movies = c.search(query)
        for movie in movies:
            image_url = movie.poster
            r = requests.get(image_url)
            fname = image_url.split('/')[-1]
            with open(fname, 'wb') as image_file:
                image_file.write(r.content)
            movie.poster = fname
            self.safe_add_movie(movie, movies_widget)

    def safe_add_movie(self, movie, movies_widget):
        GLib.idle_add(self.add_movie, movie, movies_widget)

    def add_movie(self, movie, movies_widget):
        movie_widget = MovieWidget(movie.title, movie.year, movie.poster)
        movies_widget.add(movie_widget)
        self.show_all()

    def _style():
        with open('style.css') as style_file:
            css = style_file.read().encode()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

if __name__ == '__main__':
    win = Window()
    Gtk.main()
