from enum import Enum, unique


@unique
class ScreenState(Enum):
    UNKNOWN = -1
    OFF = 0
    ON = 1
    USER_PRESENT = 2

    def is_on(self):
        return self == ScreenState.ON or self == ScreenState.USER_PRESENT

    def is_off(self):
        return self == ScreenState.OFF


@unique
class ScreenOrientation(Enum):
    UNKNOWN = -1
    ZERO = 0
    NINETY = 90
    ONE_EIGHTY = 180
    TWO_SEVENTY = 270

    def is_portrait(self):
        return self == ScreenOrientation.ZERO or self == ScreenOrientation.ONE_EIGHTY

    def is_landscape(self):
        return self == ScreenOrientation.NINETY or self == ScreenOrientation.TWO_SEVENTY


@unique
class PhoneState(Enum):
    UNKNOWN = -1
    IDLE = 0
    OFF_HOOK = 1
    RINGING = 2


@unique
class HeadsetState(Enum):
    UNKNOWN = -1
    UNPLUGGED = 0
    PLUGGED = 1

    def is_plugged(self):
        return self == HeadsetState.PLUGGED

    def is_unplugged(self):
        return self == HeadsetState.UNPLUGGED


@unique
class DockState(Enum):
    UNKNOWN = -1
    UNDOCKED = 0
    CAR = 1
    DESK = 2
    HE_DESK = 3
    LE_DESK = 4

    def is_undocked(self):
        return self == DockState.UNDOCKED


@unique
class NetworkType(Enum):
    UNKNOWN = -1
    MOBILE = 0
    ETHERNET = 1
    WIFI = 2
    BLUETOOTH = 3
    WIMAX = 4


@unique
class NetworkConnectionState(Enum):
    UNKNOWN = -1
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


class NetworkState:
    def __init__(self):
        self.type = NetworkType.UNKNOWN
        self.connection_state = NetworkConnectionState.UNKNOWN


@unique
class BatteryStatus(Enum):
    UNKNOWN = -1
    DISCHARGING = 0
    NOT_CHARGING = 1
    CHARGING = 2
    FULL = 3


@unique
class BatteryPlugState(Enum):
    NONE = 0
    AC = 1
    USB = 2
    WIRELESS = 3


@unique
class BatteryEnergyState(Enum):
    UNKNOWN = -1
    LOW = 0
    OKAY = 1


class BatteryState:
    def __init__(self):
        self.level = None
        self.temp = None
        self.status = BatteryStatus.UNKNOWN
        self.plug_state = BatteryPlugState.NONE
        self.energy_state = BatteryEnergyState.UNKNOWN


@unique
class StorageState(Enum):
    UNKNOWN = -1
    LOW = 0
    OKAY = 1


class DeviceState:
    def __init__(self):
        self.current_time = None
        self.screen_state = ScreenState.UNKNOWN
        self.screen_orientation = ScreenOrientation.UNKNOWN
        self.phone_state = PhoneState.UNKNOWN
        self.headset_state = HeadsetState.UNKNOWN
        self.dock_state = DockState.UNKNOWN
        self.network_state = NetworkState()
        self.battery_state = BatteryState()
