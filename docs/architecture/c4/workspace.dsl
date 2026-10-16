workspace "BiblioUNSA" "Modelo C4" {
    !identifiers hierarchical

    model {
        estudiante = person "Estudiante" "Consulta, reserva y recibe préstamos de libros."
        bibliotecario = person "Bibliotecario" "Registra préstamos, devoluciones y multas."

        bibliounsa = softwareSystem "BiblioUNSA" "Sistema de catálogo, reservas y préstamos de bibliotecas UNSA." {
            web = container "Aplicación Web" "Presentación para estudiantes y bibliotecarios." "Angular" "Web Browser"
            api = container "Backend API" "Backend de monolito modular." "Django" {
                usuarios = component "Usuarios y autenticación" "Identidad, perfiles y acceso institucional." "Módulo backend"
                catalogo = component "Catálogo" "Consulta libros y ejemplares." "Módulo backend"
                reservas = component "Reservas" "Registra reservas y controla conflictos de disponibilidad." "Módulo backend"
                prestamos = component "Préstamos" "Registra entregas y devoluciones." "Módulo backend"
                multas = component "Multas" "Calcula y gestiona sanciones por retraso." "Módulo backend"
                integracion = component "Integración académica" "Adaptador para consumir API académica e identidad." "Módulo backend"
            }
            db = container "Base de datos BiblioUNSA" "Libros, ejemplares, reservas, préstamos y multas." "PostgreSQL" "Database"
        }
        academico = softwareSystem "Sistema académico UNSA" "Proporciona el estado de matrícula mediante API." "Externo"
        identidad = softwareSystem "Autenticación institucional" "Valida credenciales institucionales." "Externo"

        estudiante -> bibliounsa "Consulta catálogo y solicita reservas"
        bibliotecario -> bibliounsa "Registra préstamos y devoluciones"
        bibliounsa -> academico "Consulta matrícula vigente" "HTTPS/JSON"
        bibliounsa -> identidad "Autentica usuarios" "HTTPS"
        estudiante -> bibliounsa.web "Usa el portal" "HTTPS"
        bibliotecario -> bibliounsa.web "Usa el portal" "HTTPS"
        bibliounsa.web -> bibliounsa.api "Solicita operaciones de biblioteca" "HTTPS/JSON"
        bibliounsa.api -> bibliounsa.db "Lee y escribe datos" "SQL/TCP"
        bibliounsa.api.usuarios -> identidad "Verifica identidad" "HTTPS (por verificar)"
        bibliounsa.api.integracion -> academico "Valida matrícula" "HTTPS/JSON"
        bibliounsa.api.reservas -> bibliounsa.api.catalogo "Consulta ejemplares disponibles"
        bibliounsa.api.reservas -> bibliounsa.api.integracion "Valida matrícula del estudiante"
        bibliounsa.api.prestamos -> bibliounsa.api.reservas "Consume reserva confirmada"
        bibliounsa.api.prestamos -> bibliounsa.api.catalogo "Actualiza disponibilidad"
        bibliounsa.api.multas -> bibliounsa.api.prestamos "Consulta préstamos vencidos"
        bibliounsa.api.reservas -> bibliounsa.api.usuarios "Identifica estudiante"
        bibliounsa.api.prestamos -> bibliounsa.api.usuarios "Valida bibliotecario"
        bibliounsa.api.usuarios -> bibliounsa.api.integracion "Solicita autenticación institucional"

        // E4: el endpoint de reserva se detalla dentro del backend (secuencia del Lab 05).
        bibliounsa.web -> bibliounsa.api.reservas "Solicita reservar un ejemplar mediante la API" "HTTPS/JSON"
        // Los repositorios del UML se abstraen como acceso a PostgreSQL, según ADR-002.
        bibliounsa.api.catalogo -> bibliounsa.db "Consulta disponibilidad de ejemplares" "SQL/TCP"
        bibliounsa.api.reservas -> bibliounsa.db "Registra una reserva activa mediante transacción" "SQL/TCP"

        // E5: topología del Lab 04; es un diseño, no infraestructura ya contratada.
        produccion = deploymentEnvironment "Producción" {
            deploymentNode "Dispositivo del usuario" "Equipo o celular del estudiante o bibliotecario; no se exige un SO específico." "Navegador web" {
                deploymentNode "Navegador" "Ejecuta la aplicación Angular y accede a la API mediante HTTPS." "JavaScript / Angular" {
                    containerInstance bibliounsa.web
                }
            }
            deploymentNode "Servidor en la nube" "Servidor único propuesto para el MVP de bajo presupuesto, según el despliegue del Lab 04." "Servidor único del MVP" {
                properties {
                    "Origen" "docs/architecture/diagramas/despliegue.py"
                    "Restricción" "R-03: presupuesto bajo; justificar servicios de pago"
                    "Pendiente" "Confirmar proveedor, SO, CPU, RAM y costo antes de contratar"
                }
                deploymentNode "Entorno de aplicación" "Nginx atiende HTTPS y dirige las solicitudes al monolito Django." "Nginx / Python / Django" {
                    containerInstance bibliounsa.api
                }
                deploymentNode "Servicio de base de datos" "PostgreSQL en el mismo servidor; datos propios de BiblioUNSA y transacciones de reserva." "PostgreSQL" {
                    containerInstance bibliounsa.db
                }
            }
        }
    }

    views {
        systemContext bibliounsa "Contexto" "Modelo C4 - Contexto" {
            title "Diagrama de Contexto - BiblioUnsa"
            include *
            autolayout lr
        }
        container bibliounsa "Contenedores" "Modelo C4 - Contenedores" {
            title "Diagrama de Contenedores - BiblioUnsa"
            include *
            autolayout lr
        }
        component bibliounsa.api "Componentes" "Modelo C4 - Componentes" {
            title "Diagrama de Componentes - BiblioUnsa"
            include *
            autolayout lr
        }
        // El alcance del backend permite mostrar sus componentes, la Web y el sistema externo.
        dynamic bibliounsa.api "DinamicaReserva" "Pasos para reservar un ejemplar, desde la solicitud del estudiante hasta la base de datos." {
            title "BiblioUNSA - Dinámica de reserva de un ejemplar"
            1: estudiante -> bibliounsa.web "Selecciona el ejemplar y solicita reservar"
            2: bibliounsa.web -> bibliounsa.api.reservas "Envía la solicitud al endpoint de reservas"
            3: bibliounsa.api.reservas -> bibliounsa.api.integracion "Solicita validar matrícula vigente"
            4: bibliounsa.api.integracion -> academico "Consulta matrícula mediante API"
            5: bibliounsa.api.reservas -> bibliounsa.api.catalogo "Solicita comprobar disponibilidad"
            6: bibliounsa.api.catalogo -> bibliounsa.db "Consulta el estado actual del ejemplar"
            7: bibliounsa.api.reservas -> bibliounsa.db "Confirma reserva y actualiza ejemplar en una transacción; rechaza conflicto"
            autolayout lr
        }
        deployment bibliounsa produccion "DespliegueProduccion" "Dónde se ejecuta cada contenedor de BiblioUNSA en producción." {
            title "BiblioUNSA - Despliegue en Producción"
            include *
            autolayout lr
        }
        styles {
            element "Person" {
                shape person 
                background #08427B 
                color #ffffff 
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Externo" {
                background #999999
                color #ffffff
            }
            element "Container" { 
                background #438DD5
                color #ffffff 
            }
            element "Component" { 
                background #85BBF0 
                color #000000 
            }
            element "Database" { 
                shape cylinder
            }
            element "Web Browser" {
                shape WebBrowser 
            }
        }
    }
}

