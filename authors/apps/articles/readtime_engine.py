import re


class ArticleTimeEngine:
    """
    Class for estimating the time it takes to 
    read an article
    """
    def __init__(self, article_body):
        self.article_body = article_body

    def filter_words(self):
        """
        Method filters out words from an article body
        """
        filtered_words = re.findall(r'\w+', self.article_body)
        return filtered_words
    
    def total_word_count(self):
        """
        Method returns total number of filtered words
        """
        return len(self.filter_words())

    def calculate_read_time(self):
        """
        Method calculates minutes it takes to read an article
        """
        # Average reading time for a normal person in words per minute
        WPM = 250
        time = self.total_word_count()/WPM
        actual_time = round(time)
        return actual_time
    
    def read_time(self):
        # minutes in an hour
        hour = 60
        # hours a day
        day = 24
        # get calculated time
        time = self.calculate_read_time()
        # check if time is less than a minute
        if time < 1:
            return "less than a minute read"
        # check if time is greater than 1 hour
        if time >= hour:
            # convert minutes to hours
            hours = round(time/hour)
            # check if time is greater than a day
            if hours >= day:
                # convert hours to days
                days = round(hours/day)
                return f"{days} day read"
            return f"{hours} hour read"
        return f"{time} minute read"
