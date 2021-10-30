# github 使用笔记

### 基本操作
`git branch --set-upstream-to=<remote branch> <local branch>`:本地分支与远程分支关联

`git remote add <name> <url/ssh>`:添加git远程仓库

`git remote remove <name>`:删除git远程仓库

`git branch -a`:查看所有分支（本地和远程）

### 合并分支
`git merge <branch>`:将分支合并到当前分支
### 删除分支
`git branch -D <branch>`:删除本地分支

`git push origin --delete <remote branch>`:删除远程分支
