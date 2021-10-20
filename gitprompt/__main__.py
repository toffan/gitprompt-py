from . import GitPrompt, Config


if __name__ == "__main__":
    config = Config.from_env()
    print(GitPrompt(config).run())
