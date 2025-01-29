import subprocess
from datetime import datetime
from modules.llm_processor import get_llm_output

def get_calendar_meetings():
    script = '''
    tell application "Calendar"
        set todayDate to current date
        -- Set start date to beginning of today
        set startDate to todayDate - (time of todayDate)
        -- Set end date to end of today
        set endDate to startDate + (24 * hours)
        
        set eventList to {}
        
        repeat with calendarAccount in calendars
            try
                set theEvents to (every event of calendarAccount whose start date ≥ startDate and start date < endDate)
                
                repeat with anEvent in theEvents
                    set eventStart to start date of anEvent
                    set eventHour to text -2 thru -1 of ("0" & (hours of eventStart as integer))
                    set eventMinute to text -2 thru -1 of ("0" & (minutes of eventStart as integer))
                    set eventTime to eventHour & ":" & eventMinute
                    set eventTitle to summary of anEvent
                    
                    copy {eventTime, eventTitle} to end of eventList
                end repeat
            end try
        end repeat
        
        return eventList
    end tell
    '''
    
    try:
        process = subprocess.Popen(['osascript', '-e', script],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        output, error = process.communicate()
        
        meetings = []
        if output:
            output_str = output.decode('utf-8').strip()
            parts = output_str.split(', ')
            
            for i in range(0, len(parts), 2):
                if i + 1 < len(parts):
                    time = parts[i]
                    title = parts[i + 1]
                    meetings.append([time, title])
        
        meetings.sort(key=lambda x: x[0])
        print(f"Generated meetings: {meetings}")
        return meetings
        
    except Exception as e:
        print(f"Error accessing Calendar: {e}")
        return []

def get_last_10_emails():
    import os.path
    import base64
    import re
    from email.mime.text import MIMEText
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    output = []

    try:
        creds = None
        if os.path.exists("credentials/token.json"):
            creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    os.remove("credentials/token.json")
                    flow = InstalledAppFlow.from_client_secrets_file("credentials/credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open("credentials/token.json", "w") as token:
                token.write(creds.to_json())

        service = build("gmail", "v1", credentials=creds)
        
        messages = service.users().messages().list(
            userId='me',
            maxResults=10,
            q="category:primary is:unread"
        ).execute()

        if 'messages' not in messages:
            return "No unread messages in Primary category."

        output.append("Latest 10 unread emails from Primary:")
        output.append("-" * 70)

        for i, message in enumerate(messages['messages'], 1):
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()

            payload = msg['payload']
            headers = payload['headers']

            subject = ''
            sender = ''
            date = ''
            sender_email = ''
            for header in headers:
                if header['name'].lower() == 'subject':
                    subject = header['value']
                if header['name'].lower() == 'from':
                    sender = header['value']
                    email_match = re.search(r'<([^>]+)>', sender)
                    if email_match:
                        sender_email = email_match.group(1)
                    else:
                        sender_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
                        sender_email = sender_email.group(0) if sender_email else sender
                if header['name'].lower() == 'date':
                    date = header['value']

            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
            else:
                if 'body' in payload and 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

            if not body:
                body = "No plain text content available"

            output.append(f"\nEmail {i}:")
            output.append(f"From: {sender}")
            output.append(f"Email: {sender_email}")
            output.append(f"Date: {date}")
            output.append(f"Subject: {subject}")
            output.append("\nContent:")
            content_preview = body[:200]
            if len(body) > 200:
                content_preview += "..."
            output.append(content_preview)
            output.append("-" * 70)

        return "\n".join(output)

    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_content(query="computer vision", max_papers=5):
    import arxiv
    import os
    import PyPDF2
    import re
    from datetime import datetime
    from urllib.request import urlretrieve
    
    def extract_introduction(pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for i in range(min(3, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                intro_match = re.search(r'(?i)(introduction|1\.?\s+introduction).*?(?=[2-9]\.|\n\s*[2-9]\.)', text, re.DOTALL)
                if intro_match:
                    return intro_match.group(0)
                return text[:1500]
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def clean_text(text):
        return ' '.join(text.split())
    
    client = arxiv.Client()
    search = arxiv.Search(
        query=f'cat:cs.CV AND "{query}"',
        max_results=max_papers * 2,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    temp_dir = "temp_arxiv_papers"
    os.makedirs(temp_dir, exist_ok=True)
    
    paper_summaries = []
    processed_count = 0
    
    try:
        for paper in client.results(search):
            if processed_count >= max_papers:
                break
                
            if 'cs.CV' in paper.primary_category:
                pdf_path = os.path.join(temp_dir, f"{paper.get_short_id()}.pdf")
                
                try:
                    urlretrieve(paper.pdf_url, pdf_path)
                    
                    paper_info = (
                        f"Paper title: {paper.title}\n"
                        f"Authors: {', '.join(author.name for author in paper.authors)}\n"
                        f"Publication date: {paper.published.strftime('%Y-%m-%d')}\n"
                        f"Category: {paper.primary_category}\n"
                        f"Abstract: {clean_text(paper.summary)}\n"
                        f"Introduction: {clean_text(extract_introduction(pdf_path))}\n"
                        f"{'='*80}\n\n"
                    )
                    paper_summaries.append(paper_info)
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing {paper.title}: {str(e)}")
                finally:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
    
    finally:
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except:
                pass
    
    final_output = (
        f"ArXiv Paper Summaries - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Query: {query} (Computer Vision papers only)\n"
        f"{'='*80}\n\n"
    )
    final_output += ''.join(paper_summaries)
    
    return final_output

def process_input(input_data, input_type, is_processing, meetings, prev_email_summary, prev_content_summary):
    from modules.input_handlers import handle_gesture, handle_audio
    
    if not is_processing:
        return None, meetings if meetings else None, prev_email_summary, prev_content_summary, False, meetings, prev_email_summary, prev_content_summary

    if input_type == "gesture":
        task_num = handle_gesture(input_data, is_processing)
        transcribed_text = None
    else:
        task_num, transcribed_text = handle_audio(input_data, is_processing)

    _, calendar_data, email_output, content_summary, new_is_processing, new_meetings, new_email_summary, new_content_summary = execute_task(
        task_num, transcribed_text, prev_email_summary, meetings, prev_content_summary
    )
    
    return (transcribed_text, calendar_data, email_output, content_summary, 
            new_is_processing, new_meetings, new_email_summary, new_content_summary)

def execute_task(task_num, transcribed_text, prev_email_summary, meetings, prev_content_summary):
    if task_num == -1:
        return None, None, prev_email_summary, prev_content_summary, True, meetings, prev_email_summary, prev_content_summary
        
    if task_num == 1:
        new_emails = get_last_10_emails()
        llm_output = get_llm_output(new_emails, "email_summary")
        return None, None, llm_output, prev_content_summary, False, meetings, llm_output, prev_content_summary

    elif task_num == 2:
        new_meetings = get_calendar_meetings()
        meetings_data = [[str(meeting[0]), str(meeting[1])] for meeting in new_meetings]
        return None, meetings_data, prev_email_summary, prev_content_summary, False, meetings_data, prev_email_summary, prev_content_summary
    
    elif task_num == 3:
        content = get_content()
        summary = get_llm_output(content, "content_summarizer")
        return None, None, prev_email_summary, summary, False, meetings, prev_email_summary, summary
            
    return None, None, prev_email_summary, prev_content_summary, True, meetings, prev_email_summary, prev_content_summary