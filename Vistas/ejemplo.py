
# Agregar una relación a la clase User para las tarjetas
User.cards = relationship("Card", order_by=Card.card_number, back_populates="user")

# Configurar la conexión a la base de datos (aquí se utiliza una base de datos SQLite en memoria)
engine = create_engine('sqlite:///:memory:', echo=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo crear una nueva tarjeta y asociarla a un usuario
new_user = User(name='Juan')
session.add(new_user)
session.commit()

new_card = Card(card_number=1234567890123456, nip=1234, expiration_date='05/26', user=new_user, balance=1000)
session.add(new_card)
session.commit()

# Ejemplo de cómo consultar todas las tarjetas asociadas a un usuario
user_cards = session.query(User).filter_by(name='Juan').first().cards
for card in user_cards:
    print(f"Número de Tarjeta: {card.card_number}, NIP: {card.nip}, Fecha de Vencimiento: {card.expiration_date}, Saldo: {card.balance}")

# Cierra la sesión al finalizar
session.close()
