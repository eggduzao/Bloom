
##### Import

from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

##### Constants

# Time Constants
H = 60 * 60 * 1000
M = 60 * 1000
S = 1000

##### Functions

# Stretching
def stretch(segment: AudioSegment, factor: float) -> AudioSegment:
    """
    factor > 1.0  -> speed up (shorter, higher pitch)
    factor < 1.0  -> slow down (longer, lower pitch)
    """
    new_frame_rate = int(segment.frame_rate * factor)
    # reinterpret raw data with new frame rate
    altered = segment._spawn(segment.raw_data, overrides={"frame_rate": new_frame_rate})
    # resample back to original frame rate so it plays nicely with others
    return altered.set_frame_rate(segment.frame_rate)

# Find how long the track needs to be:
def compute_total_duration_ms(events):
    total = 0
    for ev in events:
        end = ev["start_ms"] + len(ev["segment"])
        if end > total:
            total = end
    return total

##### Timeline

# Load original track
root = Path("/Users/egg/Music/Music/one_more_time")
morespell_path = root / "eddie_johns_more_spell_on_you_1979.wav"
song = AudioSegment.from_file(morespell_path)

# Optional: work in mono for simplicity (and smaller memory)
song = song.set_channels(1)

# Samples
A = 18*S
low_samp  = song[A+(1*S)+880:A+(2*S)+752]
mid_rep   = song[A+(4*S)+94:A+(5*S)+52]
high_rep  = song[A+(5*S)+893:A+(6*S)+373]

# ========= Create looped versions =========
# You can multiply segments to repeat them.
low_samp_stretch = stretch(low_samp, 0.94)
lb = low_samp_stretch
mid_samp_stretch = stretch(mid_rep, 0.94)
la = mid_samp_stretch
high_samp_stretch = stretch(high_rep, 0.94)
lc = high_samp_stretch

sample_1 = la + la + la + lb 
sample_2 = lc + lc + lc + lc + lc + lc + lb

sample = sample_1 + sample_1 + sample_1 + sample_2

# ========= Build a timeline with events =========
# We'll represent the timeline as a list of dicts:
#   { "start_ms": <int>, "segment": <AudioSegment> }

events = []

# Example structure (you can adapt to taste):

# Loop B
events.append({"start_ms": 0, "segment": sample})

# Render the timeline
total_duration_ms = compute_total_duration_ms(events)

# Start with silence
mix = AudioSegment.silent(duration=total_duration_ms)

# Overlay each event
for ev in events:
    mix = mix.overlay(ev["segment"], position=ev["start_ms"])

# Play
mix.export("onemoretime.mp3", format="mp3")
# play(mix)

# Export
# mix.export("remix.wav", format="wav")




# BBB = B * 3   # B B B
# CCCCCCCC = C * 8
# pattern = (B * 3) + A + (B * 3) + A + (B * 3) + A + CCCCCCCC





"""
# ========= Load original track =========
# Use your local file here; can be .mp3, .wav, etc.
morespell_path = Path("/Users/egg/Music/Music/eddie_johns_more_spell_on_you_1979.wav")
song = AudioSegment.from_file(morespell_path)

# Optional: work in mono for simplicity (and smaller memory)
song = song.set_channels(1)

# ========= Define some sample cuts =========
# Replace these with the exact ms you want from your track.
# For example:
#   - a short vocal stab
#   - a kick loop
#   - a synth riff

# (All times below are placeholders, not from the actual Daft Punk track.)
A = 18*S
low_rep  = song[A+(1*S)+10:A+(2*S)+100]   # 1s chunk starting at 10s
mid_rep = song[A+(3*S)+1:A+(3*S)+200]   # 1.5s chunk starting at 20.5s
high_rep  = song[A+(3*S)+500:A+(4*S)+1]   # 0.5s chunk (kick)

# ========= Create looped versions =========
# You can multiply segments to repeat them.
vocal_loop_8   = vocal_hit * 8     # 8 repetitions in sequence
synth_loop_4   = synth_riff * 4
kick_loop_16   = kick_loop * 16

# ========= Build a timeline with events =========
# We'll represent the timeline as a list of dicts:
#   { "start_ms": <int>, "segment": <AudioSegment> }

events = []

# Example structure (you can adapt to taste):

# 0–8s: vocal loop
events.append({"start_ms": 0, "segment": vocal_loop_8})

# 4–12s: synth loop coming in halfway, overlapping vocals
events.append({"start_ms": 4 * SEC_MS, "segment": synth_loop_4})

# 0–8s: kick underneath everything (loops for 8s)
events.append({"start_ms": 0, "segment": kick_loop_16})

# 12–20s: another block of vocal loop
events.append({"start_ms": 12 * SEC_MS, "segment": vocal_loop_8})

# You can add as many as you want, including re-using the same segments
# in multiple places with different start times.

# ========= Render the timeline =========
# Find how long the track needs to be:
def compute_total_duration_ms(events):
    total = 0
    for ev in events:
        end = ev["start_ms"] + len(ev["segment"])
        if end > total:
            total = end
    return total

total_duration_ms = compute_total_duration_ms(events)

# Start with silence, then overlay each event.
mix = AudioSegment.silent(duration=total_duration_ms)

for ev in events:
    mix = mix.overlay(ev["segment"], position=ev["start_ms"])

# Optional: normalize / adjust volume
mix = mix.apply_gain(-3)  # e.g., turn down a bit to avoid clipping

# ========= Export =========
mix.export("remix.wav", format="wav")
print("Done! Wrote remix.wav")

# =====================================================================================

import simpleaudio as sa

play_obj = sa.play_buffer(
    audio.raw_data,
    num_channels=audio.channels,
    bytes_per_sample=audio.sample_width,
    sample_rate=audio.frame_rate
)

play_obj.wait_done()

"""

