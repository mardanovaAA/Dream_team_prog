import numpy as np
import cmath as cm


class Calculations():

    def __init__(self, layers_list, initial_medium_refractive_index=1 + 0j, final_medium_refractive_index=1 + 0j,
                 vacuum_wavelenght=500.0):
        self.layers_list = layers_list
        self.initial_medium_refractive_index = initial_medium_refractive_index
        self.final_medium_refractive_index = final_medium_refractive_index
        self.vacuum_wavelenght = vacuum_wavelenght

    def TE_transfer_matrix(self, theta: float):
        if (theta < 0) or (theta > np.pi / 2):
            raise Exception('Angle is not in range [0, pi/2].')

        transfer_matrix = np.array([[1, 0], [0, 1]])

        final_medium_matrix = np.array([[1, 1],
                                        [- self.final_medium_refractive_index * cm.sqrt(1 - (
                                                self.initial_medium_refractive_index * np.sin(
                                            theta) / self.final_medium_refractive_index) ** 2),
                                         self.final_medium_refractive_index * cm.sqrt(1 - (
                                                 self.initial_medium_refractive_index * np.sin(
                                             theta) / self.final_medium_refractive_index) ** 2)]])
        transfer_matrix = np.dot(final_medium_matrix, transfer_matrix)

        for layer in reversed(self.layers_list):
            cos_theta_m = cm.sqrt(
                1 - (self.initial_medium_refractive_index * np.sin(theta) / layer.refractive_index) ** 2)
            dynamical_matrix = np.array([[1, 1],
                                         [- layer.refractive_index * cos_theta_m,
                                          layer.refractive_index * cos_theta_m]])
            propagation_matrix = np.array([[cm.exp(
                - layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / self.vacuum_wavelenght * 1j),
                0],
                [0, cm.exp(
                    layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / self.vacuum_wavelenght * 1j)]])

            transfer_matrix = np.dot(np.linalg.inv(dynamical_matrix), transfer_matrix)
            transfer_matrix = np.dot(propagation_matrix, transfer_matrix)
            transfer_matrix = np.dot(dynamical_matrix, transfer_matrix)

        initial_medium_matrix = np.array([[1, 1],
                                          [- self.initial_medium_refractive_index * np.cos(theta),
                                           self.initial_medium_refractive_index * np.cos(theta)]])
        transfer_matrix = np.dot(np.linalg.inv(initial_medium_matrix), transfer_matrix)

        return transfer_matrix

    def TM_transfer_matrix(self, theta: float):
        if (theta < 0) or (theta > np.pi / 2):
            raise Exception('Angle is not in range [0, pi/2].')

        transfer_matrix = np.array([[1, 0], [0, 1]])

        final_medium_matrix = np.array(
            [[cm.sqrt(
                1 - (self.initial_medium_refractive_index * np.sin(theta) / self.final_medium_refractive_index) ** 2),
              cm.sqrt(1 - (self.initial_medium_refractive_index * np.sin(
                  theta) / self.final_medium_refractive_index) ** 2)],
             [self.final_medium_refractive_index,
              - self.final_medium_refractive_index]])
        transfer_matrix = np.dot(final_medium_matrix, transfer_matrix)

        for layer in reversed(self.layers_list):
            cos_theta_m = cm.sqrt(
                1 - (self.initial_medium_refractive_index * np.sin(theta) / layer.refractive_index) ** 2)
            dynamical_matrix = np.array([[cos_theta_m, cos_theta_m],
                                         [layer.refractive_index,
                                          - layer.refractive_index]])
            propagation_matrix = np.array([[cm.exp(
                - layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / self.vacuum_wavelenght * 1j),
                0],
                [0, cm.exp(
                    layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / self.vacuum_wavelenght * 1j)]])

            transfer_matrix = np.dot(np.linalg.inv(dynamical_matrix), transfer_matrix)
            transfer_matrix = np.dot(propagation_matrix, transfer_matrix)
            transfer_matrix = np.dot(dynamical_matrix, transfer_matrix)

        initial_medium_matrix = np.array([[np.cos(theta), np.cos(theta)],
                                          [self.initial_medium_refractive_index,
                                           - self.initial_medium_refractive_index]])
        transfer_matrix = np.dot(np.linalg.inv(initial_medium_matrix), transfer_matrix)

        return transfer_matrix

    def TE_reflectance(self):
        return np.vectorize(
            lambda theta: abs(self.TE_transfer_matrix(theta)[1][0] / self.TE_transfer_matrix(theta)[0][0]) ** 2)

    def TE_transmittance(self):
        return np.vectorize(lambda theta: ((self.final_medium_refractive_index *
                                            cm.sqrt(1 - (self.initial_medium_refractive_index *
                                                         np.sin(theta) / self.final_medium_refractive_index) ** 2) /
                                            (self.initial_medium_refractive_index * np.cos(theta))).real *
                                           abs(1 / self.TE_transfer_matrix(theta)[0][0]) ** 2))

    def TM_reflectance(self):
        return np.vectorize(
            lambda theta: abs(self.TM_transfer_matrix(theta)[1][0] / self.TM_transfer_matrix(theta)[0][0]) ** 2)

    def TM_transmittance(self):
        return np.vectorize(lambda theta: ((self.final_medium_refractive_index *
                                            cm.sqrt(1 - (self.initial_medium_refractive_index *
                                                         np.sin(theta) / self.final_medium_refractive_index) ** 2) /
                                            (self.initial_medium_refractive_index * np.cos(theta)) *
                                            abs(1 / self.TM_transfer_matrix(theta)[0][0]) ** 2)).real)

    def TE_absorption_coefficient(self):
        return np.vectorize(lambda theta: 1 - self.TE_reflectance()(theta) - self.TE_transmittance()(theta))

    def TM_absorption_coefficient(self):
        return np.vectorize(lambda theta: 1 - self.TM_reflectance()(theta) - self.TM_transmittance()(theta))
