# Prompts and Speech Synthesis Specifications: Assignment 07

## 1. Domain Overview
Text-to-Speech (TTS) synthesizes natural spoken human speech from written text. Modern neural TTS pipelines decouple synthesis into two distinct neural networks:
1. **Acoustic Model (e.g. FastSpeech 2)**: Converts phoneme sequences into intermediate mel-spectrogram representations (frequency distribution over time).
2. **Neural Vocoder (e.g. HiFi-GAN)**: Inverts mel-spectrograms into high-fidelity time-domain audio waveforms ($\sim 22,050 \text{ Hz}$).

---

## 2. Sample Speech Synthesis Prompts

| Sample ID | Domain / Intent | Synthesis Prompt | Intended Cadence |
| :--- | :--- | :--- | :--- |
| **TTS-01** | Standard Verification | *"Hello, this is a test run of the Hugging Face Text to Speech model."* | Neutral, informative benchmark tone |
| **TTS-02** | Educational / Program | *"Welcome to the AI Application Engineer training program. Today we explore neural audio synthesis."* | Formal, clear, articulate pedagogical pace |
| **TTS-03** | Logistics Voice Dispatch | *"Attention driver, heavy traffic reported on Interstate 95 due to construction. Rerouting dispatched."* | Urgent, crisp dispatch alert pacing |

---

## 3. Phonetic Text Normalization Guidelines
Neural acoustic models perform best when text is pre-normalized:
- **Numbers**: Convert numerals into spelled-out words (e.g., `400V` $\rightarrow$ *"four hundred volts"`, `10` $\rightarrow$ *"ten"*).
- **Acronyms**: Use hyphens or uppercase spaces for letter-by-letter pronunciation (e.g., `TTS` $\rightarrow$ *"T-T-S"*, `AI` $\rightarrow$ *"A-I"*).
- **Punctuation**: Commas inject brief pauses ($150\text{ms}$), periods terminate prosodic contours ($350\text{ms}$), and question marks elevate end-of-sentence pitch.

---

## 4. Modern Neural TTS Architecture Comparison

| Architecture | Pipeline Style | Latency | Voice Quality | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **FastSpeech 2 + HiFi-GAN** (This Assignment) | Two-stage Non-Autoregressive | **Ultra-Low** (Real-Time Factor $< 0.05$) | High, natural prosody | Edge devices, real-time voice assistants, low-latency APIs |
| **VITS** | Single-stage End-to-End VAE-GAN | **Low** (Real-Time Factor $< 0.1$) | Very High, natural expressive rhythm | Production voiceovers, interactive characters |
| **SpeechT5** | Unified Encoder-Decoder Transformer | **Moderate** | High with zero-shot speaker embedding support | Multi-speaker cloning, cross-lingual tasks |
| **Bark / AudioLM** | Autoregressive Audio Language Model | **High** | Ultra-expressive (laughter, sighs, breathing) | Creative storytelling, podcasts, cinematic dialogue |
