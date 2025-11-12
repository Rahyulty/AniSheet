import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AniSheet")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="AniSheet", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.mainframe = ctk.CTkFrame(self)
        self.mainframe.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=0, minsize=250)

        # make the preview canvas
        self.preview_canvas = ctk.CTkCanvas(self.mainframe, bg="#202020", highlightthickness=0)
        self.preview_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        # Bind canvas resize to update preview
        self.preview_canvas.bind("<Configure>", self.on_canvas_configure)

        # make the controls frame
        self.controls_frame = ctk.CTkFrame(self.mainframe, width=250)
        self.controls_frame.grid(row=0, column=1, sticky="nsew")
        self.controls_frame.grid_columnconfigure(0, weight=1)
        
        # Configure controls frame to have padding
        row = 0
        
        # Load Sprite Sheet button
        self.load_button = ctk.CTkButton(
            self.controls_frame, 
            text="Load Sprite Sheet", 
            command=self.load_image
        )
        self.load_button.grid(row=row, column=0, padx=15, pady=(15, 10), sticky="ew")
        row += 1
        
        # Frame dimensions section
        dimensions_label = ctk.CTkLabel(
            self.controls_frame, 
            text="Frame Dimensions", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        dimensions_label.grid(row=row, column=0, padx=15, pady=(10, 5), sticky="w")
        row += 1
        
        self.frame_width = ctk.CTkEntry(
            self.controls_frame, 
            placeholder_text="Width"
        )
        self.frame_width.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        row += 1
        
        self.frame_height = ctk.CTkEntry(
            self.controls_frame, 
            placeholder_text="Height"

        )
        self.frame_height.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        row += 1
        
        # FPS section
        fps_label = ctk.CTkLabel(
            self.controls_frame, 
            text="FPS", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        fps_label.grid(row=row, column=0, padx=15, pady=(15, 5), sticky="w")
        row += 1
        
        self.fps_slider = ctk.CTkSlider(
            self.controls_frame, 
            from_=1, 
            to=60,
            number_of_steps=59
        )
        self.fps_slider.set(12)
        self.fps_slider.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.fps_slider.configure(command=self.update_fps_label)
        row += 1
        
        self.fps_label = ctk.CTkLabel(
            self.controls_frame, 
            text="FPS: 12"
        )
        self.fps_label.grid(row=row, column=0, padx=15, pady=(0, 10), sticky="w")
        row += 1
        
        # Play button
        self.play_button = ctk.CTkButton(
            self.controls_frame, 
            text="▶ Play", 
            command=self.toggle_play,
            font=ctk.CTkFont(size=14)
        )
        self.play_button.grid(row=row, column=0, padx=15, pady=(10, 15), sticky="ew")
        
        # Set initial play state
        self.is_playing = False
        self.frames = []
        self.current_frame = 0
        self.animation_id = None
        self.sprite_sheet = None
        self.update_timer = None
        
        # Bind entry fields to update sprite sheet when dimensions change
        self.frame_width.bind("<KeyRelease>", self.on_dimension_change)
        self.frame_height.bind("<KeyRelease>", self.on_dimension_change)
        
        # Bind keyboard shortcuts on the main window
        # Space bar to toggle play/pause (only works when window has focus)
        self.bind("<KeyPress-space>", lambda e: self.toggle_play())
        # Left arrow for previous frame
        self.bind("<KeyPress-Left>", lambda e: self.step_frame(-1))
        # Right arrow for next frame
        self.bind("<KeyPress-Right>", lambda e: self.step_frame(1))
        
        # Bind arrow keys on entry fields so they work even when fields have focus
        # Arrow keys will step frames if sprite sheet is loaded
        def handle_arrow_in_entry(event, direction):
            if hasattr(self, 'frames') and self.frames:
                self.step_frame(direction)
                return "break"  # Prevent default arrow key behavior in entry fields
            return None
        
        self.frame_width.bind("<KeyPress-Left>", lambda e: handle_arrow_in_entry(e, -1))
        self.frame_height.bind("<KeyPress-Left>", lambda e: handle_arrow_in_entry(e, -1))
        self.frame_width.bind("<KeyPress-Right>", lambda e: handle_arrow_in_entry(e, 1))
        self.frame_height.bind("<KeyPress-Right>", lambda e: handle_arrow_in_entry(e, 1))
        
        # Allow window to receive keyboard focus for space bar shortcut
        # Users can click on the canvas or window to activate space bar toggle
        self.preview_canvas.bind("<Button-1>", lambda e: self.focus_set())
    
    def update_fps_label(self, value):
        fps_value = int(float(value))
        self.fps_label.configure(text=f"FPS: {fps_value}")
    
    def load_image(self):
        path = filedialog.askopenfilename(
            title="Select Sprite Sheet",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )

        if not path:
            return
        
        # Get frame dimensions
        frame_w_str = self.frame_width.get().strip()
        frame_h_str = self.frame_height.get().strip()
        
        if not frame_w_str or not frame_h_str:
            messagebox.showerror("Error", "Please enter frame width and height")
            return
        
        try:
            frame_w = int(frame_w_str)
            frame_h = int(frame_h_str)
            if frame_w <= 0 or frame_h <= 0:
                messagebox.showerror("Error", "Frame width and height must be positive integers")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid frame width and height (numbers only)")
            return
        
        try:
            self.sprite_sheet = Image.open(path)
            self.update_sprite_sheet_slicing(frame_w, frame_h)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def update_sprite_sheet_slicing(self, frame_w, frame_h):
        """Update sprite sheet slicing with new dimensions"""
        if not hasattr(self, 'sprite_sheet') or self.sprite_sheet is None:
            return
        
        try:
            was_playing = self.is_playing
            
            # Slice the sprite sheet with new dimensions
            self.frames = self.slice_sprite_sheet(self.sprite_sheet, frame_w, frame_h)
            
            if not self.frames:
                messagebox.showerror("Error", "No frames found. Check frame dimensions.")
                return
            
            # Reset to first frame and maintain playing state
            self.current_frame = 0
            
            # Cancel any existing animation
            if self.animation_id:
                self.after_cancel(self.animation_id)
                self.animation_id = None
            
            # Resume animation if it was playing
            if was_playing:
                # Ensure playing state is True and button text is correct
                self.is_playing = True
                self.play_button.configure(text="⏸ Pause")
                # Start animation from first frame (update_preview will draw it)
                self.update_preview()
            else:
                # Ensure playing state is False
                self.is_playing = False
                self.play_button.configure(text="▶ Play")
                # Draw first frame (don't start animation)
                self.draw_frame()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update sprite sheet: {str(e)}")
    
    def on_dimension_change(self, event=None):
        """Handle dimension changes with debouncing"""
        # Cancel any pending update
        if self.update_timer:
            self.after_cancel(self.update_timer)
        
        # Schedule update after a short delay (debounce)
        self.update_timer = self.after(500, self.check_and_update_dimensions)
    
    def check_and_update_dimensions(self):
        """Check if dimensions are valid and update sprite sheet if loaded"""
        # Check if sprite sheet is loaded
        if not hasattr(self, 'sprite_sheet') or self.sprite_sheet is None:
            return
        
        # Get frame dimensions
        frame_w_str = self.frame_width.get().strip()
        frame_h_str = self.frame_height.get().strip()
        
        # Skip if fields are empty
        if not frame_w_str or not frame_h_str:
            return
        
        try:
            frame_w = int(frame_w_str)
            frame_h = int(frame_h_str)
            
            # Validate dimensions
            if frame_w <= 0 or frame_h <= 0:
                return
            
            # Update sprite sheet slicing
            self.update_sprite_sheet_slicing(frame_w, frame_h)
        except ValueError:
            # Invalid input, ignore silently (user might still be typing)
            pass

    def slice_sprite_sheet(self, sheet, frame_w, frame_h):
        """Slice sprite sheet into frames, ensuring all frames stay within image boundaries.
        Only includes complete frames that fit fully within the image to avoid black spots."""
        frames = []
        sheet_w, sheet_h = sheet.size
        
        # Iterate through possible frame positions
        for y in range(0, sheet_h, frame_h):
            for x in range(0, sheet_w, frame_w):
                # Calculate crop coordinates
                left = x
                top = y
                right = x + frame_w
                bottom = y + frame_h
                
                # Check if frame extends beyond image boundaries
                # Skip partial frames to avoid black spots or empty areas
                if right > sheet_w or bottom > sheet_h:
                    # This frame would extend beyond image boundaries, skip it
                    continue
                
                # Frame is fully within boundaries, safe to crop
                # PIL's crop method will only crop what's in the image, but we've
                # already checked, so this is guaranteed to be within bounds
                frame = sheet.crop((left, top, right, bottom))
                
                # Verify frame size matches expected dimensions (safety check)
                if frame.size == (frame_w, frame_h):
                    frames.append(frame)
                # If size doesn't match (shouldn't happen with our check), skip it
        
        return frames
    
    def on_canvas_configure(self, event=None):
        if hasattr(self, 'frames') and self.frames:
            self.draw_frame()
    
    def draw_frame(self):
        if not hasattr(self, 'frames') or not self.frames:
            return
        
        self.preview_canvas.delete("all")
        
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        if self.current_frame < 0:
            self.current_frame = len(self.frames) - 1
            
        frame = self.frames[self.current_frame]
        
        # Convert to PhotoImage
        frame_tk = ImageTk.PhotoImage(frame)
        
        # Get canvas size
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        # Center the image
        if canvas_width > 1 and canvas_height > 1:
            x = canvas_width // 2
            y = canvas_height // 2
            self.preview_canvas.create_image(x, y, anchor="center", image=frame_tk)
        else:
            # Canvas not yet sized, place at top-left
            self.preview_canvas.create_image(0, 0, anchor="nw", image=frame_tk)
        
        # Keep a reference to prevent garbage collection
        self.preview_canvas.image = frame_tk
    
    def update_preview(self):
        if not hasattr(self, 'frames') or not self.frames:
            return
        
        # Draw current frame
        self.draw_frame()
        
        # Only schedule next update if playing
        if self.is_playing:
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Get FPS and calculate delay in milliseconds
            fps = self.fps_slider.get()
            delay_ms = int(1000 / fps)  # Convert to integer milliseconds
            
            # Schedule next update
            self.animation_id = self.after(delay_ms, self.update_preview)

    def toggle_play(self):
        if not hasattr(self, 'frames') or not self.frames:
            messagebox.showwarning("Warning", "Please load a sprite sheet first")
            return
        
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.configure(text="⏸ Pause")
            # Start animation
            self.update_preview()
        else:
            self.play_button.configure(text="▶ Play")
            if self.animation_id:
                self.after_cancel(self.animation_id)
                self.animation_id = None
            self.draw_frame()
    
    def step_frame(self, direction):
        """Step forward or backward one frame (direction: 1 for next, -1 for previous)"""
        if not hasattr(self, 'frames') or not self.frames:
            return
        
        # Pause animation if playing
        if self.is_playing:
            self.is_playing = False
            self.play_button.configure(text="▶ Play")
            if self.animation_id:
                self.after_cancel(self.animation_id)
                self.animation_id = None
        
        # Step to next or previous frame
        if direction > 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = (self.current_frame - 1) % len(self.frames)
        
        # Draw the frame
        self.draw_frame()


if __name__ == "__main__":
    app = App()
    app.mainloop()

