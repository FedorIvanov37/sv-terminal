from enum import Enum
from common.lib.core.EpaySpecification import EpaySpecification


spec: EpaySpecification = EpaySpecification()

message_type_indicator = Enum("message_type_indicators", spec.get_mti_dict())

generated_field = Enum("generated_field", spec.get_generated_fields_dict())
