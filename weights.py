import itertools
from datetime import datetime
import yaml
from applogger import logger
import appconfig

filename = 'word_stats.yaml'

def calculate_summary(filename:str = None) -> dict:
    try:
        stats = {}
        # load word_stats file 
        if filename.endswith('.yaml'):
            with open(filename, 'r') as f:
                yamldata = yaml.safe_load(f)
        else: 
            raise ValueError('Invalid file extension')        
            # generate summary grouped by word and test_type
        for _, item in yamldata.items():
            word = item['word']
            test_type = item.get('test_type', 'unknown')
            if word not in stats:
                stats[word] = {}
            if test_type not in stats[word]:
                stats[word][test_type] = {
                    'occurrence': 0,
                    'success': 0,
                    'date': item['date']
                }
                stats[word][test_type]['occurrence'] += 1
            if item['success']:
                stats[word][test_type]['success'] += 1
            # Update date if newer
            if item['date'] > stats[word][test_type]['date']:
                stats[word][test_type]['date'] = item['date']

        print (f'Summary calculated: {len(stats.keys())} words.')
        return stats

    except Exception as e:
        logger.error(f"Calculate summary: {str(e)}")
        return {}
