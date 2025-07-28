# src/core/models/address.py
from enum import StrEnum


class AddressingType(StrEnum):
    ANALOG_SIGNAL = "4-20mA or '%'"
    MODBUS_RTU_ADDRESS = "Modbus RTU Slave ID"
    IP_NETWORK = "IPv4 Network"
    IP_ADDRESS = "IPv4 Address"
    OPC_UA_ADDRESS = "OPC UA Address"
    MES_TAG_ADDRESS = "MES Tag Address"
    DNS_NAME = "DNS Name"
    SCADA_TAG_ADDRESS = "SCADA Tag Address"
    DATABASE_CONNECTION = "Database Connection String"
    HTTP_URL = "HTTP URL"
    EMAIL_ADDRESS = "Email Address"
