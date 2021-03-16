import re
import sys

def ProgressBar(percentage_done: int, bar_width: int=60):
	progress = int(bar_width * percentage_done / 100)
	bar = '=' * progress + ' ' * (bar_width - progress)
	sys.stdout.write('[{0}] {1:.2f}{2}\r'.format(bar, percentage_done, '%'))
	sys.stdout.flush()

def CustomSplit(string, separatorList):
    # create regular expression dynamically
    regularExpression = '|'.join(map(re.escape, separatorList))
    return re.split(regularExpression, string)