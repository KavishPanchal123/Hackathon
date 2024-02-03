import tkinter as tk
from tkinter import ttk, messagebox

MAX_USERS = 10
MAX_JOBS = 100

class Job:
    def __init__(self, id, deadline, profit, time_taken):
        self.id = id
        self.deadline = deadline
        self.profit = profit
        self.time_taken = time_taken

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

def schedule_jobs(jobs):
    jobs.sort(key=lambda x: (x.deadline, -x.time_taken), reverse=True)
    slot = [False] * len(jobs)
    total_profit = 0
    total_time = 0
    result_text = ""

    for job in jobs:
        for j in range(min(job.deadline - 1, len(jobs) - 1), -1, -1):
            if not slot[j]:
                if total_time + job.time_taken <= j + 1:
                    slot[j] = True
                    total_time += job.time_taken
                    total_profit += job.profit
                    result_text += f"Job {job.id} scheduled at slot {j + 1} - Time taken: {job.time_taken} units\n"
                    break
        else:
            for k in range(len(jobs) - 1, -1, -1):
                if not slot[k] and total_time + jobs[k].time_taken <= jobs[k].deadline:
                    slot[k] = True
                    total_time += jobs[k].time_taken
                    total_profit += jobs[k].profit
                    result_text += f"Job {jobs[k].id} scheduled at slot {k + 1} - Time taken: {jobs[k].time_taken} units (Fallback)\n"
                    break

    result_text += f"Total profit: {total_profit}"
    return result_text

def save_jobs_for_current_user(users, current_user):
    for user in users:
        if user.username == current_user.username:
            user.jobs = current_user.jobs
            return True
    else:
        return False

def display_job_schedule_for_current_user(current_user):
    result_text = ""
    if current_user.jobs:
        result_text += f"Current Job Schedule for user: {current_user.username}\n"
        for job in current_user.jobs:
            result_text += f"Job {job.id}: Deadline={job.deadline}, Profit={job.profit}, Time taken={job.time_taken} units\n"
    else:
        result_text += "No jobs scheduled for the current user."
    return result_text

class JobSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Scheduler")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#D3E3FC')
        self.style.configure('TLabel', background='#D3E3FC', font=('Helvetica', 12))
        self.style.configure('TButton', background='#007BFF', foreground='white', font=('Helvetica', 12))

        self.users = []
        self.current_user = None

        self.create_gui()

    def create_gui(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame, text="Create Account", command=self.create_account).grid(row=3, column=0, columnspan=2, pady=10)

        self.job_frame = ttk.Frame(self.root)

        ttk.Label(self.job_frame, text="Deadline:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.deadline_entry = ttk.Entry(self.job_frame)
        self.deadline_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.job_frame, text="Profit:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.profit_entry = ttk.Entry(self.job_frame)
        self.profit_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.job_frame, text="Time taken:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.time_taken_entry = ttk.Entry(self.job_frame)
        self.time_taken_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(self.job_frame, text="Add Job", command=self.add_job).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.job_frame, text="Schedule Jobs", command=self.schedule_jobs).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self.job_frame, text="Save Job Schedule", command=self.save_job_schedule).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.job_frame, text="Display Job Schedule", command=self.display_job_schedule).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self.job_frame, text="Logout", command=self.logout).grid(row=7, column=0, columnspan=2, pady=10)

        # Center align frames
        for frame in [self.login_frame, self.job_frame]:
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_login_frame()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                messagebox.showinfo("Login Successful", f"Logged in successfully as user: {username}")
                self.show_job_frame()
                return

        messagebox.showerror("Login Failed", "Invalid username or password. Login failed.")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Invalid Input", "Username and password cannot be empty.")
            return

        if len(self.users) < MAX_USERS:
            if any(user.username == username for user in self.users):
                messagebox.showerror("Username Taken", "Username is already taken. Please choose another.")
            else:
                new_user = User(username, password)
                self.users.append(new_user)
                messagebox.showinfo("Account Created", f"Account created successfully for user: {username}")
        else:
            messagebox.showerror("User Limit Reached", f"Maximum number of users ({MAX_USERS}) reached. Cannot create more accounts.")

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "Logged out successfully")
        self.show_login_frame()

    def add_job(self):
        if self.current_user:
            try:
                deadline = int(self.deadline_entry.get())
                profit = int(self.profit_entry.get())
                time_taken = int(self.time_taken_entry.get())

                new_job = Job(
                    id=len(self.current_user.jobs) + 1,
                    deadline=deadline,
                    profit=profit,
                    time_taken=time_taken
                )
                self.current_user.add_job(new_job)
                messagebox.showinfo("Job Added", "Job added successfully.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        else:
            messagebox.showerror("Cannot Add Job", "Cannot add job without a logged-in user. Please log in.")

    def schedule_jobs(self):
        if self.current_user and self.current_user.jobs:
            result_text = schedule_jobs(self.current_user.jobs)
            messagebox.showinfo("Job Schedule", result_text)
        else:
            messagebox.showinfo("No Jobs", "No jobs to schedule. Add jobs first.")

    def save_job_schedule(self):
        if self.current_user:
            if save_jobs_for_current_user(self.users, self.current_user):
                messagebox.showinfo("Save Successful", f"Job schedule saved for user: {self.current_user.username}")
            else:
                messagebox.showerror("Save Failed", "Cannot save job schedule without a user. Please log in.")
        else:
            messagebox.showerror("Save Failed", "Cannot save job schedule without a user. Please log in.")

    def display_job_schedule(self):
        if self.current_user:
            result_text = display_job_schedule_for_current_user(self.current_user)
            messagebox.showinfo("Job Schedule", result_text)
        else:
            messagebox.showerror("No User", "No user is logged in. Please log in first.")

    def show_login_frame(self):
        self.job_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    def show_job_frame(self):
        self.login_frame.grid_forget()
        self.job_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

def main():
    root = tk.Tk()
    app = JobSchedulerApp(root)
    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("+{}+{}".format(position_right, position_down))
    root.mainloop()

if __name__ == "__main__":
    main()
