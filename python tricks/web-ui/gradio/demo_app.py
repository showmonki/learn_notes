import os
import pandas as pd

import gradio as gr


def load_df(df_file):
    print(df_file[0].name)
    file_df = pd.read_csv(df_file[0].name)
    print(file_df)
    return file_df

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            upload_file = gr.File(file_count="multiple", file_types=["text", ".json", ".csv"])
    #     gr.Examples(
    #     examples=[['file1'],['file2']],
    #     inputs=[input_file],
    #     outputs = df
    # )
        df = gr.DataFrame(type="pandas")
        btn = gr.Button('Run')
        btn.click(fn=load_df, inputs=[upload_file], outputs=[df])

if __name__ == "__main__":
    demo.launch()
