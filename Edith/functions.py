def longmsg(text):
    window=Tk()
    window.title('Edith')
    lbl=Label(window, text=text, fg="white", bg="black", font=("Arial",12))
    lbl.place(x=20, y=20)
    window.configure(background='black')
    window.geometry("400x600+5+5")
    window.mainloop()