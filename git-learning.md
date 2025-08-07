# 📘 Git & GitHub Learning Notes

## 🔹 What is Git?
> Git is a **version control system** that helps you track changes in your code and collaborate with others.

- It stores **snapshots of your code** as commits.
- You can **go back in time**, compare versions, or create branches for features.

## 🔹 What is GitHub?
> GitHub is a **cloud platform** that hosts your Git repositories online.

- Share your code with others
- Collaborate on projects using branches, pull requests, issues, etc.

---

## ✨ Basic Git Commands

| Command                  | Description                                 |
|--------------------------|---------------------------------------------|
| `git init`              | Initialize a Git repository                 |
| `git add .`             | Stage all changed and new files             |
| `git commit -m "msg"`   | Save a snapshot of changes with a message   |
| `git status`            | Show status of tracked/untracked files      |
| `git log --oneline`     | View commit history (short format)          |
| `git branch`            | Show branches                               |
| `git checkout -b name`  | Create and switch to a new branch           |
| `git push origin main`  | Push local commits to GitHub (main branch)  |
| `git pull`              | Get the latest changes from GitHub          |

---

## 🌐 GitHub Flow (Simple)

1. `git init` — create repo  
2. `git add .` — stage files  
3. `git commit -m "Initial commit"` — commit  
4. Create repo on GitHub  
5. `git remote add origin <url>` — link remote  
6. `git push -u origin main` — push to GitHub  
