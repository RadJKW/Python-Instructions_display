# %%
# Imports necessary packages and creates the Base Metadata classes.
from datetime import datetime
import random
from urllib.parse import quote_plus as url_quote
from click import echo
from sqlalchemy import (
    TEXT,
    Float,
    ForeignKey,
    SmallInteger,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    create_engine
)
from sqlalchemy.orm import declarative_base, Session, relationship


Base = declarative_base()


class Operators(Base):
    __tablename__ = "operators"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    session_start = Column(DateTime, nullable=True)
    session_end = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<Operators(name='%s', session_start='%s', session_end='%s')>" % (
            self.name,
            self.session_start,
            self.session_end,
        )


class Machines(Base):
    __tablename__ = "machines"
    id = Column(Integer, primary_key=True)
    division = Column(String(10))
    host_name = Column(String(20))
    host_ip = Column(String(15))
    host_type = Column(String(10))
    active = Column(Boolean)
    last_updated = Column(DateTime)

    def __repr__(self):
        return "<CoilWinderMachines(id='{}', division='{}', host_name='{}', host_id='{}', host_ip='{}', host_type='{}', active='{}', last_updated='{}')>".format(
            self.id,
            self.division,
            self.host_name,
            self.host_ip,
            self.host_type,
            self.active,
            self.last_updated,
        )


class CoilData(Base):
    __tablename__ = "coil_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    coil_number = Column(String(15))
    division = Column(SmallInteger)
    stop_code = Column(String(10))
    layer = Column(String(10))
    material = Column(String(10))
    width = Column(Float)
    rx_message = Column(String(50))
    web_url = Column(TEXT)
    date_time = Column(DateTime)
    warnings = Column(TEXT)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    machine = relationship("Machines", backref="coil_data")
    operator_id = Column(Integer, ForeignKey("operators.id"))
    operator = relationship("Operators", backref="coils")

    def __repr__(self):
        return "<CoilData(id='{}', coil_number='{}', division='{}', stop_code='{}', layer='{}', material='{}', width='{}', rx_message='{}', web_url='{}', date_time='{}', warnings='{}', machine_id='{}', operator_id='{}')>".format(
            self.id,
            self.coil_number,
            self.division,
            self.stop_code,
            self.layer,
            self.material,
            self.width,
            self.rx_message,
            self.web_url,
            self.date_time,
            self.warnings,
            self.machine_id,
            self.operator_id,
        )


# --------------------------------------------------------------------

# %%
# Connect to the database and create a session
mysql_engine = create_engine(
    "mysql+pymysql://radjkw:{}@localhost:3306/coil_winder".format(url_quote("P@$$w0rd"))
)

# %%
# ADDS THE MODELS TO THE DATABASE IF THEY DONT ALREADY EXIST

Base.metadata.create_all(mysql_engine)


# %%
with Session(mysql_engine) as session:
    # Create a new operator
    john_doe = Operators(
        id=10001,
        name="John Doe",
        session_start=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    jane_doe = Operators(
        id=20001,
        name="Jane Doe",
        session_start=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    session.add_all([john_doe, jane_doe])
    session.commit()

# %%
with Session(mysql_engine) as session:
    # Create a new machine
    coil_winder_1 = Machines(
        id="001",
        division=1,
        host_name="cw-001",
        host_ip="192.0.0.1",
        host_type="PC",
        active=True,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    session.add(coil_winder_1)
    session.commit()
# %%
random_coil_number = "0050" + str(random.randint(100000000, 999999999))

with Session(mysql_engine) as session:
    # generate a random coil number where total legth is 13 digits and the first 4 digita are 0050

    coil_data_1 = CoilData(
        coil_number=random_coil_number,
        division=1,
        stop_code="NC",
        rx_message="NC,{},1".format(random_coil_number),
        web_url="http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=NC",
        date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        machine_id="001",
        operator_id=10001,
    )

    session.add(coil_data_1)
    session.commit()

# %%
random_coil_number = "0050" + str(random.randint(100000000, 999999999))
with Session(mysql_engine) as session:
    coil_data_2 = CoilData(
        coil_number=random_coil_number,
        division=2,
        stop_code="NW",
        rx_message="NW,LV,SC,00.00410",
        web_url="http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=NC",
        date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        machine_id="001",
        operator_id=20001,
        layer="LV",
        material="SC",
        width=0.00410,
    )

    session.add(coil_data_2)
    session.commit()

# %%
with Session(mysql_engine) as session:
    # remove all coil data entries
    session.query(CoilData).delete()
    # drop the table coildata
    session.query(CoilData).delete()
    session.commit()

# %%

# get all coil data entries for the opeator with id 10001
with Session(mysql_engine) as session:
    view_operators_coils = (
        session.query(CoilData).filter(CoilData.operator_id == 10001).all()
    )
    session.commit()
    print(view_operators_coils)
    session.close()


