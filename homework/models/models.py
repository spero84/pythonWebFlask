from homework import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # content = db.Column(db.LargeBinary, nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def serialize(self):
        return {"id": self.id, "created": self.created, "name": self.name, "content": self.content}



