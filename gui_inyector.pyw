import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Import the core engine functions from inyector_reloaded
import inyector_reloaded

class InyectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Reloaded - Inyector Seguro y Justificado")
        self.root.geometry("640x720")
        self.root.minsize(580, 680)
        
        # Color palette
        self.bg_color = "#18181b"       # Zinc 900
        self.card_bg = "#27272a"        # Zinc 800
        self.card_border = "#3f3f46"    # Zinc 700
        self.fg_color = "#f4f4f5"       # Zinc 100
        self.muted_fg = "#a1a1aa"       # Zinc 400
        self.accent_color = "#6366f1"   # Indigo 500
        self.accent_hover = "#4f46e5"   # Indigo 600
        self.success_color = "#22c55e"  # Green 500
        
        self.root.configure(bg=self.bg_color)
        self.setup_styles()
        self.create_widgets()
        self.refresh_live_status()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg)
        
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=self.card_bg, foreground=self.muted_fg, font=("Segoe UI", 9))
        style.configure("CardTitle.TLabel", background=self.card_bg, foreground=self.fg_color, font=("Segoe UI", 11, "bold"))
        style.configure("CardVal.TLabel", background=self.card_bg, foreground="#38bdf8", font=("Segoe UI", 10, "bold"))
        
        style.configure("Accent.TButton", background=self.accent_color, foreground="#ffffff", font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", self.accent_hover)])
        
        style.configure("Quick.TButton", background="#3f3f46", foreground="#ffffff", font=("Segoe UI", 9), borderwidth=0)
        style.map("Quick.TButton", background=[("active", "#52525b")])

    def create_widgets(self):
        main_container = ttk.Frame(self.root, padding=16)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        title_lbl = tk.Label(header_frame, text="POKÉMON RELOADED", font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg="#fbbf24")
        title_lbl.pack(anchor="w")
        subtitle_lbl = tk.Label(header_frame, text="Inyector Seguro con Justificación Criptográfica Nativa (Anti-Cheat Bypass)", font=("Segoe UI", 9), bg=self.bg_color, fg=self.muted_fg)
        subtitle_lbl.pack(anchor="w")

        # Live Status Card
        status_card = tk.LabelFrame(main_container, text=" Estado Actual de la Partida ", bg=self.card_bg, fg="#fbbf24", font=("Segoe UI", 10, "bold"), padx=12, pady=8, bd=1, relief=tk.SOLID)
        status_card.pack(fill=tk.X, pady=(0, 12))
        
        st_grid = tk.Frame(status_card, bg=self.card_bg)
        st_grid.pack(fill=tk.X)
        
        tk.Label(st_grid, text="Dinero en Cartera:", bg=self.card_bg, fg=self.muted_fg, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=2)
        self.lbl_dinero = tk.Label(st_grid, text="-- €", bg=self.card_bg, fg="#4ade80", font=("Segoe UI", 9, "bold"))
        self.lbl_dinero.grid(row=0, column=1, sticky="w", padx=(5, 20), pady=2)
        
        tk.Label(st_grid, text="Dinero en Banco:", bg=self.card_bg, fg=self.muted_fg, font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", pady=2)
        self.lbl_banco = tk.Label(st_grid, text="-- €", bg=self.card_bg, fg="#4ade80", font=("Segoe UI", 9, "bold"))
        self.lbl_banco.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        tk.Label(st_grid, text="Master Balls:", bg=self.card_bg, fg=self.muted_fg, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=2)
        self.lbl_mb = tk.Label(st_grid, text="--", bg=self.card_bg, fg="#c084fc", font=("Segoe UI", 9, "bold"))
        self.lbl_mb.grid(row=1, column=1, sticky="w", padx=(5, 20), pady=2)
        
        tk.Label(st_grid, text="Caramelos Raros:", bg=self.card_bg, fg=self.muted_fg, font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", pady=2)
        self.lbl_caramelos = tk.Label(st_grid, text="--", bg=self.card_bg, fg="#38bdf8", font=("Segoe UI", 9, "bold"))
        self.lbl_caramelos.grid(row=1, column=3, sticky="w", padx=5, pady=2)

        tk.Label(st_grid, text="MTs en Mochila:", bg=self.card_bg, fg=self.muted_fg, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=2)
        self.lbl_mts = tk.Label(st_grid, text="--", bg=self.card_bg, fg="#f59e0b", font=("Segoe UI", 9, "bold"))
        self.lbl_mts.grid(row=2, column=1, sticky="w", padx=(5, 20), pady=2)

        # Quick Actions Card
        quick_card = tk.LabelFrame(main_container, text=" Acciones Rápidas (1 Clic) ", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 10, "bold"), padx=10, pady=8, bd=1, relief=tk.SOLID)
        quick_card.pack(fill=tk.X, pady=(0, 12))
        
        btn_q1 = tk.Button(quick_card, text="⭐ Pack Aventura (10 Master Balls + 50 Caramelos + 50 Ultra Balls)", bg="#3f3f46", fg="#ffffff", font=("Segoe UI", 9), bd=0, padx=8, pady=5, cursor="hand2", command=self.apply_pack_aventura)
        btn_q1.pack(fill=tk.X, pady=3)
        
        btn_q2 = tk.Button(quick_card, text="💪 Maxear Stats (Lote de 30 Vitaminas de cada tipo: PS, Atk, Def, Vel...)", bg="#3f3f46", fg="#ffffff", font=("Segoe UI", 9), bd=0, padx=8, pady=5, cursor="hand2", command=self.apply_pack_vitaminas)
        btn_q2.pack(fill=tk.X, pady=3)

        btn_q3 = tk.Button(quick_card, text="💰 Máximo Dinero (999.999 € Cartera + 1.000.000 € Banco)", bg="#3f3f46", fg="#ffffff", font=("Segoe UI", 9), bd=0, padx=8, pady=5, cursor="hand2", command=self.apply_pack_dinero)
        btn_q3.pack(fill=tk.X, pady=3)

        btn_q4 = tk.Button(quick_card, text="💿 Añadir MTs de Tienda y Casino (19 MTs: Terremoto, Rayo, Lanzallamas...)", bg="#3f3f46", fg="#ffffff", font=("Segoe UI", 9), bd=0, padx=8, pady=5, cursor="hand2", command=self.apply_pack_mts)
        btn_q4.pack(fill=tk.X, pady=3)

        # Custom Fields Card
        custom_card = tk.LabelFrame(main_container, text=" Personalizar Cantidades ", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 10, "bold"), padx=12, pady=10, bd=1, relief=tk.SOLID)
        custom_card.pack(fill=tk.X, pady=(0, 12))
        
        cf_grid = tk.Frame(custom_card, bg=self.card_bg)
        cf_grid.pack(fill=tk.X)
        
        # Row 0: Master Balls
        tk.Label(cf_grid, text="Master Balls a fijar:", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
        self.ent_mb = tk.Entry(cf_grid, width=12, font=("Segoe UI", 10), bg="#18181b", fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_mb.grid(row=0, column=1, sticky="w", padx=10, pady=4)
        self.ent_mb.insert(0, "10")
        
        # Row 1: Caramelos Raros
        tk.Label(cf_grid, text="Caramelos Raros a fijar:", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)
        self.ent_caramelos = tk.Entry(cf_grid, width=12, font=("Segoe UI", 10), bg="#18181b", fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_caramelos.grid(row=1, column=1, sticky="w", padx=10, pady=4)
        self.ent_caramelos.insert(0, "50")

        # Row 2: Dinero Cartera
        tk.Label(cf_grid, text="Dinero en Cartera (€):", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=4)
        self.ent_dinero = tk.Entry(cf_grid, width=12, font=("Segoe UI", 10), bg="#18181b", fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_dinero.grid(row=2, column=1, sticky="w", padx=10, pady=4)
        self.ent_dinero.insert(0, "950000")

        # Row 3: Dinero Banco
        tk.Label(cf_grid, text="Dinero en Banco (€):", bg=self.card_bg, fg=self.fg_color, font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", pady=4)
        self.ent_banco = tk.Entry(cf_grid, width=12, font=("Segoe UI", 10), bg="#18181b", fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_banco.grid(row=3, column=1, sticky="w", padx=10, pady=4)
        self.ent_banco.insert(0, "1000000")

        # Inject Button
        self.btn_inject = tk.Button(main_container, text="⚡ INYECTAR Y JUSTIFICAR EN LA PARTIDA", bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 11, "bold"), bd=0, pady=8, cursor="hand2", command=self.apply_custom_injection)
        self.btn_inject.pack(fill=tk.X, pady=(0, 10))

        # Log Output Box
        log_frame = tk.Frame(main_container, bg=self.bg_color)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(log_frame, text="Registro de Verificación:", bg=self.bg_color, fg=self.muted_fg, font=("Segoe UI", 9)).pack(anchor="w")
        self.txt_log = tk.Text(log_frame, height=6, bg="#09090b", fg="#4ade80", font=("Consolas", 9), bd=1, relief=tk.SOLID, padx=6, pady=6)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        # Footer Buttons
        footer_frame = tk.Frame(main_container, bg=self.bg_color)
        footer_frame.pack(fill=tk.X)
        
        btn_refresh = tk.Button(footer_frame, text="🔄 Recargar Estado", bg="#3f3f46", fg="#ffffff", font=("Segoe UI", 9), bd=0, padx=12, pady=5, cursor="hand2", command=self.refresh_live_status)
        btn_refresh.pack(side=tk.LEFT)
        
        btn_launch = tk.Button(footer_frame, text="🎮 Abrir Pokémon Reloaded", bg="#16a34a", fg="#ffffff", font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=5, cursor="hand2", command=self.launch_game)
        btn_launch.pack(side=tk.RIGHT)

    def log(self, text):
        self.txt_log.insert(tk.END, text + "\n")
        self.txt_log.see(tk.END)
        self.root.update_idletasks()

    def refresh_live_status(self):
        if not os.path.exists(inyector_reloaded.SAVE_PATH):
            self.lbl_dinero.config(text="No encontrado")
            return
        try:
            data = open(inyector_reloaded.SAVE_PATH, 'rb').read()
            st = inyector_reloaded.load_save_state(data)
            glb = st['glb']
            obj_18 = st['obj_18']
            
            # Dinero
            din = int(glb.dinero)
            ban = int(obj_18.ingreso)
            self.lbl_dinero.config(text=f"{din:,} €".replace(",", "."))
            self.lbl_banco.config(text=f"{ban:,} €".replace(",", "."))
            
            # Master balls
            mb = 0
            for i in range(30):
                if int(glb.ObBall[i]) == 4:
                    mb = int(glb.nObBall[i])
                    break
            self.lbl_mb.config(text=str(mb))
            
            # Caramelos
            car = 0
            for i in range(420):
                if int(glb.ObItem[i]) == 38:
                    car = int(glb.nObItem[i])
                    break
            self.lbl_caramelos.config(text=str(car))

            # MTs
            mts_cnt = 0
            for i in range(1001):
                if int(glb.ObMT[i]) > 0 and int(glb.nObMT[i]) > 0:
                    mts_cnt += 1
            self.lbl_mts.config(text=f"{mts_cnt} MTs")

            self.log("[Info] Estado del guardado sincronizado correctamente.")
        except Exception as e:
            self.log(f"[Error] No se pudo leer el guardado: {e}")

    def run_injection_wrapper(self, **kwargs):
        self.txt_log.delete("1.0", tk.END)
        self.log(">>> Iniciando inyección segura y justificada...")
        try:
            inyector_reloaded.execute_injection(**kwargs)
            self.log("[Éxito] Inyección completada y guardada sin anomalías.")
            messagebox.showinfo("Inyección Completada", "¡La partida fue modificada y verificada al 100% con éxito!\nYa puedes jugar sin riesgo de error.")
            self.refresh_live_status()
        except Exception as e:
            self.log(f"[Error] Falló la inyección: {e}")
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def apply_pack_aventura(self):
        self.run_injection_wrapper(masterballs=10, caramelos=50, ultraballs=50)

    def apply_pack_vitaminas(self):
        self.run_injection_wrapper(vitaminas=30)

    def apply_pack_dinero(self):
        self.run_injection_wrapper(dinero=999999, banco=1000000)

    def apply_pack_mts(self):
        self.run_injection_wrapper(mts=True)

    def apply_custom_injection(self):
        try:
            mb = int(self.ent_mb.get().strip()) if self.ent_mb.get().strip() else None
            car = int(self.ent_caramelos.get().strip()) if self.ent_caramelos.get().strip() else None
            din = int(self.ent_dinero.get().strip()) if self.ent_dinero.get().strip() else None
            ban = int(self.ent_banco.get().strip()) if self.ent_banco.get().strip() else None
            
            self.run_injection_wrapper(dinero=din, banco=ban, masterballs=mb, caramelos=car)
        except ValueError:
            messagebox.showerror("Error de formato", "Por favor ingresa números enteros válidos en los campos.")

    def launch_game(self):
        exe_path = r"Proyecto Reloaded The Last Beta 1.9.2.2 Full\Proyecto Reloaded The Last Beta 1.9.2.2 Full.exe"
        if os.path.exists(exe_path):
            cwd = os.path.dirname(os.path.abspath(exe_path))
            subprocess.Popen([os.path.abspath(exe_path)], cwd=cwd)
            self.log("[Juego] Lanzando Pokémon Reloaded...")
        else:
            messagebox.showerror("No encontrado", f"No se encontró el ejecutable en:\n{exe_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InyectorApp(root)
    root.mainloop()

