"""Test New Entity Sensor"""

import unittest

import responses
from st2tests.mocks import sensor

from serviceflow_st2.sensors import new_entity_sensor

TEST_SERVER = 'http://localhost.com/entities'
TEST_SERVER_RESPONSE = [
    {"entity_id": "1"},
    {"entity_id": "2"},
    {"entity_id": "3"},
    {"entity_id": "4"},
]
ENTITY_PREFIX = "entity_"


class CustomNewEntitySensor(new_entity_sensor.NewEntitySensor):
    """Custom Sensor implementing NewEntitySensor"""

    def __init__(self, sensor_service):
        super().__init__(sensor_service, wrapper_api=TEST_SERVER)

    def setup(self):
        pass

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def poll_new_entity(self, new_entities):
        pass


class TestNewEntity(unittest.TestCase):
    """Test New Entity"""

    def setUp(self):
        sensor_wrapper = sensor.MockSensorWrapper(pack='tests', class_name=CustomNewEntitySensor.__name__)
        self.sensor_service = sensor.MockSensorService(sensor_wrapper=sensor_wrapper)
        self.test_sensor = CustomNewEntitySensor(self.sensor_service)
        responses.add(responses.GET, TEST_SERVER, json=TEST_SERVER_RESPONSE, status=200)

    @responses.activate
    def test_entities_are_added_to_store(self):
        self.test_sensor.poll()
        self.assertEqual(len(self.test_sensor.get_all_entities()), 4)

    @responses.activate
    def test_if_existing_entities_are_already_seen_dont_add_them_to_new_entities(self):
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "1", {"seen": True, "entity_id": "1"})
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "2", {"seen": True, "entity_id": "2"})
        self.test_sensor.poll()
        self.assertEqual(len(self.test_sensor.get_all_entities()), 2)

    @responses.activate
    def test_if_existing_entities_are_not_seen_add_them_to_new_entities(self):
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "1", {"seen": True, "entity_id": "1"})
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "2", {"seen": False, "entity_id": "2"})
        self.test_sensor.poll()
        self.assertEqual(len(self.test_sensor.get_all_entities()), 3)

    @responses.activate
    def test_if_entity_is_marked_seen_dont_add_them_to_new_entities(self):
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "1", {"seen": True, "entity_id": "1"})
        self.test_sensor.sensor_service.set_value(ENTITY_PREFIX + "2", {"seen": False, "entity_id": "2"})
        self.test_sensor.mark_entity_as_seen("2")
        self.test_sensor.poll()
        self.assertEqual(len(self.test_sensor.get_all_entities()), 2)
