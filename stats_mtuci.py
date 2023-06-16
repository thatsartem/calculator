import models
from database import SessionLocal

stats = []
with open('universities/MTUCI/mtuci_stats.csv','r') as f:
    for l in f.readlines():
        stats.append(l.strip().split(','))

with SessionLocal() as session:
    for stat in stats:
        directions = session.query(models.Directions).filter(
            models.Directions.code.like(stat[0]),
            models.Directions.university.like('Московский Технический Университет Связи и Информатики'),
            models.Directions.form.like(stat[1])).all()
        for direction in directions:
            direction.mean, direction.dispersion = stat[3],stat[2]
    session.commit()

print('insertion complete')