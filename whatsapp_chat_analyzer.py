import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import re
import os
import textwrap
from datetime import datetime
from collections import Counter

import pandas as pd

# Matplotlib for charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ==================================================
# WhatsApp Chat Analyzer - Single File GUI App
# - Dark Netflix-style UI
# - Load .txt export from WhatsApp
# - Show stats, top users, top words, activity charts
# ==================================================


# ==========================================
# PART 1: COLORS & BASIC UI COMPONENTS
# ==========================================

class Colors:
    BACKGROUND = "#111111"
    SURFACE = "#1E1E1E"
    SURFACE_HOVER = "#2A2A2A"
    ACCENT = "#25D366"  # WhatsApp green-ish
    TEXT_MAIN = "#FFFFFF"
    TEXT_SUB = "#B3B3B3"
    BORDER = "#333333"
    DANGER = "#E50914"


class ScrollableFrame(tk.Frame):
    """Reusable vertical scrollable frame."""
    def __init__(self, parent, bg=Colors.BACKGROUND, *args, **kwargs):
        super().__init__(parent, bg=bg, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel scroll
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        )


class StatsCard(tk.Frame):
    """Small card widget to display a number + label."""
    def __init__(self, parent, title, value="0", width=160):
        super().__init__(parent, bg=Colors.SURFACE, highlightthickness=1,
                         highlightbackground=Colors.BORDER, padx=10, pady=8)

        self.configure(width=width)
        self.grid_propagate(False)

        self.lbl_title = tk.Label(
            self, text=title, font=("Helvetica", 9),
            bg=Colors.SURFACE, fg=Colors.TEXT_SUB, anchor="w"
        )
        self.lbl_title.pack(fill="x")

        self.lbl_value = tk.Label(
            self, text=value, font=("Helvetica", 16, "bold"),
            bg=Colors.SURFACE, fg=Colors.TEXT_MAIN, anchor="w"
        )
        self.lbl_value.pack(fill="x", pady=(4, 0))

    def set_value(self, value):
        self.lbl_value.config(text=str(value))


class MessagePreviewCard(tk.Frame):
    """Card to show a sample message snippet."""
    def __init__(self, parent, sender, text, timestamp):
        super().__init__(parent, bg=Colors.SURFACE, highlightbackground=Colors.BORDER,
                         highlightthickness=1, padx=8, pady=6)

        self.columnconfigure(0, weight=1)

        header_text = f"{sender} • {timestamp}"
        self.lbl_header = tk.Label(
            self, text=header_text, font=("Helvetica", 9, "bold"),
            bg=Colors.SURFACE, fg=Colors.ACCENT, anchor="w"
        )
        self.lbl_header.grid(row=0, column=0, sticky="ew")

        snippet = textwrap.shorten(text, width=120, placeholder=" ...")
        self.lbl_body = tk.Label(
            self, text=snippet, font=("Helvetica", 9),
            bg=Colors.SURFACE, fg=Colors.TEXT_MAIN,
            wraplength=600, justify="left", anchor="w"
        )
        self.lbl_body.grid(row=1, column=0, sticky="ew", pady=(3, 0))


# ==========================================
# PART 2: WHATSAPP CHAT PARSER & ANALYZER
# ==========================================

