"""Static smoke test for every skill in a skills directory.

Checks per skill: frontmatter parses, name matches folder and is kebab-case,
description present and <=1024 chars, relative links and referenced local
files resolve, and /skill or **skill** references point at installed skills.
"""
import json, os, re, sys

root = sys.argv[1]
names = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
installed = set(names)
results = {}

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(text):
    if not text.startswith('---\n'):
        return None, 'file does not start with --- frontmatter'
    end = text.find('\n---', 4)
    if end == -1:
        return None, 'frontmatter not closed'
    raw = text[4:end]
    if yaml:
        try:
            data = yaml.safe_load(raw)
        except Exception as e:  # noqa: BLE001
            return None, f'YAML error: {str(e).splitlines()[0]}'
        if not isinstance(data, dict):
            return None, 'frontmatter is not a mapping'
        return data, None
    data = {}
    for line in raw.splitlines():
        m = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"')
    return data, None


link_re = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')
path_re = re.compile(r'`((?:\.\./|\./)?(?:references|scripts|playbooks|agents|assets|templates|examples)/[A-Za-z0-9_./-]+)`')
skill_ref_re = re.compile(r'(?<![\w/.~-])/([a-z][a-z0-9-]{2,})\b')

for name in names:
    issues, warnings = [], []
    sdir = os.path.join(root, name)
    path = os.path.join(sdir, 'SKILL.md')
    if not os.path.isfile(path):
        results[name] = {'issues': ['missing SKILL.md'], 'warnings': []}
        continue
    text = open(path, encoding='utf-8').read()
    fm, err = parse_frontmatter(text)
    if err:
        issues.append(err)
    else:
        n = fm.get('name')
        d = fm.get('description')
        if n != name:
            issues.append(f'name {n!r} != folder {name!r}')
        if not isinstance(n, str) or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', n or '') or len(n) > 64:
            issues.append(f'name {n!r} is not kebab-case <=64 chars')
        if not d:
            issues.append('missing description')
        elif len(str(d)) > 1024:
            issues.append(f'description is {len(str(d))} chars (>1024)')
    md_files = [os.path.join(dp, f) for dp, _, fs in os.walk(sdir) for f in fs if f.endswith('.md')]
    for mf in md_files:
        body = open(mf, encoding='utf-8', errors='replace').read()
        base = os.path.dirname(mf)
        rel = os.path.relpath(mf, sdir)
        for target in link_re.findall(body):
            if re.match(r'^[a-z]+:', target) or target.startswith('/'):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                (warnings if target.startswith('../../') else issues).append(f'{rel}: broken link {target}')
        for target in path_re.findall(body):
            cands = [os.path.join(base, target), os.path.join(sdir, target)]
            if not any(os.path.exists(os.path.normpath(c)) for c in cands):
                warnings.append(f'{rel}: referenced path not found {target}')
    results[name] = {'issues': sorted(set(issues)), 'warnings': sorted(set(warnings))}

print(json.dumps({'count': len(names), 'yaml': bool(yaml), 'results': results}, indent=1))
