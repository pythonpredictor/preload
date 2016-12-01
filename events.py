from enum import Enum, unique
import json
import dateutil.parser
import device


@unique
class EventType(Enum):
    """ Enumeration of different simulator events

    Enumeration of the list of events that can occur
    during simulation. This list is a mixture of events
    that are generated by the trace file, a set of events
    used to model the system, and a set of events used by
    the simulator.

    Each event type is represented by a string. A hierarchy
    of events is described by using the "." character. For
    example, "event_a.sub_event_b" represents the event
    "sub_event_b" that falls under the scope of events
    "event_a". This is done so that simulator modules can
    choose to filter events specifically, aka on sub_event_b",
    or generally, such as for any event of type "event_a".
    """
    PSEUDO = 'pseudo'
    # Trace File Events
    APP_LAUNCH = 'app.launch'
    APP_ACTIVITY_USAGE = 'app.activity_usage'
    SCREEN = 'screen'
    SCREEN_ORIENTATION = 'screen_orientation'
    PHONE = 'phone'
    PACKAGE = 'package'

    # Notification events
    NOTIFICATION = 'notification'

    # Network Events
    NETWORK = 'network'
    NETWORK_TYPE = 'network.type'
    NETWORK_STATUS = 'network.status'

    # Battery Events
    BATTERY = 'battery'
    BATTERY_LEVEL = 'battery.level'
    BATTERY_TEMPERATURE = 'battery.temperature'
    BATTERY_STATUS = 'battery.status'
    BATTERY_PLUG_STATE = 'battery.plug_status'
    BATTERY_ENERGY_STATE = 'battery.energy_state'

    DEVICE_STORAGE = 'storage'
    HEADSET = 'headset'
    DOCK = 'dock'
    BLUETOOTH = 'bluetooth'

    SYSTEM_MEMORY_SNAPSHOT = 'system.memory_snapshot'

    PRELOAD_APP = 'preload_app'

    # Simulator Events
    SIM = 'sim'
    DEBUG = 'sim.debug'


class Event:
    """ Base event class

    Describes the minimal implementation of a simulator event.

    This event should rarely be instantiated directly. Instead,
    most Events should be created as a subclass of this event, in
    order to hold any other information that may describe the event.

    Attributes:
        timestamp (:obj'datetime'): Time when event occurs
        event_type (:obj:'EventType'): Type of event

    """

    def __init__(self, timestamp, event_type):
        self.timestamp = timestamp
        self.event_type = event_type
        self.source = None
        self.destination = None

    def __repr__(self, *args, **kwargs):
        return '[%s] %s' % (self.timestamp, self.event_type.value)


class AppLaunchEvent(Event):
    """ Represents application launch event

    The event that describes the launch of an application
    on the device.

    Attributes:
        app_id (str): Unique id representing launched application
    """
    def __init__(self, timestamp, app_id):
        Event.__init__(self, event_type=EventType.APP_LAUNCH, timestamp=timestamp)
        self.app_id = app_id

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % (Event.__repr__(self, args, kwargs), self.app_id)


class AppActivityUsageEvent(Event):
    """ Represent an application's activity usage event

    The event that describes an application usage event. This event
    correlates to Android's UsageEvents.Event class that is logged
    from the UsageLogger application.

    Attributes:
        app_id (str): Unique id representing launched application
        source_class (str): Name of applications activity
        usage_event (:obj:'AppActivityUsageEvent':'UsageEvent'):
            Type of usage event
    """

    @unique
    class UsageEvent(Enum):
        """ Different usage type events

        Enumeration of different usage events. Correlated to constants
        defined in Android's UsageEvents.Event class.
        """
        MOVE_BACKGROUND = 0
        MOVE_FOREGROUND = 1

    def __init__(self, timestamp, app_id, source_class, usage_event):
        Event.__init__(self, event_type=EventType.APP_ACTIVITY_USAGE, timestamp=timestamp)
        self.app_id = app_id
        self.source_class = source_class
        self.usage_event = usage_event

    def __repr__(self, *args, **kwargs):
        return '%s: %s - %s %s' % \
               (Event.__repr__(self, args, kwargs),
                self.app_id, self.source_class,
                self.usage_event.name)


