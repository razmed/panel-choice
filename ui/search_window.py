import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional, List, Dict, Any
import os

class SearchWindow:
    """Fenêtre de recherche simplifiée de fichiers"""
    
    def __init__(self, root: ctk.CTkToplevel, db, file_handler, on_file_select: Callable):
        self.root = root
        self.db = db
        self.file_handler = file_handler
        self.on_file_select = on_file_select
        
        self.root.title("🔍 Recherche de Fichiers")
        self.root.geometry("900x600")
        
        self.center_window()
        self.create_widgets()
        
        # Effectuer une recherche initiale (tous les fichiers)
        self.search_files()
    
    def center_window(self):
        """Centrer la fenêtre"""
        self.root.update_idletasks()
        width = 900
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Créer les widgets"""
        # ============= EN-TÊTE =============
        header = ctk.CTkFrame(
            self.root,
            height=80,
            corner_radius=0,
            fg_color=("#1f538d", "#14375e")
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="🔍 Recherche de Fichiers",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="✖️ Fermer",
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#dc3545", "#b02a37"),
            hover_color=("#e04555", "#c03545"),
            command=self.root.destroy
        ).pack(side="right", padx=30)
        
        # ============= ZONE DE RECHERCHE SIMPLIFIÉE =============
        search_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        search_container.pack(fill="x", padx=20, pady=20)
        
        search_frame = ctk.CTkFrame(
            search_container,
            fg_color=("#f0f8ff", "#1a2a3a"),
            corner_radius=15,
            border_width=2,
            border_color=("#1f538d", "#2563a8")
        )
        search_frame.pack(fill="x")
        
        # Titre
        ctk.CTkLabel(
            search_frame,
            text="🎯 Recherche Simple",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#2563a8")
        ).pack(pady=(15, 20))
        
        # Frame principal des critères
        criteria_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        criteria_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Ligne 1: Nom et Extension
        row1 = ctk.CTkFrame(criteria_frame, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        # Nom du fichier
        name_frame = ctk.CTkFrame(row1, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        ctk.CTkLabel(
            name_frame,
            text="📄 Nom du fichier:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x")
        
        self.filename_entry = ctk.CTkEntry(
            name_frame,
            height=40,
            font=ctk.CTkFont(size=14),
            placeholder_text="Entrez le nom du fichier (optionnel)..."
        )
        self.filename_entry.pack(fill="x", pady=(5, 0))
        
        # Extension
        ext_frame = ctk.CTkFrame(row1, fg_color="transparent")
        ext_frame.pack(side="right")
        
        ctk.CTkLabel(
            ext_frame,
            text="📋 Type de fichier:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack()
        
        self.extension_combo = ctk.CTkComboBox(
            ext_frame,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            values=["Tous les fichiers", "PDF", "Word (docx)", "Excel (xlsx)", "Ancien Word (doc)", "Ancien Excel (xls)", "Texte (txt)", "Image (png)", "Image (jpg)"]
        )
        self.extension_combo.pack(pady=(5, 0))
        self.extension_combo.set("Tous les fichiers")
        
        # Raccourcis rapides
        shortcuts_frame = ctk.CTkFrame(criteria_frame, fg_color="transparent")
        shortcuts_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            shortcuts_frame,
            text="🚀 Raccourcis rapides:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")
        
        shortcuts = [
            ("📄 PDF", lambda: self.set_filter("PDF")),
            ("📝 Word", lambda: self.set_filter("Word (docx)")),
            ("📊 Excel", lambda: self.set_filter("Excel (xlsx)")),
            ("🧹 Tout", lambda: self.clear_filters())
        ]
        
        for text, command in shortcuts:
            ctk.CTkButton(
                shortcuts_frame,
                text=text,
                width=100,
                height=35,
                font=ctk.CTkFont(size=12),
                fg_color=("#6c757d", "#5a6268"),
                hover_color=("#7c858d", "#6a7278"),
                command=command
            ).pack(side="left", padx=5)
        
        # Boutons principaux
        main_buttons = ctk.CTkFrame(criteria_frame, fg_color="transparent")
        main_buttons.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            main_buttons,
            text="🔍 Rechercher",
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#28a745", "#1e7e34"),
            hover_color=("#32b349", "#229143"),
            command=self.search_files
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            main_buttons,
            text="🧹 Effacer",
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#ffc107", "#e0a800"),
            hover_color=("#ffcd39", "#efb810"),
            command=self.clear_filters
        ).pack(side="left", padx=10)
        
        # ============= RÉSULTATS =============
        results_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        results_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # En-tête des résultats
        results_header = ctk.CTkFrame(
            results_container,
            height=50,
            fg_color=("#e7f3ff", "#1a3a52"),
            corner_radius=10
        )
        results_header.pack(fill="x", pady=(0, 10))
        results_header.pack_propagate(False)
        
        self.results_label = ctk.CTkLabel(
            results_header,
            text="🔍 Résultats de la recherche - 0 fichier(s)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1f538d", "#2563a8")
        )
        self.results_label.pack(pady=15)
        
        # Liste des résultats
        self.results_list = ctk.CTkScrollableFrame(
            results_container,
            fg_color=("gray95", "gray15"),
            corner_radius=15
        )
        self.results_list.pack(fill="both", expand=True)
        
        # Liaison des événements
        self.filename_entry.bind('<KeyRelease>', lambda e: self.auto_search())
        self.extension_combo.configure(command=lambda _: self.auto_search())
    
    def set_filter(self, extension_type: str):
        """Définir un filtre rapide"""
        self.extension_combo.set(extension_type)
        self.search_files()
    
    def clear_filters(self):
        """Effacer tous les filtres"""
        self.filename_entry.delete(0, "end")
        self.extension_combo.set("Tous les fichiers")
        self.search_files()
    
    def auto_search(self):
        """Recherche automatique lors de la saisie"""
        # Petite temporisation pour éviter trop de recherches
        self.root.after(300, self.search_files)
    
    def search_files(self):
        """Effectuer la recherche avec les critères actuels"""
        try:
            # Récupérer les critères
            filename = self.filename_entry.get().strip()
            extension_type = self.extension_combo.get()
            
            # Convertir le type en extension
            extension_map = {
                "Tous les fichiers": "",
                "PDF": "pdf",
                "Word (docx)": "docx", 
                "Excel (xlsx)": "xlsx",
                "Ancien Word (doc)": "doc",
                "Ancien Excel (xls)": "xls",
                "Texte (txt)": "txt",
                "Image (png)": "png",
                "Image (jpg)": "jpg"
            }
            
            extension = extension_map.get(extension_type, "")
            
            # Effectuer la recherche simplifiée
            results = self.db.search_files(
                filename=filename,
                extension=extension
            )
            
            # Afficher les résultats
            self.display_results(results)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors de la recherche:\n{e}")
            print(f"Erreur recherche: {e}")
    
    def display_results(self, files: List[Dict[str, Any]]):
        """Afficher les résultats de la recherche"""
        # Nettoyer
        for widget in self.results_list.winfo_children():
            widget.destroy()
        
        # Mettre à jour le compteur
        count = len(files)
        self.results_label.configure(text=f"🔍 Résultats de la recherche - {count} fichier(s)")
        
        if count == 0:
            ctk.CTkLabel(
                self.results_list,
                text="📭 Aucun fichier trouvé\n\nEssayez de modifier vos critères de recherche",
                font=ctk.CTkFont(size=16),
                text_color=("gray50", "gray60")
            ).pack(expand=True, pady=100)
            return
        
        # Afficher chaque fichier
        for file in files:
            self.create_file_result_card(file)
    
    def create_file_result_card(self, file: Dict[str, Any]):
        """Créer une carte de résultat pour un fichier"""
        extension = file['filename'].rsplit('.', 1)[-1].lower() if '.' in file['filename'] else ''
        icon = self.file_handler.get_file_icon(extension)
        is_pdf = extension == 'pdf'
        
        # Frame de la carte
        card = ctk.CTkFrame(
            self.results_list,
            height=90,
            fg_color=("white", "gray20"),
            corner_radius=10,
            border_width=1,
            border_color=("gray80", "gray40")
        )
        card.pack(fill="x", pady=5, padx=5)
        card.pack_propagate(False)
        
        # Icône
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=32),
            width=80
        )
        icon_label.pack(side="left", padx=15)
        
        # Informations du fichier
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=15)
        
        # Nom du fichier
        name_label = ctk.CTkLabel(
            info_frame,
            text=file['filename'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # Dossier parent
        folder = self.db.get_folder(file['folder_id'])
        folder_name = folder['name'] if folder else "Dossier supprimé"
        
        folder_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {folder_name}",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        folder_label.pack(fill="x")
        
        # Type de fichier
        type_text = "🔒 PDF (Lecture seule)" if is_pdf else "💾 Fichier téléchargeable"
        
        type_label = ctk.CTkLabel(
            info_frame,
            text=type_text,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        type_label.pack(fill="x")
        
        # Boutons d'action
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(side="right", padx=15)
        
        # Bouton Ouvrir
        action_text = "👁️ Visualiser" if is_pdf else "📥 Ouvrir"
        open_btn = ctk.CTkButton(
            button_frame,
            text=action_text,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#2563a8", "#1a4a7a"),
            command=lambda f=file: self.open_file(f)
        )
        open_btn.pack(pady=2)
        
        # Bouton Localiser
        locate_btn = ctk.CTkButton(
            button_frame,
            text="📍 Localiser",
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#28a745", "#1e7e34"),
            hover_color=("#32b349", "#229143"),
            command=lambda f=file: self.locate_file(f)
        )
        locate_btn.pack(pady=2)
        
        # Double-clic pour ouvrir
        card.bind('<Double-Button-1>', lambda e, f=file: self.open_file(f))
    
    def open_file(self, file: Dict[str, Any]):
        """Ouvrir un fichier avec le bon viewer"""
        if not os.path.exists(file['filepath']):
            messagebox.showerror("Erreur", "❌ Le fichier n'existe plus")
            return
        
        extension = file['filename'].rsplit('.', 1)[-1].lower() if '.' in file['filename'] else ''
        
        # Si c'est un PDF, utiliser le viewer intégré
        if extension == 'pdf':
            try:
                from .pdf_viewer import PDFViewer
                pdf_window = ctk.CTkToplevel(self.root)
                PDFViewer(pdf_window, file['filepath'], file['filename'])
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Impossible d'ouvrir le PDF:\n{e}")
        else:
            # Pour les autres fichiers, utiliser le gestionnaire de fichiers
            success = self.file_handler.open_file(file['filepath'])
            if not success:
                messagebox.showerror("Erreur", "❌ Impossible d'ouvrir le fichier")
    
    def locate_file(self, file: Dict[str, Any]):
        """Localiser un fichier dans son dossier"""
        try:
            # Fermer la fenêtre de recherche
            self.root.destroy()
            
            # Appeler le callback pour naviguer vers le dossier
            if self.on_file_select:
                self.on_file_select(file['folder_id'])
                
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Impossible de localiser:\n{e}")
