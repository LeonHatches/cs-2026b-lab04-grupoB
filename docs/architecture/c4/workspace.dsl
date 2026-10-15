workspace "BiblioUNSA" "Modelo C4" {
    !identifiers hierarchical

    model {
        estudiante = person "Estudiante" "Consulta, reserva y recibe préstamos de libros."
        bibliotecario = person "Bibliotecario" "Registra préstamos, devoluciones y multas."

        bibliounsa = softwareSystem "BiblioUNSA" "Sistema de catálogo, reservas y préstamos de bibliotecas UNSA." {
            web = container "Aplicación Web" "Presentación para estudiantes y bibliotecarios." "Angular" "Web Browser"
            api = container "API" "Backend de monolito modular." "Django" {
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
        component bibliounsa.api "Componentes" "E3: componentes internos de aplicación BiblioUNSA" {
            include *
            autolayout lr
        }
        // E4: Hatches debe agregar aquí una vista dynamic del caso Reservar libro
        // E5: Hatches debe agregar en model el deploymentEnvironment Producción
        // y aquí una vista deployment referida a ese entorno.
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

