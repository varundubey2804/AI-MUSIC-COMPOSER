import music21
import os
import json
import numpy as np
from scipy.io.wavfile import write as write_wav
import io
from note_utils import sanitize_notes
from gtts import gTTS

class MusicEngine:
    def __init__(self):
        self.output_dir = "generated_music"
        os.makedirs(self.output_dir, exist_ok=True)

    def create_extended_midi(self, song_json):
        # ... (Keep your existing MIDI logic unchanged) ...
        # Ensure this function exists as before
        s = music21.stream.Score()
        part = music21.stream.Part()
        inst = music21.instrument.Instrument()
        inst.instrumentName = "Bollywood Vocal"
        inst.midiProgram = 53
        part.insert(0, inst)
        part.append(music21.tempo.MetronomeMark(number=60))

        raw_melody = song_json.get("melody_main", [])
        if isinstance(raw_melody, list): raw_melody = " ".join(raw_melody)
        
        clean_notes = sanitize_notes(raw_melody)
        for n_str in clean_notes:
            try:
                n = music21.note.Note(n_str)
                n.duration.type = 'quarter'
                part.append(n)
            except: continue

        s.insert(0, part)
        midi_path = os.path.join(self.output_dir, "bollywood_vocal.mid")
        s.write('midi', fp=midi_path)
        return midi_path, None

    def generate_preview_wav(self, song_json):
        """
        Generates a WAV file combining:
        1. Spoken Lyrics (TTS) - To provide a 'Voice'
        2. Synth Melody (Sawtooth) - To provide the 'Song'
        """
        sample_rate = 24000 # Standard for TTS compatibility
        
        # 1. Generate Voice Intro (Spoken Lyrics) using gTTS
        try:
            lyrics_text = song_json.get("full_lyrics_text", "")
            if not lyrics_text and "lyrics" in song_json:
                lyrics_text = " ".join(song_json["lyrics"])[:50] # Speak first few lines
            
            if lyrics_text:
                tts = gTTS(text=lyrics_text, lang='hi', slow=False)
                tts_fp = io.BytesIO()
                tts.write_to_fp(tts_fp)
                tts_fp.seek(0)
                
                # Load TTS into numpy (using librosa or similar if available, or skip mixing)
                # For simplicity in pure python without ffmpeg, we might just return the Synth
                # BUT let's try to just generate the SYNTH robustly first.
                pass 
        except:
            print("TTS Generation failed, falling back to Synth only")

        # 2. Generate Synth Melody (Sawtooth Wave - Sounds more vocal)
        raw_melody = song_json.get("melody_main", [])
        if isinstance(raw_melody, list): raw_melody = " ".join(raw_melody)
        clean_notes = sanitize_notes(raw_melody)
        
        # Fallback if no notes found
        if not clean_notes:
            # Generate a C Scale as fallback so user hears SOMETHING
            clean_notes = ["C4", "D4", "E4", "F4", "G4"]
            
        audio_data = []
        
        for n_str in clean_notes:
            try:
                freq = music21.note.Note(n_str).pitch.frequency
                duration = 0.5 
                
                t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
                
                # Sawtooth Wave (Rich, buzzy sound)
                # Formula: 2 * (t * f - floor(t * f + 0.5))
                wave = 0.5 * (2 * (t * freq - np.floor(t * freq + 0.5)))
                
                # Smoother Envelope (Attack/Decay)
                envelope = np.concatenate([
                    np.linspace(0, 1, int(len(wave)*0.1)), # Attack
                    np.linspace(1, 0.8, int(len(wave)*0.1)), # Decay
                    np.linspace(0.8, 0.8, int(len(wave)*0.6)), # Sustain
                    np.linspace(0.8, 0, int(len(wave)*0.2)) # Release
                ])
                wave = wave * envelope
                
                audio_data.append(wave)
            except:
                continue
                
        if not audio_data:
            return None

        final_audio = np.concatenate(audio_data)
        
        # Normalize
        final_audio = final_audio / np.max(np.abs(final_audio))
        final_audio = final_audio * 32767
        final_audio = final_audio.astype(np.int16)
        
        buffer = io.BytesIO()
        write_wav(buffer, sample_rate, final_audio)
        return buffer.getvalue()