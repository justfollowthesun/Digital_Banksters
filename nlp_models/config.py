import os

filename_path = os.path.basename(__file__)
current_dir = os.path.abspath(__file__).replace(filename_path, '')

news_model_pth = os.path.join(current_dir, 'ru_core_news_md')
navec_pth = os.path.join(current_dir, 'navec_news_v1_1B_250K_300d_100q.tar')
ner_pth = os.path.join(current_dir, 'slovnet_ner_news_v1.tar')