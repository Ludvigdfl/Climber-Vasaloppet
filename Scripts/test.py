TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("❌ GitHub TOKEN token not found. Make sure you're running this in GitHub Actions.")
    exit(1)

OPEN_AI_API = os.getenv("OPEN_AI_API")
if not OPEN_AI_API:
    print("❌ GitHub OPEN_AI_API token not found. Make sure you're running this in GitHub Actions.")
    exit(1)

