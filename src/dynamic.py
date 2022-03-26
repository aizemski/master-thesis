import time

import numpy as np
import pandas as pd


def action_for_all_data(state, current_value, next_value, result_array, visited, fee=0.0):
    log_fee = np.log(1 - fee)
    if len(next_value) > 1:
        current_value = current_value * int(bool(state)) + max(
            (action_for_all_data(state=1, current_value=next_value.iloc[1], next_value=next_value.iloc[1:],
                                 result_array=result_array, visited=visited,
                                 fee=fee) - (
                     log_fee * int(bool(state))))
            if visited[1, -len(next_value)] == 0
            else result_array[1, -len(next_value)],
            (action_for_all_data(state=0, current_value=next_value.iloc[1], next_value=next_value.iloc[1:],
                                 result_array=result_array, visited=visited,
                                 fee=fee) + (
                     log_fee * (1 - int(bool(state)))))
            if visited[0, -len(next_value)] == 0
            else result_array[0, -len(next_value)],
        )
    else:
        current_value = (current_value - log_fee) * int(bool(state))
    result_array[state, -len(next_value)] = current_value
    visited[state, -len(next_value)] = 1
    return current_value


def optimal_for_all_data(frame, fee=0.0):
    start_time = time.time()
    frame_close_change = ((frame['Close']).pct_change().fillna(0) + 1)
    frame_close_change = np.log(frame_close_change)
    result_array = np.zeros((2, len(frame_close_change)))
    visited = np.zeros((2, len(frame_close_change)))
    action_for_all_data(state=0, current_value=frame_close_change.iloc[0],
                        next_value=frame_close_change[1:], result_array=result_array, visited=visited, fee=fee)
    print(time.time() - start_time)
    return pd.DataFrame(result_array[0]), pd.DataFrame(result_array[1])
