# notes for textcnn
1. tfidf、标准化等，都应该把train 和test分开处理。真实数据是不会得到train+test的分布，一起处理失去了split的效果
2. 字level的处理，如果只用count 比较容易处理？
3. tfidf之前貌似效果不好，是因为toarray()已经返回了矩阵，不应该再使用toarray()[0]
4. CountVectorizer和TfidfVectorizer都是返回二维矩阵(错误，不是返回二维，用错了。)，都是很稀疏的。如果seq_len不给够(50已经很少了)，则会返回全是0的矩阵,且cnn层数多后，信息确实过多
5. 单纯count_id train_acc从47直接上升到98