# from pydub import AudioSegment
#
# # Load the background audio
# background_audio = AudioSegment.from_file("background.mp3")
#
#
# def overlay_audio_segments(background_audio, diarized_data, reduction_dB=-20):
#     for segment in diarized_data:
#         # Load the speaker's audio segment
#         speaker_audio = AudioSegment.from_file(segment["audio_file"])
#         # Reduce the volume of the background audio during the speaker's segment
#         start_ms = segment["start"] * 1000
#         end_ms = segment["end"] * 1000
#         # Adjusting the volume of the background audio segment where the speech occurs
#         background_audio = background_audio.overlay(speaker_audio + reduction_dB, position=start_ms)
#
#     return background_audio
#
#
# # Overlay the voice audio segments onto the background audio
# diarized_data = []
# output_audio = overlay_audio_segments(background_audio, diarized_data)
#
# # Save the final audio mix to a file
# output_audio.export("final_mix.mp3", format="mp3")
