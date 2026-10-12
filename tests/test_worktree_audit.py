import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/poteto-mode/scripts/worktree-audit.sh'

class WorktreeAuditTests(unittest.TestCase):
    def test_closed_unmerged_unpushed_and_space_paths(self):
        with tempfile.TemporaryDirectory(prefix='audit fixture ') as directory:
            root = Path(directory)
            repo = root / 'main repo'
            def git(*args, cwd=repo):
                return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()
            repo.mkdir()
            git('init', '-b', 'main')
            git('config', 'user.email', 'test@example.test')
            git('config', 'user.name', 'Test')
            (repo / 'base').write_text('base')
            git('add', 'base'); git('commit', '-m', 'base')
            git('update-ref', 'refs/remotes/origin/main', 'HEAD')
            paths={}
            for branch in ['closed', 'merged', 'unpushed', 'ancestor', 'recent']:
                wt=root / (branch+' worktree');paths[branch]=wt
                git('worktree', 'add', '-b', branch, str(wt))
                if branch!='ancestor':
                    (wt/'change').write_text(branch)
                    git('add', 'change',cwd=wt);git('commit','-m',branch,cwd=wt)
                if branch!='unpushed':git('update-ref','refs/remotes/origin/'+branch,git('rev-parse','HEAD',cwd=wt))
            git('update-ref','refs/remotes/origin/unpushed',git('rev-parse','main'))
            commands=root/'bin';commands.mkdir()
            (commands/'gh').write_text('#!/bin/sh\ncat <<END\n[{"number":1,"state":"CLOSED","headRefName":"closed"},{"number":2,"state":"MERGED","headRefName":"merged"},{"number":3,"state":"MERGED","headRefName":"unpushed"}]\nEND\n')
            (commands/'gh').chmod(0o755)
            home=root/'home';transcripts=home/'.cursor/projects'/str(repo).lstrip('/').replace('/','-')/'agent-transcripts';transcripts.mkdir(parents=True)
            (transcripts/'recent chat.txt').write_text('"'+str(paths['recent'])+'/file"')
            env={**os.environ,'HOME':str(home),'PATH':str(commands)+':'+os.environ['PATH']}
            result=subprocess.run(['bash',str(SCRIPT),str(repo)],env=env,text=True,capture_output=True,check=True)
            rows={line.split('\t')[-1]:line.split('\t') for line in result.stdout.splitlines()[1:]}
            for branch,bucket in [('closed','review'),('merged','safe'),('unpushed','hold-unpushed'),('ancestor','safe'),('recent','verify-recent-chat')]:
                self.assertEqual(rows[str(paths[branch])][-2],bucket,result.stdout)
            self.assertRegex(rows[str(paths['recent'])][-3],r'^\d{4}-\d{2}-\d{2}$')

if __name__ == '__main__':unittest.main()
