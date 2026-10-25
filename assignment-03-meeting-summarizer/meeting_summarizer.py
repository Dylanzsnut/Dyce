"""
Assignment 03: AI-Powered Meeting Summarizer Using Azure OpenAI API
-------------------------------------------------------------------
Processes raw meeting transcripts and generates structured, concise summaries
highlighting:
- Executive Overview
- Key Discussion Points
- Decisions Made
- Action Items (Owner & Deadline)

Supports:
- Batch processing all 5 sample transcripts (default)
- Single-file summarization (--file path/to/transcript.txt)
- Interactive command-line UI (--interactive)
- Automatic chunking for large meeting transcripts

Required Environment Variables:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI resource API key
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI resource endpoint URL
- AZURE_OPENAI_DEPLOYMENT_NAME: Model deployment name (defaults to 'gpt-4o-mini')
"""

import argparse
import os
import sys
from pathlib import Path
from openai import AzureOpenAI, OpenAIError

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
    load_dotenv()
except ImportError:
    pass


API_VERSION = "2024-07-01-preview"
DEFAULT_DEPLOYMENT = "gpt-4o-mini"
MAX_CHUNK_CHARS = 12000

SYSTEM_PROMPT = (
    "You are a helpful assistant specialized in summarizing meeting notes. "
    "Produce clear, accurate, and concise summaries organized into four sections: "
    "1. Executive Overview, 2. Key Points, 3. Decisions Made, and "
    "4. Action Items (including owner and deadline when mentioned)."
)


# Step 1: Azure OpenAI Client Setup
def create_azure_client():
    """Initialize and return the AzureOpenAI client and deployment name from env vars."""
    api_key = (os.getenv("AZURE_OPENAI_API_KEY") or "").strip()
    endpoint = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
    api_version = (os.getenv("AZURE_OPENAI_API_VERSION") or API_VERSION).strip()
    deployment_name = (
        os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or DEFAULT_DEPLOYMENT
    ).strip()

    missing = []
    if not api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}.\n"
            "Please set them in your environment or create a .env file from .env.example."
        )

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )
    return client, deployment_name


# Step 2: Load Transcript Text from File
def load_transcript(file_path):
    """Read and validate a meeting transcript text file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Transcript file not found: {path}")

    transcript = path.read_text(encoding="utf-8").strip()
    if not transcript:
        raise ValueError(f"Transcript file is empty: {path}")

    return transcript


# Step 3: Craft Prompt & Handle Large Textual Inputs
def build_summary_prompt(transcript):
    """Craft the summarization prompt for a meeting transcript."""
    return (
        "Summarize the following meeting transcript with key points, "
        "decisions, and action items.\n\n"
        "Use this exact Markdown structure:\n"
        "### Executive Overview\n"
        "- Brief 1-2 sentence overview of the meeting purpose and outcome.\n\n"
        "### Key Points\n"
        "- Bullet points of the main topics, metrics, and risks discussed.\n\n"
        "### Decisions Made\n"
        "- Bullet points of all concrete decisions agreed upon by the team.\n\n"
        "### Action Items\n"
        "- **[Owner]**: Task description *(Due: [Date/Timeframe])*\n\n"
        f"Meeting Transcript:\n{transcript}"
    )


def split_into_chunks(text, max_chars=MAX_CHUNK_CHARS):
    """Split very long transcripts along line boundaries so chunks fit model context."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_lines = []
    current_len = 0

    for line in text.splitlines(keepends=True):
        if current_len + len(line) > max_chars and current_lines:
            chunks.append("".join(current_lines).strip())
            current_lines = [line]
            current_len = len(line)
        else:
            current_lines.append(line)
            current_len += len(line)

    if current_lines:
        chunks.append("".join(current_lines).strip())

    return chunks


# Step 4: Call Azure OpenAI ChatCompletion API
def summarize_transcript(
    transcript,
    client=None,
    deployment_name=None,
    temperature=0.3,
    max_tokens=500,
):
    """
    Summarize a meeting transcript using Azure OpenAI GPT models.
    Automatically chunks and combines summaries if the transcript is very large.
    """
    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError("Transcript text must be a non-empty string.")

    if client is None or deployment_name is None:
        client, deployment_name = create_azure_client()

    chunks = split_into_chunks(transcript.strip())

    # Standard single-pass summarization
    if len(chunks) == 1:
        prompt = build_summary_prompt(chunks[0])
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content or ""
        return content.strip()

    # Multi-chunk map-reduce summarization for lengthy transcripts
    partial_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        chunk_prompt = (
            f"Summarize part {idx} of {len(chunks)} of this meeting transcript, "
            f"capturing key points, decisions, and action items:\n\n{chunk}"
        )
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": chunk_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        partial_summaries.append((response.choices[0].message.content or "").strip())

    combined_notes = "\n\n---\n\n".join(partial_summaries)
    final_prompt = build_summary_prompt(combined_notes)
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": final_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return (final_response.choices[0].message.content or "").strip()


