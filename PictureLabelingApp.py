import os
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
from PIL.ImageTk import PhotoImage
import pandas as pd

root = Tk()
root.title("Image Labeler App")
root.geometry("512x512")

# Function for checking if a file is image
def jpg_or_png(filename):
    if ".jpg" or ".png" in filename: return 1
    return 0

# button functions
def forward():
    global imgs, img_label, index, n_images
    global forward_button, backward_button
    img_label.grid_forget()
    index += 1
    img_label = Label(image=imgs[index])
    img_label.grid(row=0,column=0,columnspan=2)

    # disable button if at the end
    if index + 1 == n_images:
        forward_button = Button(root, text=">>", command=forward, state=DISABLED)
        forward_button.grid(row=1, column=1)
    # enable backward button
    elif index == 1:
        backward = Button(root, text="<<", command=backward)
        backward_button.grid(row=1, column=0)
    
def backward():
    global imgs, img_label, index, n_images
    global forward_button, backward_button
    img_label.grid_forget()
    index -= 1
    img_label = Label(image=imgs[index])
    img_label.grid(row=0,column=0,columnspan=2)

    # disable button if at the start
    if index == 0:
        backward_button = Button(root, text="<<", command=backward, state=DISABLED)
        backward_button.grid(row=1, column=0)
    # enable forward button
    elif index + 2 == n_images:
        forward_button = Button(root, text=">>", command=forward)
        forward_button.grid(row=1, column=1)

def label_0():
    global index, n_images, labels
    labels[index] = 0
    if index + 1 == n_images:
        if askyesno("Labeling complete","Save results?"):
            return save_results()
        return 0
    forward()

def label_1():
    global index, n_images, labels
    labels[index] = 1
    if index + 1 == n_images:
        if askyesno("Labeling complete","Save results?"):
            return save_results()
        return 0
    forward()

# save results function
def save_results():
    global files_of_directory, labels
    results_dataframe = pd.DataFrame(zip(files_of_directory, labels), columns=["image","label"])
    filename = askstring("Save results", "Save result to file")
    if not ".csv" in filename:
        filename = filename + ".csv"
    results_dataframe.to_csv(filename, index = False)


# Button function
def start_labeling():
    global imgs, img_label
    global index, n_images
    global labels
    global files_of_directory
    global forward_button, backward_button
    # Select a directory
    image_directory = filedialog.askdirectory(initialdir="./", title="Select a folder containing images to be labeled")
    # Get all the files in the directory
    files_of_directory = os.listdir(image_directory)
    # select only .jpg or .png images
    files_of_directory = [filename for filename in files_of_directory if jpg_or_png(filename)]
    # open the images
    imgs = []
    for filename in files_of_directory:
        filepath = os.path.normpath(os.path.join(image_directory, filename))
        imgs.append(PhotoImage(file=filepath))

    forward_button = Button(root, text=">>", command=forward)
    backward_button = Button(root, text="<<", command=backward, state=DISABLED)
    label_0_button = Button(root, text="0", command=label_0)
    label_1_button = Button(root, text="1", command=label_1)
    forward_button.grid(row=1, column=1)
    backward_button.grid(row=1, column=0)
    label_0_button.grid(row=2, column=0)
    label_1_button.grid(row=2, column=1)


    n_images = len(imgs)
    labels = [0] * n_images
    index = 0
    img_label = Label(image=imgs[0])
    img_label.grid(row=0,column=0,columnspan=2)



# Create a basic menu
app_menu = Menu(root)
root.config(menu=app_menu)

# menu item 1
file_menu = Menu(app_menu)
app_menu.add_cascade(label="File", menu=file_menu)
# add functionality
file_menu.add_command(label="Open directory for labeling", command=start_labeling)
file_menu.add_command(label="Exit", command=root.quit)

# Run mainloop
root.mainloop()
