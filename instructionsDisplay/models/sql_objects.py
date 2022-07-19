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
    
)
from sqlalchemy.orm import declarative_base, relationship

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
