import rom


class Player(rom.Model):
    row = rom.Integer(index=True)
    column = rom.Integer(index=True)
    tasks = rom.Json()

    def to_json(self, include_tasks=True):
        json = {
            "row": self.row,
            "column": self.column
        }

        if include_tasks:
            json.update({'tasks': self.tasks})

        return json