# Step 5: Process Sample Files & Interactive UI
def process_all_samples(client, deployment_name):
    """Summarize all 5 sample transcripts and save individual + combined outputs."""
    base_dir = Path(__file__).resolve().parent
    transcripts_dir = base_dir / "sample_transcripts"
    outputs_dir = base_dir / "sample_outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    sample_files = sorted(transcripts_dir.glob("sample_*.txt"))
    if not sample_files:
        raise FileNotFoundError(f"No sample_*.txt files found in {transcripts_dir}")

    combined_sections = [
        "# AI-Powered Meeting Summarizer — 5 Sample Transcripts & Outputs\n",
        f"Generated using Azure OpenAI (`model={deployment_name}`, `temperature=0.3`, `max_tokens=500`).\n",
    ]

    for idx, transcript_path in enumerate(sample_files, start=1):
        transcript_text = load_transcript(transcript_path)
        summary_text = summarize_transcript(
            transcript_text,
            client=client,
            deployment_name=deployment_name,
        )

        print(f"=== Sample {idx}: {transcript_path.name} ===")
        print("Meeting Summary:\n")
        print(f"{summary_text}\n")

        summary_filename = transcript_path.stem.replace("sample_", "summary_") + ".md"
        summary_path = outputs_dir / summary_filename
        summary_doc = (
            f"# Meeting Summary — Sample {idx:02d}\n\n"
            f"**Source Transcript:** `{transcript_path.name}`\n\n"
            f"{summary_text}\n"
        )
        summary_path.write_text(summary_doc, encoding="utf-8")

        combined_sections.append(f"## Sample {idx}: `{transcript_path.name}`\n")
        combined_sections.append("### Raw Meeting Transcript\n")
        combined_sections.append(f"```text\n{transcript_text}\n```\n")
        combined_sections.append("### Generated Meeting Summary\n")
        combined_sections.append(f"{summary_text}\n")
        combined_sections.append("---\n")

    combined_path = base_dir / "all_sample_summaries.md"
    combined_path.write_text("\n".join(combined_sections), encoding="utf-8")
    print(f"Saved {len(sample_files)} summary files to: {outputs_dir}")
    print(f"Saved combined report to: {combined_path}")


def run_interactive_ui(client, deployment_name):
    """Run a simple command-line UI for uploading/selecting transcripts to summarize."""
    base_dir = Path(__file__).resolve().parent
    sample_files = sorted((base_dir / "sample_transcripts").glob("sample_*.txt"))

    print("====================================================")
    print("   AI-Powered Meeting Summarizer (Azure OpenAI)     ")
    print("====================================================")

    while True:
        try:
            print("\nOptions:")
            for idx, f in enumerate(sample_files, start=1):
                print(f"  [{idx}] Summarize sample: {f.name}")
            print("  [f] Upload / specify a custom transcript file path")
            print("  [a] Summarize all 5 sample transcripts")
            print("  [q] Quit")

            choice = input("\nSelect an option: ").strip().lower()
            if choice in ("q", "quit", "exit"):
                print("Exiting Meeting Summarizer. Goodbye!")
                break
            elif choice == "a":
                process_all_samples(client, deployment_name)
            elif choice == "f":
                custom_path = input("Enter path to transcript .txt file: ").strip().strip('"')
                try:
                    text = load_transcript(custom_path)
                    summary = summarize_transcript(text, client=client, deployment_name=deployment_name)
                    print("\nMeeting Summary:\n")
                    print(summary)
                except (FileNotFoundError, ValueError, OpenAIError) as err:
                    print(f"Error: {err}")
            elif choice.isdigit() and 1 <= int(choice) <= len(sample_files):
                selected = sample_files[int(choice) - 1]
                text = load_transcript(selected)
                summary = summarize_transcript(text, client=client, deployment_name=deployment_name)
                print(f"\n=== {selected.name} ===")
                print("Meeting Summary:\n")
                print(summary)
            else:
                print("Invalid option. Please choose a valid menu option.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Meeting Summarizer. Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Meeting Summarizer Using Azure OpenAI API"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a specific meeting transcript file to summarize.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional output file path when summarizing a single file with --file.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch the interactive command-line user interface.",
    )
    args = parser.parse_args()

    try:
        client, deployment_name = create_azure_client()
    except EnvironmentError as env_err:
        print(f"Configuration Error:\n{env_err}", file=sys.stderr)
        sys.exit(1)

    if args.interactive:
        run_interactive_ui(client, deployment_name)
        return

    if args.file:
        try:
            transcript_text = load_transcript(args.file)
            summary = summarize_transcript(
                transcript_text,
                client=client,
                deployment_name=deployment_name,
            )
            print("Meeting Summary:\n")
            print(summary)
            if args.output:
                Path(args.output).write_text(summary + "\n", encoding="utf-8")
                print(f"\nSaved summary to: {args.output}")
        except (FileNotFoundError, ValueError, OpenAIError) as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
        return

    # Default: Summarize all 5 sample meeting transcripts
    try:
        process_all_samples(client, deployment_name)
    except (FileNotFoundError, ValueError, OpenAIError) as err:
        print(f"Error processing sample transcripts: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
