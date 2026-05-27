import customtkinter as ctk
import random
import string
import threading
import time
import winsound

#слова
WORDS = [
    "python","matrix","cipher","shadow","binary","system","access","decode",
    "kernel","signal","server","buffer","script","botnet","crypto","daemon",
    "filter","socket","thread","vector","trojan","packet","router","bypass",
    "shield","memory","module","hunter","breach","stealth","quantum","portal",
    "nexus","proxy","vault","ghost","alarm","stack","shell","patch","frame",
    "agent","index","trace","block","chain","crypt","delta","error","flash",
    "forge","guard","input","laser","logic","media","nodes","omega","phase",
    "query","radar","relay","reset","rogue","spawn","surge","sweep","token",
    "turbo","ultra","virus","wired","yield","zebra","admin","alert","alpha",
    "angel","array","audit","beast","blade","brain","cable","clock","cloud",
    "cobra","codec","comet","creed","cyber","debug","drive","drone","dwarf",
    "eagle","ether","event","exile","field","final","force","front","frost",
    "grant","graph","grave","greed","grid","hash","helix","hydra","image",
    "intel","iris","judge","lance","layer","level","light","limit","linux",
    "local","lock","login","lumen","macro","magic","major","maker","march",
    "match","maze","mesh","mind","minor","model","morse","nano","nerve","night",
    "noise","north","nova","null","ocean","open","orbit","order","panic","parse",
    "path","peak","pixel","plan","point","power","prime","probe","proof","proto",
    "pulse","purge","range","rank","rapid","rate","reach","realm","recon","reign",
    "relic","rival","robot","root","route","royal","rule","safe","saint","scale",
    "scan","scope","score","scout","seize","sense","setup","shade","shaft","sharp",
    "shift","shock","shore","siege","sight","slice","slide","slope","smart","snake",
    "solar","solid","solve","sonic","south","space","spark","speed","spike","split",
    "squad","stage","stake","stamp","state","steel","stick","stone","store","storm",
    "strap","study","style","super","sword","sync","table","tango","task","teach",
    "team","tempo","tesla","test","titan","torch","total","touch","tower","track",
    "trail","train","trait","trap","trend","trial","tribe","trick","trust","twist",
    "union","unity","unlock","urban","user","valid","value","valve","venom","verse",
    "video","vigor","viral","visit","vital","voice","watch","water","wave","weave",
    "white","whole","world","worth","write","zenith","zero","zeta","zoom",
]
WORDS = sorted(set(w for w in WORDS if 4 <= len(w) <= 8))

NOISE_CHARS  = r"!@#$%^&*()_+-=[]{}|;:,.<>?/~`\\"
GREEN        = "#00FF41"
DIM_GREEN    = "#007A1F"
DARK_GREEN   = "#003D10"
BG           = "#000000"
AMBER        = "#FFB000"
RED_FLASH    = "#FF3030"
RED          = "#FF3030"

TOTAL_LEVELS = 100
MAX_ATTEMPTS = 8
TIMER_START  = 60
LINE_COUNT   = 45
LINE_LEN     = 240
MOVE_EVERY   = 8
NOISE_TICK   = 0.15

def noise_char():
    return random.choice(NOISE_CHARS + string.digits)

def make_noise_line(length=LINE_LEN):
    return "".join(noise_char() for _ in range(length))

def embed_word(word, line_len=LINE_LEN):
    max_start = line_len - len(word)
    start = random.randint(0, max_start)
    before = "".join(noise_char() for _ in range(start))
    after  = "".join(noise_char() for _ in range(line_len - start - len(word)))
    return before + word.upper() + after, start


class HackerGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("TERMINAL_v2.1 — HACK THE SYSTEM")
        
        self.attributes("-fullscreen", True)
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        
        self.configure(fg_color=BG)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.level        = 1
        self.word         = ""
        self.word_line    = 0
        self.word_start   = 0
        self.attempts     = MAX_ATTEMPTS
        self.game_over    = False
        self.word_found   = False
        self.rain_running = False
        self.rain_lines   = []
        self.noise_tick   = 0          
        self.timer_val    = TIMER_START
        self.timer_running = False

        self._build_ui()
        self._start_level()

    def _build_ui(self):

        top = ctk.CTkFrame(self, fg_color=BG)
        top.pack(fill="x", padx=10, pady=(8, 0))

        self.lbl_level = ctk.CTkLabel(top, text="LEVEL: 001 / 100",
            font=("Courier New", 18, "bold"), text_color=GREEN)
        self.lbl_level.pack(side="left")

        self.lbl_timer = ctk.CTkLabel(top, text="TIME: 60s",
            font=("Courier New", 14, "bold"), text_color=GREEN)
        self.lbl_timer.pack(side="left", padx=30)

        self.lbl_attempts = ctk.CTkLabel(top, text="ATTEMPTS: 8",
            font=("Courier New", 18, "bold"), text_color=AMBER)
        self.lbl_attempts.pack(side="right")

        self.lbl_word_len = ctk.CTkLabel(top, text="WORD LEN: ?",
            font=("Courier New", 18, "bold"), text_color=DIM_GREEN)
        self.lbl_word_len.pack(side="right", padx=20)


        self.progress = ctk.CTkProgressBar(self, progress_color=DIM_GREEN,
            fg_color=DARK_GREEN, height=4)
        self.progress.pack(fill="x", padx=10, pady=(4, 0))
        self.progress.set(0)

        self.timer_bar = ctk.CTkProgressBar(self, progress_color=GREEN,
            fg_color=DARK_GREEN, height=6)
        self.timer_bar.pack(fill="x", padx=10, pady=(2, 0))
        self.timer_bar.set(1.0)

        self.term_frame = ctk.CTkFrame(self, fg_color="#050505",
            border_color=DIM_GREEN, border_width=1, corner_radius=4)
        self.term_frame.pack(fill="both", expand=True, padx=10, pady=6)

        self.term_text = ctk.CTkTextbox(
        self.term_frame,
        font=("Courier New", 18),
        fg_color="#050505",
        text_color=DIM_GREEN,
        wrap="none",
        state="disabled",
        activate_scrollbars=False,
        cursor="arrow"
    )
        self.term_text.pack(fill="both", expand=True, padx=2, pady=2)

        self.term_text.tag_config("noise",  foreground=DIM_GREEN)
        self.term_text.tag_config("found",  foreground=AMBER)
        self.term_text.tag_config("flash",  foreground=RED_FLASH)
        self.term_text.tag_config("header", foreground=GREEN)
        self.term_text.tag_config("wrong_line", foreground=RED_FLASH)

        self.term_text._textbox.bind("<Button-1>", self._on_click)

        gf = ctk.CTkFrame(self, fg_color=BG)
        gf.pack(fill="x", padx=10, pady=(0, 3))

        self.lbl_hint = ctk.CTkLabel(gf,
            text=">> FIND AND CLICK THE HIDDEN WORD  |  HINT: _ = wrong  * = wrong place  LETTER = correct",
            font=("Courier New", 11), text_color=DIM_GREEN)
        self.lbl_hint.pack(anchor="w")

        self.guess_display = ctk.CTkFrame(gf, fg_color=BG)
        self.guess_display.pack(anchor="w", pady=2)

        self.history_text = ctk.CTkTextbox(self, height=210,
            font=("Courier New", 18),
            fg_color="#050505",
            text_color=DIM_GREEN,
            state="disabled",
            border_color=DARK_GREEN, border_width=1)
        self.history_text.pack(fill="x", padx=10, pady=(0, 8))
        self.history_text.tag_config("correct",  foreground=GREEN)
        self.history_text.tag_config("miss",      foreground=AMBER)
        self.history_text.tag_config("wrong",     foreground="#444444")
        self.history_text.tag_config("info",      foreground=DIM_GREEN)
        self.history_text.tag_config("danger",    foreground=RED_FLASH)

    def _start_level(self):
        self.word       = random.choice(WORDS).upper()
        self.attempts   = MAX_ATTEMPTS
        self.word_found = False
        self.noise_tick = 0
        self._clear_guess_display()
        self._update_header()
        self._log(f"[SYSTEM] Level {self.level:03d} initialized. Seek word length={len(self.word)}.", "info")
        self._log("[SYSTEM] Word moves every few seconds. Click it to capture.", "info")
        self._build_terminal()
        self._reset_timer()

    def _update_header(self):
        self.lbl_level.configure(text=f"LEVEL: {self.level:03d} / {TOTAL_LEVELS}")
        self.lbl_attempts.configure(text=f"ATTEMPTS: {self.attempts}")
        self.lbl_word_len.configure(text=f"WORD LEN: {len(self.word) if self.word else '?'}")
        self.progress.set((self.level - 1) / TOTAL_LEVELS)

    def _build_terminal(self):
        self.word_line  = random.randint(2, LINE_COUNT - 3)
        self.rain_lines = []
        for i in range(LINE_COUNT):
            if i == self.word_line:
                line, self.word_start = embed_word(self.word)
                self.rain_lines.append(line)
            else:
                self.rain_lines.append(make_noise_line())
        self._render_terminal()

    def _move_word(self):
        """Regenerate the word's line at a new random position."""
        # clear old line to pure noise
        self.rain_lines[self.word_line] = make_noise_line()
        # pick new line
        self.word_line  = random.randint(2, LINE_COUNT - 3)
        line, self.word_start = embed_word(self.word)
        self.rain_lines[self.word_line] = line

    def _render_terminal(self, flash_row=None):
        tb = self.term_text._textbox
        tb.config(state="normal")
        tb.delete("1.0", "end")

        header = (
            f"root@SYSTEM:~# scan --level={self.level:03d} "
            f"--word-len={len(self.word)} --attempts={self.attempts}\n"
            f"{'─'*LINE_LEN}\n"
        )
        tb.insert("end", header, "header")

        for i, line in enumerate(self.rain_lines):
            if self.word_found and i == self.word_line:
                tb.insert("end", line + "\n", "found")
            elif flash_row is not None and i == flash_row:
                tb.insert("end", line + "\n", "wrong_line")
            else:
                tb.insert("end", line + "\n", "noise")

        tb.config(state="disabled")


    def _reset_timer(self):
        self.timer_val     = TIMER_START
        self.timer_running = True
        self._tick_timer()

    def _tick_timer(self):
        if not self.timer_running or self.word_found or self.game_over:
            return
        self.timer_val -= 1
        ratio = max(self.timer_val / TIMER_START, 0)

        # colour shifts: green → amber → red
        if self.timer_val > 30:
            col = GREEN
        elif self.timer_val > 10:
            col = AMBER
        else:
            col = RED

        self.lbl_timer.configure(text=f"TIME: {self.timer_val:02d}s", text_color=col)
        self.timer_bar.configure(progress_color=col)
        self.timer_bar.set(ratio)

        if self.timer_val <= 0:
            self._timer_expired()
        else:
            self.after(1000, self._tick_timer)

    def _timer_expired(self):
        self.timer_running = False
        self._log(f"[TIMEOUT] Time expired. Word was: {self.word}. Level restarting...", "danger")
        self.attempts -= 1
        self.lbl_attempts.configure(text=f"ATTEMPTS: {self.attempts}")
        if self.attempts <= 0:
            self._game_over_level()
        else:
            self.after(1400, self._start_level)


    def _on_click(self, event):
        if self.game_over or self.word_found:
            return

        tb   = self.term_text._textbox
        idx  = tb.index(f"@{event.x},{event.y}")
        row, col = map(int, idx.split("."))


        content_row = row - 3
        word_row    = self.word_line

        if content_row == word_row:
            s = self.word_start
            e = s + len(self.word)
            if s <= col < e:
                self._correct_click()
                return


        self._wrong_click(content_row)

    def _correct_click(self):
        self.word_found    = True
        self.timer_running = False
        self._render_terminal()
        
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(base_dir, "sound", "click.wav")
        
        threading.Thread(target=lambda: winsound.PlaySound(sound_path, winsound.SND_FILENAME), daemon=True).start()
        
        self._log(f"[ACCESS GRANTED] Word '{self.word}' captured! Proceeding...", "correct")
        self.after(1000, self._next_level)

    def _wrong_click(self, clicked_row):
        # flash clicked row briefly
        self._render_terminal(flash_row=clicked_row)
        self.after(220, self._render_terminal)

        self.attempts -= 1
        self.lbl_attempts.configure(text=f"ATTEMPTS: {self.attempts}")

        # wordle-style feedback based on what letters are at that row/position
        guess = self._extract_or_random(clicked_row)
        self._evaluate_guess(guess)

        if self.attempts <= 0:
            self._game_over_level()

    def _extract_or_random(self, row):
        """Try to extract letters from the clicked line, else random."""
        if 0 <= row < len(self.rain_lines):
            line = self.rain_lines[row]
            letters = "".join(c for c in line if c.isalpha())
            if len(letters) >= len(self.word):
                start = random.randint(0, max(0, len(letters) - len(self.word)))
                return letters[start:start + len(self.word)].upper()
        return "".join(random.choice(string.ascii_uppercase) for _ in range(len(self.word)))

    def _evaluate_guess(self, guess):
        word   = self.word
        result = []
        for i, ch in enumerate(guess[:len(word)]):
            if i < len(word) and ch == word[i]:
                result.append((ch, "correct"))
            elif ch in word:
                result.append((ch, "miss"))
            else:
                result.append((ch, "wrong"))

        disp = " ".join(
            ch if s == "correct" else ("*" if s == "miss" else "_")
            for ch, s in result
        )
        dominant = result[0][1] if result else "wrong"
        self._log(f"[SCAN] {disp}  | {self.attempts} attempts left", dominant)
        self._update_guess_display(result)

    def _update_guess_display(self, result):
        self._clear_guess_display()
        color_map = {"correct": GREEN, "miss": AMBER, "wrong": "#333333"}
        for ch, status in result:
            disp_ch = ch if status == "correct" else ("*" if status == "miss" else "_")
            box = ctk.CTkFrame(self.guess_display, fg_color="#0a0a0a",
                border_color=color_map[status], border_width=1,
                width=34, height=38, corner_radius=2)
            box.pack(side="left", padx=2)
            box.pack_propagate(False)
            ctk.CTkLabel(box, text=disp_ch,
                font=("Courier New", 14, "bold"),
                text_color=color_map[status]).place(relx=.5, rely=.5, anchor="center")

    def _clear_guess_display(self):
        for w in self.guess_display.winfo_children():
            w.destroy()


    def _game_over_level(self):
        self.timer_running = False
        self._log(f"[BREACH FAILED] The word was: {self.word}. Reinitializing...", "danger")
        self.attempts = MAX_ATTEMPTS
        self.after(1600, self._start_level)

    def _next_level(self):
        if self.level >= TOTAL_LEVELS:
            self._victory()
            return
        self.level += 1
        self._start_level()

    def _victory(self):
        self.game_over     = True
        self.timer_running = False
        self._log("[ROOT] ALL 100 LEVELS BREACHED. FULL SYSTEM ACCESS GRANTED.", "correct")
        self.lbl_hint.configure(
            text=">> ROOT ACCESS ACHIEVED — SYSTEM FULLY COMPROMISED",
            text_color=GREEN)


    def _log(self, text, tag="info"):
        ht = self.history_text
        ht.configure(state="normal")
        ht.insert("end", text + "\n", tag)
        ht.see("end")
        ht.configure(state="disabled")


    def _start_rain(self):
        self.rain_running = True
        threading.Thread(target=self._rain_loop, daemon=True).start()

    def _rain_loop(self):
        while self.rain_running:
            time.sleep(NOISE_TICK)
            if self.game_over:
                continue
            if self.word_found:
                continue

            self.noise_tick += 1


            if self.noise_tick % MOVE_EVERY == 0:
                self._move_word()

            # mutate noise lines
            for i in range(len(self.rain_lines)):
                if i != self.word_line and random.random() < 0.45:
                    self.rain_lines[i] = make_noise_line()

            self.after(0, self._render_terminal)

    def _on_close(self):
        self.rain_running  = False
        self.timer_running = False
        self.destroy()


if __name__ == "__main__":
    app = HackerGame()
    app._start_rain()
    app.mainloop()
