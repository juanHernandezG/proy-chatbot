

    function sendMessage() {
        var user_input = $('#user-input').val();
        $('#user-input').val('');

        // Enviar la entrada del usuario al servidor
        $.ajax({
            type: 'POST',
            url: '/chatbot/',  
            data: {'user_input': user_input, csrfmiddlewaretoken: '{{ csrf_token }}'},
            dataType: 'json',
            success: function(data) {
                // Mostrar la respuesta del chatbot en el chatbox
                $('#chatbox').append('<div style="margin-bottom: 10px; background-color:#0040B0; color: white; text-align: right; padding: 10px; border-radius: 5px;"">' +
                                    '<img src="{% static "img/usuario.png" %}" alt="Chatbot Avatar" class="chatbot-avatar" style="width:30px; height:30px;">' +
                                    '<div class="message-content chatbot">' + user_input + '</div>' +
                                    '</div>');
                $('#chatbox').append('<div style="margin-bottom: 10px; background-color:#0040B0; color: white; text-align: left; padding: 10px; border-radius: 5px;"">' +
                                    '<img src="{% static "img/chatbot.png" %}" alt="Chatbot Avatar" class="chatbot-avatar" style="width:30px; height:30px;">' +
                                    '<div class="message-content chatbot">' + data.response + '</div>' +
                                    '</div>');
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
            },
            error: function(error) {
                console.error(error);
            }
        });
    }

    // Capturar el evento de presionar la tecla "Enter"
    document.getElementById("user-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevenir el comportamiento por defecto del Enter (enviar formulario)
            sendMessage(); // Llamar a la función para enviar el mensaje
        }
    });

    //
    // Variable para almacenar el mensaje de bienvenida
    var welcomeMessage = '';

    $(document).ready(function() {
        // Obtener la fecha actual
        var currentDate = new Date();

        // Formatear la fecha como deseas
        var formattedDate = currentDate.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        // Insertar la fecha en el chatbox arriba del mensaje de bienvenida
        $('#chatbox').prepend('<div class="current-date" style="text-align: center; color: #0040B0; font-weight: bold; margin-bottom: 10px;">' + formattedDate + '</div>');


        // Al cargar la página por primera vez, guarda el mensaje de bienvenida
        welcomeMessage = $('#chatbox .welcome-message').html();

        $('#btnPregunta').click(function() {
            $('#input-container').hide(); // Ocultar el contenedor del input y el botón
            $('#chatbox').empty(); // Limpiar el contenido del chatbox

            // Cargar el contenido del instructivo.html en el chatbox
            $('#chatbox').load('/chatbot/mostrar_instructivo/', function(response, status, xhr) {
                if (status == "error") {
                    var msg = "Error al cargar el instructivo: ";
                    console.log(msg + xhr.status + " " + xhr.statusText);
                } else {
                    // Mostrar el instructivo y el botón para volver al chat
                    $('#chatbox').append('<button id="volverChatbot"><i class="fa fa-arrow-left" aria-hidden="true"></i></button>');
                }
            });
        });
        
        // Manejar el clic del botón "Volver al Chat"
        $(document).on('click', '#volverChatbot', function() {
            $('#chatbox').empty(); // Limpiar el contenido del chatbox
            $('#input-container').show(); // Mostrar el contenedor del input y el botón
            
            // Insertar la fecha en el chatbox arriba del mensaje de bienvenida
            $('#chatbox').prepend('<div class="current-date" style="text-align: center; color: #0040B0; font-weight: bold; margin-bottom: 10px;">' + formattedDate + '</div>');
            // Mostrar el mensaje de bienvenida al volver al chatbot
            $('#chatbox').append('<div class="welcome-message" style="margin-bottom: 10px; background-color: #0040B0; color: white; text-align: left; padding: 10px; border-radius: 5px;">' + welcomeMessage + '</div>');

            // Lógica adicional si es necesario al volver al chatbot
        });
    });