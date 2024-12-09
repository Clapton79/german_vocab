from vocab import *

base_v = Vocabulary('dict.yaml')

print(f"All tags: {base_v.tags()}")
tag_filter = input('Tag: ')

print([word for word, detail in base_v.vocab.items()
      if tag_filter in detail.get('tags', [])])
