import pamqp
import aiormq
from aiormq import Channel, Connection

Props = aiormq.spec.Basic.Properties
DeliveredMessage = aiormq.types.DeliveredMessage
ArgumentsType = aiormq.types.ArgumentsType
GetEmpty, GetOk = aiormq.spec.Basic.GetEmpty, aiormq.spec.Basic.GetOk
