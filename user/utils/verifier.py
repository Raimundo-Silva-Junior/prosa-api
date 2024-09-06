from dataclasses import dataclass, field

@dataclass
class Verifier:
    
    errors: str = field(default_factory=dict)
    
    def add(self, name: str, message: str):
        self.errors.update(
            {
                name: [message]
            }
        )