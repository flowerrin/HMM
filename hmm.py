#!/usr/bin/env python3Symbol_prob
import sys
import numpy as np
import time
import os

INPUT = 11001111001110110

States = ["p", "q", "r"]

First_states_prob = {"p": 0.46, "q": 0.10, "r": 0.44}

Trans_prob = {"p": {"p": 0.55, "q": 0.18, "r": 0.27},
              "q": {"p": 0.13, "q": 0.05, "r": 0.82},
              "r": {"p": 0.54, "q": 0.09, "r": 0.37}}

Symbol_prob = [{"p": 0.78, "q": 0.68, "r": 0.59},
               {"p": 0.22, "q": 0.32, "r": 0.41}]


def digit(i, lst=[]):
    if i > 0:
        lst.append(i%10)
        return digit(i//10, lst)
    else:
        lst.reverse()
        return lst

def hmm(input_num):
    delta = []
    back_pointer = {}
    cnt = 0

    for num in input_num:
        tmp_delta = {}
        prev_back_pointer = back_pointer.copy()
        if len(back_pointer) == 0:
            for state in States:
                prob = First_states_prob[state] * Symbol_prob[num][state]
                tmp_delta[state] = prob
                back_pointer[state] = state
            delta.append(tmp_delta)
        else:
            for cur_state in States:
                max_prob = 0
                for prev_state in States:
                    trans_prob = Trans_prob[prev_state][cur_state]
                    prob = delta[cnt-1][prev_state] * trans_prob * Symbol_prob[num][cur_state]
                    if max_prob <= prob:
                        max_prob = prob
                        max_prev_state = prev_state
                tmp_delta[cur_state] = max_prob
                back_pointer[cur_state] = prev_back_pointer[max_prev_state] + cur_state
            delta.append(tmp_delta)
        cnt += 1

    final_delta = delta[-1]
    max_state = max(final_delta, key=final_delta.get)
    max_back_pointer = back_pointer[max_state]
    max_final_prob = final_delta[max_state]
    
    return max_back_pointer, max_final_prob

def main(argument_value):
    input_num = digit(INPUT)
    states, prob = hmm(input_num)
    print("Input:", INPUT)
    print("States:", states)
    print("Max prob:", prob)

if __name__ == "__main__":
    main(sys.argv)
