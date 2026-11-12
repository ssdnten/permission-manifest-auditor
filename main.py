"""Review an exported POSIX mode manifest for world-writable files, special permission bits and exposed private files."""
import argparse
import json
from pathlib import Path,PurePosixPath
import re

def audit(entries):
    findings=[]
    seen=set()
    for entry in entries:
        name=entry['path']
        if not isinstance(name,str) or not name or name in seen:
            raise ValueError('paths must be nonempty and unique')
        seen.add(name)
        mode_text=entry['mode']
        if not isinstance(mode_text,str) or not re.fullmatch('[0-7]{3,4}',mode_text):
            raise ValueError('mode must contain 3 or 4 octal digits')
        mode=int(mode_text,8)
        kind=entry['kind']
        if kind not in {'file','directory'}:
            raise ValueError('kind must be file or directory')
        reasons=[]
        if mode & 0o002:
            if kind=='directory' and mode & 0o1000:
                reasons.append('world_writable_sticky_directory_review')
            else:
                reasons.append('world_writable')
        if mode & 0o4000: reasons.append('setuid')
        if mode & 0o2000: reasons.append('setgid_review')
        base=PurePosixPath(name).name.lower()
        sensitive=base in {'.env','id_rsa','id_ed25519'} or base.endswith('.key')
        if kind=='file' and sensitive and mode & 0o077:
            reasons.append('private_file_accessible_to_group_or_others')
        if reasons: findings.append(dict(path=name,mode=mode_text,reasons=reasons))
    return findings

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps(audit(json.loads(args.input.read_text(encoding='utf-8'))),indent=2))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        parser.exit(2,f'error: {exc}\n')

if __name__=='__main__': main()
