import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox

class ColorMixerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Mixer")
        self.root.geometry("1200x900")
        self.root.configure(bg='#2c3e50')
        
        # Set theme and style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#34495e')
        style.configure('TLabel', background='#34495e', foreground='white', font=('Montserrat', 11))
        style.configure('Title.TLabel', font=('Montserrat', 32, 'bold'), foreground='#ecf0f1')
        style.configure('Subtitle.TLabel', font=('Montserrat', 14), foreground='#bdc3c7')
        style.configure('Header.TLabel', font=('Montserrat', 16, 'bold'), foreground='#ecf0f1')
        style.configure('TButton', font=('Montserrat', 11), padding=8)
        style.configure('Accent.TButton', background='#2ecc71', foreground='white')
        style.configure('Secondary.TButton', background='#e74c3c', foreground='white')
        
        # Define base colors with their RGB values
        self.base_colors = {
            'Red': '#e74c3c',
            'Blue': '#3498db', 
            'Yellow': '#f1c40f',
            'White': '#ecf0f1',
            'Black': '#2c3e50',
            'Green': '#2ecc71',
            'Orange': '#e67e22',
            'Purple': '#9b59b6',
            'Brown': '#d35400',
            'Pink': '#ff7979',
            'Cyan': '#00cec9',
            'Magenta': '#fd79a8',
            'Lime': '#00b894',
            'Teal': '#00b5cc',
            'Navy': '#273c75'
        }
        
        # Extended special mixing rules for common color combinations
        self.special_mixing_rules = {
            frozenset(['Blue', 'Yellow']): self.mix_blue_yellow,
            frozenset(['Red', 'Blue']): self.mix_red_blue,
            frozenset(['Red', 'Yellow']): self.mix_red_yellow,
            frozenset(['Red', 'White']): self.mix_with_white,
            frozenset(['Blue', 'White']): self.mix_with_white,
            frozenset(['Yellow', 'White']): self.mix_with_white,
            frozenset(['Green', 'White']): self.mix_with_white,
            frozenset(['Red', 'Black']): self.mix_with_black,
            frozenset(['Blue', 'Black']): self.mix_with_black,
            frozenset(['Yellow', 'Black']): self.mix_with_black,
            frozenset(['Green', 'Black']): self.mix_with_black,
            frozenset(['Red', 'Green']): self.mix_red_green,
            frozenset(['Blue', 'Green']): self.mix_blue_green,
            frozenset(['Purple', 'Red']): self.mix_purple_red,
            frozenset(['Yellow', 'Purple']): self.mix_yellow_purple,
            frozenset(['Orange', 'Blue']): self.mix_orange_blue,
            frozenset(['Yellow', 'Green']): self.mix_yellow_green,
        }
        
        self.selected_colors = []
        self.mixing_ratios = [0.2, 0.4, 0.5, 0.6, 0.8]
        
        self.create_gui()

    def create_gui(self):
        canvas = tk.Canvas(self.root, bg='#F5F5F7', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # Create main frame that will be scrollable
        main_frame = ttk.Frame(canvas, style='MainFrame.TFrame', padding="20")
        
        # Configure the canvas
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Bind mouse wheel to scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_frame.bind("<Configure>", configure_canvas)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.root, padding="40 40 40 40", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Title and Instructions
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.grid(row=0, column=0, pady=30, sticky='ew')
        
        ttk.Label(title_frame, text="Color Mixer", 
                 style='Title.TLabel').pack(pady=(0,15))
        ttk.Label(title_frame, text="Select up to 5 colors to see their combinations", 
                 style='Subtitle.TLabel').pack()
        
        # Create color selection frame with rounded corners and shadow effect
        color_frame = ttk.Frame(main_frame, style='TFrame')
        color_frame.grid(row=1, column=0, pady=30, padx=30)
        
        # Available Colors Section
        ttk.Label(color_frame, text="Available Colors", 
                 style='Header.TLabel').grid(row=0, column=0, pady=20)
        
        # Create color buttons
        buttons_frame = ttk.Frame(color_frame, style='TFrame')
        buttons_frame.grid(row=1, column=0, pady=15)
        
        row = 0
        col = 0
        for color_name, color_hex in self.base_colors.items():
            btn_frame = ttk.Frame(buttons_frame, padding=5)
            btn_frame.grid(row=row, column=col, padx=10, pady=10)
            
            btn = tk.Button(btn_frame, text=color_name, 
                          bg=color_hex,
                          width=16, height=2,
                          relief='flat',
                          borderwidth=0,
                          font=('Montserrat', 11, 'bold'),
                          cursor='hand2',
                          activebackground=color_hex,
                          command=lambda c=color_name: self.toggle_color(c))
            btn.pack()
            
            if color_name in ['White', 'Yellow', 'Pink', 'Lime', 'Cyan']:
                btn.config(fg='#2c3e50')
            else:
                btn.config(fg='white')
            
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Selected Colors Section
        selected_section = ttk.Frame(main_frame, style='TFrame')
        selected_section.grid(row=2, column=0, pady=5)
        
        ttk.Label(selected_section, text="Selected Colors", 
                 style='Header.TLabel').grid(row=0, column=0, pady=5)
        
        self.selected_frame = ttk.Frame(selected_section, style='TFrame')
        self.selected_frame.grid(row=1, column=0, pady=5)
        
        # Buttons Frame
        buttons_section = ttk.Frame(main_frame, style='TFrame')
        buttons_section.grid(row=3, column=0, pady=5)
        
        # Mix Colors Button
        mix_button = ttk.Button(buttons_section, text="Mix Colors",
                              style='Accent.TButton',
                              command=self.show_combinations)
        mix_button.grid(row=0, column=0, padx=5)
        
        # Clear Selection Button
        clear_button = ttk.Button(buttons_section, text="Clear Selection",
                                style='Secondary.TButton',
                                command=self.clear_selection)
        clear_button.grid(row=0, column=1, padx=5)

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def mix_colors(self, color1_hex, color2_hex, ratio, color1_name=None, color2_name=None):
        """Mix two colors based on given ratio"""
        if color1_name and color2_name:
            color_pair = frozenset([color1_name, color2_name])
            if color_pair in self.special_mixing_rules:
                return self.special_mixing_rules[color_pair](color1_hex, color2_hex, ratio, color1_name, color2_name)
        
        # Default RGB mixing for other colors
        color1_rgb = self.hex_to_rgb(color1_hex)
        color2_rgb = self.hex_to_rgb(color2_hex)
        
        mixed_rgb = tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                         for c1, c2 in zip(color1_rgb, color2_rgb))
        
        return self.rgb_to_hex(mixed_rgb), mixed_rgb

    def mix_blue_yellow(self, blue_hex, yellow_hex, ratio, *args):
        """Special mixing rule for blue and yellow to create green"""
        # More yellow makes a lighter green, more blue makes a darker green
        green_value = int(255 * (1 - abs(ratio - 0.5) * 0.5))
        blue_value = int(128 * ratio)
        rgb = (0, green_value, blue_value)
        return self.rgb_to_hex(rgb), rgb

    def mix_red_blue(self, red_hex, blue_hex, ratio, *args):
        """Special mixing rule for red and blue to create purple"""
        # Create rich purple tones
        red = int(255 * (1 - ratio))
        blue = int(255 * ratio)
        purple_value = int(min(red, blue) * 0.5)  # Add some purple tint
        rgb = (red, purple_value, blue)
        return self.rgb_to_hex(rgb), rgb

    def mix_red_yellow(self, red_hex, yellow_hex, ratio, *args):
        """Special mixing rule for red and yellow to create orange"""
        # Create vibrant orange tones
        red = 255
        green = int(255 * ratio)
        rgb = (red, green, 0)
        return self.rgb_to_hex(rgb), rgb

    def mix_with_white(self, color_hex, white_hex, ratio, color_name, white_name):
        """Special mixing rule for colors with white to create tints"""
        # Determine which hex is the color and which is white
        if color_name == 'White':
            color_hex, white_hex = white_hex, color_hex
            ratio = 1 - ratio

        base_rgb = self.hex_to_rgb(color_hex)
        # Mix towards white while maintaining color relationship
    
        mixed_rgb = tuple(int(c + (255 - c) * ratio) for c in base_rgb)
        return self.rgb_to_hex(mixed_rgb), mixed_rgb

    def mix_with_black(self, color_hex, black_hex, ratio, color_name, black_name):
        """Special mixing rule for colors with black to create shades"""
        # Determine which hex is the color and which is black
        if color_name == 'Black':
            color_hex, black_hex = black_hex, color_hex
            ratio = 1 - ratio

        base_rgb = self.hex_to_rgb(color_hex)
        # Mix towards black while maintaining color relationship
        mixed_rgb = tuple(int(c * (1 - ratio)) for c in base_rgb)
        return self.rgb_to_hex(mixed_rgb), mixed_rgb

    def mix_red_green(self, red_hex, green_hex, ratio, *args):
        """Special mixing rule for red and green to create brown/olive tones"""
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        blue = 0
        rgb = (red, green, blue)
        return self.rgb_to_hex(rgb), rgb

    def mix_blue_green(self, blue_hex, green_hex, ratio, *args):
        """Special mixing rule for blue and green to create turquoise/teal"""
        blue = int(255 * ratio)
        green = int(255 * (1 - ratio))
        rgb = (0, green, blue)
        return self.rgb_to_hex(rgb), rgb

    def mix_purple_red(self, purple_hex, red_hex, ratio, *args):
        """Special mixing rule for purple and red to create magenta/wine tones"""
        purple_rgb = self.hex_to_rgb(purple_hex)
        red = int(255 * (1 - ratio))
        blue = int(purple_rgb[2] * ratio)
        rgb = (red, 0, blue)
        return self.rgb_to_hex(rgb), rgb

    def mix_yellow_purple(self, yellow_hex, purple_hex, ratio, *args):
        """Special mixing rule for yellow and purple to create muted earth tones"""
        yellow_intensity = 1 - ratio
        rgb = (
            int(255 * yellow_intensity),
            int(128 * yellow_intensity),
            int(128 * ratio)
        )
        return self.rgb_to_hex(rgb), rgb

    def mix_orange_blue(self, orange_hex, blue_hex, ratio, *args):
        """Special mixing rule for orange and blue to create muted browns"""
        orange_rgb = self.hex_to_rgb(orange_hex)
        blue_rgb = self.hex_to_rgb(blue_hex)
        rgb = (
            int(orange_rgb[0] * (1 - ratio)),
            int(orange_rgb[1] * (1 - ratio) * 0.5),
            int(blue_rgb[2] * ratio)
        )
        return self.rgb_to_hex(rgb), rgb

    def mix_yellow_green(self, yellow_hex, green_hex, ratio, *args):
        """Special mixing rule for yellow and green to create chartreuse/lime"""
        yellow_rgb = self.hex_to_rgb(yellow_hex)
        green_rgb = self.hex_to_rgb(green_hex)
        rgb = (
            int(yellow_rgb[0] * (1 - ratio)),
            255,
            0
        )
        return self.rgb_to_hex(rgb), rgb

    def clear_selection(self):
        """Clear all selected colors"""
        self.selected_colors = []
        self.update_selected_colors_display()
    
    def toggle_color(self, color_name):
        """Toggle color selection"""
        if color_name in self.selected_colors:
            self.selected_colors.remove(color_name)
        elif len(self.selected_colors) < 5:
            self.selected_colors.append(color_name)
        else:
            messagebox.showwarning("Warning", "You can only select up to 5 colors!")
            return
        
        self.update_selected_colors_display()
    
    def update_selected_colors_display(self):
        """Update the display of selected colors"""
        for widget in self.selected_frame.winfo_children():
            widget.destroy()
        
        for i, color in enumerate(self.selected_colors):
            frame = ttk.Frame(self.selected_frame)
            frame.grid(row=0, column=i, padx=10)
            
            canvas = tk.Canvas(frame, width=60, height=60, bg=self.base_colors[color])
            canvas.grid(row=0, column=0, pady=5)
            
            ttk.Label(frame, text=color).grid(row=1, column=0)
            
            ttk.Button(frame, text="Remove", 
                      command=lambda c=color: self.toggle_color(c)).grid(row=2, column=0)
    
    def show_combinations(self):
        """Show all possible color combinations"""
        if len(self.selected_colors) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 colors!")
            return
        
        combo_window = tk.Toplevel(self.root)
        combo_window.title("Color Combinations")
        combo_window.geometry("900x800")
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(combo_window)
        scrollbar = ttk.Scrollbar(combo_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Generate combinations
        row = 0
        for i, color1 in enumerate(self.selected_colors):
            for color2 in self.selected_colors[i+1:]:
                # Create a frame for this color combination
                combo_frame = ttk.Frame(scrollable_frame)
                combo_frame.grid(row=row, column=0, pady=20, sticky='ew')
                
                # Header for each color pair
                ttk.Label(combo_frame, 
                         text=f"Color Mixing Combinations",
                         font=('Arial', 12, 'bold')).grid(row=0, column=0, 
                                                        columnspan=len(self.mixing_ratios)+2,
                                                        pady=(0,10))
                
                # Create frames for original colors with labels
                color1_frame = ttk.Frame(combo_frame)
                color1_frame.grid(row=1, column=0, padx=20, pady=5)
                
                color2_frame = ttk.Frame(combo_frame)
                color2_frame.grid(row=1, column=len(self.mixing_ratios)+1, padx=20, pady=5)
                
                # Display original colors with clear labels
                ttk.Label(color1_frame, text=color1,
                         font=('Arial', 10, 'bold')).pack(pady=(0,5))
                tk.Canvas(color1_frame, width=60, height=60,
                         bg=self.base_colors[color1]).pack()
                
                ttk.Label(color2_frame, text=color2,
                         font=('Arial', 10, 'bold')).pack(pady=(0,5))
                tk.Canvas(color2_frame, width=60, height=60,
                         bg=self.base_colors[color2]).pack()
                
                # Generate mixed colors for different ratios
                for col, ratio in enumerate(self.mixing_ratios, 1):
                    mix_frame = ttk.Frame(combo_frame)
                    mix_frame.grid(row=1, column=col, padx=10, pady=5)
                    
                    # Create ratio label with clear percentages
                    ratio_text = f"{color1} {math.ceil((1-ratio)*100)}% + {color2} {int(ratio*100)}%"
                    ttk.Label(mix_frame, text=ratio_text,
                            font=('Arial', 8)).pack(pady=(0,5))
                    
                    # Mix colors and display result
                    mixed_color_hex, _ = self.mix_colors(
                        self.base_colors[color1],
                        self.base_colors[color2],
                        ratio,
                        color1,
                        color2
                    )
                    
                    # Display mixed color
                    color_canvas = tk.Canvas(mix_frame, width=60, height=60,
                                          bg=mixed_color_hex,
                                          highlightthickness=1,
                                          highlightbackground='black')
                    color_canvas.pack(pady=5)
                    
                    # Add hex code label
                    ttk.Label(mix_frame, text=mixed_color_hex,
                            font=('Arial', 8)).pack()
                
                # Add visual separator
                ttk.Separator(scrollable_frame, orient='horizontal').grid(
                    row=row+1, column=0, sticky='ew', pady=10)
                
                row += 2
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def main():
    root = tk.Tk()
    app = ColorMixerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()