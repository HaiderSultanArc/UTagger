import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

TAGS = ['disease_eng', 'disease_persion', 'disease_urdu', 'disease_urdu_roman', 'disease_arabic', 'disease_hindi', 'disease_description', 'symptom_eng', 'symptom_persion', 'symptom_urdu', 'symptom_urdu_roman', 'symptom_arabic', 'symptom_hindi', 'symptom_description', 'cause_eng', 'cause_persion', 'cause_urdu', 'cause_urdu_roman', 'cause_arabic', 'cause_hindi', 'cause_description', 'principle_of_treatment', 'pharmacotherapy', 'comp_drug', 'reg_theropy', 'diet_recom', 'diet_restrict', 'prevention']

class UTaggerGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("UTagger")
        # self.geometry(f"{1100}x{540}")
        self.grid_columnconfigure(1, weight=1)

        
        # * Sidebar
        self.Sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.Sidebar.grid(row=0, column=0, sticky="nsew")
        self.Sidebar.grid_rowconfigure(1, weight=1)
        
        self.Label = customtkinter.CTkLabel(self.Sidebar, text="UTagger", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        
        self.File = customtkinter.CTkFrame(self.Sidebar, width=140)
        self.File.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.FileLabel = customtkinter.CTkLabel(self.File, text="File Options", anchor="w")
        self.FileLabel.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.OpenFileButton = customtkinter.CTkButton(self.File, text="Open", command=self.OpenFileEvent)
        self.OpenFileButton.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.SaveFileButton = customtkinter.CTkButton(self.File, text="Save", command=self.SaveFileEvent)
        self.SaveFileButton.grid(row=2, column=0, padx=20, pady=(20, 20))
        
        self.AppearanceModeOptionMenu = customtkinter.CTkOptionMenu(self.Sidebar, values=["Light", "Dark", "System"], command=self.ChangeAppearanceModeEvent)
        self.AppearanceModeOptionMenu.grid(row=6, column=0, padx=20, pady=(0, 20))
        self.AppearanceModeOptionMenu.set("Dark")
        
        
        # * Main Textbox
        self.MainTextBox = customtkinter.CTkTextbox(self, width=800, height=500, wrap="word")
        self.MainTextBox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        
        # * Tags
        self.Panel = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.Panel.grid(row=0, column=3, sticky="nsew")
        self.Panel.grid_rowconfigure(1, weight=1)
    
        self.Tags = customtkinter.CTkFrame(self.Panel, width=140)
        self.Tags.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.TagsLabel = customtkinter.CTkLabel(self.Tags, text="Tags Options", anchor="w")
        self.TagsLabel.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.TagsOptionMenu = customtkinter.CTkOptionMenu(self.Tags, dynamic_resizing=False, values=TAGS)
        self.TagsOptionMenu.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.AddTagButton = customtkinter.CTkButton(self.Tags, text="Add Tag", command=self.AddTag)
        self.AddTagButton.grid(row=2, column=0, padx=20, pady=(20, 20))
        
        self.RemoveTagButton = customtkinter.CTkButton(self.Tags, text="Remove Tag", command=self.RemoveTag)
        self.RemoveTagButton.grid(row=3, column=0, padx=20, pady=(20, 20))
        
        self.TypingOptions = customtkinter.CTkOptionMenu(self.Panel, dynamic_resizing=False, values=["Enable Typing", "Disable Typing"], command=self.TypingOptionsEvent)
        self.TypingOptions.grid(row=3, column=0, padx=20, pady=(20, 20))
        
    
    def AddTag(self):
        sel = self.MainTextBox.tag_ranges("sel")
        
        if sel:
            selectedText = self.MainTextBox.get(sel[0], sel[1])
            self.MainTextBox.delete(sel[0], sel[1])
            self.MainTextBox.insert(sel[0], f"<{self.TagsOptionMenu.get()}>{selectedText}</{self.TagsOptionMenu.get()}>")
    
    
    def RemoveTag(self):
        sel = self.MainTextBox.tag_ranges("sel")
        
        if sel:
            selectedText = self.MainTextBox.get(sel[0], sel[1])
            self.MainTextBox.delete(sel[0], sel[1])
            self.MainTextBox.insert(sel[0], selectedText.replace(f"<{self.TagsOptionMenu.get()}>", "").replace(f"</{self.TagsOptionMenu.get()}>", ""))
            
    
    def TypingOptionsEvent(self, option: str):
        if option == "Enable Typing":
            self.MainTextBox.unbind("<Key>")
        elif option == "Disable Typing":
            self.MainTextBox.bind("<Key>", lambda event: "break")
    
    
    def OpenFileEvent(self):
        filePath = customtkinter.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        if filePath:
            with open(filePath, "r", encoding='utf-8') as file:
                contents = file.read()
            
            self.MainTextBox.delete("1.0", "end")
            self.MainTextBox.insert("1.0", contents)
            self.TypingOptions.set("Disable Typing")
            self.TypingOptionsEvent("Disable Typing")
        
    
    def SaveFileEvent(self):
        filePath = customtkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        if filePath:
            saveText = self.MainTextBox.get("1.0", "end-1c")
            
            saveText = saveText.replace("<", "\n<").replace(">", ">\n")
            
            with open(filePath, "w", encoding='utf-8') as file:
                file.write(saveText)
    
    
    def ChangeAppearanceModeEvent(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)



if __name__ == "__main__":
    app = UTaggerGUI()
    app.mainloop()