# 🧰 Soporte Técnico / Technical Support Management (Odoo 16)

This repository contains an **Odoo 16 custom module** called **Soporte Técnico**, developed by **José Luis Ruiz Verdugo**.  
It provides a complete system for managing technical support operations, including tickets, service contracts, technicians, scheduling, and customer satisfaction.

---

English Description

🧩 Features

- Ticket management for technical incidents and support requests  
- Contract management for client support agreements  
- Product and service catalog for support operations  
- Scheduling of technical visits through the Odoo Calendar  
- Technician assignment and tracking  
- Customer satisfaction evaluation and feedback management  
- Integration with **Accounting**, **HR**, **Calendar**, and **Product** modules

⚙️ Dependencies

This module requires the following Odoo core modules:
- `base`
- `account`
- `hr`
- `calendar`
- `product`

🗂️ Installation

1. Copy the `soporte_gestion` folder into your Odoo custom addons directory:
   ```bash
   /odoo/custom/addons/soporte_gestion
Restart your Odoo server:

bash
Copiar código
./odoo-bin -u soporte_gestion
Activate developer mode in Odoo.

Go to Apps, update the app list, and install Soporte Técnico.

📋 License
This module is licensed under the AGPL-3 (GNU Affero General Public License v3).

👤 Author
José Luis Ruiz Verdugo
📧 jlruizverdugo@outlook.es
© 2025 José Luis Ruiz Verdugo. All rights reserved.

🖼️ Screenshot

Note: Unauthorized reproduction, distribution, or modification of this module is strictly prohibited without prior written permission from the author.

Descripción en Español

🧩 Características
Gestión de tickets de incidencias y solicitudes de soporte

Administración de contratos de soporte

Catálogo de productos y servicios asociados

Programación de visitas mediante el calendario de Odoo

Asignación y seguimiento de técnicos

Evaluación de satisfacción del cliente

Integración con los módulos Contabilidad, Recursos Humanos, Calendario y Productos

⚙️ Dependencias
Este módulo requiere los siguientes módulos base de Odoo:

base

account

hr

calendar

product

🗂️ Instalación
Copia la carpeta soporte_gestion dentro del directorio de addons personalizados de Odoo:

bash
Copiar código
/odoo/custom/addons/soporte_gestion
Reinicia el servidor de Odoo:

bash
Copiar código
./odoo-bin -u soporte_gestion
Activa el modo desarrollador en Odoo.

Ve a Aplicaciones, actualiza la lista y luego instala Soporte Técnico.

📋 Licencia
Este módulo está licenciado bajo AGPL-3 (Licencia Pública General Affero GNU v3).

👤 Autor
José Luis Ruiz Verdugo
📧 jlruizverdugo@outlook.es
© 2025 José Luis Ruiz Verdugo. Todos los derechos reservados.

🖼️ Captura

Nota: Queda prohibida cualquier reproducción, distribución o modificación sin autorización escrita del autor.
Diseñado para Odoo versión 16.0.

🧾 Project Information
Module name: soporte_gestion

Version: 16.0.1.0.0

Category: Services / Helpdesk

License: AGPL-3

Compatibility: Odoo 16.0

Language support: English / Español

📂 Repository Structure
pgsql
Copiar código
soporte_gestion/
├── __manifest__.py
├── __init__.py
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── models/
│   ├── account_move.py
│   ├── calendar_event.py
│   ├── cita_visita_soporte.py
│   ├── evaluacion.py
│   ├── producto_servicio.py
│   ├── soporte_contrato.py
│   ├── tecnico.py
│   ├── ticket_historial.py
│   └── ticket_incidencia.py
├── security/
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
└── views/
    ├── vistas_ticket_incidencia.xml
    ├── vistas_contrato_soporte.xml
    ├── vistas_producto_servicio.xml
    ├── vistas_evaluacion.xml
    ├── vistas_cita_visita_soporte.xml
    ├── vistas_heredadas.xml
    └── menus.xml
💡 Additional Notes
Designed for Odoo 16.0.

For licensing or customization inquiries, contact the author directly.

Ensure all dependencies are installed before loading the module.
