import math
import random
import tkinter as tk


class ParticleCore:
    """
    2D-система частиц для интерфейса Кая.

    FAST:
        человекоподобный силуэт.

    SMART:
        процессор с пинами.

    ERROR:
        текущая форма сохраняется,
        меняется только цвет частиц на красный.
    """

    FAST_MODE = "fast"
    SMART_MODE = "smart"

    NORMAL_COLOR = "#ff9d3d"
    ERROR_COLOR = "#ff3030"

    def __init__(
        self,
        canvas: tk.Canvas,
        width: int = 700,
        height: int = 700,
        particle_count: int = 1800,
    ):
        self.canvas = canvas

        self.width = width
        self.height = height
        self.particle_count = particle_count

        self.center_x = width / 2
        self.center_y = height / 2

        self.particles = []

        self.current_state = "idle"

        self.mode = self.FAST_MODE

        self.target_points = []

        self.running = True

        self.current_color = self.NORMAL_COLOR
        self.target_color = self.NORMAL_COLOR

        self._create_particles()

        self.set_state("idle")

        self._animate()

                                                               
                     
                                                               

    def _create_particles(self):
        for _ in range(self.particle_count):
            angle = random.uniform(
                0,
                math.pi * 2,
            )

            distance = random.uniform(
                40,
                280,
            )

            x = (
                self.center_x
                + math.cos(angle)
                * distance
            )

            y = (
                self.center_y
                + math.sin(angle)
                * distance
            )

            particle = {
                "x": x,
                "y": y,
                "target_x": x,
                "target_y": y,
                "vx": random.uniform(
                    -0.3,
                    0.3,
                ),
                "vy": random.uniform(
                    -0.3,
                    0.3,
                ),
                "size": random.uniform(
                    1.0,
                    2.5,
                ),
                "phase": random.uniform(
                    0,
                    math.pi * 2,
                ),
                "speed": random.uniform(
                    0.04,
                    0.12,
                ),
                "item": None,
            }

            particle["item"] = (
                self.canvas.create_oval(
                    x,
                    y,
                    x + particle["size"],
                    y + particle["size"],
                    outline="",
                    fill=self.current_color,
                )
            )

            self.particles.append(
                particle
            )

                                                               
                  
                                                               

    def set_mode(
        self,
        mode: str,
    ):
        """
        Переключает визуальный режим Кая.

        fast:
            человекоподобный силуэт.

        smart:
            процессор.

        Если сейчас активна ошибка,
        форма не меняется до её завершения.
        """

        if mode not in (
            self.FAST_MODE,
            self.SMART_MODE,
        ):
            return

        self.mode = mode

                                           
        if self.current_state == "error":
            return

        self._update_shape()

                                                               
               
                                                               

    def set_state(
        self,
        state: str,
    ):
        """
        Возможные состояния:

        idle
        listening
        processing
        speaking
        error

        Ошибка не создаёт отдельную форму.
        Она сохраняет текущую форму и
        меняет только цвет.
        """

        self.current_state = state

        if state == "error":
            self.target_color = (
                self.ERROR_COLOR
            )

                          
                                      
             
                                                 
                                               

            return

        self.target_color = (
            self.NORMAL_COLOR
        )

        self._update_shape()

                                                               
                 
                                                               

    def _update_shape(self):
        if self.mode == self.SMART_MODE:
            self.target_points = (
                self._make_processor_points()
            )

        else:
            self.target_points = (
                self._make_human_points()
            )

        self._assign_targets()

                                                               
                     
                                                               

    def _make_human_points(self):
        points = []

        cx = self.center_x
        cy = self.center_y

                                                       
                
                                                       

        head_center_x = cx
        head_center_y = cy - 115

        head_radius_x = 72
        head_radius_y = 92

        for _ in range(650):
            angle = random.uniform(
                0,
                math.pi * 2,
            )

            radius = math.sqrt(
                random.uniform(
                    0.35,
                    1.0,
                )
            )

            x = (
                head_center_x
                + math.cos(angle)
                * head_radius_x
                * radius
            )

            y = (
                head_center_y
                + math.sin(angle)
                * head_radius_y
                * radius
            )

            points.append(
                (x, y)
            )

                                                       
             
                                                       

        for _ in range(140):
            x = cx + random.uniform(
                -32,
                32,
            )

            y = random.uniform(
                cy - 28,
                cy + 30,
            )

            points.append(
                (x, y)
            )

                                                       
               
                                                       

        for _ in range(700):
            t = random.uniform(
                0,
                1,
            )

            x = (
                cx
                + (t * 2 - 1)
                * 220
            )

            shoulder_height = (
                55
                + 75
                * abs(t - 0.5)
                * 2
            )

            y = (
                cy
                + shoulder_height
                + random.uniform(
                    -35,
                    35,
                )
            )

            points.append(
                (x, y)
            )

                                                       
               
                                                       

        for _ in range(350):
            x = random.uniform(
                cx - 175,
                cx + 175,
            )

            y = random.uniform(
                cy + 70,
                cy + 180,
            )

            normalized_x = (
                (x - cx) / 180
            )

            normalized_y = (
                (y - (cy + 115))
                / 100
            )

            if (
                normalized_x ** 2
                + normalized_y ** 2
                <= 1
            ):
                points.append(
                    (x, y)
                )

        return points

                                                               
               
                                                               

    def _make_processor_points(self):
        """
        Создаёт форму микросхемы из точек.

        В центре находится корпус процессора.
        По четырём сторонам расположены пины.

        Здесь нет изображения или SVG.
        Геометрия полностью создаётся частицами.
        """

        points = []

        cx = self.center_x
        cy = self.center_y

                        

        chip_width = 250
        chip_height = 250

        half_width = chip_width / 2
        half_height = chip_height / 2

                         

        border_thickness = 22

                                                       
                               
                                                       

        border_points = 700

        for _ in range(
            border_points
        ):
            side = random.randint(
                0,
                3,
            )

            if side == 0:
                      

                x = random.uniform(
                    cx - half_width,
                    cx + half_width,
                )

                y = random.uniform(
                    cy - half_height,
                    cy - half_height
                    + border_thickness,
                )

            elif side == 1:
                       

                x = random.uniform(
                    cx + half_width
                    - border_thickness,
                    cx + half_width,
                )

                y = random.uniform(
                    cy - half_height,
                    cy + half_height,
                )

            elif side == 2:
                     

                x = random.uniform(
                    cx - half_width,
                    cx + half_width,
                )

                y = random.uniform(
                    cy + half_height
                    - border_thickness,
                    cy + half_height,
                )

            else:
                      

                x = random.uniform(
                    cx - half_width,
                    cx - half_width
                    + border_thickness,
                )

                y = random.uniform(
                    cy - half_height,
                    cy + half_height,
                )

            points.append(
                (x, y)
            )

                                                       
                          
                                                       

        core_width = 135
        core_height = 135

        for _ in range(650):
            x = random.uniform(
                cx - core_width / 2,
                cx + core_width / 2,
            )

            y = random.uniform(
                cy - core_height / 2,
                cy + core_height / 2,
            )

            points.append(
                (x, y)
            )

                                                       
                            
                                                       

                      

        for _ in range(180):
            x = random.choice(
                [
                    cx - 85,
                    cx + 85,
                ]
            )

            x += random.uniform(
                -3,
                3,
            )

            y = random.uniform(
                cy - 105,
                cy + 105,
            )

            points.append(
                (x, y)
            )

                        

        for _ in range(180):
            x = random.uniform(
                cx - 105,
                cx + 105,
            )

            y = random.choice(
                [
                    cy - 85,
                    cy + 85,
                ]
            )

            y += random.uniform(
                -3,
                3,
            )

            points.append(
                (x, y)
            )

                                                       
              
                                                       

        pin_count = 18

        pin_length = 55
        pin_thickness = 7

                    

        for index in range(
            pin_count
        ):
            x = (
                cx
                - half_width
                + 20
                + index
                * (
                    (
                        chip_width
                        - 40
                    )
                    / (
                        pin_count
                        - 1
                    )
                )
            )

                         

            for _ in range(14):
                px = x + random.uniform(
                    -pin_thickness,
                    pin_thickness,
                )

                py = random.uniform(
                    cy - half_height
                    - pin_length,
                    cy - half_height,
                )

                points.append(
                    (px, py)
                )

                        

            for _ in range(14):
                px = x + random.uniform(
                    -pin_thickness,
                    pin_thickness,
                )

                py = random.uniform(
                    cy + half_height,
                    cy + half_height
                    + pin_length,
                )

                points.append(
                    (px, py)
                )

                      

        for index in range(
            pin_count
        ):
            y = (
                cy
                - half_height
                + 20
                + index
                * (
                    (
                        chip_height
                        - 40
                    )
                    / (
                        pin_count
                        - 1
                    )
                )
            )

                       

            for _ in range(14):
                px = random.uniform(
                    cx - half_width
                    - pin_length,
                    cx - half_width,
                )

                py = y + random.uniform(
                    -pin_thickness,
                    pin_thickness,
                )

                points.append(
                    (px, py)
                )

                        

            for _ in range(14):
                px = random.uniform(
                    cx + half_width,
                    cx + half_width
                    + pin_length,
                )

                py = y + random.uniform(
                    -pin_thickness,
                    pin_thickness,
                )

                points.append(
                    (px, py)
                )

                                                       
                                
                                                       

        for _ in range(100):
            angle = random.uniform(
                0,
                math.pi * 2,
            )

            distance = random.uniform(
                190,
                230,
            )

            x = (
                cx
                + math.cos(angle)
                * distance
            )

            y = (
                cy
                + math.sin(angle)
                * distance
            )

            points.append(
                (x, y)
            )

        return points

                                                               
                         
                                                               

    def _assign_targets(self):
        if not self.target_points:
            return

        shuffled = (
            self.target_points.copy()
        )

        random.shuffle(
            shuffled
        )

        for index, particle in enumerate(
            self.particles
        ):
            target = shuffled[
                index
                % len(shuffled)
            ]

            particle["target_x"] = (
                target[0]
            )

            particle["target_y"] = (
                target[1]
            )

                                                               
          
                                                               

    @staticmethod
    def _hex_to_rgb(
        color: str,
    ):
        color = color.lstrip(
            "#"
        )

        return tuple(
            int(
                color[index:index + 2],
                16,
            )
            for index in (
                0,
                2,
                4,
            )
        )

    @staticmethod
    def _rgb_to_hex(
        rgb,
    ):
        return (
            "#{:02x}{:02x}{:02x}"
            .format(
                *rgb
            )
        )

    def _update_color(self):
        current = self._hex_to_rgb(
            self.current_color
        )

        target = self._hex_to_rgb(
            self.target_color
        )

        new_color = []

        for current_value, target_value in zip(
            current,
            target,
        ):
            value = (
                current_value
                + (
                    target_value
                    - current_value
                )
                * 0.08
            )

            new_color.append(
                int(value)
            )

        self.current_color = (
            self._rgb_to_hex(
                new_color
            )
        )

        for particle in self.particles:
            self.canvas.itemconfig(
                particle["item"],
                fill=self.current_color,
            )

                                                               
              
                                                               

    def _animate(self):
        if not self.running:
            return

        self._update_color()

        for particle in self.particles:
            x = particle["x"]
            y = particle["y"]

            target_x = (
                particle["target_x"]
            )

            target_y = (
                particle["target_y"]
            )

                                

            dx = target_x - x
            dy = target_y - y

            distance = math.sqrt(
                dx * dx
                + dy * dy
            )

                                 
                                   

            attraction = 0.035

            particle["vx"] += (
                dx * attraction
            )

            particle["vy"] += (
                dy * attraction
            )

                                      

            noise_x = math.sin(
                particle["phase"]
                + x * 0.01
            )

            noise_y = math.cos(
                particle["phase"]
                + y * 0.01
            )

            particle["vx"] += (
                noise_x * 0.015
            )

            particle["vy"] += (
                noise_y * 0.015
            )

                                   

            max_speed = 7.0

            speed = math.sqrt(
                particle["vx"] ** 2
                + particle["vy"] ** 2
            )

            if speed > max_speed:
                particle["vx"] = (
                    particle["vx"]
                    / speed
                    * max_speed
                )

                particle["vy"] = (
                    particle["vy"]
                    / speed
                    * max_speed
                )

                      

            particle["x"] += (
                particle["vx"]
            )

            particle["y"] += (
                particle["vy"]
            )

                    

            particle["vx"] *= 0.90
            particle["vy"] *= 0.90

                       

            particle["phase"] += 0.025

            pulse = (
                math.sin(
                    particle["phase"]
                )
                + 1
            ) / 2

            size = (
                particle["size"]
                + pulse * 0.8
            )

                                  

            if self.current_state == "listening":
                size += (
                    math.sin(
                        particle["phase"]
                        * 2
                    )
                    + 1
                ) * 0.8

            elif self.current_state == "processing":
                size += (
                    math.sin(
                        particle["phase"]
                        * 3
                    )
                    + 1
                ) * 1.2

            elif self.current_state == "speaking":
                size += (
                    math.sin(
                        particle["phase"]
                        * 4
                    )
                    + 1
                ) * 0.7

            elif self.current_state == "error":
                size += (
                    math.sin(
                        particle["phase"]
                        * 5
                    )
                    + 1
                ) * 0.6

            self.canvas.coords(
                particle["item"],
                particle["x"],
                particle["y"],
                particle["x"] + size,
                particle["y"] + size,
            )

        self.canvas.after(
            16,
            self._animate,
        )

                                                               
               
                                                               

    def stop(self):
        self.running = False