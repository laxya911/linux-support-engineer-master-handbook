import os
import subprocess
import shutil

repo_root = r"d:\LSEMH\linux-support-engineer-master-handbook"
volumes_dir = os.path.join(repo_root, "volumes")
samples_dir = os.path.join(repo_root, "samples")

if not os.path.exists(samples_dir):
    os.makedirs(samples_dir)

def build_full():
    print("Building full handbooks...")
    for vol_idx in range(1, 6):
        vol_str = f"volume0{vol_idx}"
        script_path = os.path.join(volumes_dir, vol_str, "scripts", f"build_vol{vol_idx}.py")
        if os.path.exists(script_path):
            print(f"Building {vol_str}...")
            subprocess.run(["python", script_path], cwd=repo_root, check=True)

def build_samples():
    print("Building sample handbooks...")
    for vol_idx in range(1, 6):
        vol_str = f"volume0{vol_idx}"
        script_path = os.path.join(volumes_dir, vol_str, "scripts", f"build_vol{vol_idx}.py")
        if not os.path.exists(script_path):
            continue
            
        print(f"Building sample for {vol_str}...")
        
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Change output file
        content = content.replace(f'handbooks", "Linux_Support_Engineer_Master_Handbook_Vol{vol_idx}.pdf"',
                                  f'samples", "Linux_Support_Engineer_Master_Handbook_Vol{vol_idx}_SAMPLE.pdf"')
                                  
        # Limit chapters logic
        chapter_logic = """    # Read chapters
    chapters = []
    for f in os.listdir(chapters_dir):
        if f.endswith('.md'):
            chapters.append(f)
    
    # Sort files properly
    chapters.sort()"""
    
        new_chapter_logic = """    # Read chapters
    chapters = []
    for f in os.listdir(chapters_dir):
        if f.endswith('.md'):
            chapters.append(f)
    
    # Sort files properly
    chapters.sort()
    
    # Limit to front matter + first two chapters for sample
    chapters = chapters[:3]"""
        
        content = content.replace(chapter_logic, new_chapter_logic)
        
        # Add watermark
        css_watermark = """
    body::after {
        content: "SAMPLE PREVIEW - NOT FOR RESALE";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 40pt;
        color: rgba(150, 150, 150, 0.4);
        z-index: 9999;
        pointer-events: none;
        white-space: nowrap;
    }
</style>"""
        content = content.replace("</style>", css_watermark, 1)
        
        # Write temporary script
        temp_script_path = os.path.join(volumes_dir, vol_str, "scripts", f"build_vol{vol_idx}_sample.py")
        with open(temp_script_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Run temporary script
        try:
            subprocess.run(["python", temp_script_path], cwd=repo_root, check=True)
        finally:
            os.remove(temp_script_path)

if __name__ == "__main__":
    build_full()
    build_samples()
    print("All builds completed successfully!")
