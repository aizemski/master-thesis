import pandas as pd
import numpy as np


def action(state, current, next, fee=0.0):
    fee = np.log(1 - fee)
    if len(next) > 1:
        current = current * int(bool(state)) + max(
            (action(state=1, current=next.iloc[1], next=next.iloc[1:], fee=fee) - (fee * int(bool(state)))),
            (action(state=0, current=next.iloc[1], next=next.iloc[1:], fee=fee) + (fee * (1 - int(bool(state)))))
        )
    else:
        current = (current - fee) * int(bool(state))
    return current


def optimal(state, frame, prediction_period=1, fee=0.0):
    frame = np.log(frame[1:])

    while len(state) < len(frame):
        state.append(
            [action(state=0, current=frame.iloc[len(state) - 1],
                    next=frame[len(state) - 1:min(len(state) + prediction_period, len(frame) - 1)], fee=fee),
             action(state=1, current=frame.iloc[len(state) - 1],
                    next=frame[len(state) - 1:min(len(state) + prediction_period, len(frame) - 1)], fee=fee)])
