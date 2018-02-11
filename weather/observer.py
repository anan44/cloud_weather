"""Contains Observer class and related functionalities"""


class Observer():
    """Observation point and related limits.
    init arguments:
    name - name of the location
    min_temp = lower temperature limit for alarms
    max_temp = higher temperature limit for alarms
    """
    def __init__(self, name, min_temp, max_temp):
        self.name = name
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.forecasts = None

    def __str__(self):
        return "%s: Min alert: %s, Max alert: %s" % (self.name, self.min_temp,
                                                     self.max_temp)
