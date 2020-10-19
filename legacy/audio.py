import pyaudio
import wave


class AudioRecording:
    def __init__(self):
        self.recording = True
        self.audio = pyaudio.PyAudio()
        self.form_1 = pyaudio.paInt16
        self.pchannel = 1
        self.__sample_rate = 44100
        self.__chunk = 4096
        self.device_index = 1  # Found by record
        self.__stream = self.audio.open(format=self.form_1, rate=self.__sample_rate, channels=self.pchannel,
                                        input_device_index=self.device_index, input=True,
                                        frames_per_buffer=self.__chunk)
        self.frames = []

    def get_device_list(self):
        device_list = []
        for ii in range(self.audio.get_device_count()):
            device_list.append(self.audio.get_device_info_by_index(ii).get('name'))
        return device_list

    def record(self):
        while self.recording:
            data = self.__stream.read(self.__chunk)
            self.frames.append(data)
        

    def stop_recording(self):
        self.recording = False
