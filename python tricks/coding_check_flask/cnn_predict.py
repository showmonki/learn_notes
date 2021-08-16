# coding: utf-8

from __future__ import print_function
from __future__ import division
import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
from cnn_model import TCNNConfig, TextCNN
import pandas as pd
from cnn_function import read_vocab, load_category, load_image


class CnnModel:
    def __init__(self,num_classes,train_dir,vocab_dir,save_path):
        self.num_classes = num_classes
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = load_category(train_dir)
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.num_classes, self.config)
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)

    def predict(self, message, num_pred):
        # content = unicode(message)
        data = [self.word_to_id[x] for x in message if x in self.word_to_id]
        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }
        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        y_pred_prob = self.session.run(self.model.y_prob_cls, feed_dict=feed_dict)
        top_prob_list = y_pred_prob.argsort()[0][-num_pred:].tolist()
        top_prob_list.reverse()
        top_prediction = dict(zip([self.categories[i].replace('\n', '') for i in top_prob_list],
                                  [y_pred_prob[:, i][0] for i in top_prob_list]))
        return top_prediction


if __name__ == '__main__':
	# pip install tensorflow==1.13.2
    cat_code = 'LAUND'
    seg_id = '1526'
    num_top_item = 3
    desc_col_name = 'PRODUCT_DESC'
    img_path = '../Model/image/CHINAops_Ecom_ZHIHAI_IMAGE_URL_20210228.csv'

    predict_cols = []
    [predict_cols.extend(['Top_%s_value' % value, 'Top_%s_prob' % value]) for value in range(1, num_top_item + 1)]
    # return corresponding number of columns

    save_name_sub = 'character_cnn'  # train的语句里时候有这个文件结构。以防文件乱掉。暂时不改动这句
    train_dir = '../Model/input/{}{}/'.format(cat_code, seg_id)
    predict_dir = '../review/{}{}.csv'.format(cat_code, seg_id)  # TODO 改为读取指定文件，不限定文件名字
    output_path = '../review/{}{}_top_{}.csv'.format(cat_code, seg_id, num_top_item)  # TODO 指定输出。只锁后缀
    save_path = '../Model/checkpoints/{}{}/{}/best_validation'.format(cat_code, seg_id, save_name_sub)
    vocab_dir = '../Model/output/{}/{}/vocab.txt'.format(cat_code+seg_id, save_name_sub)

    categories, cat_to_id = load_category(train_dir)
    num_classes = len(cat_to_id)
    cnn_model = CnnModel(num_classes)

    to_predict = pd.read_csv(predict_dir)

    to_predict['predict'] = to_predict[desc_col_name].apply(cnn_model.predict, args=(num_top_item,))
    to_predict[predict_cols] = to_predict['predict'].apply(lambda x: ','.join([','.join([key, str(value)]) for key, value in x.items()])).str.split(',', expand=True)
    del to_predict['predict']
    to_predict['TOP1_lower_0.9'] = to_predict['Top_1_prob'].astype(float) < 0.9
    to_predict.loc[to_predict['TOP1_lower_0.9'], 'IMG_URL'] = load_image(to_predict.loc[to_predict['TOP1_lower_0.9']], img_path)

    to_predict.to_csv(output_path, encoding='GBK', index=False)
