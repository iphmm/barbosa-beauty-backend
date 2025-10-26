# Manual do Desenvolvedor Back-end (Projeto Barbosa Beauty)

## Introdução: O Que é o Nosso Back-end?

Nosso back-end tem um único trabalho: ser uma **API (Application Programming Interface)**.

> Pense em uma API como um "cardápio" digital. O aplicativo (front-end) do cliente vai olhar esse cardápio e fazer "pedidos", como:
> * "Por favor, me **liste (GET)** todos os serviços disponíveis."
> * "Eu quero **criar (POST)** um novo agendamento para este cliente."
>
> Nosso trabalho é escrever o código que recebe esses pedidos, entende o que precisa ser feito (buscar no banco de dados, salvar no banco de dados) e devolve uma resposta (em formato JSON).

---

## A Anatomia de um Endpoint: Os 4 Arquivos Mágicos

Para fazer qualquer "pedido" do cardápio (um "endpoint") funcionar, nós **sempre** mexemos em 3 ou 4 arquivos, sempre na mesma ordem. O segredo é que esse padrão se repete.

Vamos usar nosso endpoint `/api/services/` como exemplo.

### 1. O Modelo (`models.py`)

* **O que é?** É o **"Molde"** da nossa tabela no banco de dados.
* **Onde fica?** `appointments/models.py`
* **O que fizemos?** Nós criamos a `class Service(models.Model)` para dizer ao Django: "Crie uma tabela 'Service' com colunas para 'name', 'price', etc."
* **Quando mexemos?** Apenas quando precisamos criar ou alterar a estrutura do banco. (Já fizemos isso, então raramente vamos mexer aqui de novo).

### 2. O Serializer (`serializers.py`)

* **O que é?** É o **"Tradutor"** oficial.
* **Onde fica?** `appointments/serializers.py`
* **Qual o trabalho dele?**
    1.  **Python -> JSON:** Pega um objeto `Service` do nosso banco (código Python) e o "traduz" para JSON (o que o aplicativo entende).
    2.  **JSON -> Python:** Pega um JSON enviado pelo aplicativo e o "traduz" para um objeto Python que o Django consegue salvar no banco.
* **Exemplo de Código:**
    ```python
    # appointments/serializers.py
    from rest_framework import serializers
    from .models import Service

    class ServiceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service  # "Traduza o modelo Service"
            fields = ['id', 'name', 'price', 'duration_minutes'] # "Traduza apenas estes campos"
    ```

### 3. A View (`views.py`)

* **O que é?** É o **"Cérebro"** do endpoint. É a lógica de negócio.
* **Onde fica?** `appointments/views.py`
* **Qual o trabalho dela?** Ela decide o que fazer quando um usuário acessa uma URL.
    * "O usuário está pedindo para *ver* a lista (GET)? Ok, vou buscar todos os serviços no banco."
    * "O usuário está pedindo para *criar* um novo (POST)? Ok, vou pegar os dados e salvar."
    * **Importante:** É aqui que colocamos a **segurança**, como `permission_classes = [IsAuthenticated]` (só usuários logados podem acessar).
* **Exemplo de Código (o jeito fácil):**
    ```python
    # appointments/views.py
    from rest_framework import generics # Importamos os "cérebros prontos"
    from .models import Service
    from .serializers import ServiceSerializer

    class ServiceListCreateView(generics.ListCreateAPIView):
        queryset = Service.objects.all()  # "O que buscar?" (Todos os serviços)
        serializer_class = ServiceSerializer # "Qual tradutor usar?"
    ```
    *(O `generics.ListCreateAPIView` é um atalho mágico do DRF que nos dá o "Listar (GET)" e o "Criar (POST)" de graça.)*

### 4. As Rotas (`urls.py`)

* **O que é?** É o **"Endereço"** final. É a URL que o usuário acessa.
* **Onde fica?** `appointments/urls.py`
* **Qual o trabalho dele?** Ligar uma URL (ex: `/services/`) a um "Cérebro" (uma View).
* **Exemplo de Código:**
    ```python
    # appointments/urls.py
    from django.urls import path
    from .views import ServiceListCreateView # Importa o cérebro

    urlpatterns = [
        # "Quando alguém acessar 'services/', use o cérebro 'ServiceListCreateView'"
        path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    ]
    ```
*(Nota: Também precisamos registrar esse arquivo `urls.py` no arquivo principal `backend/urls.py`, o que já fizemos).*

---

## A Receita de Bolo: Como Criar um Novo Endpoint do Zero

Vamos supor que precisamos criar um endpoint para listar/criar **Agendamentos (`Appointment`)**.
Siga exatamente esta receita de 3 passos.

### Passo 1: Criar o "Tradutor" (Serializer)

1.  Abra o arquivo `appointments/serializers.py`.
2.  Importe o modelo `Appointment` no topo: `from .models import Service, Address, Appointment`.
3.  Adicione a nova classe "tradutora" no final do arquivo:

    ```python
    class AppointmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Appointment
            # Escolha os campos que o app precisa ver
            fields = ['id', 'client', 'service', 'appointment_time', 'status', 'appointment_type', 'address']
    ```

### Passo 2: Criar o "Cérebro" (View)

1.  Abra o arquivo `appointments/views.py`.
2.  Importe o modelo `Appointment` e o novo `AppointmentSerializer` no topo.
3.  Adicione a nova classe "cérebro" no final do arquivo:

    ```python
    class AppointmentListCreateView(generics.ListCreateAPIView):
        serializer_class = AppointmentSerializer
        permission_classes = [IsAuthenticated] # Agendamentos são privados!

        # Lógica customizada para mostrar SÓ os agendamentos do usuário logado.
        def get_queryset(self):
            # self.request.user é o usuário logado
            return Appointment.objects.filter(client=self.request.user)

        # Lógica para garantir que o agendamento seja salvo
        # para o usuário que está logado.
        def perform_create(self, serializer):
            serializer.save(client=self.request.user)
    ```

### Passo 3: Criar o "Endereço" (URL)

1.  Abra o arquivo `appointments/urls.py`.
2.  Importe o novo "cérebro" `AppointmentListCreateView` no topo.
3.  Adicione o novo `path` à `urlpatterns`:

    ```python
    # ... outros imports ...
    from .views import ServiceListCreateView, AddressListCreateView, AppointmentListCreateView

    urlpatterns = [
        path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
        path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
        # --- ADICIONE ESTA LINHA ---
        path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    ]
    ```

### Passo 4: Testar!

1.  Salve todos os arquivos. O servidor vai reiniciar.
2.  Acesse `http://127.0.0.1:8000/api/appointments/` (lembre-se de estar logado no `/admin/` primeiro).
3.  **Pronto!** Você acabou de criar um endpoint completo.

---

## Conclusão

Quase todo endpoint que criarmos seguirá exatamente esse padrão de 3 passos:

**Serializer -> View -> URL**

Use este guia como sua referência. Quando você entende esse padrão, você entende o Django REST Framework.