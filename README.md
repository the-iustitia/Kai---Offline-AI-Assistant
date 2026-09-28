# Kai---Offline-AI-Assistant

# Kai — Offline AI Assistant

**Kai** is a local AI voice assistant for Windows, built around local models and tools.

The project is designed to control a computer and perform user tasks through natural speech.

The core principle:

```text
User voice
    ↓
 Whisper
    ↓
Qwen / Ollama
    ↓
Command Router
    ↓
 Executor
    ↓
Tool / Action
    ↓
   Kai
    ↓
  Piper
    ↓
Voice response
```

---

## Features

The current version supports:

* voice input;
* Russian speech recognition;
* local LLM through Ollama;
* two model modes;
* conversation context;
* notes;
* reminders;
* deleting notes and reminders;
* automatic execution of multiple actions;
* local text-to-speech;
* command logging;
* a simple command router;
* Tkinter-based graphical interface;
* particle-based assistant visualization;
* fully local operation of the core components.

---

# Architecture

The project is divided into several main layers.

```text
GUI
 │
 ├── Audio recording
 │
 ├── Speech-to-Text
 │       └── Faster-Whisper
 │
 ├── Conversation
 │       ├── Mode detection
 │       ├── Context
 │       ├── Command Router
 │       └── LLM
 │
 ├── Executor
 │       └── Tools
 │
 └── Text-to-Speech
         └── Piper
```

### Main pipeline

```text
Microphone
    ↓
app/audio.py
    ↓
app/transcriber.py
    ↓
app/conversation.py
    ↓
app/command_router.py
    ↓
app/agent.py
    ↓
Ollama
    ↓
app/executor.py
    ↓
app/tools/*
    ↓
app/tts.py
    ↓
app/player.py
```

---

# Tech Stack

## Runtime

* Python 3.13
* Windows 10+

## Speech-to-Text

**Faster-Whisper**

Used for local speech recognition.

Current model:

```text
medium
```

Primary language:

```text
ru
```

---

## LLM

**Ollama**

Models currently used:

```text
qwen2.5:0.5b
qwen2.5:3b
```

### FAST

```text
qwen2.5:0.5b
```

Used for everyday commands and fast responses.

### SMART

```text
qwen2.5:3b
```

Used for more complex requests.

Model selection is handled by `app/conversation.py`.

---

## Text-to-Speech

**Piper**

Used for local voice response generation.

---

## GUI

**Tkinter**

The graphical interface contains:

* particle animation;
* assistant state display;
* FAST/SMART mode visualization;
* click handling;
* voice pipeline execution.

---

# Project Structure

```text
ai-assistant/
│
├── app/
│   │
│   ├── agent.py
│   ├── audio.py
│   ├── command_log.py
│   ├── command_router.py
│   ├── conversation.py
│   ├── executor.py
│   ├── gui.py
│   ├── particle_core.py
│   ├── player.py
│   ├── reminder_worker.py
│   ├── router.py
│   ├── telegram_bot.py
│   ├── transcriber.py
│   ├── tts.py
│   │
│   └── tools/
│       ├── notes.py
│       ├── reminder_parser.py
│       └── reminders.py
│
├── data/
│   ├── notes.txt
│   ├── reminders.db
│   ├── command_log.db
│   └── piper/
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── remove_comments.py
```

---

# Core Components

## `app/gui.py`

Main entry point for the graphical interface.

Responsible for:

* creating the window;
* particle animation;
* starting the voice pipeline;
* displaying assistant state;
* starting the reminder worker;
* playing voice responses.

---

## `app/particle_core.py`

Responsible for Kai's visual state.

Main states:

```text
idle
listening
processing
speaking
error
```

It also supports two modes:

```text
fast
smart
```

In FAST mode, particles form a human silhouette.

In SMART mode, particles form a processor.

When an error occurs, the current shape is preserved while the particle color changes.

---

## `app/conversation.py`

Main orchestration layer.

Responsible for:

* conversation history;
* current mode;
* model selection;
* special command handling;
* command routing;
* LLM calls;
* action execution;
* final response generation.

The current mode is stored inside:

```python
Conversation()
```

Therefore, the mode state exists within the current assistant process.

---

## `app/agent.py`

Responsible for communication with the LLM.

Main functions:

```python
analyze_command()
generate_response()
```

`analyze_command()` instructs the model to return an action as JSON.

Example:

```json
{
    "action": "create_note",
    "text": "Buy a water filter"
}
```

For multiple actions:

```json
{
    "actions": [
        {
            "action": "create_note",
            "text": "Buy a filter"
        },
        {
            "action": "create_reminder",
            "text": "Call Sergey",
            "when": "tomorrow at 18:00"
        }
    ]
}
```

---

# Executor

## `app/executor.py`

The Executor receives an action from the LLM and calls the corresponding tool.

Supported actions:

```text
create_note
get_notes
delete_note

create_reminder
get_reminders
delete_reminder

chat
```

The LLM does not execute functions directly.

It only determines:

```text
what needs to be done
```

The Executor determines:

```text
how it should be done
```

