"""
Created on 2019-01-28

@author: revanth
"""
import abc


class Presenter(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def present_create_bet(cls, output_data):
        pass
