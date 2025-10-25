import yaml
import os

class Config:
    def __init__(self, profile: str = None, path: str  = None):
        filename = path or os.getenv("VOCABAPP_PROFILESOURCE") or "config.yaml"
        
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        profile = profile or os.getenv("VOCABAPP_PROFILE") or "de_hu"

        if profile not in config.keys():
            raise ValueError(f'Unknown profile {profile}')

        self.profile = profile
        self.settings = config[profile]

    def __getitem__(self, key):
        return self.settings.get(key)

    def __repr__(self):
        return f"<Config profile={self.profile}>"

