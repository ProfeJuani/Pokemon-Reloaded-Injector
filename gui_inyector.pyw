import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

import inyector_reloaded


class InyectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Reloaded - Inyector Seguro")
        self.root.geometry("860x600")
        self.root.minsize(780, 540)

        # Paleta oscura moderna (Zinc + Indigo + Amber)
        self.bg_main = "#18181b"
        self.bg_sidebar = "#111113"
        self.bg_card = "#27272a"
        self.bg_input = "#121215"
        self.border_col = "#3f3f46"
        self.fg_text = "#f4f4f5"
        self.fg_muted = "#a1a1aa"
        self.accent = "#6366f1"
        self.accent_hover = "#4f46e5"
        self.green = "#16a34a"

        self.catalog = inyector_reloaded.load_item_catalog() + inyector_reloaded.load_mt_catalog()
        self.pkmn_catalog = inyector_reloaded.load_pokemon_catalog()
        self.atk_catalog = inyector_reloaded.load_attack_catalog()
        self.bag_counts = {}
        self.queued_items = []  # [(id, name, pocket, qty)]
        self.nav_buttons = {}
        self.pages = {}
        self.current_page = None
        self.pocket_widgets = {}

        self.root.configure(bg=self.bg_main)
        self._setup_styles()
        self._build_layout()
        self.refresh_live_status()
        self.show_page("home")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.Treeview",
            background=self.bg_input,
            foreground=self.fg_text,
            fieldbackground=self.bg_input,
            borderwidth=0,
            rowheight=26,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=self.bg_card,
            foreground="#fbbf24",
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", self.accent_hover)],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=self.bg_card,
            troughcolor=self.bg_input,
            borderwidth=0,
            arrowcolor=self.fg_muted,
        )

    def _build_layout(self):
        # Contenedor principal horizontal: Sidebar | Contenido
        container = tk.Frame(self.root, bg=self.bg_main)
        container.pack(fill=tk.BOTH, expand=True)

        # --- SIDEBAR IZQUIERDO ---
        sidebar = tk.Frame(container, bg=self.bg_sidebar, width=210)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=self.bg_sidebar, padx=16, pady=18)
        brand.pack(fill=tk.X)
        tk.Label(
            brand, text="⚡ PKM RELOADED", font=("Segoe UI", 12, "bold"),
            bg=self.bg_sidebar, fg="#fbbf24"
        ).pack(anchor="w")
        tk.Label(
            brand, text="Inyector Seguro • Anti-Cheat", font=("Segoe UI", 8),
            bg=self.bg_sidebar, fg=self.fg_muted
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(sidebar, bg=self.border_col, height=1).pack(fill=tk.X, padx=12, pady=(0, 10))

        items_count = sum(1 for c in self.catalog if c["pocket"] == "item")
        balls_count = sum(1 for c in self.catalog if c["pocket"] == "ball")
        mts_count = sum(1 for c in self.catalog if c["pocket"] == "mt")

        nav_items = [
            ("home", "🏠  Resumen y Packs"),
            ("pokemon", f"🐉  Pokémon ({len(self.pkmn_catalog)})"),
            ("items", f"🎒  Objetos ({items_count})"),
            ("balls", f"🔴  Poké Balls ({balls_count})"),
            ("mts", f"💿  MTs y MOs ({mts_count})"),
            ("money", "💰  Dinero y MTs"),
            ("log", "📋  Registro"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                sidebar, text=label, anchor="w", padx=16, pady=10,
                bg=self.bg_sidebar, fg=self.fg_muted,
                activebackground=self.bg_card, activeforeground="#ffffff",
                font=("Segoe UI", 10), bd=0, cursor="hand2",
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(fill=tk.X, padx=8, pady=2)
            self.nav_buttons[key] = btn

        # Botones inferiores del sidebar
        bottom_bar = tk.Frame(sidebar, bg=self.bg_sidebar, padx=12, pady=12)
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(
            bottom_bar, text="📥 Bajar de la Nube", bg="#0284c7", fg="#ffffff",
            activebackground="#0369a1", activeforeground="#ffffff",
            font=("Segoe UI", 8, "bold"), bd=0, pady=6, cursor="hand2",
            command=self.sync_pull_cloud,
        ).pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            bottom_bar, text="📤 Subir a la Nube", bg="#0d9488", fg="#ffffff",
            activebackground="#0f766e", activeforeground="#ffffff",
            font=("Segoe UI", 8, "bold"), bd=0, pady=6, cursor="hand2",
            command=self.sync_push_cloud,
        ).pack(fill=tk.X, pady=(0, 8))

        tk.Button(
            bottom_bar, text="🔄 Recargar Partida", bg=self.bg_card, fg=self.fg_text,
            activebackground="#3f3f46", activeforeground="#ffffff",
            font=("Segoe UI", 9), bd=0, pady=7, cursor="hand2",
            command=self.refresh_live_status,
        ).pack(fill=tk.X, pady=(0, 6))

        tk.Button(
            bottom_bar, text="🎮 Abrir Juego", bg=self.green, fg="#ffffff",
            activebackground="#15803d", activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, pady=8, cursor="hand2",
            command=self.launch_game,
        ).pack(fill=tk.X)

        # --- ÁREA DE CONTENIDO DERECHA ---
        right_area = tk.Frame(container, bg=self.bg_main)
        right_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(right_area, bg=self.bg_main, padx=20, pady=18)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de estado inferior
        status_bar = tk.Frame(right_area, bg=self.bg_sidebar, height=28, padx=14)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)
        self.lbl_status = tk.Label(
            status_bar, text="Listo.", bg=self.bg_sidebar, fg=self.fg_muted,
            font=("Segoe UI", 8), anchor="w"
        )
        self.lbl_status.pack(fill=tk.BOTH, expand=True)

        # Construir páginas
        self._build_home_page()
        self._build_pokemon_page()
        self._build_pocket_page("items", "item", "🎒 Mochila de Objetos", "Busca cualquier objeto, pon la cantidad y envíalo directo a tu mochila.")
        self._build_pocket_page("balls", "ball", "🔴 Mochila de Poké Balls", "Las Master Balls se justifican automáticamente en la historia (ev_1434).")
        self._build_pocket_page("mts", "mt", "💿 Catálogo Completo de MTs y MOs", "Añade cualquier MT/MO individual o todas las MTs (MT1–MT110) con 1 clic.")
        tk.Button(
            self.pages["mts"], text="💿 Añadir TODAS las MTs (MT1 – MT110) a mi Mochila",
            bg="#0284c7", fg="#ffffff", font=("Segoe UI", 9, "bold"),
            bd=0, padx=14, pady=8, cursor="hand2",
            command=lambda: self.run_injection_wrapper(mts="all"),
        ).pack(fill=tk.X, pady=(8, 0))
        self._build_money_page()
        self._build_log_page()

    def show_page(self, key):
        if self.current_page == key:
            return
        for k, frame in self.pages.items():
            frame.pack_forget()
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.config(bg=self.bg_card, fg="#ffffff", font=("Segoe UI", 10, "bold"))
            else:
                btn.config(bg=self.bg_sidebar, fg=self.fg_muted, font=("Segoe UI", 10))
        self.pages[key].pack(fill=tk.BOTH, expand=True)
        self.current_page = key

    def _build_home_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_main)
        self.pages["home"] = page

        tk.Label(page, text="Resumen de tu Partida", font=("Segoe UI", 15, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w")
        tk.Label(page, text="Estado en vivo de reloaded1.savc con verificación de 60 checkpoints ACS.", font=("Segoe UI", 9), bg=self.bg_main, fg=self.fg_muted).pack(anchor="w", pady=(2, 14))

        # Grid 2x2 de tarjetas de estado
        cards_grid = tk.Frame(page, bg=self.bg_main)
        cards_grid.pack(fill=tk.X, pady=(0, 18))
        cards_grid.columnconfigure(0, weight=1)
        cards_grid.columnconfigure(1, weight=1)

        self.stat_labels = {}
        stats = [
            ("dinero", "Dinero en Cartera", "#4ade80", 0, 0),
            ("banco", "Dinero en Banco", "#4ade80", 0, 1),
            ("mb", "Master Balls", "#c084fc", 1, 0),
            ("caramelos", "Caramelos Raros / MTs", "#38bdf8", 1, 1),
        ]
        for key, title, color, r, c in stats:
            card = tk.Frame(cards_grid, bg=self.bg_card, padx=14, pady=12, highlightthickness=1, highlightbackground=self.border_col)
            card.grid(row=r, column=c, sticky="ew", padx=(0 if c == 0 else 6, 6 if c == 0 else 0), pady=5)
            tk.Label(card, text=title, bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9)).pack(anchor="w")
            lbl = tk.Label(card, text="--", bg=self.bg_card, fg=color, font=("Segoe UI", 14, "bold"))
            lbl.pack(anchor="w", pady=(3, 0))
            self.stat_labels[key] = lbl

        tk.Label(page, text="Packs Rápidos (1 Clic)", font=("Segoe UI", 12, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w", pady=(4, 8))

        packs = [
            ("⭐  Pack Aventura", "Fija 10 Master Balls + 50 Caramelos Raros + 50 Ultra Balls", lambda: self.run_injection_wrapper(masterballs=10, caramelos=50, ultraballs=50)),
            ("💪  Maxear Stats (Vitaminas)", "Fija 30 unidades de cada vitamina (Más PS, Proteína, Hierro, Calcio, Carb., Zinc)", lambda: self.run_injection_wrapper(vitaminas=30)),
            ("💰  Máximo Dinero", "Fija 999.999 € en cartera + 1.000.000 € en banco", lambda: self.run_injection_wrapper(dinero=999999, banco=1000000)),
            ("💿  Pack de 19 MTs (Tienda y Casino)", "Añade Hiperrayo, Terremoto, Rayo, Lanzallamas, Rayo Hielo, Puños, Climas...", lambda: self.run_injection_wrapper(mts=True)),
        ]
        for title, desc, cmd in packs:
            row = tk.Frame(page, bg=self.bg_card, padx=14, pady=10, highlightthickness=1, highlightbackground=self.border_col)
            row.pack(fill=tk.X, pady=4)
            txt_box = tk.Frame(row, bg=self.bg_card)
            txt_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(txt_box, text=title, bg=self.bg_card, fg=self.fg_text, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(txt_box, text=desc, bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 8)).pack(anchor="w")
            tk.Button(
                row, text="Aplicar", bg=self.accent, fg="#ffffff",
                activebackground=self.accent_hover, activeforeground="#ffffff",
                font=("Segoe UI", 9, "bold"), bd=0, padx=14, pady=6, cursor="hand2",
                command=cmd,
            ).pack(side=tk.RIGHT, padx=(10, 0))

    def _build_pocket_page(self, page_key, pocket_type, title, subtitle):
        page = tk.Frame(self.content_frame, bg=self.bg_main)
        self.pages[page_key] = page

        tk.Label(page, text=title, font=("Segoe UI", 15, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w")
        tk.Label(page, text=subtitle, font=("Segoe UI", 9), bg=self.bg_main, fg=self.fg_muted).pack(anchor="w", pady=(2, 10))

        # Barra de búsqueda y filtros
        top_bar = tk.Frame(page, bg=self.bg_main)
        top_bar.pack(fill=tk.X, pady=(0, 8))

        tk.Label(top_bar, text="🔍 Buscar:", bg=self.bg_main, fg=self.fg_text, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        var_search = tk.StringVar()
        ent_search = tk.Entry(top_bar, textvariable=var_search, font=("Segoe UI", 10), bg=self.bg_input, fg="#ffffff", insertbackground="#ffffff", bd=1, relief=tk.SOLID)
        ent_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 12))

        var_only_owned = tk.BooleanVar(value=False)
        chk_owned = tk.Checkbutton(
            top_bar, text="Solo en mi mochila", variable=var_only_owned,
            bg=self.bg_main, fg=self.fg_text, selectcolor=self.bg_input,
            activebackground=self.bg_main, activeforeground="#ffffff",
            font=("Segoe UI", 9),
            command=lambda p=pocket_type: self._refresh_pocket_tree(p),
        )
        chk_owned.pack(side=tk.RIGHT)

        # Tabla Treeview
        tree_frame = tk.Frame(page, bg=self.bg_input, highlightthickness=1, highlightbackground=self.border_col)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tree = ttk.Treeview(tree_frame, columns=("id", "name", "desc", "qty"), show="headings", style="Dark.Treeview", selectmode="browse")
        tree.heading("id", text="ID")
        tree.heading("name", text="Nombre")
        tree.heading("desc", text="Función / Descripción")
        tree.heading("qty", text="En Mochila")
        tree.column("id", width=50, anchor="center", stretch=False)
        tree.column("name", width=165, anchor="w", stretch=False)
        tree.column("desc", width=290, anchor="w")
        tree.column("qty", width=85, anchor="center", stretch=False)

        scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview, style="Vertical.TScrollbar")
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel inferior de acción
        action_card = tk.Frame(page, bg=self.bg_card, padx=14, pady=12, highlightthickness=1, highlightbackground=self.border_col)
        action_card.pack(fill=tk.X)

        lbl_sel = tk.Label(action_card, text="Selecciona un elemento de la lista", bg=self.bg_card, fg="#fbbf24", font=("Segoe UI", 10, "bold"))
        lbl_sel.pack(anchor="w")
        lbl_desc = tk.Label(action_card, text="", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9), wraplength=580, justify="left")
        lbl_desc.pack(anchor="w", pady=(2, 8))

        controls = tk.Frame(action_card, bg=self.bg_card)
        controls.pack(fill=tk.X)

        tk.Label(controls, text="Cantidad a fijar:", bg=self.bg_card, fg=self.fg_text, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        ent_qty = tk.Entry(controls, width=8, font=("Segoe UI", 10, "bold"), bg=self.bg_input, fg="#ffffff", insertbackground="#ffffff", bd=1, justify="center")
        ent_qty.pack(side=tk.LEFT, padx=(8, 8))
        ent_qty.insert(0, "99")

        # Botones rápidos de cantidad
        for preset in (1, 10, 50, 99, 999):
            tk.Button(
                controls, text=str(preset), bg="#3f3f46", fg="#ffffff",
                activebackground="#52525b", activeforeground="#ffffff",
                font=("Segoe UI", 8), bd=0, padx=7, pady=4, cursor="hand2",
                command=lambda v=preset, e=ent_qty: (e.delete(0, tk.END), e.insert(0, str(v))),
            ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            controls, text="⚡ Poner en Mochila", bg=self.accent, fg="#ffffff",
            activebackground=self.accent_hover, activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, padx=14, pady=6, cursor="hand2",
            command=lambda p=pocket_type: self._inject_pocket_selection(p),
        ).pack(side=tk.RIGHT)

        tk.Button(
            controls, text="➕ A la cola", bg="#3f3f46", fg="#ffffff",
            activebackground="#52525b", activeforeground="#ffffff",
            font=("Segoe UI", 9), bd=0, padx=10, pady=6, cursor="hand2",
            command=lambda p=pocket_type: self._queue_pocket_selection(p),
        ).pack(side=tk.RIGHT, padx=(0, 6))

        # Barra de cola (visible cuando hay ítems en cola)
        queue_bar = tk.Frame(page, bg=self.bg_card, padx=12, pady=8, highlightthickness=1, highlightbackground=self.accent)
        lbl_queue = tk.Label(queue_bar, text="", bg=self.bg_card, fg="#38bdf8", font=("Segoe UI", 9))
        lbl_queue.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(
            queue_bar, text="Limpiar", bg="#52525b", fg="#ffffff",
            font=("Segoe UI", 8), bd=0, padx=8, pady=4, cursor="hand2",
            command=self._clear_queue,
        ).pack(side=tk.RIGHT, padx=(6, 0))
        tk.Button(
            queue_bar, text="⚡ Aplicar Toda la Cola", bg=self.green, fg="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, cursor="hand2",
            command=self._inject_queue,
        ).pack(side=tk.RIGHT)

        self.pocket_widgets[pocket_type] = {
            "var_search": var_search,
            "var_only_owned": var_only_owned,
            "tree": tree,
            "lbl_sel": lbl_sel,
            "lbl_desc": lbl_desc,
            "ent_qty": ent_qty,
            "queue_bar": queue_bar,
            "lbl_queue": lbl_queue,
            "filtered": [],
        }

        var_search.trace_add("write", lambda *_, p=pocket_type: self._refresh_pocket_tree(p))
        tree.bind("<<ListboxSelect>>", lambda *_, p=pocket_type: self._on_tree_select(p))
        tree.bind("<<TreeviewSelect>>", lambda *_, p=pocket_type: self._on_tree_select(p))
        self._refresh_pocket_tree(pocket_type)

    def _build_money_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_main)
        self.pages["money"] = page

        tk.Label(page, text="💰 Dinero y MTs", font=("Segoe UI", 15, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w")
        tk.Label(page, text="Deja un campo vacío si no quieres modificar ese valor.", font=("Segoe UI", 9), bg=self.bg_main, fg=self.fg_muted).pack(anchor="w", pady=(2, 14))

        card = tk.Frame(page, bg=self.bg_card, padx=18, pady=16, highlightthickness=1, highlightbackground=self.border_col)
        card.pack(fill=tk.X, pady=(0, 14))

        tk.Label(card, text="Dinero en Cartera (€):", bg=self.bg_card, fg=self.fg_text, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=8)
        self.ent_dinero = tk.Entry(card, width=18, font=("Segoe UI", 11), bg=self.bg_input, fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_dinero.grid(row=0, column=1, sticky="w", padx=14, pady=8)

        tk.Label(card, text="Dinero en Banco (€):", bg=self.bg_card, fg=self.fg_text, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=8)
        self.ent_banco = tk.Entry(card, width=18, font=("Segoe UI", 11), bg=self.bg_input, fg="#ffffff", insertbackground="#ffffff", bd=1)
        self.ent_banco.grid(row=1, column=1, sticky="w", padx=14, pady=8)

        tk.Button(
            card, text="⚡ Actualizar Dinero", bg=self.accent, fg="#ffffff",
            activebackground=self.accent_hover, activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"), bd=0, padx=16, pady=8, cursor="hand2",
            command=self._apply_money,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))

        mt_card = tk.Frame(page, bg=self.bg_card, padx=18, pady=16, highlightthickness=1, highlightbackground=self.border_col)
        mt_card.pack(fill=tk.X)
        tk.Label(mt_card, text="💿 MTs de Tienda y Casino (19 MTs)", bg=self.bg_card, fg=self.fg_text, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(mt_card, text="Incluye Hiperrayo, Terremoto, Rayo, Rayo Hielo, Lanzallamas, Climas, Puños elementales y Reflejo.", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9), wraplength=540, justify="left").pack(anchor="w", pady=(4, 10))
        tk.Button(
            mt_card, text="💿 Añadir las 19 MTs a mi Mochila", bg="#0284c7", fg="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, padx=14, pady=7, cursor="hand2",
            command=lambda: self.run_injection_wrapper(mts=True),
        ).pack(anchor="w")

    def _build_log_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_main)
        self.pages["log"] = page

        tk.Label(page, text="📋 Registro de Verificación", font=("Segoe UI", 15, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w")
        tk.Label(page, text="Detalle técnico de copias de seguridad y recálculo de checksums ACS.", font=("Segoe UI", 9), bg=self.bg_main, fg=self.fg_muted).pack(anchor="w", pady=(2, 10))

        self.txt_log = tk.Text(page, bg="#09090b", fg="#4ade80", font=("Consolas", 9), bd=1, relief=tk.SOLID, padx=10, pady=10)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def _refresh_pocket_tree(self, pocket_type):
        w = self.pocket_widgets[pocket_type]
        q = w["var_search"].get().strip().lower()
        only_owned = w["var_only_owned"].get()
        tree = w["tree"]
        tree.delete(*tree.get_children())
        filtered = []

        for entry in self.catalog:
            if entry["pocket"] != pocket_type:
                continue
            owned = self.bag_counts.get((pocket_type, entry["id"]), 0)
            if only_owned and owned <= 0:
                continue
            if q and q not in entry["name"].lower() and q not in entry.get("desc", "").lower() and q != str(entry["id"]):
                continue
            filtered.append(entry)
            qty_txt = str(owned) if owned > 0 else "—"
            tree.insert("", tk.END, iid=str(entry["id"]), values=(f"{entry['id']:03d}", entry["name"], entry.get("desc", ""), qty_txt))

        w["filtered"] = filtered

    def _get_selected_entry(self, pocket_type):
        w = self.pocket_widgets[pocket_type]
        sel = w["tree"].selection()
        if not sel:
            return None
        sel_id = int(sel[0])
        for entry in w["filtered"]:
            if entry["id"] == sel_id:
                return entry
        return None

    def _on_tree_select(self, pocket_type):
        entry = self._get_selected_entry(pocket_type)
        if not entry:
            return
        curr = self.bag_counts.get((pocket_type, entry["id"]), 0)
        self.pocket_widgets[pocket_type]["lbl_sel"].config(
            text=f"Seleccionado: {entry['name']} (ID {entry['id']})  •  En tu mochila: {curr}"
        )
        self.pocket_widgets[pocket_type]["lbl_desc"].config(
            text=f"Función: {entry.get('desc', '')}"
        )

    def _parse_qty(self, pocket_type):
        raw = self.pocket_widgets[pocket_type]["ent_qty"].get().strip()
        val = int(raw)
        if val < 0:
            raise ValueError("La cantidad debe ser 0 o mayor.")
        return val

    def _inject_pocket_selection(self, pocket_type):
        entry = self._get_selected_entry(pocket_type)
        if not entry:
            messagebox.showwarning("Sin selección", "Selecciona un elemento de la lista primero.")
            return
        try:
            qty = self._parse_qty(pocket_type)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Ingresa un número entero válido (0 o mayor).")
            return

        if pocket_type == "ball":
            self.run_injection_wrapper(balls_custom=[(entry["id"], qty)])
        elif pocket_type == "mt":
            self.run_injection_wrapper(mts=[(entry["id"], qty)])
        else:
            self.run_injection_wrapper(items_custom=[(entry["id"], qty)])

    def _queue_pocket_selection(self, pocket_type):
        entry = self._get_selected_entry(pocket_type)
        if not entry:
            messagebox.showwarning("Sin selección", "Selecciona un elemento de la lista primero.")
            return
        try:
            qty = self._parse_qty(pocket_type)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Ingresa un número entero válido (0 o mayor).")
            return

        for idx, (eid, _n, ep, _q) in enumerate(self.queued_items):
            if eid == entry["id"] and ep == pocket_type:
                self.queued_items[idx] = (entry["id"], entry["name"], pocket_type, qty)
                self._update_queue_bars()
                return
        self.queued_items.append((entry["id"], entry["name"], pocket_type, qty))
        self._update_queue_bars()

    def _update_queue_bars(self):
        count = len(self.queued_items)
        summary = ", ".join(f"{n} x{q}" for _i, n, _p, q in self.queued_items[:4])
        if count > 4:
            summary += f" (+{count - 4} más)"
        for w in self.pocket_widgets.values():
            if count > 0:
                w["lbl_queue"].config(text=f"En cola ({count}): {summary}")
                w["queue_bar"].pack(fill=tk.X, pady=(8, 0))
            else:
                w["queue_bar"].pack_forget()

    def _clear_queue(self):
        self.queued_items.clear()
        self._update_queue_bars()

    def _inject_queue(self):
        if not self.queued_items:
            return
        items_c = [(eid, qty) for eid, _n, pocket, qty in self.queued_items if pocket == "item"]
        balls_c = [(eid, qty) for eid, _n, pocket, qty in self.queued_items if pocket == "ball"]
        mts_c = [(eid, qty) for eid, _n, pocket, qty in self.queued_items if pocket == "mt"]
        if self.run_injection_wrapper(items_custom=items_c or None, balls_custom=balls_c or None, mts=mts_c or None):
            self._clear_queue()

    def _apply_money(self):
        try:
            din_raw = self.ent_dinero.get().strip()
            ban_raw = self.ent_banco.get().strip()
            din = int(din_raw) if din_raw else None
            ban = int(ban_raw) if ban_raw else None
            if din is None and ban is None:
                messagebox.showinfo("Sin cambios", "Ingresa al menos una cantidad de dinero.")
                return
            self.run_injection_wrapper(dinero=din, banco=ban)
        except ValueError:
            messagebox.showerror("Formato inválido", "Ingresa números enteros válidos para el dinero.")

    def log(self, text):
        self.txt_log.insert(tk.END, text + "\n")
        self.txt_log.see(tk.END)
        self.lbl_status.config(text=text)
        self.root.update_idletasks()

    def refresh_live_status(self):
        if not os.path.exists(inyector_reloaded.SAVE_PATH):
            self.lbl_status.config(text="Archivo de partida no encontrado.")
            return
        try:
            data = open(inyector_reloaded.SAVE_PATH, "rb").read()
            st = inyector_reloaded.load_save_state(data)
            glb = st["glb"]
            obj_18 = st["obj_18"]

            din = int(glb.dinero)
            ban = int(obj_18.ingreso)
            self.stat_labels["dinero"].config(text=f"{din:,} €".replace(",", "."))
            self.stat_labels["banco"].config(text=f"{ban:,} €".replace(",", "."))

            self.bag_counts = {}
            for i in range(30):
                bid = int(glb.ObBall[i])
                bn = int(glb.nObBall[i])
                if bid > 0 and bn > 0:
                    self.bag_counts[("ball", bid)] = bn
            for i in range(420):
                iid = int(glb.ObItem[i])
                inq = int(glb.nObItem[i])
                if iid > 0 and inq > 0:
                    self.bag_counts[("item", iid)] = inq

            mb = self.bag_counts.get(("ball", 4), 0)
            car = self.bag_counts.get(("item", 38), 0)
            mts_cnt = 0
            for i in range(1000):
                mid = int(glb.ObMT[i])
                mq = int(glb.nObMT[i])
                if mid > 0 and mq > 0:
                    self.bag_counts[("mt", mid)] = mq
                    mts_cnt += 1

            self.stat_labels["mb"].config(text=str(mb))
            self.stat_labels["caramelos"].config(text=f"{car}  /  {mts_cnt} MTs")

            self._refresh_pocket_tree("item")
            self._refresh_pocket_tree("ball")
            self._refresh_pocket_tree("mt")
            self._on_tree_select("item")
            self._on_tree_select("ball")
            self._on_tree_select("mt")
            self.log("[Info] Partida sincronizada correctamente.")
        except Exception as e:
            self.log(f"[Error] No se pudo leer la partida: {e}")

    def run_injection_wrapper(self, **kwargs):
        self.log(">>> Iniciando inyección segura y justificada...")
        try:
            ok = inyector_reloaded.execute_injection(**kwargs)
            if not ok:
                raise RuntimeError("Falló la verificación de seguridad. Se restauró el respaldo original.")
            self.log("[Éxito] Inyección completada y verificada al 100% sin anomalías.")
            messagebox.showinfo("Inyección Completada", "¡Cambios aplicados en tu mochila y verificados al 100%!\nPuedes abrir el juego sin riesgo.")
            self.refresh_live_status()
            return True
        except Exception as e:
            self.log(f"[Error] Falló la inyección: {e}")
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
            return False

    def _run_cloud_bat(self, bat_name, start_msg, ok_msg):
        self.log(start_msg)
        bat_path = os.path.abspath(bat_name)
        if not os.path.exists(bat_path):
            messagebox.showerror("Error", f"No se encontró {bat_name}")
            return
        res = subprocess.run(["cmd", "/c", bat_path], capture_output=True, text=True)
        if res.returncode == 0:
            self.log(f"[Éxito] {ok_msg}")
            messagebox.showinfo("Nube", ok_msg)
            self.refresh_live_status()
        else:
            self.log(f"[Error Nube] {res.stderr or res.stdout}")
            messagebox.showerror("Error Nube", f"No se pudo completar {bat_name}.")

    def sync_pull_cloud(self):
        self._run_cloud_bat(
            "Descargar_Partida_Nube.bat",
            ">>> Sincronizando: Descargando partida desde la nube (GitHub)...",
            "¡Partida descargada y sincronizada desde la nube con éxito!",
        )

    def sync_push_cloud(self):
        self._run_cloud_bat(
            "Subir_Partida_Nube.bat",
            ">>> Sincronizando: Subiendo partida actual a la nube (GitHub)...",
            "¡Partida respaldada y subida a tu repositorio de guardados en GitHub!",
        )

    def _build_pokemon_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_main)
        self.pages["pokemon"] = page

        tk.Label(page, text="🐉 Inyector Seguro de Pokémon (Caja del PC)", font=("Segoe UI", 15, "bold"), bg=self.bg_main, fg=self.fg_text).pack(anchor="w")
        tk.Label(page, text="Inyecta Pokémon en cualquier Caja del PC recalculando vsietecj y vsietecj2. Al sacarlos del PC el juego calcula todos sus stats y tipos.", font=("Segoe UI", 9), bg=self.bg_main, fg=self.fg_muted).pack(anchor="w", pady=(2, 10))

        tk.Button(
            page,
            text="⭐ Inyectar Equipo Élite de Aventura en Caja PC 6 (Garchomp, Gardevoir, Greninja, Talonflame, Metagross, Sceptile — Nv.42)",
            bg="#059669", fg="#ffffff", activebackground="#047857", activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=8, cursor="hand2",
            command=self._inject_dream_team_box6,
        ).pack(fill=tk.X, pady=(0, 10))

        # Buscador
        search_bar = tk.Frame(page, bg=self.bg_main)
        search_bar.pack(fill=tk.X, pady=(0, 8))
        tk.Label(search_bar, text="🔍 Buscar Pokémon:", bg=self.bg_main, fg=self.fg_muted, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.var_pkmn_search = tk.StringVar()
        self.var_pkmn_search.trace_add("write", lambda *_: self._refresh_pkmn_tree())
        tk.Entry(
            search_bar, textvariable=self.var_pkmn_search, bg=self.bg_input, fg=self.fg_text,
            insertbackground="#ffffff", font=("Segoe UI", 10), bd=1, relief=tk.SOLID
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0), ipady=3)

        # Tabla de Pokémon
        tree_wrap = tk.Frame(page, bg=self.border_col, bd=1)
        tree_wrap.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.pkmn_tree = ttk.Treeview(tree_wrap, columns=("id", "name"), show="headings", style="Dark.Treeview", selectmode="browse")
        self.pkmn_tree.heading("id", text="ID")
        self.pkmn_tree.heading("name", text="Pokémon")
        self.pkmn_tree.column("id", width=70, anchor="center", stretch=False)
        self.pkmn_tree.column("name", width=400, anchor="w")
        sb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.pkmn_tree.yview, style="Vertical.TScrollbar")
        self.pkmn_tree.configure(yscrollcommand=sb.set)
        self.pkmn_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuración del Pokémon
        cfg = tk.Frame(page, bg=self.bg_card, padx=12, pady=10, highlightbackground=self.border_col, highlightthickness=1)
        cfg.pack(fill=tk.X)

        row1 = tk.Frame(cfg, bg=self.bg_card)
        row1.pack(fill=tk.X, pady=(0, 6))
        tk.Label(row1, text="Caja PC:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.ent_pk_box = tk.Entry(row1, width=4, bg=self.bg_input, fg=self.fg_text, insertbackground="#ffffff", font=("Segoe UI", 9), bd=1)
        self.ent_pk_box.insert(0, "6")
        self.ent_pk_box.pack(side=tk.LEFT, padx=(4, 12))

        tk.Label(row1, text="Nivel:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.ent_pk_lvl = tk.Entry(row1, width=5, bg=self.bg_input, fg=self.fg_text, insertbackground="#ffffff", font=("Segoe UI", 9), bd=1)
        self.ent_pk_lvl.insert(0, "42")
        self.ent_pk_lvl.pack(side=tk.LEFT, padx=(4, 12))

        tk.Label(row1, text="IVs (999999=Max):", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.ent_pk_iv = tk.Entry(row1, width=8, bg=self.bg_input, fg=self.fg_text, insertbackground="#ffffff", font=("Segoe UI", 9), bd=1)
        self.ent_pk_iv.insert(0, "999999")
        self.ent_pk_iv.pack(side=tk.LEFT, padx=(4, 12))

        tk.Label(row1, text="Obj ID:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.ent_pk_obj = tk.Entry(row1, width=6, bg=self.bg_input, fg=self.fg_text, insertbackground="#ffffff", font=("Segoe UI", 9), bd=1)
        self.ent_pk_obj.insert(0, "303")
        self.ent_pk_obj.pack(side=tk.LEFT, padx=(4, 0))

        row2 = tk.Frame(cfg, bg=self.bg_card)
        row2.pack(fill=tk.X, pady=(0, 8))
        atk_values = [f"{a['id']} - {a['name']}" for a in self.atk_catalog]
        defaults = ["17 - Terremoto", "41 - Rayo", "73 - Rayo hielo", "16 - Bola sombra"]
        self.cmb_atks = []
        for idx in range(4):
            cmb = ttk.Combobox(row2, values=atk_values, width=16, font=("Segoe UI", 8))
            cmb.set(defaults[idx])
            cmb.pack(side=tk.LEFT, padx=(0 if idx == 0 else 4, 0), fill=tk.X, expand=True)
            self.cmb_atks.append(cmb)

        tk.Button(
            cfg, text="➕ Inyectar Pokémon Seleccionado en la Caja PC",
            bg=self.accent, fg="#ffffff", activebackground=self.accent_hover, activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), bd=0, pady=7, cursor="hand2",
            command=self._inject_selected_pokemon,
        ).pack(fill=tk.X)

        self._refresh_pkmn_tree()

    def _refresh_pkmn_tree(self):
        q = self.var_pkmn_search.get().strip().lower()
        self.pkmn_tree.delete(*self.pkmn_tree.get_children())
        for p in self.pkmn_catalog:
            if not q or q in p["name"].lower() or q == str(p["id"]):
                self.pkmn_tree.insert("", tk.END, values=(p["id"], p["name"]))

    def _inject_selected_pokemon(self):
        sel = self.pkmn_tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un Pokémon de la lista.")
            return
        pk_id, pk_name = self.pkmn_tree.item(sel[0], "values")
        try:
            box = int(self.ent_pk_box.get().strip())
            lvl = int(self.ent_pk_lvl.get().strip())
            iv = int(self.ent_pk_iv.get().strip())
            obj_id = int(self.ent_pk_obj.get().strip() or "0")
            atks = []
            for cmb in self.cmb_atks:
                raw = cmb.get().strip()
                atks.append(int(raw.split(" - ")[0]) if raw else 0)
        except ValueError:
            messagebox.showerror("Error", "Revisa que Caja, Nivel, IVs, Objeto y Ataques tengan números válidos.")
            return

        spec = {
            "box": box, "pkmn_id": int(pk_id), "name": pk_name,
            "level": lvl, "iv": iv, "item_id": obj_id, "attacks": atks, "sex": 1,
        }
        self.run_injection_wrapper(box_pokemon=[spec])

    def _inject_dream_team_box6(self):
        team = [dict(p, box=6) for p in inyector_reloaded.ADVENTURE_DREAM_TEAM]
        self.run_injection_wrapper(box_pokemon=team)

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