class ScreenEvent(Event):
    """ Represents screen usage event

    Represents user interactions with the device that
    can have an effect on the screen. Specifically,
    describes if screen turned on, screen turned off, or
    screen unlocked.

    Attributes:
        state (:obj:'ScreenState'): New state of the screen
    """

    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.SCREEN, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class ScreenOrientationEvent(Event):
    """ Represents screen orientation event

    Represents a change in screen orientation.

    Attributes:
        state (:obj:'ScreenState'): New orientation of the screen
    """

    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.SCREEN_ORIENTATION, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class PhoneEvent(Event):
    """ Represents phone call event

    Represents events related to phone calls

    Attributes:
        state (:obj:'PhoneState'): New state of phone call
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.PHONE, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class PackageEvent(Event):
    """ Represents application/package management event

    Represents events related to application/package managment,
    such as installation, update, etc.

    Attributes:
        management_event (:obj:'PackageEvent':'PackageManagementEvent'):
            Type of package management event that has occurred
    """

    @unique
    class PackageManagementEvent(Enum):
        """ Possible package management events"""
        INSTALLED = 0
        UNINSTALLED = 1
        UPDATED = 2
        REPLACED = 3

    def __init__(self, timestamp, package_event, package=None):
        Event.__init__(self, event_type=EventType.PACKAGE, timestamp=timestamp)
        self.management_event = package_event
        self.app_id = package

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.management_event.name)


class NotificationEvent(Event):
    """ Represents events related to device notifications

    Attributes:
        action (:obj:'NotificationEvent':'NotificationAction'):
            The notification action that has occurred
        app_id (str): The unique id for the application responsible for
            the notification
        notification_id (str): The id of the notification
        tag (str): The tag of the notification
    """

    @unique
    class NotificationAction(Enum):
        """ Possible actions related to notifications

        Different actions that may occur with device notifications
        """
        POSTED = 1
        REMOVED = 0

    def __init__(self, timestamp, action, app_id, notification_id, tag):
        Event.__init__(self, event_type=EventType.NOTIFICATION, timestamp=timestamp)
        self.action = action
        self.app_id = app_id
        self.notification_id = notification_id
        self.tag = tag

    def __repr__(self, *args, **kwargs):
        return '%s: %s - %s' % \
               (Event.__repr__(self, args, kwargs), self.action.name, self.app_id)


class NetworkEvent(Event):
    def __init__(self, timestamp):
        Event.__init__(self, event_type=EventType.NETWORK, timestamp=timestamp)


class NetworkStatusEvent(Event):
    """ Represents network status events

    Represents events related to the current device's
    network connection state.

    Attributes:
        state (:obj:'NetworkConnectionState'):  Network connection state
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.NETWORK_STATUS, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class NetworkTypeEvent(Event):
    """ Represents network type events

    Represents events related to the type of network
    a device is connected to.

    Attributes:
        network_type (:obj:'NetworkType'): A type of network
    """
    def __init__(self, timestamp, network_type):
        Event.__init__(self, event_type=EventType.NETWORK_TYPE, timestamp=timestamp)
        self.network_type = network_type

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.network_type.name)


class BatteryEvent(Event):
    def __init__(self, timestamp):
        Event.__init__(self, event_type=EventType.BATTERY, timestamp=timestamp)


