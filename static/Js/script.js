$(document).ready(function() {
    const fileUploadButton = $("#file-upload-button");
    const fileInput = $("#file-input");
    const uploadFileBtn = $("#upload-file-btn");
    const fileNamePlaceholder = $("#file-name-placeholder");
    const chatMessages = $("#chat-messages");

    fileUploadButton.on("click", function() {
        fileInput.click();
    });

    fileInput.on("change", function() {
        if (fileInput[0].files.length > 0) {
            fileNamePlaceholder.text(fileInput[0].files[0].name);
            uploadFileBtn.show();
        }
    });

    // Envio de formulário de upload via AJAX
    $("#file-upload-form").on("submit", function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.duplicate) {
                    if (confirm(response.message)) {
                        // Usuário deseja substituir o arquivo
                        formData.append('substituir', true);
                        $.ajax({
                            url: $("#file-upload-form").attr('action'),
                            type: $("#file-upload-form").attr('method'),
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function(response) {
                                $("#success-message").text(response.message);
                                $("#success-modal").css("display", "block");
                            },
                            error: function(xhr, status, error) {
                                $("#success-message").text('Erro: ' + xhr.responseText);
                                $("#success-modal").css("display", "block");
                            }
                        });
                    } else {
                        alert('Upload cancelado.');
                    }
                } else {
                    $("#success-message").text(response.message);
                    $("#success-modal").css("display", "block");
                }
            },
            error: function(xhr, status, error) {
                $("#success-message").text('Erro: ' + xhr.responseText);
                $("#success-modal").css("display", "block");
            }
        });
    });

    // Envio de formulário de consulta via AJAX
    $("#user-message-form").on("submit", function(event) {
        event.preventDefault(); // Impede o comportamento padrão de envio do formulário
        var consultaInput = $("#consulta-input"); // Obtém o elemento de entrada de consulta
        var userMessage = consultaInput.val().trim(); // Obtém o texto do campo de entrada e remove espaços em branco extras
        consultaInput.val(""); // Limpa o campo de entrada após o envio

        if (userMessage) { // Verifica se a mensagem do usuário não está vazia
            // Adiciona a mensagem do usuário ao chat
            chatMessages.append("<div class='user-message'>" + userMessage + "</div>");

            // Envia a mensagem do usuário via AJAX
            $.ajax({
                url: $(this).attr('action'), // Obtém a URL do atributo 'action' do formulário
                type: $(this).attr('method'), // Obtém o método HTTP do atributo 'method' do formulário
                data: {
                    consulta: userMessage, // Envia a mensagem do usuário como parte dos dados
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function(response) { // Função de retorno de chamada em caso de sucesso
                    if (response.respostas && response.respostas.length > 0) { // Verifica se há respostas válidas no objeto de resposta
                        response.respostas.forEach(function(resposta) { // Itera sobre cada resposta no array de respostas
                            chatMessages.append("<div class='bot-message'>" + JSON.stringify(resposta) + "</div>"); // Adiciona cada resposta ao elemento de mensagens do chatbot
                        });
                    } else {
                        chatMessages.append("<div class='bot-message'>Nenhuma resposta encontrada.</div>"); // Adiciona uma mensagem de "Nenhuma resposta encontrada" caso não haja respostas
                    }
                    chatMessages.scrollTop(chatMessages[0].scrollHeight); // Rola para a última mensagem
                },
                error: function(xhr, status, error) { // Função de retorno de chamada em caso de erro
                    chatMessages.append("<div class='bot-message'>Erro: " + xhr.responseText + "</div>"); // Adiciona uma mensagem de erro ao elemento de mensagens do chatbot
                    chatMessages.scrollTop(chatMessages[0].scrollHeight); // Rola para a última mensagem
                }
            });
        }
    });

    $(".close").on("click", function() {
        $("#success-modal").css("display", "none");
    });

    $(window).on("click", function(event) {
        var modal = $("#success-modal");
        if (event.target == modal[0]) {
            modal.css("display", "none");
        }
    });
});
