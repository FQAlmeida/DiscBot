class Achievements:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.requirements = ""

    def __str__(self):
        return f"""
{self.id}
{self.name}
{self.description}
{self.requirements}
"""
