import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

class ListDataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("List Data Viewer")
        self.root.geometry("1200x700")
        
        # Create main container
        main_container = ttk.Frame(root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add title label
        title_label = ttk.Label(main_container, text="List Data", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Create frame for treeview
        tree_frame = ttk.Frame(main_container)
        tree_frame.pack(fill='both', expand=True)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        
        self.load_excel_data()
        
    def load_excel_data(self):
        try:
            # Read Excel file
            df = pd.read_excel('List data.xlsx')
            
            # Remove 'Unnamed: 0' column if it exists
            if 'Unnamed: 0' in df.columns:
                df = df.drop('Unnamed: 0', axis=1)
            
            # Configure columns
            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"
            
            # Set column headings
            for column in df.columns:
                self.tree.heading(column, text=column)
                # Adjust column width
                max_width = max(
                    df[column].astype(str).apply(len).max() * 10,
                    len(str(column)) * 10
                )
                self.tree.column(column, width=min(max_width, 300))
            
            # Add data rows
            for idx, row in df.iterrows():
                values = [row[col] for col in df.columns]
                self.tree.insert("", "end", values=values, tags=('row',))
            
            # Add striped row colors
            self.tree.tag_configure('row', background='white')
            for i, item in enumerate(self.tree.get_children()):
                if i % 2 == 0:
                    self.tree.item(item, tags=('evenrow',))
            self.tree.tag_configure('evenrow', background='#f0f0f0')
            
            # Add status label
            status_label = ttk.Label(
                self.root, 
                text=f"Total Records: {len(df)}", 
                font=('Helvetica', 10)
            )
            status_label.pack(pady=5)
            
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find 'List data.xlsx'")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

def main():
    root = tk.Tk()
    app = ListDataViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()