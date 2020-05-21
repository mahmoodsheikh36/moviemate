class Movie:
    def __init__(self, title, year, poster, small_poster=None):
        self.title = title
        print(year.split('–')[0])
        self.year = year.split('–')[0]
        self.poster = poster
        self.small_poster = small_poster
