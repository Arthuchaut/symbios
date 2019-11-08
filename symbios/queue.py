'''
@desc    The queue class for manage queues.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''


class Queue:
    '''The Queue class declaration.

    Attributes:
        queue (str): The queue name.
        passive (bool): Not create queue if it not exists.
        durable (bool): Not delete the queue after a broker restart.
        exclusive (bool): Delete the queue after closed the connection.
        auto_delete (bool): Delete queue when it empty from consumers.
        nowait (bool): Not send a reply callback.
        arguments (dict): Some arguments for the declaration.
    '''

    def __init__(
        self,
        queue: str = '',
        *,
        passive: bool = False,
        durable: bool = False,
        exclusive: bool = False,
        auto_delete: bool = False,
        nowait: bool = False,
        arguments: dict = None
    ):
        '''The Queue initializer.

        Args:
            queue (str): The queue name. Default to ''.
            passive (bool): Not create queue if it not exists.
                Default to False.
            durable (bool): Not delete the queue after a broker restart.
                Default to False.
            exclusive (bool): Delete the queue after closed the connection.
                Default to False.
            auto_delete (bool): Delete queue when it empty from consumers.
                Default to False.
            nowait (bool): Not send a reply callback.
                Default to False.
            arguments (dict): Some arguments for the declaration.
                Default to {}.
        '''

        self.queue: str = queue
        self.passive: bool = passive
        self.durable: bool = durable
        self.exclusive: bool = exclusive
        self.auto_delete: bool = auto_delete
        self.nowait: bool = nowait
        self.arguments: dict = arguments or {}
