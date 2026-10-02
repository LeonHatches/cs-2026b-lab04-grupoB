from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Nginx, Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana

with Diagram(
    "BiblioUNSA - Vista de despliegue",
    show=False,
    direction="LR",
    outformat="png"
):

    usuarios = Users("Estudiantes y bibliotecarios")
    dispositivo = Mobile("Navegador / celular")

    with Cluster("Servidor en la nube"):
        proxy = Nginx("HTTPS / Reverse Proxy")
        app = Server("BiblioUNSA\nMonolito modular")
        db = PostgreSQL("PostgreSQL")
        monitoreo = Grafana("Monitoreo")

    sistema_academico = Internet("API Sistema Académico")
    correo = Internet("Correo institucional")

    usuarios >> dispositivo >> proxy >> app
    app >> db
    app >> Edge(label="validación") >> sistema_academico
    app >> Edge(label="autenticación") >> correo
    app >> Edge(style="dotted") >> monitoreo