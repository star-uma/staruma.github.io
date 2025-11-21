---
translationKey: contact
title: Contact
description: "Ponte en contacto con RoboRescue UMA: estudiantes, patrocinadores y colaboradores. Horarios, ubicación y formulario de contacto."
date: 2024-09-23

type: landing

sections:
  - block: contact
    content:
      title: Contacto
      text: |-
        Si eres un estudiante que quiere unirse a nuestro equipo, una empresa interesada en patrocinarnos o simplemente alguien con curiosidad por conocer nuestro proyecto, ¡no dudes en contactarnos!
      email: roborescue@uma.es
      # phone: (añade número de contacto aquí si se desea)
      address:
        street: Edificio de Ingenierías UMA, Arquitecto Francisco Peñalosa, 6
        city: Málaga
        region: Andalucía
        postcode: '29010'
        country: España
        country_code: ES
      coordinates:
        latitude: '36.71549'
        longitude: '-4.49056'
      directions: Entra en la nave y gira a la izquierda, la primera puerta Taller 27
      office_hours:
        - 'Martes de 15:00 a 18:00'
        - 'Jueves de 15:00 a 16:15'
      # appointment_url: 'https://calendly.com' # No implementado
      #contact_links:
      #  - icon: comments
      #    icon_pack: fas
      #    name: Discuss on Forum
      #    link: 'https://discourse.gohugo.io'

      # Automatically link email and phone or display as text?
      autolink: true

      # Email form provider
      form:
        provider: netlify
        formspree:
          id:
        netlify:
          # Enable CAPTCHA challenge to reduce spam?
          captcha: false
    design:
      columns: '1'

  - block: markdown
    content:
      title:
      subtitle: ''
      text:
    design:
      columns: '1'
      background:
        image:
          filename: contact.jpg
          filters:
            brightness: 1
          parallax: false
          position: center
          size: cover
          text_color_light: true
      spacing:
        padding: ['20px', '0', '20px', '0']
      css_class: fullscreen
---
