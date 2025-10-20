# appointments/models.py

from django.db import models
from django.contrib.auth.models import User

# ==============================================================================
# 1. TABELA DE SERVIÇOS
# Armazena todos os serviços oferecidos pelo estúdio.
# ==============================================================================
class Service(models.Model):
    """
    Representa um serviço oferecido pelo estúdio.
    """
    name = models.CharField("Nome do Serviço", max_length=100)
    description = models.TextField("Descrição", blank=True, null=True)
    price = models.DecimalField("Preço", max_digits=7, decimal_places=2)
    duration_minutes = models.IntegerField("Duração em Minutos")
    image = models.ImageField("Imagem do Serviço", upload_to='service_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['name'] # Ordena os serviços por nome, em ordem alfabética.

    def __str__(self):
        return self.name

# ==============================================================================
# 2. TABELA DE ENDEREÇOS
# Armazena os endereços dos clientes para atendimentos a domicílio.
# ==============================================================================
class Address(models.Model):
    """
    Representa o endereço de um cliente para atendimentos a domicílio.
    Está ligado diretamente a um cliente.
    """
    client = models.ForeignKey(User, verbose_name="Cliente", on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField("Logradouro", max_length=255)
    number = models.CharField("Número", max_length=20)
    neighborhood = models.CharField("Bairro", max_length=100)
    city = models.CharField("Cidade", max_length=100)
    state = models.CharField("UF", max_length=2)
    zip_code = models.CharField("CEP", max_length=9)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.number} ({self.client.username})"

# ==============================================================================
# 3. TABELA DE AGENDAMENTOS
# A tabela que conecta Clientes, Serviços e, opcionalmente, Endereços.
# ==============================================================================
class Appointment(models.Model):
    """
    Representa um agendamento de um cliente para um serviço específico.
    """
    # Opções para os campos de escolha (choices).
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        CONFIRMED = 'CONFIRMED', 'Confirmado'
        DONE = 'DONE', 'Concluído'
        CANCELED = 'CANCELED', 'Cancelado'

    class AppointmentType(models.TextChoices):
        STUDIO = 'STUDIO', 'No Salão'
        HOME = 'HOME', 'Residência'

    # --- Relacionamentos (Chaves Estrangeiras) ---
    client = models.ForeignKey(User, verbose_name="Cliente", on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, verbose_name="Serviço", on_delete=models.CASCADE, related_name="appointments")
    address = models.ForeignKey(
        Address,
        verbose_name="Endereço de Atendimento",
        on_delete=models.SET_NULL, # Se o endereço for apagado, o agendamento não é apagado.
        null=True,  # Permite que o campo seja nulo no banco.
        blank=True  # Permite que o campo seja opcional no admin.
    )

    # --- Campos de Dados do Agendamento ---
    appointment_time = models.DateTimeField("Data e Hora do Agendamento")
    status = models.CharField("Status", max_length=10, choices=Status.choices, default=Status.PENDING)
    appointment_type = models.CharField(
        "Tipo de Atendimento",
        max_length=10,
        choices=AppointmentType.choices,
        default=AppointmentType.STUDIO
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-appointment_time'] # Ordena pelos mais recentes primeiro.

    def __str__(self):
        formatted_time = self.appointment_time.strftime("%d/%m/%Y às %H:%M")
        return f"{self.service.name} para {self.client.username} - {formatted_time}"