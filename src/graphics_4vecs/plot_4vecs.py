from __future__ import annotations

import manim
import numpy as np
import pandas as pd

###### SPECIFY DATA FILE, ANIMATION MODE, AND DECAY NUMBER HERE ######
filename = "initial_branches.csv"
animation_mode = "rotation"  # Choose from: picture, rotation, dynamic
decay_num = 2
######################################################################

dataframe = pd.read_csv(filename)


class Decay(manim.ThreeDScene):  # type: ignore[misc]
    def construct(self) -> None:
        """
        Build Manim scene for visualization of particle events.

        Usage: With manim installed, run in the command-line: manim -qh plot_4vecs.py Decay
        This will generate a visualization based on the settings specified at the top of plot_4vecs.py

        Parameters
        ----------
        None

        Returns
        ---------
        .png or .mp4 file when called by Manim
        """

        # Create sphere representing parent particle
        parent_radius = 0.5
        parent = manim.Sphere(radius=parent_radius)
        parent.set_color(manim.BLUE)

        # Construct vectors, no positioning yet
        scaling_factor = 1.4

        K_vec = scaling_factor * np.array(
            [
                dataframe["K_px"][decay_num],
                dataframe["K_py"][decay_num],
                dataframe["K_pz"][decay_num],
            ]
        )
        pi_m2_vec = scaling_factor * np.array(
            [
                dataframe["pi_minus_2_px"][decay_num],
                dataframe["pi_minus_2_py"][decay_num],
                dataframe["pi_minus_2_pz"][decay_num],
            ]
        )
        pi_m3_vec = scaling_factor * np.array(
            [
                dataframe["pi_minus_3_px"][decay_num],
                dataframe["pi_minus_3_py"][decay_num],
                dataframe["pi_minus_3_pz"][decay_num],
            ]
        )
        pi_p4_vec = scaling_factor * np.array(
            [
                dataframe["pi_plus_4_px"][decay_num],
                dataframe["pi_plus_4_py"][decay_num],
                dataframe["pi_plus_4_pz"][decay_num],
            ]
        )

        K_vec /= np.linalg.norm(K_vec)
        pi_m2_vec /= np.linalg.norm(pi_m2_vec)
        pi_m3_vec /= np.linalg.norm(pi_m3_vec)
        pi_p4_vec /= np.linalg.norm(pi_p4_vec)

        K_vec *= scaling_factor
        pi_m2_vec *= scaling_factor
        pi_m3_vec *= scaling_factor
        pi_p4_vec *= scaling_factor

        # Compute summed vectors of both decays, and their unit vectors
        dec1 = K_vec + pi_m2_vec
        dec2 = pi_m3_vec + pi_p4_vec
        dec1_unit_vec = dec1 / np.linalg.norm(dec1)
        dec2_unit_vec = dec2 / np.linalg.norm(dec2)

        # Create vector for daughter 1 decay
        daughter1_length = 1
        daughter1_start = dec1_unit_vec * parent_radius
        daughter1_end = daughter1_start + (dec1_unit_vec * daughter1_length)
        daughter1_vec = manim.Arrow3D(
            start=daughter1_start, end=daughter1_end, resolution=8
        )

        # Create vector for daughter 2 decay
        daughter2_length = 1
        daughter2_start = dec2_unit_vec * parent_radius
        daughter2_end = daughter2_start + (dec2_unit_vec * daughter2_length)
        daughter2_vec = manim.Arrow3D(
            start=daughter2_start, end=daughter2_end, resolution=8
        )

        # Create daughter 1 sphere
        daughter1_sphere_r = 0.25  # radius of daughter 1 sphere
        daughter1_sphere_center = daughter1_end + (daughter1_sphere_r * dec1_unit_vec)
        daughter1_sphere = manim.Sphere(
            center=daughter1_sphere_center, radius=daughter1_sphere_r
        )
        daughter1_sphere.set_color(manim.RED)

        # Create daughter 2 sphere
        daughter2_sphere_r = 0.25  # radius of daughter 1 sphere
        daughter2_sphere_center = daughter2_end + (daughter2_sphere_r * dec2_unit_vec)
        daughter2_sphere = manim.Sphere(
            center=daughter2_sphere_center, radius=daughter2_sphere_r
        )
        daughter2_sphere.set_color(manim.PURPLE)

        # Compute start point of K and pi2 vectors
        k_pi2_start = daughter1_sphere_center

        # Construct K arrow:
        K_arrow = manim.Arrow3D(
            start=k_pi2_start,
            end=[
                k_pi2_start[0] + K_vec[0],
                k_pi2_start[1] + K_vec[1],
                k_pi2_start[2] + K_vec[2],
            ],
            resolution=8,
        )

        # Construct pi2 arrow:
        pi2_arrow = manim.Arrow3D(
            start=k_pi2_start,
            end=[
                k_pi2_start[0] + pi_m2_vec[0],
                k_pi2_start[1] + pi_m2_vec[1],
                k_pi2_start[2] + pi_m2_vec[2],
            ],
            resolution=8,
        )

        # Compute start point of pi3 and pi4 arrows
        pi3_pi4_start = daughter2_sphere_center

        # Construct pi3 arrow:
        pi3_arrow = manim.Arrow3D(
            start=pi3_pi4_start,
            end=[
                pi3_pi4_start[0] + pi_m3_vec[0],
                pi3_pi4_start[1] + pi_m3_vec[1],
                pi3_pi4_start[2] + pi_m3_vec[2],
            ],
            resolution=8,
        )

        # Construct pi4 arrow:
        pi4_arrow = manim.Arrow3D(
            start=pi3_pi4_start,
            end=[
                pi3_pi4_start[0] + pi_p4_vec[0],
                pi3_pi4_start[1] + pi_p4_vec[1],
                pi3_pi4_start[2] + pi_p4_vec[2],
            ],
            resolution=8,
        )

        # Set arrow colors
        K_arrow.set_color(manim.RED)
        pi2_arrow.set_color(manim.ORANGE)
        pi3_arrow.set_color(manim.BLUE)
        pi4_arrow.set_color(manim.PURPLE)

        if animation_mode == "picture":
            # Set camera orientation to face in direction of vector perpendicular to decay
            # Use Gram-Schmidt process to generate a vector orthogonal to dec1
            orth_vec = np.random.randn(3)
            orth_vec = np.array([2.0, -1.0, 0.5])
            orth_vec -= orth_vec.dot(dec1) * dec1 / np.linalg.norm(dec1) ** 2
            orth_vec /= np.linalg.norm(orth_vec)

            # Compute phi and theta coordinates of orth_vec
            phi = np.arccos(orth_vec[2])
            theta = np.arccos(orth_vec[0] / np.sin(phi))

            self.set_camera_orientation(phi=phi, theta=theta)

            # Add objects to scene
            self.add(parent, daughter1_vec, daughter2_vec)
            self.add(daughter1_sphere, daughter2_sphere)
            self.add(K_arrow, pi2_arrow, pi3_arrow, pi4_arrow)

        elif animation_mode == "rotation":
            self.set_camera_orientation(
                phi=90 * manim.DEGREES, theta=270 * manim.DEGREES
            )  # phi=90, theta=270 shows side profile with +x axis to the right

            # Add objects to scene
            self.add(parent, daughter1_vec, daughter2_vec)
            self.add(daughter1_sphere, daughter2_sphere)
            self.add(K_arrow, pi2_arrow, pi3_arrow, pi4_arrow)

            # Ambient rotation
            self.begin_ambient_camera_rotation(rate=1)
            self.wait(12)
            self.stop_ambient_camera_rotation()

        elif animation_mode == "dynamic":
            # Set camera orientation to face in direction of vector perpendicular to decay
            # Use Gram-Schmidt process to generate a vector orthogonal to dec1
            orth_vec = np.random.randn(3)
            orth_vec -= orth_vec.dot(dec1) * dec1 / np.linalg.norm(dec1) ** 2
            orth_vec /= np.linalg.norm(orth_vec)

            # Compute phi and theta coordinates of orth_vec
            phi = np.arccos(orth_vec[2])
            theta = np.arccos(orth_vec[0] / np.sin(phi))

            self.set_camera_orientation(phi=phi, theta=theta)

            self.play(manim.Write(parent))
            self.wait(2)
            daughter_group = manim.VGroup(daughter1_vec, daughter2_vec)
            self.play(manim.Create(daughter_group))

            dsphere_group = manim.VGroup(daughter1_sphere, daughter2_sphere)
            self.play(manim.Create(dsphere_group))
            self.wait(2)

            self.play(
                manim.Create(K_arrow),
                manim.Create(pi2_arrow),
                manim.Create(pi3_arrow),
                manim.Create(pi4_arrow),
            )
            self.wait(2)

            self.begin_ambient_camera_rotation(rate=1)
            self.wait(12)
            self.stop_ambient_camera_rotation()
