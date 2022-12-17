from prometheus_client.core import GaugeMetricFamily
import RPi.GPIO as GPIO


class Collector(object):
    def __init__(self, logger):
        self.logger = logger

    def collect(self):
        sensor = GaugeMetricFamily(
            'sensor',
            'Show sensor state',
        )

        self.logger.debug('================ Collect data ==================')

        m = self.getMetrics()
        if m is not None:
            sensor.add_metric(labels=[], value=m)
        else:
            self.logger.warn('Nothing to return...')

        yield sensor

        return

    def getMetrics(self):
        return GPIO.input(18)
