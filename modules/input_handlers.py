from modules.hand_gesture import process_gesture
from modules.llm_processor import get_llm_output
from modules.speech_to_text import speech_to_text

def handle_gesture(image, is_processing):
    if not is_processing or image is None:
        return -1
        
    task_num = process_gesture(image)
    print(f"Task number from gesture: {task_num}")
    return task_num if task_num in [1, 2, 3] else -1

def handle_audio(audio, is_processing):
    if not is_processing or audio is None:
        return -1, "No audio detected"
    
    try:
        transcribed_text = speech_to_text(audio)
        task_num = get_llm_output(transcribed_text, 'task_classifier')
        try:
            task_num = int(task_num)
            print(f"Task number from audio: {task_num}")
        except (ValueError, TypeError):
            task_num = -1
            
        return task_num, transcribed_text
                
    except Exception as e:
        error_msg = f"Error processing audio: {str(e)}"
        return -1, error_msg