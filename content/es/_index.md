---
title: RoboRescue UMA
date: 2022-10-24
type: landing
translationKey: home

sections:
  - block: hero
    id: inicio
    content:
      title: RoboRescue UMA
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
            brightness: 0.75
        text_color_light: true

  - block: features
    id: about
    content:
      title: Sobre Nosotros
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
        - name: Web
          description: Desarrollo y mantenimiento de la web.
          icon: code
          icon_pack: fas
    design:
      columns: 2
      view: showcase

  - block: hero
    id: donatello
    content:
      title: DONATELLO
      text: |
        Donatello es nuestro robot insignia, diseñado para operar en entornos hostiles y realizar tareas de rescate. Cuenta con un sistema de tracción avanzado y sensores de última generación.
    design:
      background:
        image:
          filename: donatello/donatello_9.jpg
          filters:
            brightness: 0.75
        text_color_light: true

  - block: hero
    id: horu
    content:
      title: HORU
      subtitle: El Futuro del Rescate
      text: |
        HORU es nuestro nuevo prototipo, enfocado en la agilidad y la autonomía. Incorpora nuevas tecnologías de visión artificial y navegación.
    design:
      columns: 1
      background:
        image:
          filename: robots/robot_1.png
          filters:
            brightness: 0.75
        text_color_light: true

  - block: people
    content:
      title: Nuestro Equipo
      user_groups:
        - Coordinadores
        - Mentores
        - Profesores colaboradores
        - Jefes de Departamento
        - Hardware
        - Software
        - Comunicación
        - Marketing
        - Web
        - Antiguos miembros
      sort_by: Params.last_name
      sort_ascending: true
    design:
      show_interests: false
      show_role: true
      show_social: true

  - block: markdown
    id: sponsors
    content:
      title: Patrocinadores
      subtitle: Gracias a nuestros patrocinadores
      text: |
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
          <img src="logos_y_fondos/Sponsors-24.png" alt="Sponsor 1" style="height: 100px;">
          <img src="logos_y_fondos/Sponsors-25.png" alt="Sponsor 2" style="height: 100px;">
          <img src="logos_y_fondos/Sponsors-26.png" alt="Sponsor 3" style="height: 100px;">
        </div>
    design:
      columns: 1

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
