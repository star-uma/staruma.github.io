---
# Leave the homepage title empty to use the site title
title:
date: 2022-10-24
type: landing
description: "Equipo estudiantil de la Universidad de Málaga dedicado a la robótica de rescate: proyectos, noticias y miembros."

sections:
  - block: hero
    content:
      title: |
        RoboRescue UMA

      image:
        filename: logoh.png
        alt: Logo RoboRescue UMA
      url: '#inicio'
      text: |
         <div style="text-align: left">
            Somos un equipo compuesto por estudiantes de diversos ámbitos pertenecientes a la Universidad de Málaga unidos con un fin común. Nos dedicamos al desarrollo tecnológico-robótico de rescate. Este proyecto comenzó en 2019, con la intención de dar visibilidad a las posibles
            soluciones prácticas que podemos encontrar gracias a la robótica, y a la automatización.
          </div>

# No hay noticias actualmente
#  - block: collection
#    content:
#      title: Noticias Recientes
#      subtitle: Actualizaciones del proyecto HORU y actividades
#      text:
#      count: 5
#      filters:
#        folders:
#          - noticias
#        exclude_featured: false
#      offset: 0
#      order: desc
#      page_type: post
#    design:
#      view: card
#      columns: '1'

# Redundante (ya que hay un slider más abajo)
#  - block: markdown
#    content:
#      title:
#      subtitle: ''
#      text:
#    design:
#      columns: '1'
#      background:
#        image:
#          filename: coders.jpg
#          filters:
#            brightness: 1
#          parallax: false
#          position: center
#          size: cover
#          text_color_light: true
#      spacing:
#        padding: ['20px', '0', '20px', '0']
#      css_class: fullscreen


  - block: slider
    content:
      slides:
      - title: 👋 Bienvenido al Equipo de Robótica de Rescate
        content: Echa un vistazo en lo que estamos trabajando...
        align: center
        background:
          image:
            filename: coders.jpg
            filters:
              brightness: 0.5
          position: right
          color: '#666'
      - title: Talleres, Charlas y Lunch & Learn ☕️
        content: '¡Comparte tu conocimiento con el equipo y descubre el excitante mundo de la robótica con nosotros!'
        align: left
        background:
          image:
            filename: contact.jpg
            filters:
              brightness: 0.7
          position: center
          color: '#555'
      - title: Taller de Baterias para Robots
        content: '¡Construyendo la batería del nuevo robot HORU!'
        align: right
        background:
          image:
            filename: welcome.jpg
            filters:
              brightness: 0.5
          position: center
          color: '#333'
        link:
          icon: graduation-cap
          icon_pack: fas
          text: ¡Únete al Equipo!
          url: https://forms.gle/wGeDcg52BzjjMgvU8
    design:
      # Slide height is automatic unless you force a specific height (e.g. '400px')
      slide_height: ''
      is_fullscreen: true
      # Automatically transition through slides?
      loop: false
      # Duration of transition between slides (in ms)
      interval: 2000

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./equipo/" cta_text="Conoce el equipo →" %}}
    design:
      columns: '1'
---
