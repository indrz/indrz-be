from .importer import list_changed_files, import_firsttime
from .georef import apply_georef
from .config import RAW_PREFIX

def run_cycle():
    changed_files = list_changed_files()
    if changed_files:
        print(f"Changed files: {changed_files}")
        for fname in changed_files:
            base = fname.stem.lower()
            import_firsttime(fname)
            apply_georef(base)
    else:
        print("No changes detected in DXF files.")

# def main():
#     while True:
#         run_cycle()
#         # sleep until next day at 23:00 handled by cron, so here just exit
#         break

if __name__ == "__main__":
    # main()
    run_cycle()
