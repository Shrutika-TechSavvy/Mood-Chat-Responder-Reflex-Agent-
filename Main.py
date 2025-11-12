import tkinter as tk
from tkinter import scrolledtext
import string  # for punctuation cleanup

# -------------------------------------------------
#  Reflex Agent for Mood Detection
# -------------------------------------------------
class ChatMoodResponder:
    def __init__(self):
        #  Words that usually indicate positive emotions
        self.positive_words = {
            "happy", "good", "love", "fun", "great", "awesome", "cool", "joy",
            "fantastic", "amazing", "wonderful", "excited", "relaxed", "smile",
            "beautiful", "kind", "peaceful", "yay", "like", "grateful", "hopeful"
        }

        #  Words that usually indicate negative emotions
        self.negative_words = {
            "sad", "bad", "hate", "tired", "angry", "upset", "bored", "terrible",
            "mad", "lonely", "depressed", "anxious", "worried", "stress", "cry",
            "broken", "annoyed", "frustrated", "noisy", "dark", "awful"
        }

        #  Negation words can flip the meaning of the next sentiment word
        self.negations = {"not", "never", "don't", "didn't", "isn't", "wasn't", "can't", "won't", "no"}

    def perceive(self, user_input):
        """
         Perceive the user's text input and decide whether the overall
        mood feels positive, negative, or neutral.
        """

        #  Clean up punctuation and lowercase everything
        cleaned_input = user_input.lower().translate(str.maketrans('', '', string.punctuation))
        words = cleaned_input.split()

        mood_score = 0
        negate_next = False

        for word in words:
            if word in self.negations:
                negate_next = True
                continue

            # Positive word found
            if word in self.positive_words:
                mood_score += -1 if negate_next else 1

            # Negative word found
            elif word in self.negative_words:
                mood_score += 1 if negate_next else -1

            # Reset negation flag after one word
            negate_next = False

        #  Interpret the final mood score
        if mood_score > 0:
            return "positive"
        elif mood_score < 0:
            return "negative"
        else:
            return "neutral"

    def decide(self, mood):
        """
        Decide what to say based on detected mood.
        """
        if mood == "positive":
            return "That's wonderful to hear! Keep that energy up "
        elif mood == "negative":
            return "I'm really sorry you're feeling that way  Remember, it's okay to take a break."
        else:
            return "Hmm, I see... tell me more about how you feel."


# -------------------------------------------------
#  GUI using Tkinter
# -------------------------------------------------
class ChatGUI:
    def __init__(self, root):
        self.bot = ChatMoodResponder()

        #  Window setup
        root.title("Chat Mood Responder")
        root.geometry("520x460")
        root.resizable(False, False)

        #  Main container
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill='both', expand=True)

        #  Chat display area
        self.chat_log = scrolledtext.ScrolledText(
            frame, state='disabled', wrap='word', font=("Arial", 12), height=20
        )
        self.chat_log.pack(pady=(0, 10), fill='both', expand=True)

        # 👋 Friendly bot intro
        self.append_chat(
            "Bot",
            " Hello! I'm MoodBot — your friendly mood buddy.\n"
            "I can sense your vibes a little — tell me how you're feeling!"
        )

        #  Entry box + Send button
        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill='x')

        self.entry = tk.Entry(entry_frame, font=("Arial", 12))
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side='right')

    def send_message(self, event=None):
        """
         Triggered when user sends a message (presses Enter or clicks Send).
        """
        user_input = self.entry.get().strip()
        if not user_input:
            return

        # Show user message
        self.append_chat("You", user_input)

        # Bot processes mood and replies
        mood = self.bot.perceive(user_input)
        response = self.bot.decide(mood)
        self.append_chat("Bot", response)

        # Clear input box
        self.entry.delete(0, tk.END)

    def append_chat(self, sender, message):
        """
         Append messages to chat area with simple formatting.
        """
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)


# -------------------------------------------------
# Run the App
# -------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()
