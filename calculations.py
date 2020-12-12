import numpy as np
import cmath as cm
import matplotlib.pyplot as plt


class Layer():
    def __init__(self, number: int, thickness: float, refractive_index: complex, name: str):
        self.number = number
        self.thickness = thickness
        self.refractive_index = refractive_index
        self.name = name

'''
layers_list = [Layer(1, 20, 0.524 + 10.742j, 'gold')]
'''

layers_list = []
initial_medium_refractive_index = 1.444
final_medium_refractive_index = 1

vacuum_wavelenght = 1550


def TE_transfer_matrix(theta: float):
    if (theta < 0) or (theta > np.pi / 2):
        raise Exception('Angle is not in range [0, pi/2].')

    transfer_matrix = np.array([[1, 0], [0, 1]])

    final_medium_matrix = np.array([[1, 1],
                                    [- final_medium_refractive_index * cm.sqrt(1 - (
                                            initial_medium_refractive_index * np.sin(
                                        theta) / final_medium_refractive_index) ** 2),
                                     final_medium_refractive_index * cm.sqrt(1 - (
                                             initial_medium_refractive_index * np.sin(
                                         theta) / final_medium_refractive_index) ** 2)]])
    transfer_matrix = np.dot(final_medium_matrix, transfer_matrix)

    for layer in reversed(layers_list):
        cos_theta_m = cm.sqrt(1 - (initial_medium_refractive_index * np.sin(theta) / layer.refractive_index) ** 2)
        dynamical_matrix = np.array([[1, 1],
                                     [- layer.refractive_index * cos_theta_m,
                                      layer.refractive_index * cos_theta_m]])
        propagation_matrix = np.array([[cm.exp(
            - layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / vacuum_wavelenght * 1j),
            0],
            [0, cm.exp(
                layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / vacuum_wavelenght * 1j)]])

        transfer_matrix = np.dot(np.linalg.inv(dynamical_matrix), transfer_matrix)
        transfer_matrix = np.dot(propagation_matrix, transfer_matrix)
        transfer_matrix = np.dot(dynamical_matrix, transfer_matrix)

    initial_medium_matrix = np.array([[1, 1],
                                      [- initial_medium_refractive_index * np.cos(theta),
                                       initial_medium_refractive_index * np.cos(theta)]])
    transfer_matrix = np.dot(np.linalg.inv(initial_medium_matrix), transfer_matrix)

    return transfer_matrix


def TM_transfer_matrix(theta: float):
    if (theta < 0) or (theta > np.pi / 2):
        raise Exception('Angle is not in range [0, pi/2].')

    transfer_matrix = np.array([[1, 0], [0, 1]])

    final_medium_matrix = np.array(
        [[cm.sqrt(1 - (initial_medium_refractive_index * np.sin(theta) / final_medium_refractive_index) ** 2),
          cm.sqrt(1 - (initial_medium_refractive_index * np.sin(theta) / final_medium_refractive_index) ** 2)],
         [final_medium_refractive_index,
          - final_medium_refractive_index]])
    transfer_matrix = np.dot(final_medium_matrix, transfer_matrix)

    for layer in reversed(layers_list):
        cos_theta_m = cm.sqrt(1 - (initial_medium_refractive_index * np.sin(theta) / layer.refractive_index) ** 2)
        dynamical_matrix = np.array([[cos_theta_m, cos_theta_m],
                                     [layer.refractive_index,
                                      - layer.refractive_index]])
        propagation_matrix = np.array([[cm.exp(
            - layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / vacuum_wavelenght * 1j),
            0],
            [0, cm.exp(
                layer.refractive_index * cos_theta_m * 2 * np.pi * layer.thickness / vacuum_wavelenght * 1j)]])

        transfer_matrix = np.dot(np.linalg.inv(dynamical_matrix), transfer_matrix)
        transfer_matrix = np.dot(propagation_matrix, transfer_matrix)
        transfer_matrix = np.dot(dynamical_matrix, transfer_matrix)

    initial_medium_matrix = np.array([[np.cos(theta), np.cos(theta)],
                                      [initial_medium_refractive_index,
                                       - initial_medium_refractive_index]])
    transfer_matrix = np.dot(np.linalg.inv(initial_medium_matrix), transfer_matrix)

    return transfer_matrix


def TE_reflectance():
    return np.vectorize(lambda theta: abs(TE_transfer_matrix(theta)[1][0] / TE_transfer_matrix(theta)[0][0]) ** 2)


def TE_transmittance():
    return np.vectorize(lambda theta: ((final_medium_refractive_index *
                                       cm.sqrt(1 - (initial_medium_refractive_index *
                                                    np.sin(theta) / final_medium_refractive_index) ** 2) /
                                       (initial_medium_refractive_index * np.cos(theta))).real *
                                       abs(1 / TE_transfer_matrix(theta)[0][0]) ** 2))


def TM_reflectance():
    return np.vectorize(lambda theta: abs(TM_transfer_matrix(theta)[1][0] / TM_transfer_matrix(theta)[0][0]) ** 2)


def TM_transmittance():
    return np.vectorize(lambda theta: ((final_medium_refractive_index *
                                       cm.sqrt(1 - (initial_medium_refractive_index *
                                                    np.sin(theta) / final_medium_refractive_index) ** 2) /
                                       (initial_medium_refractive_index * np.cos(theta)) *
                                       abs(1 / TM_transfer_matrix(theta)[0][0]) ** 2)).real)

'''
theta = np.arange(0, np.pi / 2, 0.01)
plt.plot(theta, TE_reflectance()(theta))
plt.plot(theta, TE_transmittance()(theta))
plt.plot(theta, TM_reflectance()(theta))
plt.plot(theta, TM_transmittance()(theta))
plt.show()
'''

def BuiltGraph():
    theta = np.arange(0, np.pi / 2, 0.001)
    plt.plot(theta, TE_reflectance()(theta))
    plt.plot(theta, TE_transmittance()(theta))
    plt.plot(theta, TM_reflectance()(theta))
    plt.plot(theta, TM_transmittance()(theta))
    plt.show()