class WhatsAppChatParser:
    """
    Parses WhatsApp exported chat .txt file into a pandas DataFrame.

    Expected line format examples:
    - "12/09/21, 10:35 pm - John Doe: Hello!"
    - "1/1/2022, 09:01 - Jane: Happy New Year!"
    Continuation lines (no date at start) are appended to previous message.
    """
    # Regex for common WhatsApp formats
    # e.g. "12/09/21, 10:35 pm - Name: Message"
    LINE_REGEX = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)\s+-\s+(.*)$'
    )

    def __init__(self):
        self.df = pd.DataFrame()

    def parse_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        messages = []
        current_msg = None

        for raw in lines:
            match = self.LINE_REGEX.match(raw)
            if match:
                # New message starts
                date_str, time_str, rest = match.groups()

                sender, message = self._split_sender_message(rest)

                dt = self._parse_datetime(date_str, time_str)

                if current_msg:
                    messages.append(current_msg)

                current_msg = {
                    "datetime": dt,
                    "date": dt.date(),
                    "time": dt.time(),
                    "sender": sender,
                    "message": message.strip()
                }
            else:
                # Continuation of previous message
                if current_msg:
                    current_msg["message"] += "\n" + raw
                else:
                    # System info before first recognized line
                    continue

        if current_msg:
            messages.append(current_msg)

        if not messages:
            raise ValueError("No WhatsApp messages recognized. Check file format.")

        self.df = pd.DataFrame(messages)
        self._add_extra_columns()
        return self.df

    def _split_sender_message(self, rest):
        """
        Split "Name: message" and handle system messages.
        """
        if ": " in rest:
            sender, msg = rest.split(": ", 1)
        else:
            sender = "System"
            msg = rest
        return sender, msg

    def _parse_datetime(self, date_str, time_str):
        """
        Try a few common datetime formats for WhatsApp.
        """
        # Clean up time like "10:35 pm" or "10:35pm" to strptime-friendly
        time_str = time_str.replace("p. m.", "PM").replace("a. m.", "AM")
        time_str = time_str.replace("p.m.", "PM").replace("a.m.", "AM")
        time_str = time_str.replace("pm", "PM").replace("am", "AM")
        # Try multiple formats
        formats = [
            "%d/%m/%y, %I:%M %p",
            "%d/%m/%Y, %I:%M %p",
            "%d/%m/%y, %H:%M",
            "%d/%m/%Y, %H:%M",
        ]
        full_str = f"{date_str}, {time_str}"
        for fmt in formats:
            try:
                return datetime.strptime(full_str, fmt)
            except ValueError:
                continue
        # Fallback: try without comma in time
        full_str2 = f"{date_str} {time_str}"
        formats2 = [
            "%d/%m/%y %H:%M",
            "%d/%m/%Y %H:%M",
            "%d/%m/%y %I:%M %p",
            "%d/%m/%Y %I:%M %p",
        ]
        for fmt in formats2:
            try:
                return datetime.strptime(full_str2, fmt)
            except ValueError:
                continue
        # If everything fails, use "now" but keep original data
        return datetime.now()

    def _add_extra_columns(self):
        if self.df.empty:
            return
        self.df["weekday"] = self.df["datetime"].dt.day_name()
        self.df["hour"] = self.df["datetime"].dt.hour
        self.df["word_count"] = self.df["message"].apply(
            lambda x: len(str(x).split())
        )
        self.df["is_media"] = self.df["message"].str.contains(
            r"<Media omitted>|image omitted|video omitted", case=False, na=False
        )


class ChatAnalyzer:
    """Performs statistics & text analysis on the parsed DataFrame."""
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def basic_stats(self):
        total_messages = len(self.df)
        total_words = int(self.df["word_count"].sum())
        total_media = int(self.df["is_media"].sum())
        total_days = self.df["date"].nunique()
        first_date = self.df["date"].min()
        last_date = self.df["date"].max()
        return {
            "total_messages": total_messages,
            "total_words": total_words,
            "total_media": total_media,
            "total_days": total_days,
            "first_date": first_date,
            "last_date": last_date
        }

    def messages_by_user(self):
        return self.df["sender"].value_counts()

    def words_by_user(self):
        return self.df.groupby("sender")["word_count"].sum().sort_values(ascending=False)

    def busiest_hours(self):
        return self.df.groupby("hour").size()

    def busiest_weekdays(self):
        # Use ordered weekday index
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                         "Friday", "Saturday", "Sunday"]
        counts = self.df["weekday"].value_counts()
        return counts.reindex(weekday_order).fillna(0).astype(int)

    def top_words(self, n=20, stopwords=None):
        if stopwords is None:
            stopwords = set()
        all_words = []
        for msg in self.df["message"]:
            words = re.findall(r"\b\w+\b", str(msg).lower())
            words = [w for w in words if w not in stopwords and len(w) > 2]
            all_words.extend(words)
        counter = Counter(all_words)
        return counter.most_common(n)


