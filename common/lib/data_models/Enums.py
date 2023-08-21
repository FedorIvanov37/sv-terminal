from enum import Enum
from common.lib.core.EpaySpecification import EpaySpecification


spec: EpaySpecification = EpaySpecification()

generated_field = Enum("generated_field", spec.get_generated_fields_dict())
