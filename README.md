# ⚡ Inyector Seguro y Justificado - Pokémon Reloaded (The Last Beta 1.9.2.2)

Herramienta autónoma y visual para la edición y modificación segura de partidas (`.savc` / `.savb`) en **Pokémon Reloaded (The Last Beta 1.9.2.2)** con evasión y recálculo matemático de todos los sistemas anti-trampas nativos.

---

## ✨ Características Principales

1. **🛡️ 100% Seguro contra Anomalías y Anti-Cheat:**
   * Recálculo en tiempo real de los 59 checkpoints de seguridad criptográfica (ACS).
   * Generación y sincronización de firmas criptográficas para:
     * **Cartera:** `vochodin`, `vsietedin`, `secodin`.
     * **Banco:** `vochoban`, `vsieteban`, `secoban`.
     * **Mochila de Balls:** `vsietevbl`, `secovbl`.
     * **Mochila de Objetos:** `vsietevob`, `secovob`.
     * **Mochila de MTs:** `vsietevmt`, `secovmt` (sin límite narrativo).
     * **Equipo Pokémon:** Validación de integridad en combate (`vsietepk` y `vsietepk2` para evitar el error `8315692`).
   * **Justificación Legal de Master Balls:** Ajuste automático de los flags de historia de eventos (`ev_1434` / `ev_1435`) para cumplir la regla estricta `has <= dis` del juego.

2. **🖥️ Interfaz Gráfica Moderna (`gui_inyector.pyw`):**
   * Panel visual oscuro estilo dashboard (Tkinter).
   * Lectura y monitor en vivo del estado de la partida (dinero, banco, Master Balls, caramelos, MTs).
   * **Acciones rápidas a 1 clic:**
     * ⭐ *Pack Aventura:* 10 Master Balls + 50 Caramelos Raros + 50 Ultra Balls.
     * 💪 *Maxear Stats:* Lote de 30 unidades de cada vitamina (Más PS, Proteína, Hierro, Calcio, Carbohidratos, Zinc).
     * 💰 *Máximo Dinero:* 999.999 € en cartera + 1.000.000 € en banco.
     * 💿 *Pack de MTs:* 19 MTs comprables de Casino y Centro Comercial (Hiperrayo, Terremoto, Rayo, Lanzallamas, Rayo Hielo, Puños elementales, Pantallas, Climas, etc.).
   * Entradas personalizadas para fijar cualquier cantidad deseada.
   * Botón directo para lanzar el juego.

3. **💾 Copias de Seguridad Automáticas:**
   * Antes de aplicar cualquier cambio, crea automáticamente un respaldo sellado con marca de tiempo en la carpeta `backups/`.
   * Sincroniza simultáneamente `reloaded1.savc` y `reloaded1_bk.savc`.
   * Si alguna verificación matemática falla, revierte inmediatamente los cambios al estado original.

---

## 🚀 Cómo Usarlo en tu PC

### Requisitos
* Windows 10 u 11.
* [Python 3.10+](https://www.python.org/downloads/) instalado (asegúrate de marcar la casilla **"Add Python to PATH"** durante la instalación).

### Instalación
1. Descarga o clona este repositorio en tu ordenador:
   ```bash
   git clone https://github.com/<tu-usuario>/pokemon-reloaded-injector.git
   ```
2. Coloca los archivos del inyector en la carpeta raíz donde tengas instalado Pokémon Reloaded (junto a la carpeta `Proyecto Reloaded The Last Beta 1.9.2.2 Full`).
3. Haz doble clic en **`Abrir_Inyector.bat`**.
4. ¡Listo! La interfaz se abrirá automáticamente.

---

## 📂 Estructura del Repositorio

* `Abrir_Inyector.bat`: Lanzador de 1 clic para Windows (detecta automáticamente el ejecutable de Python).
* `gui_inyector.pyw`: Interfaz gráfica de usuario.
* `inyector_reloaded.py`: Motor central de inyección y recálculo de sumas criptográficas.
* `run_loader.py`: Deserializador del stream binario `.savc`.
* `.gitignore`: Filtro de exclusión para no subir partidas personales ni archivos pesados del juego.

---

## 📜 Licencia
Uso personal y educativo para la comunidad de Pokémon Reloaded. Todos los derechos del juego pertenecen a F3R y sus desarrolladores.

