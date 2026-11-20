import argparse
import glob
import hashlib
import os
import shutil
import subprocess
import sys
import time

import inyector_reloaded

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVES_REPO_URL = "https://github.com/ProfeJuani/pokemon-reloated-saves.git"
CACHE_DIR = os.path.join(BASE_DIR, ".cloud_saves_cache")
PARTIDAS_DIR = os.path.join(inyector_reloaded.GAME_DIR, "data", "partidas")
BACKUP_DIR = inyector_reloaded.BACKUP_DIR


def _run_git(args, cwd):
    return subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def _sha256(path):
    if not os.path.exists(path):
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_saves_cache():
    if os.path.exists(os.path.join(CACHE_DIR, ".git")):
        r = _run_git(["pull", "--rebase", "origin", "main"], cwd=CACHE_DIR)
        if r.returncode != 0:
            _run_git(["fetch", "origin", "main"], cwd=CACHE_DIR)
            _run_git(["reset", "--hard", "origin/main"], cwd=CACHE_DIR)
        return True, "Caché de nube actualizado."
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
    r = _run_git(["clone", SAVES_REPO_URL, CACHE_DIR], cwd=BASE_DIR)
    if r.returncode != 0:
        return False, f"Error clonando nube de partidas: {(r.stderr or r.stdout).strip()}"
    return True, "Caché de nube inicializado."


def pull_injector():
    if not os.path.exists(os.path.join(BASE_DIR, ".git")):
        return False, "Esta carpeta no es un repositorio git."
    r = _run_git(["pull", "--ff-only", "origin", "main"], cwd=BASE_DIR)
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip()
    out = (r.stdout or "").strip()
    return True, out or "Inyector al día."


def pull_saves(force=False):
    ok, msg = ensure_saves_cache()
    if not ok:
        return False, msg

    cloud_files = glob.glob(os.path.join(CACHE_DIR, "reloaded*.*"))
    if not cloud_files:
        return False, "No se encontraron archivos reloaded*.* en la nube."

    cloud_savc = os.path.join(CACHE_DIR, "reloaded1.savc")
    local_savc = os.path.join(PARTIDAS_DIR, "reloaded1.savc")
    if not force and _sha256(cloud_savc) == _sha256(local_savc):
        return True, "Partida local ya coincide con la nube."

    os.makedirs(PARTIDAS_DIR, exist_ok=True)
    if os.path.exists(local_savc):
        ts = time.strftime("%Y%m%d_%H%M%S")
        b_dir = os.path.join(BACKUP_DIR, f"before_cloud_pull_{ts}")
        os.makedirs(b_dir, exist_ok=True)
        for lf in glob.glob(os.path.join(PARTIDAS_DIR, "reloaded*.*")):
            shutil.copy2(lf, os.path.join(b_dir, os.path.basename(lf)))

    for cf in cloud_files:
        shutil.copy2(cf, os.path.join(PARTIDAS_DIR, os.path.basename(cf)))

    v_ok, v_msg = inyector_reloaded.verify_save(local_savc)
    if not v_ok:
        return False, f"Partida descargada falló verificación: {v_msg}"
    return True, f"Partida descargada de GitHub y verificada ({v_msg})."


