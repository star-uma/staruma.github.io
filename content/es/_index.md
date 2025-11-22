---
title: RoboRescue UMA
date: 2022-10-24
type: landing

sections:
  - block: hero
    id: inicio
    content:
      title: RoboRescue UMA
      image:
        filename: donatello/donatello_mejor_foto.jpg
        alt: Robot Donatello
      text: |
        Somos un equipo compuesto por estudiantes de diversos ámbitos pertenecientes a la Universidad de Málaga unidos con un fin común. Nos dedicamos al desarrollo tecnológico-robótico de rescate.
      cta:
        label: Conoce más
        url: "#about"
        icon_pack: fas
        icon: arrow-down
    design:
      background:
        image:
          filename: donatello/donatello_mejor_foto.jpg
          filters:
            brightness: 0.5
        text_color_light: true

  - block: features
    id: about
    content:
      title: About Us
      subtitle: Nuestros Departamentos
      items:
        - name: Hardware
          description: Diseño y construcción de robots.
          icon: microchip
          icon_pack: fas
        - name: Software
          description: Inteligencia y control.
          icon: code
          icon_pack: fas
        - name: Comunicación
          description: Difusión y redes sociales.
          icon: bullhorn
          icon_pack: fas
        - name: Mentores
          description: Guía y apoyo experto.
          icon: chalkboard-teacher
          icon_pack: fas
    design:
      columns: "2"
      view: showcase

  - block: markdown
    id: donatello
    content:
      title: Donatello
      subtitle: Nuestro Robot de Rescate
      text: |
        ![Donatello](donatello/donatello_1.jpg)

        Donatello es nuestro robot insignia, diseñado para operar en entornos hostiles y realizar tareas de rescate. Cuenta con un sistema de tracción avanzado y sensores de última generación.
    design:
      columns: "1"

  - block: markdown
    id: horu
    content:
      title: HORU
      subtitle: El Futuro del Rescate
      text: |
        ![HORU](robots/robot_1.png)

        HORU es nuestro nuevo prototipo, enfocado en la agilidad y la autonomía. Incorpora nuevas tecnologías de visión artificial y navegación.
    design:
      columns: "1"

  - block: features
    id: team
    content:
      title: Our Team
      subtitle: Conoce a los miembros
      items:
        - name: Hardware Team
          description: Los constructores.
          icon: tools
          icon_pack: fas
        - name: Software Team
          description: Los programadores.
          icon: laptop-code
          icon_pack: fas
        - name: Communication Team
          description: La voz del equipo.
          icon: comments
          icon_pack: fas
    design:
      columns: "3"
      view: card

  - block: markdown
    id: sponsors
    content:
      title: Sponsors
      subtitle: Gracias a nuestros patrocinadores
      text: |
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
          <img src="logos_y_fondos/Sponsors-24.png" alt="Sponsor 1" style="height: 100px;">
          <img src="logos_y_fondos/Sponsors-25.png" alt="Sponsor 2" style="height: 100px;">
          <img src="logos_y_fondos/Sponsors-26.png" alt="Sponsor 3" style="height: 100px;">
        </div>
    design:
      columns: "1"

  - block: contact
    id: contact
    content:
      title: Contacto
      subtitle: Encuéntranos
      email: info@roborescueuma.com
      address:
        street: Bulevar Louis Pasteur, 35
        city: Málaga
        region: Málaga
        postcode: "29071"
        country: Spain
        country_code: ES
      coordinates:
        latitude: "36.715"
        longitude: "-4.478"
    design:
      columns: "2"
---
