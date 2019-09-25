'''
@desc    The Queue test class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

import pytest

from libs.symbios.queue import Queue


class TestQueue:
    @pytest.mark.parametrize('name', ['queue_name'])
    @pytest.mark.parametrize('passive', [False, True])
    @pytest.mark.parametrize('durable', [False, True])
    @pytest.mark.parametrize('exclusive', [False, True])
    @pytest.mark.parametrize('auto_delete', [False, True])
    @pytest.mark.parametrize('nowait', [False, True])
    @pytest.mark.parametrize('arguments', [{}])
    def test_queue(
        self,
        name: str,
        passive: bool,
        durable: bool,
        exclusive: bool,
        auto_delete: bool,
        nowait: bool,
        arguments: dict,
    ) -> None:
        queue: Queue = Queue(
            name,
            passive=passive,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            nowait=nowait,
            arguments=arguments,
        )

        assert (
            queue.queue == name
            and queue.passive == passive
            and queue.durable == durable
            and queue.exclusive == exclusive
            and queue.auto_delete == auto_delete
            and queue.nowait == nowait
            and queue.arguments == arguments
        )