This separation is an important part of the architecture.

---

# Tools

Tools are located in:

```text
app/tools/
```

## Notes

`app/tools/notes.py`

Notes are stored in:

```text
data/notes.txt
```

Supported operations:

```text
create
get
delete
```

---

## Reminders

`app/tools/reminders.py`

Reminders are stored in:

```text
data/reminders.db
```

SQLite is used for persistent storage.

Time expressions are processed by:

```text
app/tools/reminder_parser.py
```

Supported expressions include:

```text
in 30 minutes
in 2 hours
in 3 days

today at 18:00
tomorrow at 10:30
the day after tomorrow at 09:00
```

---

# Command Router

`app/command_router.py`

The Router allows known commands to be executed without calling the LLM.

It uses fuzzy matching.

This reduces processing time for frequently repeated commands.

The current implementation uses:

* `SequenceMatcher`;
* word overlap;
* a similarity threshold.

The LLM remains the fallback mechanism for commands that the Router does not recognize.

---

# Context

Conversation history is stored in:

```python
Conversation.messages
```

Only a limited number of recent messages are passed to the LLM.

Current limits:

```text
MAX_HISTORY_MESSAGES = 20
MAX_CONTEXT_MESSAGES = 20
```

The context allows Kai to handle commands such as:

> Remember this.

or:

> Delete the last one.

when the required information is present in the previous conversation.

---

# Model Modes

Mode switching is handled before the LLM is called.

## SMART

Commands include:

```text
think
think about it
enable advanced mode
enable smart mode
smart mode
```

Uses:

```text
qwen2.5:3b
```

## FAST

Commands include:

```text
normal mode
fast mode
enable normal mode
enable fast mode
disable advanced mode
disable smart mode
```

Uses:

```text
qwen2.5:0.5b
```

Text normalization is performed before command matching.

This is useful because speech recognition may produce variations of the same command.

For example, Whisper may recognize a command incorrectly, while the normalizer can correct known recognition patterns before processing.

---

# Running the Project

## 1. Install dependencies

```cmd
py -3 -m pip install -r requirements.txt
```

---

## 2. Start Ollama

If Ollama is not already running:

```cmd
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
```

In another terminal, check the installed models:

```cmd
ollama list
```

The following models are required:

```text
qwen2.5:0.5b
qwen2.5:3b
```

---

## 3. Start Kai

From the project root:

```cmd
py -3 app\gui.py
```

The graphical interface will appear.

Clicking the window starts voice recording.

---

# Environment Variables

Sensitive data should be stored in:

```text
.env
```

The `.env` file must not be committed to Git.

Example:

```text
TELEGRAM_BOT_TOKEN=...
```

If Telegram functionality is not being used, the token is not required for the local GUI.

---

# Telegram

Telegram was added as an additional interface.

The primary interface is currently:

```text
GUI + microphone
```

Telegram is not required for local operation of Kai.

---

# Offline Operation

The main pipeline can operate without an internet connection:

```text
Microphone
    ↓
Faster-Whisper
    ↓
Ollama
    ↓
Executor
    ↓
Tools
    ↓
Piper
```

All of these components run locally.

An internet connection is only required for features that communicate with external services, as well as for the initial installation and model downloads.

---

# Git Workflow

Before making major changes, it is recommended to create a commit with the current working state.

Basic workflow:

```cmd
git add .
git commit -m "Description of changes"
git push
```

The project also includes a helper script:

```cmd
py -3 git_kai.py
```

It shows the current changes, asks for a description, and automatically runs:

```text
git add
git commit
git push
```

---

# Current Status

The project is under active development.

The main pipeline is currently working:

```text
Voice
  ↓
Whisper
  ↓
Conversation
  ↓
Router / Qwen
  ↓
Executor
  ↓
Tools
  ↓
Response
  ↓
Piper
  ↓
Voice
```

Currently implemented tools:

```text
Notes
Reminders
Chat
```

Also implemented:

```text
FAST / SMART modes
Conversation context
Command Router
SQLite reminders
Local TTS
Particle GUI
```

---

# Development Roadmap

Current development priorities include:

* improving speech recognition;
* optimizing Whisper performance;
* improving LLM action selection;
* improving conversational context;
* expanding the tool system;
* file operations;
* Windows application control;
* system commands;
* calendar integration;
* email integration;
* internet-based tools;
* more advanced reminders;
* persistent memory;
* GUI improvements;
* full voice-based computer control.

The architecture is also intended to support other platforms in the future.

---

# Project Principles

### Local-first

Computations should be performed locally whenever practical.

### Tool-based architecture

The LLM should not directly perform system operations.

It selects an action, while execution is handled by a controlled tool.

### Model routing

Simple tasks should use the faster model.

More complex tasks can be routed to the more capable model.

### Voice-first

Voice is the primary interaction method.

The GUI is primarily used for visualizing the assistant's state and controlling the interaction.

### Modular architecture

New capabilities should be added as separate tools rather than turning `agent.py` into a giant collection of unrelated logic.

---

# License

The project is currently under development
