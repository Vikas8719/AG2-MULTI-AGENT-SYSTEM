"""Git operations service"""
import git
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GitService:
    def __init__(self, config):
        self.config = config
        self.github_token = config.github.github_token
        self.username = config.github.github_username
    
    def init_repo(self, project_path: Path):
        repo = git.Repo.init(project_path)
        logger.info(f"Initialized git repo at {project_path}")
        return repo
    
    def create_remote_repo(self, repo_name: str):
        # Use PyGithub to create remote repository
        logger.info(f"Creating remote repo: {repo_name}")
        return f"https://github.com/{self.username}/{repo_name}"
    
    def push_to_remote(self, repo, remote_url: str):
        origin = repo.create_remote('origin', remote_url)
        repo.index.add('*')
        repo.index.commit('Initial commit by AG2 Multi-Agent System')
        origin.push('main')
        logger.info("Pushed to remote repository")
