import torchaudio
import os

def redact_audio(audio_path, pii_segments):
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    # Use soundfile backend (default when soundfile is installed)
    # torchaudio.set_audio_backend("soundfile")

    # Extract filename and rename from in- to out-
    input_filename = os.path.basename(audio_path)
    output_filename = input_filename.replace("in-", "out-")
    output_dir = "output_audio"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    # Filter valid segments
    valid_segments = [seg for seg in pii_segments if seg is not None]

    # Load audio
    waveform, sample_rate = torchaudio.load(audio_path)

    # Redact PII segments
    for start, end in valid_segments:
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)
        waveform[:, start_sample:end_sample] = 0  # Silence

    # Save the redacted audio
    torchaudio.save(output_path, waveform, sample_rate)
    print(f"✅ Redacted audio saved at: {output_path}")
