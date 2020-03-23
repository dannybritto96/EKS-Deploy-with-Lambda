# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: v1.13.5
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class V2beta2PodsMetricStatus(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'current': 'V2beta2MetricValueStatus',
        'metric': 'V2beta2MetricIdentifier'
    }

    attribute_map = {
        'current': 'current',
        'metric': 'metric'
    }

    def __init__(self, current=None, metric=None):
        """
        V2beta2PodsMetricStatus - a model defined in Swagger
        """

        self._current = None
        self._metric = None
        self.discriminator = None

        self.current = current
        self.metric = metric

    @property
    def current(self):
        """
        Gets the current of this V2beta2PodsMetricStatus.
        current contains the current value for the given metric

        :return: The current of this V2beta2PodsMetricStatus.
        :rtype: V2beta2MetricValueStatus
        """
        return self._current

    @current.setter
    def current(self, current):
        """
        Sets the current of this V2beta2PodsMetricStatus.
        current contains the current value for the given metric

        :param current: The current of this V2beta2PodsMetricStatus.
        :type: V2beta2MetricValueStatus
        """
        if current is None:
            raise ValueError("Invalid value for `current`, must not be `None`")

        self._current = current

    @property
    def metric(self):
        """
        Gets the metric of this V2beta2PodsMetricStatus.
        metric identifies the target metric by name and selector

        :return: The metric of this V2beta2PodsMetricStatus.
        :rtype: V2beta2MetricIdentifier
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this V2beta2PodsMetricStatus.
        metric identifies the target metric by name and selector

        :param metric: The metric of this V2beta2PodsMetricStatus.
        :type: V2beta2MetricIdentifier
        """
        if metric is None:
            raise ValueError("Invalid value for `metric`, must not be `None`")

        self._metric = metric

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, V2beta2PodsMetricStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
