import os
import glob

def summarize():
    with open("pages_summary.txt", "w", encoding="utf-8") as out:
        # Welcome file
        welcome_files = [f for f in os.listdir(".") if f.endswith("_Welcome.py")]
        if welcome_files:
            w_file = welcome_files[0]
            out.write(f"=== ENTRYPOINT: {w_file} ===\n")
            with open(w_file, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                out.write(f"Length: {len(content)} chars\n")
                lines = content.splitlines()
                out.write("First 40 lines:\n")
                out.write("\n".join(lines[:40]) + "\n\n")

        # Pages
        pages = sorted(os.listdir("pages"))
        for p in pages:
            if not p.endswith(".py"): continue
            p_path = os.path.join("pages", p)
            out.write(f"=== PAGE: {p} ===\n")
            with open(p_path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()
                out.write(f"Total lines: {len(lines)}\n")
                # find imports, functions, apis
                apis = [l.strip() for l in lines if "http" in l or "api" in l.lower() or "requests." in l]
                defs = [l.strip() for l in lines if l.strip().startswith("def ") or l.strip().startswith("class ")]
                st_titles = [l.strip() for l in lines if "st.title" in l or "st.header" in l or "st.subheader" in l]
                out.write(f"Defs: {defs[:10]}\n")
                out.write(f"Titles: {st_titles[:10]}\n")
                out.write(f"Sample APIs: {apis[:8]}\n\n")

summarize()
print("Done writing pages_summary.txt")