# ==========================================
# PART 3: MAIN APP - GUI
# ==========================================

class WhatsAppAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhatsApp Chat Analyzer")
        self.geometry("1100x700")
        self.configure(bg=Colors.BACKGROUND)

        # Data related
        self.parser = WhatsAppChatParser()
        self.df = pd.DataFrame()
        self.analyzer = None
        self.current_file = None

        # Matplotlib figures cache
        self.current_figure = None
        self.current_canvas = None

        # Setup UI
        self._setup_styles()
        self._create_header()
        self._create_layout()
        self._create_overview_panel()
        self._create_right_panel()

        self._set_status("Load a WhatsApp .txt chat file to begin.")

    # -------------- Styles & Layout --------------

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TButton", padding=4)
        style.configure("Accent.TButton", background=Colors.ACCENT, foreground="white")
        style.map("Accent.TButton",
                  background=[("active", "#1EB858")])

    def _create_header(self):
        header = tk.Frame(self, bg=Colors.BACKGROUND, height=60)
        header.pack(fill="x", padx=16, pady=(10, 0))

        title = tk.Label(
            header, text="WhatsApp Chat Analyzer",
            font=("Helvetica", 20, "bold"),
            bg=Colors.BACKGROUND, fg=Colors.ACCENT
        )
        title.pack(side="left")

        self.file_label = tk.Label(
            header, text="No file loaded",
            font=("Helvetica", 9),
            bg=Colors.BACKGROUND, fg=Colors.TEXT_SUB
        )
        self.file_label.pack(side="right")

    def _create_layout(self):
        main = tk.Frame(self, bg=Colors.BACKGROUND)
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # Left sidebar
        self.sidebar = tk.Frame(main, bg=Colors.SURFACE, width=250,
                                highlightbackground=Colors.BORDER, highlightthickness=1)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_propagate(False)

        # Right content
        self.content = tk.Frame(main, bg=Colors.BACKGROUND)
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar controls
        self._create_sidebar_controls()

        # Status bar
        footer = tk.Frame(self, bg=Colors.SURFACE, height=24)
        footer.pack(fill="x", side="bottom")
        self.status_label = tk.Label(
            footer, text="", anchor="w",
            bg=Colors.SURFACE, fg=Colors.TEXT_SUB, padx=8, font=("Helvetica", 9)
        )
        self.status_label.pack(fill="both")

    def _create_sidebar_controls(self):
        lbl = tk.Label(self.sidebar, text="Controls", font=("Helvetica", 11, "bold"),
                       bg=Colors.SURFACE, fg=Colors.TEXT_MAIN, anchor="w")
        lbl.pack(fill="x", padx=10, pady=(10, 4))

        btn_load = tk.Button(
            self.sidebar, text="Load WhatsApp Chat (.txt)",
            command=self.load_chat_file,
            bg=Colors.ACCENT, fg="white",
            activebackground="#1EB858", activeforeground="white",
            relief="flat", padx=8, pady=4, font=("Helvetica", 9, "bold")
        )
        btn_load.pack(fill="x", padx=10, pady=(0, 12))

        # Filters separator
        sep = tk.Frame(self.sidebar, bg=Colors.BORDER, height=1)
        sep.pack(fill="x", padx=10, pady=(0, 8))

        # User filter
        lbl_user = tk.Label(self.sidebar, text="Filter by sender",
                            font=("Helvetica", 9), bg=Colors.SURFACE,
                            fg=Colors.TEXT_SUB, anchor="w")
        lbl_user.pack(fill="x", padx=10)
        self.sender_var = tk.StringVar(value="All")
        self.sender_combo = ttk.Combobox(
            self.sidebar, textvariable=self.sender_var, state="readonly",
            values=["All"]
        )
        self.sender_combo.pack(fill="x", padx=10, pady=(0, 10))
        self.sender_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())

        # Keyword filter
        lbl_kw = tk.Label(self.sidebar, text="Filter by keyword",
                          font=("Helvetica", 9), bg=Colors.SURFACE,
                          fg=Colors.TEXT_SUB, anchor="w")
        lbl_kw.pack(fill="x", padx=10)
        self.keyword_var = tk.StringVar()
        entry_kw = tk.Entry(self.sidebar, textvariable=self.keyword_var,
                            bg=Colors.BACKGROUND, fg=Colors.TEXT_MAIN,
                            insertbackground=Colors.TEXT_MAIN,
                            relief="flat", font=("Helvetica", 9))
        entry_kw.pack(fill="x", padx=10, pady=(0, 4))

        btn_apply = tk.Button(
            self.sidebar, text="Apply Filters",
            command=self._apply_filters,
            bg=Colors.SURFACE_HOVER, fg=Colors.TEXT_MAIN,
            activebackground=Colors.SURFACE_HOVER, activeforeground=Colors.TEXT_MAIN,
            relief="flat", padx=8, pady=3, font=("Helvetica", 9)
        )
        btn_apply.pack(fill="x", padx=10, pady=(0, 8))

        btn_reset = tk.Button(
            self.sidebar, text="Reset Filters",
            command=self._reset_filters,
            bg=Colors.SURFACE, fg=Colors.TEXT_SUB,
            activebackground=Colors.SURFACE_HOVER, activeforeground=Colors.TEXT_MAIN,
            relief="flat", padx=8, pady=3, font=("Helvetica", 9)
        )
        btn_reset.pack(fill="x", padx=10, pady=(0, 10))

        # Small info label
        info = tk.Label(
            self.sidebar,
            text="Tip: export chat from WhatsApp\nwithout media, then load the .txt file.",
            font=("Helvetica", 8),
            bg=Colors.SURFACE, fg=Colors.TEXT_SUB, justify="left"
        )
        info.pack(fill="x", padx=10, pady=(10, 10))

    def _create_overview_panel(self):
        # Top area: overview statistics & charts
        top = tk.Frame(self.content, bg=Colors.BACKGROUND)
        top.pack(fill="both", expand=True)

        # Stats frame (top row)
        stats_frame = tk.Frame(top, bg=Colors.BACKGROUND)
        stats_frame.pack(fill="x", pady=(0, 10))

        self.card_messages = StatsCard(stats_frame, "Total Messages")
        self.card_messages.pack(side="left", padx=(0, 10))

        self.card_words = StatsCard(stats_frame, "Total Words")
        self.card_words.pack(side="left", padx=(0, 10))

        self.card_media = StatsCard(stats_frame, "Media Messages")
        self.card_media.pack(side="left", padx=(0, 10))

        self.card_days = StatsCard(stats_frame, "Active Days")
        self.card_days.pack(side="left", padx=(0, 10))

        # Date range label
        self.lbl_range = tk.Label(
            stats_frame, text="Date range: -",
            font=("Helvetica", 9), bg=Colors.BACKGROUND,
            fg=Colors.TEXT_SUB
        )
        self.lbl_range.pack(side="right", padx=4)

        # Middle: chart + right stats
        mid = tk.Frame(top, bg=Colors.BACKGROUND)
        mid.pack(fill="both", expand=True)

        # Left chart area
        chart_frame = tk.Frame(mid, bg=Colors.SURFACE,
                               highlightbackground=Colors.BORDER, highlightthickness=1)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        chart_frame.pack_propagate(False)

        self.chart_frame_inner = chart_frame

        # Right side: top users & words
        side_stats = tk.Frame(mid, bg=Colors.BACKGROUND)
        side_stats.pack(side="right", fill="y", padx=(8, 0))

        lbl_users = tk.Label(
            side_stats, text="Top Senders",
            font=("Helvetica", 11, "bold"), bg=Colors.BACKGROUND,
            fg=Colors.TEXT_MAIN
        )
        lbl_users.pack(anchor="w")

        self.txt_users = tk.Text(
            side_stats, height=10, width=32,
            bg=Colors.SURFACE, fg=Colors.TEXT_MAIN,
            insertbackground=Colors.TEXT_MAIN, relief="flat",
            font=("Helvetica", 9)
        )
        self.txt_users.pack(fill="x", pady=(2, 6))

        lbl_words = tk.Label(
            side_stats, text="Top Words",
            font=("Helvetica", 11, "bold"), bg=Colors.BACKGROUND,
            fg=Colors.TEXT_MAIN
        )
        lbl_words.pack(anchor="w", pady=(4, 0))

        self.txt_words = tk.Text(
            side_stats, height=10, width=32,
            bg=Colors.SURFACE, fg=Colors.TEXT_MAIN,
            insertbackground=Colors.TEXT_MAIN, relief="flat",
            font=("Helvetica", 9)
        )
        self.txt_words.pack(fill="x", pady=(2, 6))

    def _create_right_panel(self):
        # Bottom area: sample messages
        bottom_label = tk.Label(
            self.content, text="Sample Messages (after filters)",
            font=("Helvetica", 11, "bold"),
            bg=Colors.BACKGROUND, fg=Colors.TEXT_MAIN
        )
        bottom_label.pack(anchor="w", pady=(8, 0))

        self.messages_scroll = ScrollableFrame(self.content, bg=Colors.BACKGROUND)
        self.messages_scroll.pack(fill="both", expand=True, pady=(4, 4))

    # -------------- Status helper --------------

    def _set_status(self, text):
        self.status_label.config(text=text)
        self.update_idletasks()

    # -------------- File loading & data prep --------------

    def load_chat_file(self):
        path = filedialog.askopenfilename(
            title="Select WhatsApp Chat .txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            df = self.parser.parse_file(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse chat file:\n{e}")
            self._set_status("Failed to load file.")
            return

        self.current_file = path
        self.df = df
        self.analyzer = ChatAnalyzer(df)
        filename = os.path.basename(path)
        self.file_label.config(text=filename)
        self._set_status(f"Loaded {filename} with {len(df)} messages.")

        # Populate sender filter options
        senders = sorted(self.df["sender"].unique().tolist())
        self.sender_combo["values"] = ["All"] + senders
        self.sender_combo.current(0)

        # Reset filters and refresh UI
        self.keyword_var.set("")
        self._update_overview()
        self._populate_sample_messages()

    # -------------- Filtering --------------

    def _apply_filters(self):
        if self.df.empty:
            return
        df_filtered = self.df.copy()

        # Sender filter
        sender = self.sender_var.get()
        if sender and sender != "All":
            df_filtered = df_filtered[df_filtered["sender"] == sender]

        # Keyword filter
        keyword = self.keyword_var.get().strip()
        if keyword:
            df_filtered = df_filtered[
                df_filtered["message"].str.contains(keyword, case=False, na=False)
            ]

        if df_filtered.empty:
            self._set_status("No messages match current filters.")
        else:
            self._set_status(f"{len(df_filtered)} messages match current filters.")

        self.analyzer = ChatAnalyzer(df_filtered)
        self._update_overview()
        self._populate_sample_messages()

    def _reset_filters(self):
        if self.df.empty:
            return
        self.sender_combo.current(0)
        self.keyword_var.set("")
        self.analyzer = ChatAnalyzer(self.df)
        self._update_overview()
        self._populate_sample_messages()
        self._set_status("Filters reset.")

    # -------------- Overview update --------------

    def _update_overview(self):
        if not self.analyzer:
            return
        stats = self.analyzer.basic_stats()
        self.card_messages.set_value(stats["total_messages"])
        self.card_words.set_value(stats["total_words"])
        self.card_media.set_value(stats["total_media"])
        self.card_days.set_value(stats["total_days"])

        if stats["total_messages"] > 0:
            self.lbl_range.config(
                text=f"Date range: {stats['first_date']}  →  {stats['last_date']}"
            )
        else:
            self.lbl_range.config(text="Date range: -")

        # Top users
        self._update_top_users()
        # Top words
        self._update_top_words()
        # Chart
        self._update_chart()

    def _update_top_users(self):
        if not self.analyzer:
            return
        self.txt_users.config(state="normal")
        self.txt_users.delete("1.0", "end")
        s = self.analyzer.messages_by_user()
        if s.empty:
            self.txt_users.insert("end", "No data.\n")
        else:
            total = int(s.sum())
            for name, count in s.head(10).items():
                pct = (count / total) * 100 if total else 0
                self.txt_users.insert(
                    "end",
                    f"{name}: {count} msgs ({pct:.1f}%)\n"
                )
        self.txt_users.config(state="disabled")

    def _update_top_words(self):
        if not self.analyzer:
            return
        self.txt_words.config(state="normal")
        self.txt_words.delete("1.0", "end")

        # Simple stopwords list (you can expand this)
        stopwords = {
            "the", "and", "for", "this", "that", "you", "are", "was", "with", "have",
            "but", "not", "your", "from", "all", "just", "like", "one", "get", "what",
            "out", "can", "see", "our", "now", "too", "why", "how", "who", "she", "him",
            "her", "they", "them", "then", "there", "here", "when", "where", "been",
            "will", "would", "could", "should", "did", "had", "has", "got", "yeah",
        }

        top_words = self.analyzer.top_words(n=20, stopwords=stopwords)
        if not top_words:
            self.txt_words.insert("end", "No data.\n")
        else:
            for word, count in top_words:
                self.txt_words.insert("end", f"{word}: {count}\n")
        self.txt_words.config(state="disabled")

    def _update_chart(self):
        # Destroy previous chart
        if self.current_canvas is not None:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None

        if not self.analyzer:
            return

        # Create figure
        fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0))
        plt.subplots_adjust(wspace=0.4)

        # Left: hourly distribution
        hours = self.analyzer.busiest_hours()
        if not hours.empty:
            axes[0].bar(hours.index.astype(str), hours.values)
            axes[0].set_title("Messages by Hour", fontsize=8)
            axes[0].set_xlabel("Hour", fontsize=7)
            axes[0].set_ylabel("Messages", fontsize=7)
            axes[0].tick_params(axis="both", labelsize=7)
        else:
            axes[0].text(0.5, 0.5, "No data", ha="center", va="center", fontsize=8)
            axes[0].axis("off")

        # Right: weekday distribution
        weekdays = self.analyzer.busiest_weekdays()
        if not weekdays.empty:
            axes[1].bar(weekdays.index, weekdays.values)
            axes[1].set_title("Messages by Weekday", fontsize=8)
            axes[1].set_xlabel("Weekday", fontsize=7)
            axes[1].set_ylabel("Messages", fontsize=7)
            axes[1].tick_params(axis="x", rotation=45, labelsize=7)
            axes[1].tick_params(axis="y", labelsize=7)
        else:
            axes[1].text(0.5, 0.5, "No data", ha="center", va="center", fontsize=8)
            axes[1].axis("off")

        fig.patch.set_facecolor(Colors.SURFACE)
        for ax in axes:
            ax.set_facecolor("#202020")

        self.current_figure = fig
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame_inner)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=6, pady=6)
        self.current_canvas = canvas

    # -------------- Sample messages --------------

    def _populate_sample_messages(self):
        # Clear previous
        for child in self.messages_scroll.inner.winfo_children():
            child.destroy()

        if not self.analyzer:
            return

        df = self.analyzer.df
        if df.empty:
            lbl = tk.Label(
                self.messages_scroll.inner,
                text="No messages to display.",
                bg=Colors.BACKGROUND, fg=Colors.TEXT_SUB,
                font=("Helvetica", 9)
            )
            lbl.pack(pady=10)
            return

        # Show last 30 messages (sorted)
        df_sorted = df.sort_values("datetime").tail(30)

        for _, row in df_sorted.iterrows():
            ts = row["datetime"].strftime("%d/%m/%Y, %H:%M")
            card = MessagePreviewCard(
                self.messages_scroll.inner,
                sender=row["sender"],
                text=row["message"],
                timestamp=ts
            )
            card.pack(fill="x", pady=3)


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    try:
        app = WhatsAppAnalyzerApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
