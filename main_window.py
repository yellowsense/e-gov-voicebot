from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
from qt_designer import Ui_MainWindow
import pyaudio
import wave
import threading
from assets.wav_converter import wav_to_base64
from assets.translate import translation
from assets.api import UCLA_API_KEY, USER_ID
from combo import transcribe_audio
import pandas as pd
from assets.api import GOOGLE_API_KEY
import google.generativeai as genai


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")   
        self.df = pd.read_csv("data.csv") 

        self.setupUi(self)
        
        self.is_recording = False
        self.base64_val = None

        self.setFixedWidth(self.width())
        self.setFixedHeight(self.height())
        self.close_shortcut = QShortcut(QKeySequence("ctrl+w"), self)
        self.close_shortcut.activated.connect(self.close)

        self.comboBox.addItems([
            "en-English",
            "hi-हिन्दी",
            "kn-ಕನ್ನಡ",
            "ur-اردو",
            "ta-தமிழ்",
            "ks-कश्मीरी",
            "as-অসমীয়া",
            "bn-বাংলা",
            "mr-मराठी",
            "sd-سنڌي",
            "pa-ਪੰਜਾਬੀ",
            "ml-മലയാളം",
            "te-తెలుగు",
            "sa-संस्कृतम्",
            "ne-नेपाली",
            "gu-ગુજરાતી",
            "or-ଓଡ଼ିଆ"
        ])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.audio_output.setPlainText("-- TRANSCRIPTION AREA --")

        self.start_button.clicked.connect(self.start_recording)    
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
    
    def on_combobox_changed(self, index):
        selected_option = self.comboBox.itemText(index)
        self.selected_language.setText(f'Selected: {selected_option}')

    def get_query_result(self, query: str)->str:
        prompt = f"{query}.  Use the following data as context:\n{self.df}.  Keep the answer short and simple."
        response = self.model.generate_content(prompt)
    
        return response.text  

    def start_recording(self):
        self.is_recording = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def record(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.recording_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        sound_file = wave.open("recording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Audio Recorder", "Recording saved as 'recording.wav'")

        self.base64_val = wav_to_base64(r"C:\\Users\\Hemanth\\Desktop\\python-bhashini\\recording.wav")
        language = self.comboBox.currentText()[:2]
        print(language)

        transcription = transcribe_audio('recording.wav', language=language)

        with open("test_output.txt", "w", encoding="utf-8") as file:
            file.write(transcription)
            
        with open("test_output.txt", "r", encoding="utf-8") as file:
            output_text = file.read()
            if language != "en":
                translated_text = translation(UCLA_API_KEY, USER_ID, input_lang=language, output_lang="en", text=output_text)
                self.audio_output.setPlainText(f"{output_text}\n\n{translated_text}")
            else:
                translated_text = output_text
                self.audio_output.setPlainText(f"{output_text}\n\n{translated_text}")

        print("---")
        
        res = self.get_query_result(translated_text)
        if language != "en":
            res = translation(UCLA_API_KEY, USER_ID, input_lang="en", output_lang=language, text=res)

        QMessageBox.information(self, "Query Result", res)

        
    def closeEvent(self, event):
        print("== APP SUCCESSFULLY CLOSED ==")
        event.accept()