import math
import sys


def update_progress(current_frame, total_frames):
    progress = math.ceil((current_frame/total_frames)*100)
    sys.stdout.write('\rProgress: [{0}] {1}%'.format('>'*math.ceil(progress/10), progress))