class BatteryEnergyEvent(Event):
    """ Represents battery energy level events

    Represents events related to the current device's
    battery energy level.

    Attributes:
        state (:obj:'BatteryEnergyState'): State of battery energy level
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.BATTERY_ENERGY_STATE, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class BatteryStatusEvent(Event):
    """ Represents battery status events

    Represents events related to the current device's
    battery status.

    Attributes:
        status (:obj:'BatteryStatus'): Battery status
    """
    def __init__(self, timestamp, status):
        Event.__init__(self, event_type=EventType.BATTERY_STATUS, timestamp=timestamp)
        self.status = status

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.status.name)


class BatteryPlugStateEvent(Event):
    """ Represents battery plug events

    Represents events related to the current device's
    battery plug state.

    Attributes:
        state (:obj:'BatteryPlugState'): State of battery energy level
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.BATTERY_PLUG_STATE, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class BatteryLevelEvent(Event):
    """ Represents battery level value events

    Represents events related to updating the current
    battery energy level

    Attributes:
        level (int): Battery level value
    """
    def __init__(self, timestamp, level):
        Event.__init__(self, event_type=EventType.BATTERY_LEVEL, timestamp=timestamp)
        self.level = level

    def __repr__(self, *args, **kwargs):
        return '%s: %d' % \
               (Event.__repr__(self, args, kwargs), self.level)


class BatteryTempEvent(Event):
    """ Represents battery temperate value events

    Represents events related to updating the current
    battery temperature level

    Attributes:
        temperature (int): Battery temperature value
    """
    def __init__(self, timestamp, temperature):
        Event.__init__(self, event_type=EventType.BATTERY_TEMPERATURE, timestamp=timestamp)
        self.temperature = temperature

    def __repr__(self, *args, **kwargs):
        return '%s: %d' % \
               (Event.__repr__(self, args, kwargs), self.temperature)


class DeviceStorageEvent(Event):
    """ Represents storage level events

    Represents events related to the current device
    free storage level

    Attributes:
        state (:obj:'StorageState'): State of device storage
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.DEVICE_STORAGE, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class HeadsetEvent(Event):
    """ Represents headset plugged/unplugged events

    Represents events related to a headset being plugged into
    a device or unplugged from a device

    Attributes:
        state (:obj:'HeadsetState'): New state of headset
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.HEADSET, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class DockEvent(Event):
    """ Represents dock type events

    Represents events related to the device being docked into
    another system, such as a car

    Attributes:
        state (:obj:'DockState'): Docking state of device
    """
    def __init__(self, timestamp, state):
        Event.__init__(self, event_type=EventType.DOCK, timestamp=timestamp)
        self.state = state

    def __repr__(self, *args, **kwargs):
        return '%s: %s' % \
               (Event.__repr__(self, args, kwargs), self.state.name)


class BluetoothEvent(Event):
    """ Represents connection/disconnections of bluetooth devices

    Represents events related to where a bluetooth connection or
    disconnection is made with the device.

    Attributes:
        connection_event (:obj:'BluetoothEvent':'ConnectionEvent'):
            Whether device being connected or disconnected

    """
    @unique
    class ConnectionEvent(Enum):
        """ Enumeration of possible connection events

        List of possible connection events that can occur during
        a bluetooth event
        """
        DISCONNECTED = 0
        CONNECTED = 1

    def __init__(self, timestamp, connection_event):
        Event.__init__(self, event_type=EventType.BLUETOOTH, timestamp=timestamp)
        self.connection_event = connection_event


class SystemMemorySnapshot(Event):
    def __init__(self, timestamp):
        Event.__init__(self, event_type=EventType.SYSTEM_MEMORY_SNAPSHOT, timestamp=timestamp)


class EventJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AppActivityUsageEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'app_id': obj.app_id,
                    'source_class': obj.source_class,
                    'usage_event': obj.usage_event.value}
        elif isinstance(obj, ScreenEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, ScreenOrientationEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, PhoneEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, NotificationEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'action': obj.action.value,
                    'app_id': obj.app_id,
                    'notification_id': obj.notification_id,
                    'tag': obj.tag}
        elif isinstance(obj, NetworkStatusEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, NetworkTypeEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'network_type': obj.network_type.value}
        elif isinstance(obj, BatteryEnergyEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, BatteryStatusEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.status.value}
        elif isinstance(obj, BatteryPlugStateEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, BatteryLevelEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'level': obj.level}
        elif isinstance(obj, BatteryTempEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'temperature': obj.temperature}
        elif isinstance(obj, DeviceStorageEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, HeadsetEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'state': obj.state.value}
        elif isinstance(obj, BluetoothEvent):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value,
                    'connection_event': obj.connection_event.value}
        elif isinstance(obj, SystemMemorySnapshot):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value}
        elif isinstance(obj, Event):
            return {'timestamp': obj.timestamp.isoformat(),
                    'event_type': obj.event_type.value}
        else:
            return json.JSONEncoder.default(self, obj)


def json_decode_event(obj):
    if 'event_type' in obj:
        event_type = EventType(obj['event_type'])
        timestamp = dateutil.parser.parse(obj['timestamp'])
        if event_type == EventType.PSEUDO:
            return Event(timestamp=timestamp, event_type=EventType.PSEUDO)
        elif event_type == EventType.APP_ACTIVITY_USAGE:
            return AppActivityUsageEvent(timestamp=timestamp,
                                         app_id=obj['app_id'],
                                         source_class=obj['source_class'],
                                         usage_event=AppActivityUsageEvent.UsageEvent(obj['usage_event']))
        elif event_type == EventType.SCREEN:
            return ScreenEvent(timestamp=timestamp, state=device.ScreenState(obj['state']))
        elif event_type == EventType.SCREEN_ORIENTATION:
            return ScreenOrientationEvent(timestamp=timestamp, state=device.ScreenOrientation(obj['state']))
        elif event_type == EventType.PHONE:
            return PhoneEvent(timestamp=timestamp, state=device.PhoneState(obj['state']))
        elif event_type == EventType.NOTIFICATION:
            return NotificationEvent(timestamp=timestamp,
                                     action=NotificationEvent.NotificationAction(obj['action']),
                                     app_id=obj['app_id'],
                                     notification_id=obj['notification_id'],
                                     tag=obj['tag'])
        elif event_type == EventType.NETWORK_STATUS:
            return NetworkStatusEvent(timestamp=timestamp,
                                      state=device.NetworkConnectionState(obj['state']))
        elif event_type == EventType.NETWORK_TYPE:
            return NetworkTypeEvent(timestamp=timestamp,
                                    network_type=device.NetworkType(obj['network_type']))
        elif event_type == EventType.BATTERY_ENERGY_STATE:
            return BatteryEnergyEvent(timestamp=timestamp,
                                      state=device.BatteryEnergyState(obj['state']))
        elif event_type == EventType.BATTERY_STATUS:
            return BatteryStatusEvent(timestamp=timestamp,
                                      status=device.BatteryStatus(obj['state']))
        elif event_type == EventType.BATTERY_PLUG_STATE:
            return BatteryPlugStateEvent(timestamp=timestamp,
                                         state=device.BatteryPlugState(obj['state']))
        elif event_type == EventType.BATTERY_LEVEL:
            return BatteryLevelEvent(timestamp=timestamp, level=obj['level'])
        elif event_type == EventType.BATTERY_TEMPERATURE:
            return BatteryTempEvent(timestamp=timestamp, temperature=obj['temperature'])
        elif event_type == EventType.DEVICE_STORAGE:
            return DeviceStorageEvent(timestamp=timestamp, state=device.StorageState(obj['state']))
        elif event_type == EventType.HEADSET:
            return HeadsetEvent(timestamp=timestamp, state=device.HeadsetState(obj['state']))
        elif event_type == EventType.BLUETOOTH:
            return BluetoothEvent(timestamp=timestamp,
                                  connection_event=BluetoothEvent.ConnectionEvent(obj['connection_event']))
        elif event_type == EventType.SYSTEM_MEMORY_SNAPSHOT:
            return SystemMemorySnapshot(timestamp=timestamp)
