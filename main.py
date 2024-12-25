import customtkinter as ctk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageFilter
import numpy as np


def generate_chalkboard(
    width, height, texture_intensity, patch_params, base_color, alpha
):
    base = np.zeros((height, width), dtype=np.uint8)
    noise = np.random.randint(0, texture_intensity, (height, width), dtype=np.uint8)
    chalkboard = base + noise

    patch_intensity, patch_size, patch_count = patch_params
    for _ in range(patch_count):
        x = np.random.randint(0, width - patch_size)
        y = np.random.randint(0, height - patch_size)
        patch_noise = np.random.randint(
            0, patch_intensity, (patch_size, patch_size), dtype=np.uint8
        )
        chalkboard[y : y + patch_size, x : x + patch_size] = np.maximum(
            chalkboard[y : y + patch_size, x : x + patch_size], patch_noise
        )

    base_color = base_color[:7] + "FF" if len(base_color) == 7 else base_color

    img = Image.fromarray(chalkboard, mode="L").convert("RGBA")
    img.putalpha(alpha)
    base_layer = Image.new("RGBA", (width, height), base_color.upper())
    img = Image.alpha_composite(base_layer, img)
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    return img


def update_preview():
    global preview_image_label, base_color
    texture_intensity = int(texture_slider.get())
    patch_params = (
        int(patch_intensity_slider.get()),
        int(patch_size_slider.get()),
        int(patch_count_slider.get()),
    )
    alpha = int(alpha_slider.get())
    img = generate_chalkboard(
        800, 800, texture_intensity, patch_params, base_color, alpha
    )
    ctk_image = ctk.CTkImage(img, size=(800, 800))
    preview_image_label.configure(image=ctk_image, text="")
    preview_image_label.image = ctk_image


def save_image():
    global base_color
    texture_intensity = int(texture_slider.get())
    patch_params = (
        int(patch_intensity_slider.get()),
        int(patch_size_slider.get()),
        int(patch_count_slider.get()),
    )
    alpha = int(alpha_slider.get())
    img = generate_chalkboard(
        10000, 10000, texture_intensity, patch_params, base_color, alpha
    )
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        img.save(file_path)


def choose_base_color():
    global base_color
    color_code = colorchooser.askcolor(title="Choose Base Color")[1]
    if color_code:
        base_color = color_code
        update_preview()


base_color = "#7F7F7F"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Chalkboard Generator")
root.geometry("1300x800")

main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

preview_frame = ctk.CTkFrame(main_frame)
preview_frame.pack(side="left", padx=10, pady=10)
preview_image_label = ctk.CTkLabel(preview_frame, text="")
preview_image_label.pack()

control_frame = ctk.CTkFrame(main_frame)
control_frame.pack(side="right", padx=10, pady=10, fill="y")

ctk.CTkLabel(control_frame, text="Base Texture Intensity").grid(
    row=0, column=0, sticky="w", pady=5
)
texture_slider = ctk.CTkSlider(
    control_frame, from_=10, to=100, command=lambda v: update_preview()
)
texture_slider.set(30)
texture_slider.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(control_frame, text="Patch Intensity").grid(
    row=1, column=0, sticky="w", pady=5
)
patch_intensity_slider = ctk.CTkSlider(
    control_frame, from_=0, to=100, command=lambda v: update_preview()
)
patch_intensity_slider.set(50)
patch_intensity_slider.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(control_frame, text="Patch Size").grid(row=2, column=0, sticky="w", pady=5)
patch_size_slider = ctk.CTkSlider(
    control_frame, from_=10, to=100, command=lambda v: update_preview()
)
patch_size_slider.set(50)
patch_size_slider.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(control_frame, text="Patch Count").grid(
    row=3, column=0, sticky="w", pady=5
)
patch_count_slider = ctk.CTkSlider(
    control_frame, from_=0, to=50, command=lambda v: update_preview()
)
patch_count_slider.set(10)
patch_count_slider.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkLabel(control_frame, text="Alpha").grid(row=4, column=0, sticky="w", pady=5)
alpha_slider = ctk.CTkSlider(
    control_frame, from_=0, to=255, command=lambda v: update_preview()
)
alpha_slider.set(128)
alpha_slider.grid(row=4, column=1, padx=10, pady=5)

color_button = ctk.CTkButton(
    control_frame, text="Choose Base Color", command=choose_base_color
)
color_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

save_button = ctk.CTkButton(control_frame, text="Save Image", command=save_image)
save_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="we")

for i in range(7):
    control_frame.grid_rowconfigure(i, pad=5)
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=3)

update_preview()

root.mainloop()
