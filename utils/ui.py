import gradio as gr
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_header(logo_path):
    logo = get_base64_image(logo_path)
    instructions_header = """
    ### Welcome to secAI: Your AI Secretary
    
    secAI helps you manage your tasks using voice commands or hand gestures.
    """
    
    return [
        gr.HTML(f"""
            <style>
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    background: white;
                }}
                .content {{ padding: 20px; }}
            </style>
            <div class="header">
                <h1>secAI: Your AI Secretary</h1>
                <img src="data:image/png;base64,{logo}" alt="Logo" width="350">
            </div>
        """),
        gr.Markdown(instructions_header)
    ]

def create_footer_instructions():
    instructions = """
    ### How to Use secAI

    #### Voice Commands
    1. Click the microphone icon to start recording
    2. Speak your command clearly:
       - Say "Show my emails" or "Check my inbox" for email summary
       - Say "Show my calendar" or "What meetings do I have today" for calendar
       - Say "Summarize content" or "Get latest papers" for content summary
    3. Wait for the system to process your request

    #### Hand Gestures
    Use these gestures in front of your camera:
    - ☝️ One finger - Show a summary of your emails
    - ✌️ Two fingers - Show the meetings in your calendar
    - 👌 Three fingers - Summarize the latest papers in computer vision

    #### Additional Notes
    - Click "Start New Task" to reset and start a new request
    - The transcribed text will show what the system heard from your voice command
    - Results will appear in the corresponding tab on the right
    """
    return gr.Markdown(instructions)

def create_input_column():
    audio_input = gr.Audio(sources="microphone", type="filepath", label="Voice Input")
    audio_output = gr.Text(label="Transcribed Text")
    camera_input = gr.Image(sources="webcam", streaming=True, label="Gesture Input", interactive=True)
    reset_btn = gr.Button("Start New Task")
    return audio_input, audio_output, camera_input, reset_btn  

def create_output_column():
    with gr.Tabs():
        with gr.TabItem("Email Summary"):
            email_output = gr.Markdown(label="Email Summary", value="")
            
        with gr.TabItem("Calendar"):
            calendar_table = gr.Dataframe(
                headers=["Time", "Meeting Title"],
                label="Today's Meetings",
                value=[],
                type="array"
            )
            
        with gr.TabItem("Content Summarizer"):
            content_output = gr.Markdown(label="Content Summary", value="")
            
    return calendar_table,email_output, content_output