from os import path
from subprocess import call
import random
from Greenhub.Date import Date
from Greenhub.Graph import Graph


class Greenhub:
    file_name = 'green.hub'

    def __init__(self):
        """
        create commit file if not exists
        """

        if not path.isfile(self.file_name):
            open(self.file_name, 'w')

    @staticmethod
    def commit_graph(name=None, base_commit_times=0):
        """
        commit according to a given graph

        Args:
            name              (str): the file name of the graph
            base_commit_times (int): for all non zero commit, add this number of commit times
        """

        # get the first date of Github contribution graph
        first_date = Greenhub.get_first_date()

        # get the processed graph
        graph = Graph.process(first_date, name)

        # commit graph
        for date, commit_times in graph.items():
            # repeat commit times
            for commit in range(commit_times + base_commit_times):
                # commit on the date
                Greenhub.commit(date)

    @staticmethod
    def commit_everyday(start_date=None, commit_count_range=None):
        """
        commit everyday from a start date so the time line in github shows green

        Args:
            start_date         (str) : the start date
            commit_count_range (list): the range of the commit times (e.g. [1, 5]: will commit randomly once to five
                                       times)
        """

        # set start date to the Github contribution first date if start date is not specified
        if start_date is None:
            start_date = Greenhub.get_first_date()

        else:
            start_date = Date(start_date)

        # commit everyday until now
        Greenhub.commit_in_range(start_date, Date().tomorrow(), commit_count_range)

    @staticmethod
    def filter_commit_date():
        """
        change the commit date to author date
        """

        # git filter-branch --env-filter 'export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"'
        call(['git', 'filter-branch', '--env-filter', """export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE" """])

    @staticmethod
    def push(force=False):
        """
        push changes to github

        Args:
            force (bool): when true, do a force push
        """

        push_commit = ['git', 'push']

        if force:
            push_commit.append('--force')

        call(push_commit)

    @staticmethod
    def commit_in_range(start_date, end_date, commit_count_range=None):
        """
        commit from start date til end date (include start date, exclude end date)

        Args:
            start_date         (Date): the start date (inclusive: will have commit on this date)
            end_date           (Date): the end date (exclusive: will not have commit on this date)
            commit_count_range (list): the range of the commit times (e.g. [1, 5]: will commit randomly once to five
                                       times)
        """

        # check if start date is larger than end date
        if start_date > end_date:
            return

        if commit_count_range is None:
            commit_count_range = [1, 1]

        # commit start date and move to next date until reaches end date
        while start_date != end_date:
            for commit_times in range(0, random.randint(commit_count_range[0], commit_count_range[1])):
                Greenhub.commit(str(start_date))

            start_date.tomorrow()

    @staticmethod
    def commit(date):
        """
        commit a file and change the date to the given date

        Args:
            date (str): the commit date with date format
        """

        # update file
        Greenhub.write(date)

        # git add {file_name}
        call(['git', 'add', Greenhub.file_name])

        # git commit -m "{date}" --date="{date}"
        call(['git', 'commit', '-m', "%s" % date, '--date="%s"' % date])

    @staticmethod
    def write(date):
        """
        write green hub file a date and a random number

        Args:
            date (str): the date that will appear in the file
        """

        # set file content to a date time with a random number
        content = '%s: %f' % (date, random.random())

        # update file with the content
        with open(Greenhub.file_name, 'w') as file:
            file.write(content)

    @staticmethod
    def get_first_date():
        """
        calculate the first date of the Github page contribution

        Returns:
            Date: the first date shown in the Github page contribution
        """

        # get today date
        date = Date()

        # get today weekday
        weekday = date.get_weekday()

        # move date to 53 weeks before
        date.weeks_before(53)

        # if is not sunday, move date to sunday
        if weekday != 7:
            date.days_before(weekday)

        return date
