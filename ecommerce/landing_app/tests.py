from django.test import TestCase
from typing import List,Dict

# Create your tests here.


def test_dummy(name:str,age:int)->Dict:
    """_summary_

    Args:
        name (str): _description_
        age (int): _description_

    Returns:
        Dict: _description_
    """    
    return {"name":name,"age":age}


def test_dummy2(data):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """    
    return data