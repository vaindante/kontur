import environ

vault = environ.secrets.VaultEnvSecrets('TEST')


@environ.config(prefix="TEST")
class TestConfig:
    host = environ.var("https://api.github.com")
    user = environ.var("default_user")
    token = vault.secret()
    repos = environ.var()


cfg = environ.to_config(TestConfig)
