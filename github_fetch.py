from github import Github, Auth
from langchain_core.documents import Document

def get_github_docs(token: str):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    documents = []

    SKIP_EXTENSIONS = (
        ".png", ".jpg", ".jpeg", ".svg", ".ico",
        ".woff", ".ttf", ".eot", ".gif", ".webp",
        ".pyc", ".min.js", ".lock"
    )
    SKIP_FILES = {"package-lock.json", "yarn.lock", "poetry.lock"}

    for repo in user.get_repos():
        if repo.fork:
            continue

        print(f"Processing: {repo.name}")

        # Summary
        documents.append(Document(
            page_content=f"{repo.name}: {repo.description or 'No description'}",
            metadata={
                "source": "summary",
                "repo": repo.name,
                "language": repo.language or "unknown",
                "url": repo.html_url,
            }
        ))

        # README
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode("utf-8")
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "readme",
                    "repo": repo.name,
                    "language": repo.language or "unknown",
                    "url": repo.html_url,
                }
            ))
        except Exception:
            pass

        # Code files
        try:
            stack = list(repo.get_contents(""))
            while stack:
                item = stack.pop()
                if item.type == "dir":
                    stack.extend(repo.get_contents(item.path))
                elif (
                    item.name not in SKIP_FILES
                    and not any(item.name.endswith(ext) for ext in SKIP_EXTENSIONS)
                    and item.size < 50_000
                    and item.decoded_content is not None
                ):
                    code = item.decoded_content.decode("utf-8", errors="ignore")
                    documents.append(Document(
                        page_content=code,
                        metadata={
                            "source": "code",
                            "repo": repo.name,
                            "file": item.path,
                            "language": repo.language or "unknown",
                            "url": item.html_url,
                        }
                    ))
        except Exception as e:
            print(f"  Skipped code in {repo.name}: {e}")

    return documents