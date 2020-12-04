"""
There is only class Layer.
"""

class L():
    """
Layer of Material

number - layer number
thickness - layer thickness
permittivity - dielectric constant
"""
    def __init__(self, number = 0):    
        self.number = number
        thickness = 0
        permittivity = 0

    def get_number():
        number = int(input())

    def get_thickness():
        thickness = float(input())

    def get_permittivity():
        real = float(input())
        imagine = float(input())
        permittivity = complex(real, imagine)
