#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 12:24:25 2023

@author: danielagaio
"""

import os
import speech_recognition as sr
from pydub import AudioSegment

# Folder 
folder_path = "/Users/danielagaio/cloudstor/Gaio/audio/da_papo"

# initialize the recognizer
r = sr.Recognizer()

# List to hold the names of failed transcription files
failed_transcriptions_file_names = []


# loop through each mp3 in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        # full path 
        mp3_path = os.path.join(folder_path, filename)
        # convert to wav
        sound = AudioSegment.from_mp3(mp3_path)
        wav_path = mp3_path.replace(".mp3", ".wav")
        sound.export(wav_path, format="wav")

        # transcription
        with sr.AudioFile(wav_path) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data, language="it-IT")

                # save
                text_filename = os.path.join(folder_path, "transcribed_audio_" + filename.replace(".mp3", ".txt"))
                with open(text_filename, "w") as text_file:
                    text_file.write(text)

            except sr.UnknownValueError:
                print(f"Could not understand audio in file {filename}")
                failed_transcriptions_file_names.append(filename)
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service for file {filename}; {e}")
                failed_transcriptions_file_names.append(filename)
                
        # removal of wav file (can be opted out)
        os.remove(wav_path)

print("Transcription completed.")

# Print the list of failed transcriptions
if failed_transcriptions_file_names:
    print("Failed to transcribe the following files:")
    for failed_file in failed_transcriptions_file_names:
        print(failed_file)




# to run for failed transcriptions: 

# put failed mp3 in list and run the snippet below: 
failed_transcriptions_file_names = ["papo20141113-WA0015.m4a.mp3", 
              "papo20140909-WA0009.m4a.mp3",
              "papo20141020-WA0002.m4a.mp3",
              "papo20140917-WA0000.m4a.mp3",
              "papo20140908-WA0003.m4a.mp3",
              "papo20141027-WA0001.m4a.mp3",
              "papo20141118-WA0001.m4a.mp3",
              "papo20140912-WA0006.m4a.mp3"]


print(failed_transcriptions_file_names)

# Loop through each file name in the list
for filename in failed_transcriptions_file_names:
    try:
        # Join the folder path and file name
        mp3_path = os.path.join(folder_path, filename)

        # Convert mp3 file to wav
        sound = AudioSegment.from_mp3(mp3_path)
        wav_path = mp3_path.replace(".mp3", ".wav")
        sound.export(wav_path, format="wav")

        # Transcribe the audio file
        with sr.AudioFile(wav_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="it-IT")

            # Save the transcribed text
            text_filename = os.path.join(folder_path, "transcribed_audio_" + filename.replace(".mp3", ".txt"))
            with open(text_filename, "w") as text_file:
                text_file.write(text)

    except sr.UnknownValueError:
        print(f"Could not understand audio in file {filename}")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service for file {filename}; {e}")
    except Exception as e:
        print(f"An error occurred while processing file {filename}: {e}")

    # Optional: Remove the converted .wav file
    os.remove(wav_path)

print("Transcription completed.")

