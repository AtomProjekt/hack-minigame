<p align="center">
  <img src="logo/logo.png" alt="TERMINAL_v2.1 Logo" width="220"/>
</p>

# ⚡ TERMINAL_v2.1 — HACK THE SYSTEM

---

> **WARNING:** Critical vulnerability detected in the system core. Forced breach protocol initiated. You have exactly 60 seconds before total terminal lockdown.

**TERMINAL_v2.1** is an uncompromising, hardcore cyberpunk hacking simulator designed to test your ultimate focus and reaction speed. Your mission is to penetrate the system's security barriers by tracking down hidden codewords buried inside a constantly mutating matrix of character noise.

---

## 🎮 Gameplay

The game is a pure digital stress test. A single keyword (ranging from 4 to 8 letters) is hidden among thousands of chaotic special characters on the screen.

* ⏳ **Ticking Timer:** You only get 60 seconds per level. Time is actively working against you.
* 🌀 **Unstable Matrix:** The codeword doesn't stay still! Every few seconds it "escapes"—regenerating and shifting to another random line.
* ❌ **Limited Attempts:** You have only 8 attempts. Every mistake not only burns an attempt but also causes the line to flash an alarming red.
* 🎧 **Audio Confirmation:** Upon successfully locating the word, the system emits a crisp audio cue confirming target capture.
* 🏆 **Objective:** Overcome 100 security levels to gain full ROOT access to the system.

---

## 🔍 Analysis System (Hint Mechanics)

If you misclick and hit a false line, the terminal's advanced scanner instantly analyzes the input and provides a Wordle-style breakdown in the bottom log panel:

| Symbol | Status | Description |
| :---: | :---: | :--- |
| **letter** | `Correct` | The letter is guessed correctly and is in its perfect position. |
| **\*** | `Miss` | This letter exists in the codeword, but it belongs in a different position. |
| **\_** | `Wrong` | This letter does not exist in the secret word at all. |

---

## 🛠️ Tech Stack

The project is completely autonomous and optimized to run flawlessly on Windows:
* **CustomTkinter** — Modern GUI styled in the deep dark-green aesthetics of authentic hacker consoles.
* **Winsound & OS** — Dynamic path resolution and "out-of-the-box" audio playback without installing heavy external game engines.
* **Threading** — Multithreading ensures smooth, independent character "rain" animations and sound effects without interface micro-stutters.

---
<p align="center"><i>Good luck hacking, operator. The system is waiting. 💀</i></p>