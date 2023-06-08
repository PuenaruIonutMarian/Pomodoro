from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0 # se creeaza o variabila reps pentru a o folosi sa numeri repetitiile
timer = None # se creeaza o variabila ca sa poti folosi after si after_cancel


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00") # ce e creat in canvas este modificat in canvas
    title_label.config(text="Timer")
    check_label.config(text="")
    global reps
    reps = 0 # ca atunci cand dai reset sa o ia de la 0 sa nu ramana in memorie numarul repetitiei.


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1 # ori de cate ori ruleaza o repetitie se adauga 1 la numarul de repetitie
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:  # la fiecare a opta repetitie (4 munci si ar fi a patra pauza) se ia o pauza mare
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)  # asta schimba culoarea titlului atunci cand se schimba actiunea
    elif reps % 2 == 0:  # la fiecare a doua repetitie se ia o pauza de 5 minute
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)  # in rest se munceste 25 de minute
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    count_min = math.floor(count / 60)  # math floor pt ca e folosit pe coloana de minute si sa nu arate decimale
    count_sec = count % 60  # modulo ca sa determini numarul de secunde care ramane
    if count_sec < 10:
        count_sec = f"0{count_sec}"  # asta arata 0 inaintea numarului daca este mai mic de 10
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text,
                      text=f"{count_min}:{count_sec}")  # asta face ca loop-ul artificial "timer" sa fie imprimat in
    # grafic si nu in consola
    if count > 0:
        global timer
        timer = window.after(1000, count_down,
                             count - 1)  # este ca un loop datorita lui after - practic verifica ce sa schimbat dupa
        # 1000 milisecunde
    else:
        start_timer()  # asta face ca atunci cand timerul ajunge la 0 sa dea pauza sau sa inceapa munca.
        marks = "" # temporarly variable atunci cand nu se implineste sarcina nu se imprima nimic pe grafic
        work_sessions = math.floor(reps / 2) # se foloseste math fiindca reps / 2 ar fi fost float
        # // reps / 2 inseamna ca din 4 sesiuni 2 sunt munca si 2 pauza
        for _ in range(work_sessions):
            marks += "✔" # cand sarcina - work session- este implinita se bifeaza cu un check mark
        check_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()  # in loc de tkinter.Tk() daca ai fi importat doar tkinter
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Title label
title_label = Label(text="Timer", fg=GREEN, highlightthickness=0, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

# Start Button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

# Reset Button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Check Mark Label
check_label = Label(fg=GREEN, highlightthickness=0, bg=YELLOW, font=(FONT_NAME, 12))
check_label.grid(column=1, row=3)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(113, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

window.mainloop()
