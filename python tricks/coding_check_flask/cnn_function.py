import sys
import os

if sys.version_info[0] > 2:
    is_py3 = True
else:
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_vocab(vocab_dir):
    with open_file(vocab_dir) as fp:
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def load_category(train_dir):
    with open_file(os.path.dirname(train_dir)+'/label_dict.txt') as fp:
        categories = [native_content(_.lstrip()) for _ in fp.readlines()]
    cat_to_id = dict(zip(categories, range(len(categories))))
    return categories, cat_to_id


def save_folder(save_name, save_name_sub):
    save_dir = 'checkpoints' + '/' + save_name + '/' + save_name_sub
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, 'best_validation')
    tensorboard_dir = 'tensorboard'+'/'+save_name+'/'+save_name_sub
    if not os.path.exists(tensorboard_dir):
        os.makedirs(tensorboard_dir)
    output_path = 'output'+'/'+save_name+'/'+save_name_sub
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    vocab_dir = os.path.join(output_path, 'vocab.txt').replace('\\', '/')
    model_para_dir = os.path.join(output_path, 'model_para.txt')
    return save_path, tensorboard_dir, output_path, vocab_dir, model_para_dir


def load_image(raw_df, img_path):
    import pandas as pd
    img_file_col = ['TRANSACTION_DATE', 'SCRAPPING_TIME', 'STORE_ID', 'PROD_ID', 'IMG_URL']
    img_df = pd.read_csv(img_path, names=img_file_col)
    img_dict = dict(zip(img_df['PROD_ID'], img_df['IMG_URL']))
    raw_df['IMG_URL'] = raw_df['PROD_ID'].map(img_dict)
    return raw_df['IMG_URL']
