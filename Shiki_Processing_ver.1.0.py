import pandas as pd
import re
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


# --- Fonctions GUI ---
def choisir_fichier():
    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier CSV",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)


def choisir_dossier():
    folder_path = filedialog.askdirectory(title="Choisir dossier de sortie")
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_path)


def lancer_traitement():
    input_file = entry_file.get()
    output_folder = entry_folder.get()

    if not os.path.isfile(input_file):
        messagebox.showerror("Erreur", "Le fichier n'existe pas.")
        return
    if not os.path.isdir(output_folder):
        messagebox.showerror("Erreur", "Le dossier de sortie n'existe pas.")
        return

    try:
        colonne_formule = "formulas:formulas"

        def parse_formule(formule):
            if not isinstance(formule, str) or formule.lower() == 'nan' or formule.strip() == '':
                return {'C': 0, 'H': 0, 'N': 0, 'O': 0, 'S': 0}
            elements = re.findall(r'([CHNOS])(\d*)', formule)
            composition = {'C': 0, 'H': 0, 'N': 0, 'O': 0, 'S': 0}
            for (elem, nb) in elements:
                composition[elem] = int(nb) if nb != '' else 1
            return composition

# === Lecture et petites pré-manips du CSV ===
        df = pd.read_csv(input_file,sep=";")
        # Supprimer les lignes sans formule brute
        df[colonne_formule] = df[colonne_formule].astype(str)
        df = df.drop(columns=["fragment_scans","id"], errors='ignore')
        df = df.drop(columns=[col for col in df.columns if "datafile" in col], errors='ignore')
        df = df.drop(columns=[col for col in df.columns if "range" in col], errors='ignore')
        df = df.drop(columns=[col for col in df.columns if "scores" in col], errors='ignore')
        df = df.drop(columns=[col for col in df.columns if "score" in col], errors='ignore')

# === Extraction des compositions ===
        compositions = df[colonne_formule].apply(parse_formule)
        comp_df = pd.DataFrame(compositions.tolist())

# === Calcul des ratios ===
        comp_df["O/C"] = np.where(comp_df["C"] == 0, np.nan, comp_df["O"] / comp_df["C"])
        comp_df["H/C"] = np.where(comp_df["C"] == 0, np.nan, comp_df["H"] / comp_df["C"])

# === Fusion des résultats avec le fichier original et mise en forme ===
        df_final = pd.concat([df, comp_df], axis=1)
        df_final.rename(columns={"height": "intensity"}, inplace=True)
        df_final.rename(columns={"formulas:formulas": "formula"}, inplace=True)
        df_final = df_final[df_final['formula'] != 'nan']
        colonnes_ordre = ["mz", "rt", "intensity", "formula", "C", "H", "O", "N", "S", "O/C", "H/C"]
        colonnes_existantes = [c for c in colonnes_ordre if c in df_final.columns]
        colonnes_restantes = [c for c in df_final.columns if c not in colonnes_existantes]
        df_final = df_final[colonnes_existantes + colonnes_restantes]

        # === Sauvegarde ===
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, f"{base_name}_final.csv")
        df_final.to_csv(output_file, index=False)

        messagebox.showinfo("Terminé", f"Fichier sauvegardé sous :\n{output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# --- Création de la fenêtre ---
root = tk.Tk()

root.title("ShikiProcessing")

frame = tk.Frame(root, bg="#00050A", bd=5, relief="raised")
frame.grid(row=0, column=0, columnspan=3, pady=5)
canvas = tk.Canvas(frame, width=300, height=60, bg="#0E4280", highlightthickness=0)
canvas.pack()
canvas.create_text(150, 30, text="Shiki Processing", font=("Blackadder ITC", 30), fill="white")

message = tk.Message(
    root,
    text="Ce programme traite un CSV en sortie de Workflow de MZmine : il compte le nombre d'atomes des formules bruts, calcule les rapports H/C et O/C,  supprime les différentes colonnes inutiles et les features sans formule brutes." ,
    width=500,
    bg="#0E4280",     # couleur de fond
    fg="white",      # couleur du texte
    font=("Arial", 11), # police et taille
    bd=5,               # épaisseur du cadre
    relief="raised",      # style du cadre: flat, raised, sunken, groove, ridge
    justify=tk.LEFT
)
message.grid(row=1, column=0, columnspan=3, pady=10)

tk.Label(root, text="Fichier d'entrée au format CSV :").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Parcourir", command=choisir_fichier).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Dossier de sortie :").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_folder = tk.Entry(root, width=50)
entry_folder.grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Parcourir", command=choisir_dossier).grid(row=3, column=2, padx=5, pady=5)

tk.Button(root, text="Start", width=20, command=lancer_traitement).grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()