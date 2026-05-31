# FluentAI
FluentAI is an AI-powered English fluency coach that helps users improve their spoken English through real-time voice conversations. The application combines speech recognition, large language models, and text-to-speech technology to create an interactive language-learning experience.

## Features

* Real-time voice input
* Speech-to-text transcription using Whisper
* AI-powered conversational responses
* Text-to-speech voice generation
* Interactive English speaking practice
* User-friendly Streamlit interface
* Fast AI responses powered by Groq

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & Machine Learning

* OpenAI Whisper (Speech-to-Text)
* Groq API
* Llama 3.3

### Audio Processing

* gTTS (Google Text-to-Speech)
* Streamlit Mic Recorder

### Deployment

* Hugging Face Spaces

### Version Control

* Git
* GitHub

## System Architecture

```text
+------------------+      +---------------------+      +------------------------+
|    THE EARS      | ---> |      THE BRAIN      | ---> |       THE VOICE        |
| (OpenAI Whisper) |      | (Groq / Llama 3.3)  |      |  (gTTS Audio Engine)   |
+------------------+      +---------------------+      +------------------------+
```
### Workflow

1. User records speech through the microphone.
2. Whisper converts speech into text.
3. The text is sent to Llama 3.3 via Groq API.
4. The AI generates an intelligent response.
5. gTTS converts the response into speech.
6. The user receives both text and audio output.

## Run Locally

```bash
streamlit run app.py
```

## Use Cases

* English speaking practice
* Pronunciation improvement
* Conversation simulation
* Interview preparation
* Language learning assistance
* Communication skill development

## Demo

<img width="1913" height="783" alt="Screenshot 2026-05-31 172838" src="https://github.com/user-attachments/assets/52701c7d-d4e3-4d15-98f6-03e1ceb77dcc" />

## Future Improvements

* User authentication
* Conversation history
* Progress tracking dashboard
* Personalized learning plans
* Grammar correction
* Vocabulary enhancement suggestions
* Multi-language support

## Contributing

Contributions are welcome. Feel free to fork the repository and submit pull requests.


## License

This project is licensed under the MIT License.

## Author

**Abdulrehman Atif**

Software Engineering Student | AI & Python Developer
