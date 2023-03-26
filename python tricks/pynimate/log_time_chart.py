"""use pynimate to plot the log-time chart"""
import pandas as pd
import numpy as np
import pynimate as nim


# 更新条形图
def post_update(ax, i, datafier, bar_attr):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_facecolor("#001219")
    for bar, x, y in zip(
        bar_attr.top_bars,
        bar_attr.bar_length,
        bar_attr.bar_rank,
    ):
        ax.text(
            x - 0.3,
            y,
            datafier.col_var.loc[bar, "user_level"],
            ha="right",
            color="k",
            size=12,
        )


data_log_path = 'xxx.log'
# read log file with certain format
# log block format:
# first line is timestamp, line2-21 is log content, then follow with 2 lines to split with next log block


with open(data_log_path, 'r') as f:
    lines = f.readlines()


def get_log_time(log_block):
    return log_block[0].rstrip()


def get_log_content(log_block):
    return log_block[1:21]


# log content format: rank_idx, nickname, melee, user_rank, userid. splited by space
def get_log_content_split(log_block):
    rank_iter = [log_iter.rstrip().split(' ') for log_iter in log_block]
    rank_result = pd.DataFrame(rank_iter, columns=['rank_ts','nickname','melee','user_level','user_id'])
    return rank_result


def get_log_block(log_block):
    log_timestamp = get_log_time(log_block)
    log_content = get_log_content(log_block)
    log_content_df = get_log_content_split(log_content)
    log_content_df['log_ts'] = log_timestamp
    log_content_df['log_ts'] = pd.to_datetime(log_content_df['log_ts'])
    return log_content_df


# pivot data from long data to wide data, by user_id, value with melee, timestamp in each block
# pivot in final step to convert wide data
def pivot_data(data):
    pivoted_data = data.pivot(index='log_ts', columns='user_hidden', values='melee')
    return pivoted_data


if __name__ == '__main__':
    # split log_blocks in each 22 steps and stored into new list
    log_blocks_split = [get_log_block(lines[i:i+23]) for i in range(0, len(lines), 23)]
    log_long = pd.concat(log_blocks_split)
    user_idx_dict = {user_id:'user_'+str(idx+1) for idx,user_id in enumerate(log_long['user_id'].unique())}
    log_long['user_hidden'] = log_long.user_id.map(user_idx_dict)
    log_long['melee'] = log_long['melee'].astype('int')
    log_all_df = pivot_data(log_long)
    # log_all_df.columns = ['user_'+str(ii+1) for ii,name in enumerate(log_all_df.columns)]
    # fill na in log_all_df with lastest records
    last_result = log_all_df[log_all_df.index<'2023-03-14 22:36:30'].fillna(method='ffill').fillna(0)

    col = log_long[['user_hidden','user_level']].drop_duplicates().set_index('user_hidden')
    import random
    # color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    bar_cols = {user:"#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for idx, user in enumerate(col.index)}
    # 新建画布
    cnv = nim.Canvas(figsize=(12.8, 7.2), facecolor="#001219")
    bar = nim.Barplot(
        last_result, "%Y-%m-%d %H:%M:%S", "1S", post_update=post_update, rounded_edges=True, grid=False,n_bars=20
    )
    # 条形图分类
    bar.add_var(col_var=col)
    # 条形图颜色
    # bar.set_bar_color(bar_cols)
    # 标题设置
    bar.set_title("Sample Title", color="w", weight=600)
    # x轴设置
    bar.set_xlabel("xlabel", color="w")
    # 时间设置
    bar.set_time(
        callback=lambda i, datafier: datafier.data.index[i].strftime("%b, %Y-%m-%d %H:%M:%S"), color="w",size=30
    )
    # 文字显示
    bar.set_text(
        "sum",
        callback=lambda i, datafier: f"Total :{np.round(datafier.data.iloc[i].sum(), 2)}",
        size=20,
        x=0.72,
        y=0.20,
        color="w",
    )

    # 文字颜色设置
    bar.set_bar_annots(color="w", size=13)
    bar.set_xticks(colors="w", length=0, labelsize=13)
    bar.set_yticks(colors="w", labelsize=13)
    # 条形图边框设置
    bar.set_bar_border_props(
        edge_color="black", pad=0.1, mutation_aspect=1, radius=0.2, mutation_scale=0.6
    )
    cnv.add_plot(bar)
    cnv.animate()
    # 显示
    # plt.show()
    # 保存gif
    cnv.save("example3", 24, "mp4")
