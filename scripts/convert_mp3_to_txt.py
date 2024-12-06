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
              "papo20140912-WA0006.m4a.mp3",
              "papo20141105-WA0001.m4a.mp3",
              "papo20140911-WA0004.m4a.mp3",
              "papo20141101-WA0001.m4a.mp3",
              "papo20141002-WA0001.m4a.mp3",
              "papo20141108-WA0001.m4a.mp3",
              "papo20141030-WA0022.m4a.mp3",
              "papo20140920-WA0000.m4a.mp3",
              "papo20140924-WA0013.m4a.mp3"]

set(failed_transcriptions_file_names)
print(len(failed_transcriptions_file_names))






from pydub import AudioSegment
import os


# List of filenames that you want to split
files_to_split = failed_transcriptions_file_names  # Replace with your list of failed files

# Maximum size of each part in bytes (7.5 MB)
max_size = 7.4 * 1024 * 1024

# Loop through each file in the list
for filename in files_to_split:
    # Full path of the mp3 file
    mp3_path = os.path.join(folder_path, filename)

    # Load the file
    audio = AudioSegment.from_mp3(mp3_path)

    # Calculate the number of parts to split into based on the file size
    file_size = os.path.getsize(mp3_path)
    num_parts = max(2, int(file_size // max_size) + 1)

    # Calculate duration of each part
    part_duration = len(audio) // num_parts

    # Split and save the parts
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = start_time + part_duration if i < num_parts - 1 else len(audio)
        part = audio[start_time:end_time]
        part.export(os.path.join(folder_path, f"{filename.replace('.mp3', '')}_part_{i+1}.mp3"), format="mp3")

print("Splitting completed.")






# Initialize an empty list to store filenames
part_files = []

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if "part_" in filename:
        # Add the file to the list
        part_files.append(filename)

# Print or return the list of files
print(part_files)



# Loop through each file name in the list
for filename in part_files:
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
        print(f"service for file {filename}; {e}")
    except Exception as e:
        print(f"An error occurred while processing file {filename}: {e}")

    # Optional: Remove the converted .wav file
    os.remove(wav_path)

print("Transcription completed.")

