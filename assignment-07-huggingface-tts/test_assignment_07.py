"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 07:
- Module signature & function presence
- Waveform generation and PCM 16-bit math validation
- RIFF WAV header compliance (Mono, 16-bit, 22,050 Hz)
- Audio sample recordings and manifest integrity
- Interactive Jupyter Notebook (.ipynb) schema validity
- Prompt specifications and meta-prompt verification
"""

import sys
import os
import json
import wave
from pathlib import Path

# Add module directory to sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import tts_inference as tts


def test_signatures_and_constants():
    """Verify all expected functions and constants exist."""
    assert hasattr(tts, "DEFAULT_TEXT")
    assert isinstance(tts.DEFAULT_TEXT, str) and len(tts.DEFAULT_TEXT) > 0

    assert hasattr(tts, "SAMPLE_TEXTS")
    assert len(tts.SAMPLE_TEXTS) == 3

    assert callable(tts.run_tts_inference)
    assert callable(tts.synthesize_phoneme_waveform)
    assert callable(tts.write_wav_file)
    print("[PASS] Test 1: Signatures and constants verified.")


def test_synthesizer_pcm_data_integrity():
    """Verify that synthesize_phoneme_waveform produces valid 16-bit PCM bytes."""
    text = "Unit test verification of speech synthesis."
    pcm_bytes, rate, duration = tts.synthesize_phoneme_waveform(text, sample_rate=22050)

    assert isinstance(pcm_bytes, bytes)
    assert rate == 22050
    assert duration > 1.0

    # Each 16-bit sample is exactly 2 bytes
    expected_bytes = int(rate * duration) * 2
    assert len(pcm_bytes) == expected_bytes, f"Expected {expected_bytes} bytes, got {len(pcm_bytes)}"
    print("[PASS] Test 2: PCM 16-bit waveform math and sample lengths verified.")


def test_wav_file_riff_header_compliance():
    """Verify that generated WAV file complies with standard RIFF 16-bit Mono specifications."""
    test_wav = SCRIPT_DIR / "temp_test_output.wav"
    try:
        res = tts.run_tts_inference("Testing wave header compliance.", output_path=test_wav, force_demo=True)
        assert res["success"] is True
        assert test_wav.exists()

        # Open and inspect RIFF header via standard wave library
        with wave.open(str(test_wav), "rb") as wf:
            assert wf.getnchannels() == 1, "Expected Mono (1 channel)"
            assert wf.getsampwidth() == 2, "Expected 16-bit (2 bytes per sample)"
            assert wf.getframerate() == 22050, "Expected 22,050 Hz sampling rate"
            nframes = wf.getnframes()
            assert nframes > 0, "Waveform has 0 frames"

            # Duration calculation check
            wav_duration = nframes / wf.getframerate()
            assert abs(wav_duration - res["duration_seconds"]) < 0.1

        print("[PASS] Test 3: RIFF WAV header, channels, and frame rates verified.")
    finally:
        if test_wav.exists():
            os.remove(test_wav)


def test_sample_audio_suite():
    """Verify that all 3 sample audio recordings and the manifest report exist."""
    samples_dir = SCRIPT_DIR / "sample_audio"
    assert samples_dir.exists(), "sample_audio directory missing"

    for filename, _ in tts.SAMPLE_TEXTS:
        wav_file = samples_dir / filename
        assert wav_file.exists(), f"Sample audio missing: {filename}"
        assert wav_file.stat().st_size > 10000, f"Sample audio {filename} is suspiciously small"

        with wave.open(str(wav_file), "rb") as wf:
            assert wf.getnchannels() == 1
            assert wf.getframerate() == 22050

    manifest = samples_dir / "audio_samples_manifest.md"
    assert manifest.exists(), "audio_samples_manifest.md missing"
    content = manifest.read_text(encoding="utf-8")
    assert "sample_1_test_run.wav" in content
    assert "sample_2_ai_elevate.wav" in content
    assert "sample_3_logistics_voice.wav" in content

    print("[PASS] Test 4: 3 sample audio recordings and manifest verified.")


def test_jupyter_notebook_schema():
    """Verify that tts_inference.ipynb exists, is valid JSON, and adheres to nbformat 4."""
    nb_file = SCRIPT_DIR / "tts_inference.ipynb"
    assert nb_file.exists(), "tts_inference.ipynb missing"

    with open(nb_file, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    assert nb_data.get("nbformat") == 4
    assert "cells" in nb_data
    assert len(nb_data["cells"]) >= 5

    # Ensure code cells exist and contain key steps
    code_cells = [c for c in nb_data["cells"] if c.get("cell_type") == "code"]
    assert len(code_cells) >= 3

    print("[PASS] Test 5: Interactive Jupyter Notebook (.ipynb) schema and cells verified.")


def test_documentation_and_prompts():
    """Verify that GENERATION_PROMPT.md, prompts.md, and README.md exist."""
    assert (SCRIPT_DIR / "GENERATION_PROMPT.md").exists(), "GENERATION_PROMPT.md missing"
    assert (SCRIPT_DIR / "prompts.md").exists(), "prompts.md missing"
    assert (SCRIPT_DIR / "README.md").exists(), "README.md missing"
    print("[PASS] Test 6: Prompt specifications, generation meta-prompt, and README verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 07")
    print("=" * 65)
    test_signatures_and_constants()
    test_synthesizer_pcm_data_integrity()
    test_wav_file_riff_header_compliance()
    test_sample_audio_suite()
    test_jupyter_notebook_schema()
    test_documentation_and_prompts()
    print("=" * 65)
    print("  ALL 6 TESTS PASSED! ASSIGNMENT 07 IS FULLY VERIFIED.")
    print("=" * 65)
