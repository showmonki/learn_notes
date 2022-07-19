import torch
import tushare as ts
import json
import time
from torch.utils.data import DataLoader, TensorDataset


def get_daily(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


with open('../token.json') as token_file:
    token = json.load(token_file)['token']

pro = ts.pro_api(token)

# 不要开梯子获取数据，返回空
raw_df = pro.daily(exchange='SSE',ts_code='600812.SH',start_date='20200101', end_date='20220510')
pred_df = pro.daily(exchange='SSE',ts_code='600812.SH',start_date='20220511', end_date='20220530')
target_df = raw_df[:-int(len(raw_df)*0.1)]
renew_df = raw_df[-int(len(raw_df)*0.1):]
target_cols = list(target_df.columns)
target_cols.remove('close')
target_cols.remove('ts_code')
target_cols.remove('trade_date')
X_stocks = target_df[target_cols]
y_stocks = target_df.close

split_ratio = 0.2
split_idx = -int(len(target_df)*split_ratio)

train_x, train_y = X_stocks[:split_idx], y_stocks[:split_idx]
test_x, test_y = X_stocks[split_idx:], y_stocks[split_idx:]

train_x = torch.from_numpy(train_x.values)
train_y = torch.from_numpy(train_y.values)
test_x = torch.from_numpy(test_x.values)
test_y = torch.from_numpy(test_y.values)
train_data = TensorDataset(train_x,train_y)
val_data = TensorDataset(test_x,test_y)
train_loader = DataLoader(train_data, batch_size=64, shuffle=False)
val_loader = DataLoader(val_data, batch_size=64, shuffle=False)
renew_loader = DataLoader(TensorDataset(torch.from_numpy(renew_df[target_cols].values), torch.from_numpy(renew_df.close.values)), batch_size=8, shuffle=False)
pred_loader = DataLoader(TensorDataset(torch.from_numpy(pred_df[target_cols].values), torch.from_numpy(pred_df.close.values)), batch_size=1, shuffle=False)

torch.save({'train':train_loader, 'val':val_loader,'resume':renew_loader},'./datasets/trainval_data.pt')
torch.save(pred_loader, './datasets/pred_loader.pt')