def push_saves(reason="Auto-sync partida"):
    local_savc = os.path.join(PARTIDAS_DIR, "reloaded1.savc")
    if not os.path.exists(local_savc):
        return False, "No existe reloaded1.savc local."

    v_ok, v_msg = inyector_reloaded.verify_save(local_savc)
    if not v_ok:
        return False, f"Cancelado: la partida local no pasó verify_save ({v_msg})."

    ok, msg = ensure_saves_cache()
    if not ok:
        return False, msg

    for lf in glob.glob(os.path.join(PARTIDAS_DIR, "reloaded*.*")):
        shutil.copy2(lf, os.path.join(CACHE_DIR, os.path.basename(lf)))

    _run_git(["add", "-A"], cwd=CACHE_DIR)
    diff = _run_git(["diff", "--cached", "--quiet"], cwd=CACHE_DIR)
    if diff.returncode == 0:
        return True, "Sin cambios nuevos en la partida (ya está al día en GitHub)."

    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    c = _run_git(["commit", "-m", f"{reason} ({ts})"], cwd=CACHE_DIR)
    if c.returncode != 0:
        return False, f"Error en commit: {(c.stderr or c.stdout).strip()}"

    p = _run_git(["push", "origin", "main"], cwd=CACHE_DIR)
    if p.returncode != 0:
        return False, f"Error en push: {(p.stderr or p.stdout).strip()}"

    return True, f"Partida verificada y subida a GitHub ({ts})."


def push_injector(reason="Auto-sync inyector"):
    if not os.path.exists(os.path.join(BASE_DIR, ".git")):
        return False, "Sin repositorio git del inyector."
    st = _run_git(["status", "--porcelain"], cwd=BASE_DIR)
    if not st.stdout.strip():
        return True, "Inyector sin cambios locales pendientes."
    _run_git(["add", "-A"], cwd=BASE_DIR)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    _run_git(["commit", "-m", f"{reason} ({ts})"], cwd=BASE_DIR)
    p = _run_git(["push", "origin", "main"], cwd=BASE_DIR)
    if p.returncode != 0:
        return False, (p.stderr or p.stdout).strip()
    return True, "Cambios del inyector subidos a GitHub."


def launch_and_sync_game():
    print("========================================================")
    print("  1/3 Sincronizando desde GitHub (Inyector + Partida)...")
    print("========================================================")
    ok_i, msg_i = pull_injector()
    print(f"[Inyector] {msg_i}")
    ok_s, msg_s = pull_saves(force=False)
    print(f"[Partida ] {msg_s}")

    exe_path = os.path.join(
        inyector_reloaded.GAME_DIR,
        "Proyecto Reloaded The Last Beta 1.9.2.2 Full.exe",
    )
    if not os.path.exists(exe_path):
        print(f"[ERROR] No se encontró el ejecutable en: {exe_path}")
        return 1

    print("\n========================================================")
    print("  2/3 Lanzando Pokémon Reloaded... (no cierres esta ventana)")
    print("========================================================")
    proc = subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
    proc.wait()

    print("\n========================================================")
    print("  3/3 Juego cerrado. Subiendo tu partida a GitHub...")
    print("========================================================")
    ok_p, msg_p = push_saves("Auto-sync tras jugar")
    print(f"[Nube] {'OK' if ok_p else 'ERROR'}: {msg_p}")
    return 0 if ok_p else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincronización automática con GitHub para Pokémon Reloaded")
    parser.add_argument("action", choices=["pull", "push", "pull-injector", "push-all", "play"], help="Acción a ejecutar")
    parser.add_argument("--force", action="store_true", help="Forzar sobrescritura local al hacer pull")
    args = parser.parse_args()

    if args.action == "pull":
        ok1, m1 = pull_injector()
        ok2, m2 = pull_saves(force=args.force)
        print(f"[Inyector] {m1}")
        print(f"[Partida ] {m2}")
        sys.exit(0 if ok2 else 1)
    elif args.action == "pull-injector":
        ok, m = pull_injector()
        print(m)
        sys.exit(0 if ok else 1)
    elif args.action == "push":
        ok, m = push_saves("Sync manual")
        print(m)
        sys.exit(0 if ok else 1)
    elif args.action == "push-all":
        ok1, m1 = push_injector("Auto-sync inyector")
        ok2, m2 = push_saves("Auto-sync partida")
        print(f"[Inyector] {m1}")
        print(f"[Partida ] {m2}")
        sys.exit(0 if (ok1 and ok2) else 1)
    elif args.action == "play":
        sys.exit(launch_and_sync_game())
