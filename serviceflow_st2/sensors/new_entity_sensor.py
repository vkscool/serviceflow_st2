"""New Entity Sensor"""
import abc
import json
from typing import Optional, List

import requests
import requests.exceptions as exceptions
from st2reactor.container.sensor_wrapper import SensorService
from st2reactor.sensor import base

from serviceflow_st2.utils import sf_exceptions

SEEN = "seen"
ENTITY_ID = "entity_id"


class NewEntitySensor(base.PollingSensor):
    """New Entity Sensor

    This sensor keeps polling the data from specified source at a
    given polling period and returns only the entity which are new
    compared to the last poll.
    """

    ENTITY_PREFIX = "entity_"
    """
    ENTITY_PREFIX is prefixed to the id of the entity when storing in the Sensor DB
    By default, all entities are stored in local scope (per sensor) hence in
    most cases you will not have to modify its value.
    """

    def __init__(
        self,
        sensor_service: SensorService,
        config: Optional[dict] = None,
        poll_interval: int = 5,
        wrapper_api: str = None,
        ttl: int = 0,
    ):
        """
        This sensor keeps polling the data from specified source at a
        given polling period and returns only the entity which are new
        compared to the last poll.

        Args:
            sensor_service (SensorService): Sensor service
            config (dict): Config
            poll_interval (int): Poll Interval. Defaults to 5.
            wrapper_api (str): source URL to fetch entities from
            ttl (int): Time to live for each entity in the DB
        """
        super().__init__(
            sensor_service=sensor_service,
            config=config,
            poll_interval=poll_interval,
        )
        self.wrapper_api = wrapper_api
        self.ttl = ttl
        self.new_entities = []

    @abc.abstractmethod
    def poll_new_entity(self, new_entities: List[dict]):
        """
        Perform action with all the `NEW` Entities.
        The method receives a list of all the `NEW` Entities

        Args:
            new_entities (:obj: `list` of :obj: `obj`): List of new entities
        Raises:
            sf_exceptions.ServiceflowNotNotImplemented: When method is not implemented
        """
        raise sf_exceptions.ServiceflowNotNotImplemented(
            "Method not implemented"
        )

    def poll(self):
        """
        Poll the API to get new data.
        Once new entities is available, for each entity check if it is
        present in the DB.
        If the entity is not present, add the entity to DB with
        "SEEN" property set to False and add it to new_entities
        If the entity is present and "SEEN" is False, add it to new_entites
        else move to next.
        """
        self.new_entities = []
        try:
            response = requests.get(self.wrapper_api, verify=False)
            response.raise_for_status()
        except (exceptions.HTTPError, exceptions.ConnectionError) as e:
            raise sf_exceptions.ServiceflowError(e)
        else:
            entities = response.json()
        entities_in_store = self.sensor_service.list_values(
            prefix=self.ENTITY_PREFIX
        )
        for entity in entities:
            entity_id = str(entity.get(ENTITY_ID))
            # Returns the entity if it is present in the store, otherwise returns None

            entity_in_store = next(
                (
                    json.loads(x.value)
                    for x in entities_in_store
                    if json.loads(x.value)[ENTITY_ID] == entity_id
                ),
                None,
            )
            if not entity_in_store:
                entity[SEEN] = False
                self.new_entities.append(entity)
                self.sensor_service.set_value(
                    self.ENTITY_PREFIX + entity_id,
                    json.dumps(entity),
                    self.ttl,
                )
            elif entity_in_store[SEEN] is False:
                self.new_entities.append(entity)
        self.poll_new_entity(self.new_entities)

    def get_all_entities(self):
        """Get all the entities currently in new_entities"""
        return self.new_entities

    def mark_entity_as_seen(self, entity_id: str):
        """
        Mark entity as seen if it exists in the store

        Args:
            entity_id (str): The entity id of the entity
                             which needs to be marked as seen.
        """
        entity_in_store = json.loads(
            self.sensor_service.get_value(self.ENTITY_PREFIX + entity_id)
        )
        if entity_in_store:
            entity_in_store[SEEN] = True
            self.sensor_service.set_value(
                self.ENTITY_PREFIX + entity_id,
                json.dumps(entity_in_store),
                self.ttl,
            )
