import gradio as gr
from utils.ui import *
from utils.utils import process_input


def create_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        header_components = create_header("utils/sdaiaAcademyLogo.png")

        processing = gr.State(True)
        current_meetings = gr.State([])
        email_summary = gr.State("")
        content_summary = gr.State("")

        with gr.Row():
            with gr.Column():
                audio_input, audio_output, camera_input, reset_btn = create_input_column()

            with gr.Column():
                calendar_table, email_output, content_output = create_output_column()

        create_footer_instructions()

        def reset():
            return None, "", "", True, [], "", ""

        audio_input.change(
            fn=lambda *args: process_input(args[0], "audio", *args[1:]),
            inputs=[
                audio_input,
                processing,
                current_meetings,
                email_summary,
                content_summary,
            ],
            outputs=[
                audio_output,
                calendar_table,
                email_output,
                content_output,
                processing,
                current_meetings,
                email_summary,
                content_summary,
            ],
        )

        camera_input.stream(
            fn=lambda *args: process_input(args[0], "gesture", *args[1:]),
            inputs=[
                camera_input,
                processing,
                current_meetings,
                email_summary,
                content_summary,
            ],
            outputs=[
                audio_output,
                calendar_table,
                email_output,
                content_output,
                processing,
                current_meetings,
                email_summary,
                content_summary,
            ],
        )

        reset_btn.click(
            fn=reset,
            outputs=[
                calendar_table,
                email_output,
                content_output,
                processing,
                current_meetings,
                email_summary,
                content_summary,
            ],
        )

    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch()