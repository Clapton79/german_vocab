import itertools
from datetime import datetime
import yaml
from applogger import logger
from pprint import pprint

filename = 'word_stats.yaml'

def calculate_summary(filename:str):
    try:
        stats = {}
        # load word_stats file 
        if filename.endswith('.yaml'):
            with open(filename, 'r') as f:
                yamldata = yaml.safe_load(f)
        else: 
            raise ValueError('Invalid file extension')        

        # generate summary
        for _, item in yamldata.items():
            word = item['word']  # Get the word from the item
            if word in stats:
                stats[word]['occurrence'] += 1
                if item['success']:  # Use item instead of value
                    stats[word]['success'] += 1
                stats[word]['date'] = item['date']
            else:
                # Initialize new word entry
                stats[word] = {
                    'occurrence': 1,
                    'date': item['date'],
                    'success': 1 if item['success'] else 0
                }

        pprint(stats)

    except Exception as e:
        logger.error(f"Error loading file {filename}: {str(e)}")
        print(f"Error loading file {filename}: {str(e)}")

calculate_summary(filename)