import tkinter as tk
from tkinter import messagebox

class Question:
    def __init__(self, prompt, choices, answer):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer

    def check_answer(self, user_answer):
        return user_answer == self.answer

class Quiz:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question_index = 0

    def add_question(self, question):
        self.questions.append(question)

    def get_current_question(self):
        return self.questions[self.current_question_index]

    def next_question(self):
        self.current_question_index += 1

    def has_more_questions(self):
        return self.current_question_index < len(self.questions)

    def answer_current_question(self, user_answer):
        question = self.get_current_question()
        if question.check_answer(user_answer):
            self.score += 1

    def reset(self):
        self.score = 0
        self.current_question_index = 0

class LoginWindow:
    def __init__(self, user_db):
        self.window = tk.Tk()
        self.window.title("Login/Register")
        self.window.configure(bg="#2c3e50")  # Dull dark blue

        self.user_db = user_db
        self.role = None

        self.main_frame = tk.Frame(self.window, bg="#2c3e50")
        self.main_frame.pack(padx=20, pady=20)

        self.title_label = tk.Label(self.main_frame, text="Login or Register", bg="#2c3e50", fg="white", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.username_label = tk.Label(self.main_frame, text="Username:", bg="#2c3e50", fg="white")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.main_frame, text="Password:", bg="#2c3e50", fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self.main_frame, text="Role (admin/student):", bg="#2c3e50", fg="white")
        self.role_label.pack(pady=5)
        self.role_entry = tk.Entry(self.main_frame)
        self.role_entry.pack(pady=5)

        self.register_button = tk.Button(self.main_frame, text="Register", command=self.register, bg="white", fg="#2c3e50")
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.login, bg="white", fg="#2c3e50")
        self.login_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get().lower()

        if username and password and role in ("admin", "student"):
            if username not in self.user_db:
                self.user_db[username] = {'password': password, 'role': role}
                messagebox.showinfo("Registration Successful", "You have registered successfully!")
            else:
                messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            messagebox.showerror("Registration Failed", "Please fill in all fields correctly.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.user_db and self.user_db[username]['password'] == password:
            self.role = self.user_db[username]['role']
            self.window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def run(self):
        self.window.mainloop()
        return self.role

class AdminWindow:
    def __init__(self, quiz):
        self.quiz = quiz
        self.window = tk.Tk()
        self.window.title("Admin - Set Questions")
        self.window.configure(bg="#2c3e50")

        self.main_frame = tk.Frame(self.window, bg="#2c3e50")
        self.main_frame.pack(padx=20, pady=20)

        self.prompt_label = tk.Label(self.main_frame, text="Question Prompt:", bg="#2c3e50", fg="white")
        self.prompt_label.pack(pady=5)
        self.prompt_entry = tk.Entry(self.main_frame, width=50)
        self.prompt_entry.pack(pady=5)

        self.choices_labels = []
        self.choices_entries = []

        for i in range(4):
            choice_label = tk.Label(self.main_frame, text=f"Choice {i+1}:", bg="#2c3e50", fg="white")
            choice_label.pack(pady=5)
            choice_entry = tk.Entry(self.main_frame, width=50)
            choice_entry.pack(pady=5)
            self.choices_labels.append(choice_label)
            self.choices_entries.append(choice_entry)

        self.answer_label = tk.Label(self.main_frame, text="Answer:", bg="#2c3e50", fg="white")
        self.answer_label.pack(pady=5)
        self.answer_entry = tk.Entry(self.main_frame, width=50)
        self.answer_entry.pack(pady=5)

        self.add_button = tk.Button(self.main_frame, text="Add Question", command=self.add_question, bg="white", fg="#2c3e50")
        self.add_button.pack(pady=20)

        self.done_button = tk.Button(self.main_frame, text="Done", command=self.finish, bg="white", fg="#2c3e50")
        self.done_button.pack(pady=10)

    def add_question(self):
        prompt = self.prompt_entry.get()
        choices = [entry.get() for entry in self.choices_entries]
        answer = self.answer_entry.get()
        if prompt and all(choices) and answer:
            question = Question(prompt, choices, answer)
            self.quiz.add_question(question)
            messagebox.showinfo("Success", "Question added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Incomplete data", "Please fill out all fields.")

    def clear_entries(self):
        self.prompt_entry.delete(0, tk.END)
        for entry in self.choices_entries:
            entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def finish(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class QuizApp:
    def __init__(self, quiz):
        self.quiz = quiz
        self.window = tk.Tk()
        self.window.title("Quiz App")
        self.window.configure(bg="#2c3e50")

        self.main_frame = tk.Frame(self.window, bg="#2c3e50")
        self.main_frame.pack(side="left", padx=100, pady=20)  # Adjusted padding to move content more to the center

        self.question_number_label = tk.Label(self.main_frame, text="", wraplength=400, justify="left", bg="#2c3e50", fg="white", font=("Arial", 14))
        self.question_number_label.pack(pady=10)

        self.question_label = tk.Label(self.main_frame, text="", wraplength=400, justify="left", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.radio_value = tk.StringVar()
        self.radio_buttons = []

        for _ in range(4):  # assuming 4 choices per question
            rb = tk.Radiobutton(self.main_frame, text="", variable=self.radio_value, value="", bg="#2c3e50", fg="white", selectcolor="#2c3e50")
            rb.pack(anchor="w")
            self.radio_buttons.append(rb)

        self.submit_button = tk.Button(self.main_frame, text="Submit", command=self.submit_answer, bg="white", fg="#2c3e50")
        self.submit_button.pack(pady=20)

        # Add the logo
        self.logo_frame = tk.Frame(self.window, bg="#2c3e50")
        self.logo_frame.pack(side="right", padx=20, pady=20)

        self.logo_image = tk.PhotoImage(file="path_to_your_logo.png").subsample(1, 1)  # Increase the size slightly
        self.logo_label = tk.Label(self.logo_frame, image=self.logo_image, bg="#2c3e50")
        self.logo_label.pack()

        self.load_question()

    def load_question(self):
        if self.quiz.has_more_questions():
            question = self.quiz.get_current_question()
            question_number = self.quiz.current_question_index + 1
            self.question_number_label.config(text=f"QUESTION {question_number}")
            self.question_label.config(text=question.prompt)

            for rb, choice in zip(self.radio_buttons, question.choices):
                rb.config(text=choice, value=choice)

            self.radio_value.set(None)  # Reset radio button selection
        else:
            self.show_score()

    def submit_answer(self):
        user_answer = self.radio_value.get()
        if user_answer:
            self.quiz.answer_current_question(user_answer)
            self.quiz.next_question()
            self.load_question()
        else:
            messagebox.showwarning("No selection", "Please select an answer.")

    def show_score(self):
        score_message = f"Your final score is: {self.quiz.score} out of {len(self.quiz.questions)}"
        messagebox.showinfo("Quiz Completed", score_message)
        self.quiz.reset()  # Reset the quiz for the next user
        self.window.quit()

    def run(self):
        self.window.mainloop()

# Main logic
def main():
    user_db = {}  # User database

    quiz = Quiz()  # Initialize the quiz once and keep the questions

    while True:
        login_window = LoginWindow(user_db)
        role = login_window.run()

        if role == "admin":
            admin_window = AdminWindow(quiz)
            admin_window.run()
        elif role == "student":
            if quiz.questions:
                quiz_app = QuizApp(quiz)
                quiz_app.run()
            else:
                messagebox.showinfo("No Questions", "No questions have been set.")
        else:
            break

main()
