import os

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".cpp",
    ".c",
    ".cs",
]


def load_code_files(repo_path: str):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        for filename in filenames:

            ext = os.path.splitext(filename)[1]

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:

                    content = f.read()

                    files.append(
                        {
                            "file_path": file_path,
                            "content": content,
                        }
                    )

            except Exception:
                continue

    return files